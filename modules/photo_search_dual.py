"""
拍照搜题模块 - 双模式版本
快速答案 + AI详细讲解，效率与质量兼顾
"""

import streamlit as st
from PIL import Image
from modules.ai_service import get_ai_service
from data.history_questions import search_questions
import random

def render_photo_search():
    """渲染拍照搜题页面"""
    st.title("📷 拍照搜题")
    
    # 获取AI服务
    ai_service = get_ai_service()
    
    st.markdown("""
    <div class="info-box">
        <h3>💡 双模式搜题</h3>
        <p><strong>⚡ 快速模式</strong>：直接给答案，节省时间</p>
        <p><strong>🤖 AI详解模式</strong>：深度讲解、解题思路、知识拓展</p>
    </div>
    """, unsafe_allow_html=True)
    
    # 初始化session state
    if 'current_search_question' not in st.session_state:
        st.session_state.current_search_question = None
    if 'current_search_result' not in st.session_state:
        st.session_state.current_search_result = None
    
    # 拍照/上传区域
    st.subheader("📸 上传题目")
    
    tab1, tab2 = st.tabs(["📷 拍照上传", "⌨️ 文字输入"])
    
    with tab1:
        uploaded_file = st.file_uploader(
            "上传题目图片",
            type=['jpg', 'jpeg', 'png'],
            help="支持JPG、PNG格式"
        )
        
        if uploaded_file:
            # 显示图片
            image = Image.open(uploaded_file)
            st.image(image, caption="上传的题目", use_container_width=True)
            
            # 模拟OCR识别
            st.info("📝 正在识别题目...")
            
            # 这里应该调用OCR API，暂时模拟
            recognized_text = simulate_ocr(image)
            
            st.success("✅ 识别完成！")
            st.text_area("识别结果（可编辑）", value=recognized_text, height=100, key="ocr_result")
            
            if st.button("🔍 开始搜题", type="primary", key="btn_ocr_search"):
                # 搜索题目
                with st.spinner("🔍 正在搜索题库..."):
                    similar_questions = perform_search(recognized_text)
                    
                    # 存储结果到session state
                    if similar_questions:
                        st.session_state.current_search_question = recognized_text
                        st.session_state.current_search_result = similar_questions[0]
                    else:
                        st.session_state.current_search_question = recognized_text
                        st.session_state.current_search_result = None
    
    with tab2:
        question_text = st.text_area(
            "输入题目内容：",
            height=150,
            placeholder="例如：洋务运动为什么最终失败？"
        )
        
        if st.button("🔍 搜索答案", type="primary", key="btn_text_search") and question_text:
            # 搜索题目
            with st.spinner("🔍 正在搜索题库..."):
                similar_questions = perform_search(question_text)
                
                # 存储结果到session state
                if similar_questions:
                    st.session_state.current_search_question = question_text
                    st.session_state.current_search_result = similar_questions[0]
                else:
                    st.session_state.current_search_question = question_text
                    st.session_state.current_search_result = None
    
    # 快速搜题示例
    st.markdown("---")
    st.subheader("⚡ 试试这些题目")
    
    example_questions = [
        "洋务运动为什么最终失败？",
        "辛亥革命的历史意义是什么？",
        "中国共产党成立的历史条件有哪些？"
    ]
    
    cols = st.columns(3)
    for i, q in enumerate(example_questions):
        with cols[i]:
            if st.button(q, use_container_width=True, key=f"example_{i}"):
                # 搜索并存储结果
                similar_questions = perform_search(q)
                if similar_questions:
                    st.session_state.current_search_question = q
                    st.session_state.current_search_result = similar_questions[0]
                else:
                    st.session_state.current_search_question = q
                    st.session_state.current_search_result = None
    
    # ===== 统一在这里显示搜索结果（只调用一次） =====
    if st.session_state.current_search_result is not None:
        st.markdown("---")
        display_search_result(ai_service, st.session_state.current_search_result)


def perform_search(query_text):
    """统一的搜索函数"""
    # 尝试完整匹配
    similar_questions = search_questions(query_text)
    
    # 如果没找到，尝试用前15个字符搜索
    if not similar_questions and len(query_text) > 15:
        similar_questions = search_questions(query_text[:15])
    
    # 如果还没找到，尝试关键词搜索
    if not similar_questions:
        keywords = ["洋务运动", "辛亥革命", "中国共产党", "戊戌变法"]
        for kw in keywords:
            if kw in query_text:
                similar_questions = search_questions(kw)
                break
    
    return similar_questions


def display_search_result(ai_service, best_match):
    """显示搜索结果，支持点击按钮控制显示内容"""
    
    st.success("✅ 找到题目！")
    
    # 全屏展示区域
    with st.container():
        # 显示题目（大字体） - 始终显示
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    padding: 30px; border-radius: 15px; margin: 20px 0;'>
            <h2 style='color: white; margin: 0;'>📝 {best_match['question']}</h2>
        </div>
        """, unsafe_allow_html=True)
        
        # 如果是选择题，显示选项
        if 'options' in best_match and best_match.get('type') == 'choice':
            st.markdown("### 📋 选项")
            
            # 检查 options 是字典还是列表
            options = best_match['options']
            if isinstance(options, dict):
                for key, value in options.items():
                    st.markdown(f"""
                    <div style='background: #f8f9fa; padding: 15px; margin: 8px 0; 
                                border-radius: 8px; border-left: 4px solid #667eea;'>
                        <span style='font-weight: bold; color: #667eea;'>{key}</span> {value}
                    </div>
                    """, unsafe_allow_html=True)
            else:
                for opt in options:
                    st.markdown(f"""
                    <div style='background: #f8f9fa; padding: 15px; margin: 8px 0; 
                                border-radius: 8px; border-left: 4px solid #667eea;'>
                        {opt}
                    </div>
                    """, unsafe_allow_html=True)
        
        # 如果是材料题，显示材料
        elif best_match.get('type') == 'material':
            if 'material' in best_match:
                st.markdown("### 📄 材料")
                st.markdown(f"""
                <div style='background: #fff3cd; padding: 20px; border-radius: 10px; 
                            border-left: 4px solid #ffc107;'>
                    {best_match['material'].replace(chr(10), '<br>')}
                </div>
                """, unsafe_allow_html=True)
        
        # 显示答案和讲解按钮
        st.markdown("<br>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        
        # 使用题目ID作为固定的key
        question_id = best_match.get('id', 'unknown')
        
        with col1:
            # 使用固定key的checkbox
            show_answer = st.checkbox("👁️ 查看答案解析", key=f"show_ans_{question_id}")
        
        with col2:
            show_ai = st.checkbox("🤖 AI详细讲解", key=f"show_ai_{question_id}")
        
        # 显示答案（点击后才显示）
        if show_answer:
            if best_match.get('type') == 'choice':
                # 选择题显示答案
                st.markdown(f"""
                <div style='background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%); 
                            padding: 25px; border-radius: 12px; margin: 20px 0;'>
                    <h3 style='color: white; margin: 0 0 10px 0;'>✅ 正确答案</h3>
                    <p style='color: white; font-size: 24px; font-weight: bold; margin: 0;'>{best_match['answer']}</p>
                </div>
                """, unsafe_allow_html=True)
                
                # 简要解析（全屏宽度）
                if 'explanation' in best_match:
                    st.markdown("### 💡 解析")
                    st.markdown(f"""
                    <div style='background: #f8f9fa; padding: 25px; border-radius: 10px; 
                                border-left: 4px solid #667eea; line-height: 1.8;'>
                        {best_match['explanation']}
                    </div>
                    """, unsafe_allow_html=True)
            
            elif best_match.get('type') == 'material':
                st.markdown("### 📌 参考答案要点")
                st.markdown(f"""
                <div style='background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%); 
                            padding: 25px; border-radius: 12px; margin: 20px 0;'>
                    <h4 style='color: white; margin: 0 0 10px 0;'>✅ 参考答案</h4>
                    <p style='color: white; font-size: 16px; line-height: 1.8; margin: 0;'>{best_match['answer']}</p>
                </div>
                """, unsafe_allow_html=True)
                
                if 'explanation' in best_match:
                    st.markdown("### 💡 出题分析")
                    st.markdown(f"""
                    <div style='background: #f8f9fa; padding: 25px; border-radius: 10px; 
                                border-left: 4px solid #667eea; line-height: 1.8;'>
                        {best_match['explanation']}
                    </div>
                    """, unsafe_allow_html=True)
            
            else:
                st.markdown("### 📌 答案")
                st.success(best_match['answer'])
                
                if 'explanation' in best_match:
                    st.markdown("### 💡 解析")
                    st.info(best_match['explanation'])
        
        # AI详细讲解（点击后才显示，全屏宽度）
        if show_ai:
            with st.spinner("🤖 AI正在生成详细讲解..."):
                explanation = ai_service.explain_concept(
                    f"题目：{best_match['question']}\n答案：{best_match['answer']}",
                    level='detailed'
                )
                if explanation:
                    st.markdown(f"""
                    <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                                padding: 25px; border-radius: 12px; margin: 20px 0;'>
                        <h3 style='color: white; margin: 0;'>🤖 AI详细讲解</h3>
                    </div>
                    <div style='background: #f8f9fa; padding: 30px; border-radius: 0 0 12px 12px; 
                                border: 2px solid #667eea; border-top: none; line-height: 1.8; font-size: 16px;'>
                        {explanation}
                    </div>
                    """, unsafe_allow_html=True)
    
    # 生成相似练习题按钮 - 使用题目ID作为固定key
    st.markdown("---")
    if st.button("🎯 生成相似练习题", use_container_width=True, key=f"gen_similar_{question_id}"):
        generate_similar_questions(ai_service, best_match)


def search_quick_answer(ai_service, question_text):
    """搜索题目，快速显示答案（保持为向后兼容的函数）"""
    
    st.markdown("---")
    
    # 搜索相似题目 - 使用更长的搜索字符串，并支持模糊匹配
    with st.spinner("🔍 正在搜索题库..."):
        # 尝试完整匹配
        similar_questions = search_questions(question_text)
        
        # 如果没找到，尝试用前15个字符搜索
        if not similar_questions:
            similar_questions = search_questions(question_text[:15])
        
        # 如果还没找到，尝试关键词搜索
        if not similar_questions:
            keywords = ["洋务运动", "辛亥革命", "中国共产党", "戊戌变法"]
            for kw in keywords:
                if kw in question_text:
                    similar_questions = search_questions(kw)
                    break
    
    if similar_questions:
        # 找到相似题目 - 调用统一的显示函数
        best_match = similar_questions[0]
        display_search_result(ai_service, best_match)
    
    else:
        # 没找到题目 - 使用AI回答
        st.warning("题库中未找到匹配题目，正在使用AI为你解答...")
        
        with st.spinner("🤔 AI老师正在分析..."):
            ai_response = ai_service.explain_concept(question_text, level='detailed')
            
            if ai_response:
                st.markdown("### 🤖 AI解答")
                st.markdown(ai_response)
            else:
                st.error("❌ AI暂时无法响应，请稍后重试或在AI助手中提问")


def show_ai_detail(ai_service, question_data, original_question):
    """显示AI详细讲解"""
    
    st.markdown("---")
    st.markdown("## 🤖 AI深度讲解")
    
    with st.spinner("💭 AI老师正在准备详细讲解..."):
        # 构建讲解提示词
        prompt = f"""题目：{question_data['question']}

参考答案：{question_data['answer']}

请作为历史老师，提供深度讲解：

## 🎯 题目分析
[这道题考查什么知识点？难度如何？]

## 📖 知识讲解
[详细讲解相关历史知识，要通俗易懂]

## 💡 解题思路
[教学生如何分析这类题，答题技巧]

## 🔗 知识拓展
[相关事件、对比分析、前因后果]

## 💭 举一反三
[类似题目可能的考查角度]

## 📝 记忆技巧
[如何快速记住这个知识点]
"""
        
        explanation = ai_service.chat_with_teacher(prompt)
        
        if explanation:
            st.markdown(explanation)
            
            # 满意度反馈
            st.markdown("---")
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("👍 讲得很好", use_container_width=True):
                    st.success("感谢反馈！我会继续努力")
            with col2:
                if st.button("🤔 还想了解更多", use_container_width=True):
                    st.info("你可以在AI助手中继续提问哦！")
            with col3:
                if st.button("📝 再来一题", use_container_width=True):
                    st.info("请返回上方重新搜题")
        else:
            st.error("AI暂时无法响应，请稍后重试")


def generate_similar_questions(ai_service, question_data):
    """生成相似练习题"""
    
    st.markdown("---")
    st.markdown("## 🎯 相似练习题")
    
    with st.spinner("正在生成练习题..."):
        # 确定题型（优先生成选择题）
        question_type = "选择题" if question_data.get('type') == 'choice' else question_data.get('type', '选择题')
        
        similar_questions = ai_service.generate_questions(
            knowledge_points=[question_data.get('knowledge_point', '近代史')],
            difficulty=question_data.get('difficulty', 'medium'),
            count=2,
            question_type=question_type
        )
        
        if similar_questions:
            for i, q in enumerate(similar_questions, 1):
                with st.expander(f"📝 练习题 {i}", expanded=(i==1)):
                    st.markdown(f"**{q.get('question', '')}**")
                    
                    # 如果有选项（选择题）
                    if 'options' in q:
                        for key, value in q['options'].items():
                            st.write(f"{key}. {value}")
                    
                    # 答案和解析
                    if st.button(f"查看答案", key=f"answer_{i}"):
                        st.success(f"✅ 答案：{q.get('answer', '')}")
                        if 'explanation' in q:
                            st.info(f"💡 解析：{q['explanation']}")
        else:
            st.warning("生成失败，请稍后重试")


def simulate_ocr(image):
    """模拟OCR识别（实际应用需要接入真实OCR API）"""
    
    # 返回一些示例题目
    sample_questions = [
        "洋务运动为什么最终失败？",
        "辛亥革命的历史意义是什么？",
        "比较洋务运动和明治维新的异同",
        "中国共产党成立的历史条件有哪些？"
    ]
    
    return random.choice(sample_questions)

"""
拍照搜题模块 - AI深度讲解版
不只给答案，更要教会学生
"""

import streamlit as st
from PIL import Image
from modules.ai_service import get_ai_service
from data.history_questions import search_questions
import random

def render_photo_search():
    """渲染拍照搜题页面"""
    st.title("📷 AI拍照搜题 - 深度讲解")
    
    # 获取AI服务
    ai_service = get_ai_service()
    
    st.markdown("""
    <div class="info-box">
        <h3>✨ 不只是搜答案！</h3>
        <p>AI会：</p>
        <ul>
            <li>🎯 分析题目考查的知识点</li>
            <li>💡 讲解解题思路，不只给答案</li>
            <li>🔗 关联相关知识，举一反三</li>
            <li>📝 生成类似题目供练习</li>
            <li>🎓 教你答题技巧和方法</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
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
            
            if st.button("🔍 开始搜题", type="primary"):
                search_and_explain(ai_service, recognized_text)
    
    with tab2:
        question_text = st.text_area(
            "输入题目内容：",
            height=150,
            placeholder="例如：辛亥革命的历史意义是什么？"
        )
        
        if st.button("🔍 搜索并讲解", type="primary") and question_text:
            search_and_explain(ai_service, question_text)
    
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
                search_and_explain(ai_service, q)


def search_and_explain(ai_service, question_text):
    """搜索题目并AI深度讲解"""
    
    st.markdown("---")
    st.subheader("🎯 AI深度讲解")
    
    # 第一步：搜索相似题目
    with st.spinner("🔍 正在搜索题库..."):
        similar_questions = search_questions(question_text[:20])
    
    if similar_questions:
        st.success(f"找到 {len(similar_questions)} 道相似题目")
        
        # 显示最相似的题目
        best_match = similar_questions[0]
        
        with st.expander("📝 题库中的相似题目", expanded=True):
            st.markdown(f"**题目：** {best_match['question']}")
            if 'material' in best_match:
                st.markdown(f"**材料：**\n```\n{best_match['material']}\n```")
            st.markdown(f"**参考答案：** {best_match.get('answer', '暂无')}")
    else:
        st.warning("题库中暂无完全匹配的题目，AI将为你分析这道题")
        best_match = None
    
    # 第二步：AI深度讲解
    st.markdown("### 🤖 AI老师的深度讲解")
    
    with st.spinner("💭 AI老师正在分析题目..."):
        # 构建讲解prompt
        if best_match:
            explain_prompt = f"""这是学生问的问题：{question_text}

题库中有类似题目：
题目：{best_match['question']}
参考答案：{best_match.get('answer', '')}

请你作为历史老师，深度讲解这道题：

## 🎯 题目分析
[这道题考查什么知识点？属于哪个历史时期？]

## 📖 知识讲解
[详细讲解相关的历史知识，要深入浅出]

## 💡 解题思路
[教学生如何分析这类题目，而不是直接背答案]

## ✍️ 标准答案
[给出规范的答案示范]

## 🔗 知识拓展
[相关的历史事件、对比分析等]

## 💭 举一反三
[类似的考查角度有哪些？]
"""
        else:
            explain_prompt = f"""学生问题：{question_text}

请作为历史老师深度讲解：

## 🎯 题目分析
[考查什么？]

## 📖 知识讲解
[详细讲解]

## 💡 解题思路
[如何思考]

## ✍️ 答题要点
[怎么答]

## 🔗 知识拓展
[相关内容]
"""
        
        explanation = ai_service.chat_with_teacher(explain_prompt)
        
        if explanation:
            st.markdown(explanation)
            
            # 保存到历史
            if 'search_history' not in st.session_state:
                st.session_state.search_history = []
            
            st.session_state.search_history.append({
                'question': question_text,
                'explanation': explanation
            })
        else:
            # AI调用失败时的降级方案
            st.warning("⚠️ AI老师暂时无法响应，为你提供基础信息：")
            if best_match:
                st.markdown("### 📝 题库参考答案")
                st.markdown(best_match.get('answer', ''))
                if best_match.get('explanation'):
                    st.markdown("### 💡 解析")
                    st.markdown(best_match.get('explanation', ''))
            else:
                st.info("💡 请稍后重试AI讲解功能，或在AI助手中直接提问这个问题。")
    
    # 第三步：生成练习题
    st.markdown("---")
    st.subheader("🎯 巩固练习")
    
    if st.button("生成类似题目", use_container_width=True):
        with st.spinner("AI正在生成练习题..."):
            # 提取主题
            topic = question_text[:20]
            
            practice_questions = ai_service.generate_questions(
                topic=topic,
                difficulty='medium',
                count=3
            )
            
            if practice_questions:
                st.success("✅ 生成成功！")
                
                for i, q in enumerate(practice_questions, 1):
                    with st.expander(f"练习题 {i}"):
                        st.markdown(f"**题目：**\n{q.get('question', '')}")
                        
                        if q.get('type') == 'choice' and q.get('options'):
                            for opt in q['options']:
                                st.markdown(opt)
                        
                        if st.button(f"查看答案{i}", key=f"show_ans_{i}"):
                            st.markdown(f"**答案：** {q.get('answer', '')}")
                            st.markdown(f"**解析：**\n{q.get('explanation', '')}")


def simulate_ocr(image):
    """模拟OCR识别（实际应调用OCR API）"""
    # 这里返回模拟文本，实际应该调用百度OCR、腾讯OCR等API
    sample_questions = [
        "洋务运动为什么最终失败？请从根本原因分析。",
        "辛亥革命推翻了清朝统治，建立了中华民国。请简述辛亥革命的历史意义。",
        "阅读材料，回答问题：\n【材料】1898年6月11日，光绪帝颁布'定国是诏'...\n请问：维新变法为什么会失败？"
    ]
    
    return random.choice(sample_questions)

"""
拍照搜题功能模块
实现图片上传、题目识别、解题思路推荐
"""

import streamlit as st
from PIL import Image
import io
from data.history_questions import HISTORY_QUESTIONS, search_questions
from data.history_knowledge_graph import search_knowledge_by_keyword


def render_photo_search():
    """渲染拍照搜题页面"""
    
    st.markdown("""
    <div class="module-header">
        <div class="module-title">
            <span>📸</span> 拍照搜题
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="content-panel">
        <div class="panel-header">💡 使用说明</div>
        <ul style="color: #6b7280; line-height: 1.8;">
            <li>📷 拍摄或上传题目照片</li>
            <li>🤖 AI自动识别题型和内容</li>
            <li>💭 获得解题思路（不直接给答案）</li>
            <li>🔗 自动关联相关知识点</li>
            <li>📝 推荐类似题目练习</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    # 创建两列布局
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### 📤 上传题目")
        
        # 图片上传
        uploaded_file = st.file_uploader(
            "选择图片或拍照", 
            type=['png', 'jpg', 'jpeg'],
            help="支持PNG、JPG、JPEG格式"
        )
        
        # 或者文字输入
        st.markdown("#### ✏️ 或直接输入题目")
        question_text = st.text_area(
            "输入题目内容",
            height=150,
            placeholder="例如：鸦片战争的起因是什么？"
        )
        
        # 搜索按钮
        if st.button("🔍 开始搜索", type="primary", use_container_width=True):
            if uploaded_file or question_text:
                with st.spinner("正在识别题目..."):
                    # 模拟AI识别
                    if uploaded_file:
                        image = Image.open(uploaded_file)
                        st.session_state['search_image'] = image
                        # 这里应该调用OCR API识别图片文字
                        # 暂时使用示例题目
                        st.session_state['search_text'] = "鸦片战争对中国社会的影响"
                    else:
                        st.session_state['search_text'] = question_text
                    
                    st.session_state['search_done'] = True
                    st.rerun()
            else:
                st.warning("请上传图片或输入题目")
    
    with col2:
        st.markdown("### 📋 搜索结果")
        
        if st.session_state.get('search_done'):
            search_text = st.session_state.get('search_text', '')
            
            # 显示上传的图片
            if st.session_state.get('search_image'):
                st.image(st.session_state['search_image'], caption="上传的题目", use_container_width=True)
            
            st.markdown(f"**识别的题目：** {search_text}")
            
            # 分析题型
            st.markdown("---")
            st.markdown("#### 🎯 题型识别")
            
            # 简单的关键词匹配识别题型
            if "影响" in search_text or "意义" in search_text:
                question_type = "材料分析题"
                tips = "这是一道影响/意义类题目，答题要点：\n1. 从政治、经济、社会、文化等角度分析\n2. 注意区分积极影响和消极影响\n3. 结合史料论证观点"
            elif "原因" in search_text or "为什么" in search_text:
                question_type = "原因分析题"
                tips = "这是一道原因分析题，答题要点：\n1. 区分根本原因、直接原因、历史原因\n2. 多角度分析（政治、经济、思想等）\n3. 注意因果关系的逻辑性"
            else:
                question_type = "知识理解题"
                tips = "答题要点：\n1. 准确理解题目要求\n2. 回答要有针对性\n3. 适当展开，言之有理"
            
            st.info(f"**题型：** {question_type}")
            st.markdown(f"**💡 解题思路：**\n\n{tips}")
            
            # 搜索相关知识点
            st.markdown("---")
            st.markdown("#### 📚 相关知识点")
            
            # 从题目中提取关键词
            keywords = extract_keywords(search_text)
            knowledge_results = []
            for keyword in keywords:
                results = search_knowledge_by_keyword(keyword)
                knowledge_results.extend(results)
            
            # 去重
            unique_knowledge = {item['id']: item for item in knowledge_results}.values()
            
            if unique_knowledge:
                for knowledge in list(unique_knowledge)[:3]:  # 只显示前3个
                    with st.expander(f"📖 {knowledge['name']}", expanded=False):
                        st.markdown(f"**关键词：** {', '.join(knowledge['keywords'])}")
                        if knowledge.get('events'):
                            st.markdown("**相关事件：**")
                            for event in knowledge['events'][:3]:
                                st.markdown(f"- {event['name']} ({event['year']})")
            else:
                st.info("未找到直接相关的知识点，建议查看教材相关章节")
            
            # 推荐练习题
            st.markdown("---")
            st.markdown("#### 📝 推荐练习")
            
            # 搜索类似题目
            similar_questions = search_similar_questions(search_text)
            
            if similar_questions:
                for i, q in enumerate(similar_questions[:3], 1):
                    with st.expander(f"练习题 {i}：{q['question'][:30]}...", expanded=False):
                        st.markdown(f"**题目：** {q['question']}")
                        
                        if q['type'] == 'choice':
                            for option in q['options']:
                                st.markdown(f"{option}")
                        
                        # 默认隐藏答案
                        if st.button(f"查看答案 {i}", key=f"answer_{q['id']}"):
                            st.success(f"**答案：** {q['answer']}")
                            st.info(f"**解析：** {q['explanation']}")
            else:
                st.info("暂无推荐练习题")
            
            # 清除按钮
            if st.button("🔄 重新搜索", use_container_width=True):
                st.session_state['search_done'] = False
                st.session_state['search_text'] = ''
                if 'search_image' in st.session_state:
                    del st.session_state['search_image']
                st.rerun()
        
        else:
            st.info("👈 请在左侧上传题目或输入文字")


def extract_keywords(text):
    """从文本中提取关键词"""
    # 简单的关键词提取（实际应用中可以使用更复杂的NLP算法）
    common_keywords = [
        '鸦片战争', '洋务运动', '戊戌变法', '辛亥革命', '五四运动',
        '抗日战争', '解放战争', '新中国', '改革开放',
        '夏朝', '商朝', '周朝', '秦朝', '汉朝', '唐朝', '宋朝', '元朝', '明朝', '清朝',
        '分封制', '郡县制', '科举制', '中央集权'
    ]
    
    keywords = []
    for keyword in common_keywords:
        if keyword in text:
            keywords.append(keyword)
    
    return keywords[:5]  # 最多返回5个关键词


def search_similar_questions(search_text):
    """搜索类似题目"""
    # 提取关键词
    keywords = extract_keywords(search_text)
    
    # 搜索包含这些关键词的题目
    results = []
    for keyword in keywords:
        questions = search_questions(keyword)
        results.extend(questions)
    
    # 去重
    unique_questions = {q['id']: q for q in results}.values()
    
    return list(unique_questions)

"""
闪卡复习模块 - 双模式版本
快速复习 + AI深度讲解
"""

import streamlit as st
import random
from modules.ai_service import get_ai_service
from data.history_flashcards import get_all_flashcards

def render_flashcard_review():
    """渲染闪卡复习页面"""
    st.title("📇 闪卡复习")
    
    # 获取AI服务
    ai_service = get_ai_service()
    
    st.markdown("""
    <div class="info-box">
        <h3>💡 智能复习系统</h3>
        <p><strong>⚡ 快速模式</strong>：翻卡看答案，快速过一遍</p>
        <p><strong>🤖 AI深度模式</strong>：详细讲解、记忆技巧、知识拓展</p>
        <p><strong>🎯 智能推荐</strong>：AI根据遗忘曲线推荐复习内容</p>
    </div>
    """, unsafe_allow_html=True)
    
    # 初始化会话状态
    if 'current_card_index' not in st.session_state:
        st.session_state.current_card_index = 0
    if 'show_answer' not in st.session_state:
        st.session_state.show_answer = False
    if 'flashcard_mastery' not in st.session_state:
        st.session_state.flashcard_mastery = {}
    if 'review_mode' not in st.session_state:
        st.session_state.review_mode = 'ai_recommend'
    
    # 获取所有闪卡
    all_flashcards = get_all_flashcards()
    
    # 复习模式选择
    st.subheader("🎯 选择复习模式")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🤖 AI智能推荐", use_container_width=True, 
                    type="primary" if st.session_state.review_mode == 'ai_recommend' else "secondary"):
            st.session_state.review_mode = 'ai_recommend'
            st.session_state.current_card_index = 0
            st.rerun()
    
    with col2:
        if st.button("📚 按章节复习", use_container_width=True,
                    type="primary" if st.session_state.review_mode == 'by_chapter' else "secondary"):
            st.session_state.review_mode = 'by_chapter'
            st.rerun()
    
    with col3:
        if st.button("🎲 随机抽取", use_container_width=True,
                    type="primary" if st.session_state.review_mode == 'random' else "secondary"):
            st.session_state.review_mode = 'random'
            random.shuffle(all_flashcards)
            st.session_state.current_card_index = 0
            st.rerun()
    
    # 如果是按章节模式，显示章节选择
    if st.session_state.review_mode == 'by_chapter':
        # 章节中英文对照表
        chapter_name_map = {
            'origin': '中华文明起源',
            'xia_shang_zhou': '夏商周时期',
            'qin_han': '秦汉时期',
            'three_kingdoms': '三国两晋南北朝',
            'sui_tang': '隋唐时期',
            'song_yuan': '宋元时期',
            'ming_qing': '明清时期',
            'modern': '近代史',
            'contemporary': '现代史',
            'world': '世界史',
            '未分类': '未分类'
        }
        
        chapters_raw = list(set([card.get('chapter', '未分类') for card in all_flashcards]))
        # 将英文章节名转为中文
        chapters_display = [chapter_name_map.get(ch, ch) for ch in chapters_raw]
        
        selected_chapter_display = st.selectbox("选择章节：", chapters_display)
        
        # 找到对应的英文章节名
        selected_chapter = chapters_raw[chapters_display.index(selected_chapter_display)]
        
        all_flashcards = [card for card in all_flashcards if card.get('chapter', '未分类') == selected_chapter]
    
    # 如果是AI推荐模式，按掌握度排序
    elif st.session_state.review_mode == 'ai_recommend':
        all_flashcards = sorted(all_flashcards, 
                               key=lambda x: st.session_state.flashcard_mastery.get(x['id'], 0))
        st.info("🎯 AI已根据你的掌握情况智能排序，优先复习薄弱知识点")
    
    if not all_flashcards:
        st.warning("该章节暂无闪卡")
        return
    
    # 显示当前闪卡
    current_index = st.session_state.current_card_index % len(all_flashcards)
    current_card = all_flashcards[current_index]
    
    st.markdown("---")
    
    # 进度显示
    col1, col2 = st.columns([3, 1])
    with col1:
        st.progress((current_index + 1) / len(all_flashcards))
    with col2:
        st.markdown(f"**{current_index + 1} / {len(all_flashcards)}**")
    
    # 闪卡显示
    card_mastery = st.session_state.flashcard_mastery.get(current_card['id'], 0)
    mastery_color = get_mastery_color(card_mastery)
    
    st.markdown(f"""
    <div style='background: linear-gradient(135deg, {mastery_color}22 0%, {mastery_color}11 100%); 
                padding: 30px; border-radius: 15px; border-left: 5px solid {mastery_color};
                box-shadow: 0 4px 6px rgba(0,0,0,0.1); min-height: 250px;'>
        <div style='background-color: white; padding: 20px; border-radius: 10px;'>
            <h2 style='color: #1976d2; margin-bottom: 20px;'>
                {current_card.get('chapter', '历史知识')} - {current_card['title']}
            </h2>
            <div style='font-size: 1.1em; line-height: 1.8;'>
                <strong>🤔 问题：</strong>{current_card['question']}
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # 显示/隐藏答案
    col1, col2, col3 = st.columns([2, 2, 2])
    
    with col1:
        if not st.session_state.show_answer:
            if st.button("👁️ 查看答案", use_container_width=True, type="primary"):
                st.session_state.show_answer = True
                st.rerun()
    
    # 显示答案后的内容
    if st.session_state.show_answer:
        # 快速答案
        st.markdown(f"""
        <div style='background-color: #e8f5e9; padding: 20px; border-radius: 10px; 
                    border-left: 5px solid #4caf50; margin: 20px 0;'>
            <h3 style='color: #2e7d32; margin-bottom: 15px;'>✅ 答案</h3>
            <div style='font-size: 1.05em; line-height: 1.8;'>
                {current_card['answer']}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # 关键提示（如果有）
        if 'key_points' in current_card:
            st.markdown("**🔑 关键点：**")
            for point in current_card['key_points']:
                st.markdown(f"- {point}")
        
        # AI深度讲解按钮
        st.markdown("---")
        col_ai1, col_ai2 = st.columns(2)
        
        with col_ai1:
            if st.button("🤖 AI深度讲解", use_container_width=True, type="primary"):
                show_ai_explanation(ai_service, current_card)
        
        with col_ai2:
            if st.button("💡 AI记忆技巧", use_container_width=True):
                show_ai_memory_tips(ai_service, current_card)
        
        # 掌握度评价
        st.markdown("---")
        st.subheader("📊 掌握程度")
        
        mastery_cols = st.columns(5)
        
        mastery_labels = [
            ("😟 不会", 0),
            ("🤔 模糊", 3),
            ("😐 一般", 5),
            ("😊 熟悉", 7),
            ("🎉 掌握", 10)
        ]
        
        for i, (label, score) in enumerate(mastery_labels):
            with mastery_cols[i]:
                if st.button(label, use_container_width=True, key=f"mastery_{score}"):
                    st.session_state.flashcard_mastery[current_card['id']] = score
                    st.success(f"已记录：{label}")
                    # 自动下一张
                    st.session_state.current_card_index += 1
                    st.session_state.show_answer = False
                    st.rerun()
        
        # 导航按钮
        st.markdown("---")
        nav_col1, nav_col2, nav_col3 = st.columns([1, 2, 1])
        
        with nav_col1:
            if st.button("⬅️ 上一张", use_container_width=True):
                st.session_state.current_card_index = max(0, current_index - 1)
                st.session_state.show_answer = False
                st.rerun()
        
        with nav_col2:
            if st.button("➡️ 下一张（跳过）", use_container_width=True):
                st.session_state.current_card_index += 1
                st.session_state.show_answer = False
                st.rerun()
        
        with nav_col3:
            if st.button("🔄 重新开始", use_container_width=True):
                st.session_state.current_card_index = 0
                st.session_state.show_answer = False
                st.rerun()
    
    # 侧边栏 - 复习统计
    with st.sidebar:
        st.subheader("📈 复习统计")
        
        if st.session_state.flashcard_mastery:
            reviewed_count = len(st.session_state.flashcard_mastery)
            avg_mastery = sum(st.session_state.flashcard_mastery.values()) / reviewed_count
            
            st.metric("已复习", f"{reviewed_count} 张")
            st.metric("平均掌握度", f"{avg_mastery:.1f}/10")
            
            # 掌握度分布
            mastery_levels = {
                '完全掌握 (8-10)': len([m for m in st.session_state.flashcard_mastery.values() if m >= 8]),
                '基本掌握 (5-7)': len([m for m in st.session_state.flashcard_mastery.values() if 5 <= m < 8]),
                '需加强 (0-4)': len([m for m in st.session_state.flashcard_mastery.values() if m < 5])
            }
            
            st.markdown("**掌握度分布：**")
            for level, count in mastery_levels.items():
                st.write(f"{level}: {count} 张")
        else:
            st.info("开始复习后这里会显示统计数据")
        
        # 生成练习题
        st.markdown("---")
        st.subheader("🎯 AI生成练习题")
        
        difficulty = st.selectbox("难度：", ["简单", "中等", "困难"])
        count = st.slider("题目数量：", 1, 5, 2)
        
        if st.button("生成练习题", use_container_width=True):
            generate_practice_questions(ai_service, current_card, difficulty, count)


def show_ai_explanation(ai_service, card):
    """显示AI深度讲解"""
    st.markdown("---")
    st.markdown("## 🤖 AI深度讲解")
    
    with st.spinner("💭 AI老师正在准备详细讲解..."):
        explanation = ai_service.explain_concept(
            f"知识点：{card['title']}\n问题：{card['question']}\n答案：{card['answer']}",
            level='detailed'
        )
        
        if explanation:
            st.markdown(explanation)
        else:
            st.error("AI暂时无法响应，请稍后重试")


def show_ai_memory_tips(ai_service, card):
    """显示AI记忆技巧"""
    st.markdown("---")
    st.markdown("## 💡 AI记忆技巧")
    
    with st.spinner("🧠 AI正在生成记忆技巧..."):
        tips = ai_service.generate_memory_tips(
            card['title'],
            card['answer']
        )
        
        if tips:
            st.markdown(tips)
        else:
            st.error("AI暂时无法响应，请稍后重试")


def generate_practice_questions(ai_service, card, difficulty, count):
    """生成练习题"""
    st.markdown("---")
    st.markdown("## 📝 练习题")
    
    difficulty_map = {"简单": "easy", "中等": "medium", "困难": "hard"}
    
    with st.spinner("正在生成练习题..."):
        questions = ai_service.generate_questions(
            knowledge_points=[card['title']],
            difficulty=difficulty_map[difficulty],
            count=count,
            question_type="选择题"  # 默认生成选择题
        )
        
        if questions:
            for i, q in enumerate(questions, 1):
                with st.expander(f"📝 题目 {i}", expanded=(i==1)):
                    st.markdown(f"**{q.get('question', '')}**")
                    
                    # 选择题选项
                    if 'options' in q:
                        for key, value in q['options'].items():
                            st.write(f"{key}. {value}")
                    
                    # 查看答案按钮
                    if st.button(f"查看答案", key=f"q_answer_{i}"):
                        st.success(f"✅ 答案：{q.get('answer', '')}")
                        if 'explanation' in q:
                            st.info(f"💡 解析：{q['explanation']}")
        else:
            st.warning("生成失败，请稍后重试")


def get_mastery_color(mastery_level):
    """根据掌握度返回颜色"""
    if mastery_level >= 8:
        return "#4caf50"  # 绿色 - 掌握
    elif mastery_level >= 5:
        return "#ff9800"  # 橙色 - 一般
    elif mastery_level >= 3:
        return "#ffc107"  # 黄色 - 模糊
    else:
        return "#f44336"  # 红色 - 不会

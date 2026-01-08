"""
知识卡片/闪卡复习功能模块
基于遗忘曲线的智能复习系统
"""

import streamlit as st
from datetime import datetime, timedelta
import random
from data.history_flashcards import HISTORY_FLASHCARDS, get_cards_by_chapter, get_cards_by_difficulty


def render_flashcard_review():
    """渲染知识卡片复习页面"""
    
    st.markdown("""
    <div class="module-header">
        <div class="module-title">
            <span>🎴</span> 知识卡片复习
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="content-panel">
        <div class="panel-header">💡 功能说明</div>
        <ul style="color: #6b7280; line-height: 1.8;">
            <li>🎴 正反面卡片设计，高效记忆</li>
            <li>🔄 智能推送，基于遗忘曲线</li>
            <li>🏷️ 标记熟练度（熟练/模糊/不会）</li>
            <li>📅 每日复习任务，科学安排</li>
            <li>🏆 完成任务获得成就徽章</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    # 初始化session_state
    if 'card_mastery' not in st.session_state:
        st.session_state['card_mastery'] = {}  # 卡片掌握情况
    if 'review_history' not in st.session_state:
        st.session_state['review_history'] = []
    if 'daily_tasks' not in st.session_state:
        st.session_state['daily_tasks'] = generate_daily_tasks()
    
    # 创建标签页
    tab1, tab2, tab3 = st.tabs(["📚 今日任务", "🎴 自由复习", "📊 学习报告"])
    
    with tab1:
        render_daily_tasks()
    
    with tab2:
        render_free_review()
    
    with tab3:
        render_review_report()


def generate_daily_tasks():
    """生成每日复习任务"""
    # 根据遗忘曲线生成任务
    # 1天前、2天前、7天前学习的卡片需要复习
    
    tasks = {
        'review': [],  # 需要复习的卡片
        'new': [],     # 新卡片
        'weak': []     # 不熟练的卡片
    }
    
    # 随机选择一些卡片作为今日任务（实际应基于学习记录）
    all_cards = HISTORY_FLASHCARDS.copy()
    random.shuffle(all_cards)
    
    # 5张复习卡片
    tasks['review'] = all_cards[:5]
    
    # 7张新卡片
    tasks['new'] = all_cards[5:12]
    
    # 3张薄弱卡片
    weak_cards = [card for card in st.session_state.get('card_mastery', {}).values() 
                  if card.get('level') == 'weak']
    tasks['weak'] = weak_cards[:3] if weak_cards else all_cards[12:15]
    
    return tasks


def render_daily_tasks():
    """渲染每日任务"""
    st.markdown("### 📅 今日学习任务")
    
    tasks = st.session_state['daily_tasks']
    
    # 任务概览
    col1, col2, col3 = st.columns(3)
    
    with col1:
        total_cards = len(tasks['review']) + len(tasks['new']) + len(tasks['weak'])
        st.metric("今日任务", f"{total_cards} 张卡片")
    
    with col2:
        completed = sum(1 for card in tasks['review'] + tasks['new'] + tasks['weak']
                       if st.session_state.get('card_mastery', {}).get(card['id'], {}).get('today_reviewed', False))
        st.metric("已完成", f"{completed} 张")
    
    with col3:
        progress = int(completed / total_cards * 100) if total_cards > 0 else 0
        st.metric("完成度", f"{progress}%")
    
    # 任务详情
    st.markdown("---")
    
    # 复习任务
    with st.expander(f"🔄 巩固昨天的知识 ({len(tasks['review'])} 张)", expanded=True):
        if tasks['review']:
            for i, card in enumerate(tasks['review']):
                render_flashcard(card, f"review_{i}")
        else:
            st.info("暂无复习任务")
    
    # 新知识
    with st.expander(f"📖 学习新内容 ({len(tasks['new'])} 张)", expanded=False):
        if tasks['new']:
            for i, card in enumerate(tasks['new']):
                render_flashcard(card, f"new_{i}")
        else:
            st.info("暂无新卡片")
    
    # 薄弱项
    with st.expander(f"💪 重点攻克薄弱项 ({len(tasks['weak'])} 张)", expanded=False):
        if tasks['weak']:
            for i, card in enumerate(tasks['weak']):
                render_flashcard(card, f"weak_{i}")
        else:
            st.success("没有薄弱项，继续保持！")
    
    # 完成任务奖励
    if progress == 100:
        st.balloons()
        st.success("🎉 恭喜完成今日所有任务！获得成就徽章：每日坚持 🏅")


def render_flashcard(card, key_prefix):
    """渲染单个卡片"""
    card_id = card['id']
    
    # 卡片容器
    st.markdown(f"""
    <div class="content-panel" style="margin: 15px 0; background: linear-gradient(135deg, #fff9f0 0%, #fff 100%);">
        <div style="padding: 5px 0;">
            <span class="badge badge-primary">{card.get('category', '知识点')}</span>
            <span class="badge badge-warning" style="margin-left: 10px;">难度: {card.get('difficulty', 'medium')}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # 正面/背面切换
    show_answer_key = f"show_answer_{key_prefix}_{card_id}"
    if show_answer_key not in st.session_state:
        st.session_state[show_answer_key] = False
    
    # 显示问题
    st.markdown(f"""
    <div style="background: white; padding: 20px; border-radius: 16px; border: 2px solid #fde8dc; margin: 10px 0;">
        <div style="font-size: 16px; font-weight: 600; color: #1f2937; margin-bottom: 10px;">❓ 问题</div>
        <div style="font-size: 15px; color: #4b5563; line-height: 1.8;">{card['front']}</div>
    </div>
    """, unsafe_allow_html=True)
    
    # 显示答案（点击后）
    if st.session_state[show_answer_key]:
        st.markdown(f"""
        <div style="background: #f0fdf4; padding: 20px; border-radius: 16px; border: 2px solid #86efac; margin: 10px 0;">
            <div style="font-size: 16px; font-weight: 600; color: #166534; margin-bottom: 10px;">✅ 答案</div>
            <div style="font-size: 15px; color: #166534; line-height: 1.8; white-space: pre-wrap;">{card['back']}</div>
        </div>
        """, unsafe_allow_html=True)
        
        # 掌握程度反馈
        st.markdown("**你掌握得如何？**")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("😊 熟练", key=f"master_{key_prefix}_{card_id}", use_container_width=True):
                update_card_mastery(card_id, 'mastered')
                st.session_state[show_answer_key] = False
                st.success("✅ 已标记为熟练！")
                st.rerun()
        
        with col2:
            if st.button("🤔 模糊", key=f"fuzzy_{key_prefix}_{card_id}", use_container_width=True):
                update_card_mastery(card_id, 'fuzzy')
                st.session_state[show_answer_key] = False
                st.warning("⚠️ 已标记为模糊，建议多复习")
                st.rerun()
        
        with col3:
            if st.button("😰 不会", key=f"weak_{key_prefix}_{card_id}", use_container_width=True):
                update_card_mastery(card_id, 'weak')
                st.session_state[show_answer_key] = False
                st.error("❌ 已标记为不会，需要重点学习")
                st.rerun()
    else:
        # 显示答案按钮
        if st.button("🔍 查看答案", key=f"reveal_{key_prefix}_{card_id}", use_container_width=True):
            st.session_state[show_answer_key] = True
            st.rerun()
    
    st.markdown("---")


def update_card_mastery(card_id, level):
    """更新卡片掌握程度"""
    if 'card_mastery' not in st.session_state:
        st.session_state['card_mastery'] = {}
    
    st.session_state['card_mastery'][card_id] = {
        'level': level,
        'last_review': datetime.now().strftime('%Y-%m-%d'),
        'review_count': st.session_state['card_mastery'].get(card_id, {}).get('review_count', 0) + 1,
        'today_reviewed': True
    }
    
    # 记录到复习历史
    st.session_state['review_history'].append({
        'card_id': card_id,
        'level': level,
        'date': datetime.now().strftime('%Y-%m-%d %H:%M')
    })


def render_free_review():
    """渲染自由复习模式"""
    st.markdown("### 🎴 自由复习")
    
    st.info("💡 选择章节或难度，自由复习知识卡片")
    
    # 筛选选项
    col1, col2 = st.columns(2)
    
    with col1:
        filter_type = st.selectbox(
            "筛选方式",
            ["按章节", "按难度", "按分类", "随机抽取"]
        )
    
    with col2:
        if filter_type == "按章节":
            filter_value = st.selectbox(
                "选择章节",
                ["chapter_origin", "chapter_qin_unification", "chapter_opium_wars", 
                 "chapter_xinhai_revolution", "chapter_reform_opening"]
            )
            cards = get_cards_by_chapter(filter_value)
        
        elif filter_type == "按难度":
            filter_value = st.selectbox("选择难度", ["easy", "medium", "hard"])
            cards = get_cards_by_difficulty(filter_value)
        
        elif filter_type == "按分类":
            filter_value = st.selectbox(
                "选择分类",
                ["基础知识", "制度分析", "时代特征", "历史意义", "原因分析"]
            )
            cards = [c for c in HISTORY_FLASHCARDS if c.get('category') == filter_value]
        
        else:
            st.info("随机模式")
            cards = random.sample(HISTORY_FLASHCARDS, min(10, len(HISTORY_FLASHCARDS)))
    
    # 显示卡片数量
    st.markdown(f"**找到 {len(cards)} 张卡片**")
    
    if cards:
        # 显示卡片
        for i, card in enumerate(cards):
            render_flashcard(card, f"free_{i}")
    else:
        st.warning("没有找到符合条件的卡片")


def render_review_report():
    """渲染学习报告"""
    st.markdown("### 📊 学习报告")
    
    if not st.session_state.get('card_mastery'):
        st.info("还没有学习记录，快去复习吧！")
        return
    
    mastery_data = st.session_state['card_mastery']
    
    # 统计数据
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("累计学习", f"{len(mastery_data)} 张")
    
    with col2:
        mastered_count = sum(1 for v in mastery_data.values() if v.get('level') == 'mastered')
        st.metric("已熟练", mastered_count)
    
    with col3:
        fuzzy_count = sum(1 for v in mastery_data.values() if v.get('level') == 'fuzzy')
        st.metric("模糊", fuzzy_count)
    
    with col4:
        weak_count = sum(1 for v in mastery_data.values() if v.get('level') == 'weak')
        st.metric("不会", weak_count)
    
    # 掌握度分布
    st.markdown("---")
    st.markdown("#### 📊 掌握度分布")
    
    if len(mastery_data) > 0:
        import plotly.graph_objects as go
        
        levels = {'mastered': mastered_count, 'fuzzy': fuzzy_count, 'weak': weak_count}
        
        fig = go.Figure(data=[go.Pie(
            labels=['熟练', '模糊', '不会'],
            values=[mastered_count, fuzzy_count, weak_count],
            marker=dict(colors=['#86efac', '#fde047', '#fca5a5']),
            hole=.3
        )])
        
        fig.update_layout(
            title="知识掌握情况",
            height=300
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # 复习历史
    if st.session_state.get('review_history'):
        st.markdown("---")
        st.markdown("#### 📅 最近复习记录")
        
        import pandas as pd
        df = pd.DataFrame(st.session_state['review_history'][-10:])  # 最近10条
        st.dataframe(df, use_container_width=True, hide_index=True)
    
    # 学习建议
    st.markdown("---")
    st.markdown("#### 💡 学习建议")
    
    if weak_count > 5:
        st.warning(f"你有 {weak_count} 张卡片标记为'不会'，建议重点复习这些内容")
    elif fuzzy_count > 10:
        st.info(f"你有 {fuzzy_count} 张卡片标记为'模糊'，多复习几遍就能掌握了！")
    else:
        st.success("掌握情况良好，继续保持！可以学习更多新内容。")

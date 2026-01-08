"""
闪卡复习模块 - AI增强版
智能复习+深度讲解
"""

import streamlit as st
from data.history_flashcards import HISTORY_FLASHCARDS
from modules.ai_service import get_ai_service
import random
from datetime import datetime, timedelta

def render_flashcard_review():
    """渲染闪卡复习页面"""
    st.title("📇 AI闪卡复习 - 智能学习")
    
    # 获取AI服务
    ai_service = get_ai_service()
    
    st.markdown("""
    <div class="info-box">
        <h3>✨ AI赋能的智能复习</h3>
        <ul>
            <li>🎯 AI分析遗忘曲线，智能推荐复习</li>
            <li>💡 不只显示答案，AI深度讲解</li>
            <li>🔗 关联知识点，建立知识网络</li>
            <li>📝 AI生成记忆技巧和口诀</li>
            <li>🎓 根据掌握情况，自动调整难度</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    # 初始化学习记录
    if 'card_records' not in st.session_state:
        st.session_state.card_records = {}
        # 为每张卡片初始化记录
        for card in HISTORY_FLASHCARDS:
            st.session_state.card_records[card['id']] = {
                'mastery': 0,  # 掌握度 0-10
                'last_review': None,
                'review_count': 0,
                'correct_count': 0,
                'need_ai_help': False
            }
    
    # 学习模式选择
    st.subheader("📚 选择学习模式")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🎯 AI推荐复习", use_container_width=True, type="primary"):
            st.session_state['review_mode'] = 'ai_recommend'
    
    with col2:
        if st.button("📖 按章节复习", use_container_width=True):
            st.session_state['review_mode'] = 'by_chapter'
    
    with col3:
        if st.button("🔀 随机复习", use_container_width=True):
            st.session_state['review_mode'] = 'random'
    
    # 根据模式选择卡片
    if 'review_mode' in st.session_state:
        mode = st.session_state['review_mode']
        
        if mode == 'ai_recommend':
            cards_to_review = get_ai_recommended_cards(st.session_state.card_records)
            st.info(f"🤖 AI为你智能推荐了 {len(cards_to_review)} 张需要复习的卡片")
        
        elif mode == 'by_chapter':
            chapter = st.selectbox(
                "选择章节",
                list(set([card['chapter_id'] for card in HISTORY_FLASHCARDS]))
            )
            cards_to_review = [c for c in HISTORY_FLASHCARDS if c['chapter_id'] == chapter]
        
        else:  # random
            cards_to_review = random.sample(HISTORY_FLASHCARDS, min(10, len(HISTORY_FLASHCARDS)))
        
        # 显示复习进度
        if cards_to_review:
            if 'current_card_idx' not in st.session_state:
                st.session_state.current_card_idx = 0
            
            progress = (st.session_state.current_card_idx + 1) / len(cards_to_review)
            st.progress(progress, text=f"进度：{st.session_state.current_card_idx + 1}/{len(cards_to_review)}")
            
            # 显示当前卡片
            current_card = cards_to_review[st.session_state.current_card_idx]
            
            st.markdown("---")
            render_flashcard_with_ai(current_card, ai_service)
            
            # 导航按钮
            col1, col2, col3 = st.columns([1, 2, 1])
            
            with col1:
                if st.button("⬅️ 上一张", disabled=(st.session_state.current_card_idx == 0)):
                    st.session_state.current_card_idx -= 1
                    st.rerun()
            
            with col2:
                pass
            
            with col3:
                if st.button("下一张 ➡️", disabled=(st.session_state.current_card_idx >= len(cards_to_review) - 1)):
                    st.session_state.current_card_idx += 1
                    st.rerun()
    
    # 学习统计
    if st.session_state.card_records:
        st.markdown("---")
        st.subheader("📊 学习统计")
        
        total_cards = len(HISTORY_FLASHCARDS)
        mastered = sum(1 for r in st.session_state.card_records.values() if r['mastery'] >= 8)
        learning = sum(1 for r in st.session_state.card_records.values() if 3 <= r['mastery'] < 8)
        weak = sum(1 for r in st.session_state.card_records.values() if r['mastery'] < 3)
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("总卡片数", total_cards)
        
        with col2:
            st.metric("已掌握", mastered, delta=f"{mastered/total_cards*100:.0f}%")
        
        with col3:
            st.metric("学习中", learning)
        
        with col4:
            st.metric("需加强", weak)
        
        # AI学习建议
        if st.button("🤖 AI分析我的学习情况"):
            with st.spinner("AI正在分析..."):
                analysis = analyze_learning_progress(ai_service, st.session_state.card_records, HISTORY_FLASHCARDS)
                if analysis:
                    st.markdown("### 📋 AI学习报告")
                    st.markdown(analysis)


def render_flashcard_with_ai(card, ai_service):
    """渲染单张卡片（AI增强）"""
    
    st.markdown(f"""
    <div class="content-panel">
        <h3>📇 {card['front']}</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # 显示/隐藏答案
    if f"show_answer_{card['id']}" not in st.session_state:
        st.session_state[f"show_answer_{card['id']}"] = False
    
    if not st.session_state[f"show_answer_{card['id']}"]:
        if st.button("💡 查看答案", key=f"btn_{card['id']}", type="primary"):
            st.session_state[f"show_answer_{card['id']}"] = True
            st.rerun()
    
    else:
        # 显示基本答案
        st.markdown("### ✅ 答案")
        st.markdown(f"""
        <div style="background-color: #fff3e0; padding: 15px; border-radius: 10px;">
            {card['back']}
        </div>
        """, unsafe_allow_html=True)
        
        # AI深度讲解按钮
        if st.button("🤖 AI深度讲解", key=f"ai_explain_{card['id']}"):
            with st.spinner("AI老师正在准备讲解..."):
                explanation = ai_service.explain_concept(
                    card['front'],
                    level='detailed'
                )
                
                if explanation:
                    st.markdown("### 👨‍🏫 AI老师的深度讲解")
                    st.markdown(f"""
                    <div style="background-color: #e3f2fd; padding: 15px; border-radius: 10px;">
                        {explanation}
                    </div>
                    """, unsafe_allow_html=True)
        
        # AI生成记忆技巧
        if st.button("🎯 AI生成记忆技巧", key=f"memory_{card['id']}"):
            with st.spinner("AI正在生成记忆方法..."):
                memory_tips = ai_service.generate_memory_tips(
                    content=f"{card['front']}\n{card['back']}",
                    student_confusion=None
                )
                
                if memory_tips:
                    st.markdown("### 💡 记忆技巧")
                    st.markdown(memory_tips)
        
        # 掌握程度评估
        st.markdown("---")
        st.markdown("### 📈 掌握程度")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("😊 掌握了", use_container_width=True, type="primary"):
                update_card_mastery(card['id'], True)
                st.success("很好！继续保持！")
        
        with col2:
            if st.button("🤔 模糊", use_container_width=True):
                update_card_mastery(card['id'], False)
                st.info("没关系，多复习几次就好了")
        
        with col3:
            if st.button("❌ 不会", use_container_width=True):
                update_card_mastery(card['id'], False)
                st.session_state.card_records[card['id']]['need_ai_help'] = True
                st.warning("标记为需要重点复习")


def get_ai_recommended_cards(card_records):
    """AI推荐需要复习的卡片"""
    
    cards_with_priority = []
    
    for card in HISTORY_FLASHCARDS:
        record = card_records.get(card['id'], {'mastery': 0, 'last_review': None})
        
        # 计算优先级（0-100）
        priority = 0
        
        # 1. 掌握度低的优先
        priority += (10 - record['mastery']) * 10
        
        # 2. 距离上次复习时间久的优先
        if record['last_review']:
            days_since = (datetime.now() - record['last_review']).days
            priority += min(days_since * 5, 30)
        else:
            priority += 50  # 从未复习过的高优先级
        
        # 3. 标记为需要AI帮助的优先
        if record.get('need_ai_help'):
            priority += 20
        
        cards_with_priority.append((card, priority))
    
    # 按优先级排序
    cards_with_priority.sort(key=lambda x: x[1], reverse=True)
    
    # 返回前10张
    return [card for card, _ in cards_with_priority[:10]]


def update_card_mastery(card_id, is_correct):
    """更新卡片掌握度"""
    if card_id in st.session_state.card_records:
        record = st.session_state.card_records[card_id]
        
        # 更新复习记录
        record['review_count'] += 1
        record['last_review'] = datetime.now()
        
        if is_correct:
            record['correct_count'] += 1
            # 掌握度+1，最高10
            record['mastery'] = min(record['mastery'] + 1, 10)
        else:
            # 掌握度-1，最低0
            record['mastery'] = max(record['mastery'] - 1, 0)


def analyze_learning_progress(ai_service, card_records, all_cards):
    """AI分析学习进度"""
    
    # 准备数据
    total = len(all_cards)
    mastered = sum(1 for r in card_records.values() if r['mastery'] >= 8)
    weak_cards = [c for c in all_cards if card_records.get(c['id'], {}).get('mastery', 0) < 3]
    
    analysis_data = {
        'total_cards': total,
        'mastered_cards': mastered,
        'mastery_rate': f"{mastered/total*100:.1f}%",
        'weak_topics': [c['front'][:30] for c in weak_cards[:5]],
        'total_reviews': sum(r['review_count'] for r in card_records.values())
    }
    
    return ai_service.analyze_learning_data(analysis_data)

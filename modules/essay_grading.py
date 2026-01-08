"""
材料题智能批改功能模块
AI分析学生答案，给出评分和改进建议
"""

import streamlit as st
from data.history_questions import HISTORY_QUESTIONS, get_questions_by_type


def render_essay_grading():
    """渲染材料题批改页面"""
    
    st.markdown("""
    <div class="module-header">
        <div class="module-title">
            <span>✍️</span> 材料题智能批改
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="content-panel">
        <div class="panel-header">💡 功能说明</div>
        <ul style="color: #6b7280; line-height: 1.8;">
            <li>📝 选择材料题进行作答</li>
            <li>🤖 AI智能分析答案质量</li>
            <li>📊 评估要点覆盖度、史料使用、逻辑结构</li>
            <li>💯 给出分数和优秀范文对比</li>
            <li>💡 标注可改进之处，提升答题能力</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    # 获取所有材料题
    material_questions = get_questions_by_type('material')
    
    if not material_questions:
        st.warning("暂无材料题，请稍后再试")
        return
    
    # 创建标签页：练习模式 / 批改记录
    tab1, tab2 = st.tabs(["📝 开始练习", "📊 批改记录"])
    
    with tab1:
        render_practice_mode(material_questions)
    
    with tab2:
        render_grading_history()


def render_practice_mode(material_questions):
    """渲染练习模式"""
    st.markdown("### 📚 选择题目")
    
    # 选择题目
    question_titles = [f"{i+1}. {q['chapter_id']} - 难度：{q['difficulty']}" 
                      for i, q in enumerate(material_questions)]
    
    selected_index = st.selectbox(
        "选择要练习的材料题",
        range(len(question_titles)),
        format_func=lambda i: question_titles[i]
    )
    
    selected_question = material_questions[selected_index]
    
    # 显示题目
    st.markdown("---")
    st.markdown("### 📋 题目内容")
    
    st.markdown(f"""
    <div class="content-panel" style="background: #fff8f3;">
        <div style="white-space: pre-wrap; line-height: 1.8; color: #1f2937;">
{selected_question['question']}
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # 学生作答区
    st.markdown("---")
    st.markdown("### ✍️ 你的答案")
    
    student_answer = st.text_area(
        "在此输入你的答案",
        height=300,
        placeholder="请按照题目要求，分点作答...",
        key=f"answer_{selected_question['id']}"
    )
    
    # 提交批改
    col1, col2 = st.columns([1, 3])
    with col1:
        if st.button("🚀 提交批改", type="primary", use_container_width=True):
            if student_answer.strip():
                with st.spinner("AI正在批改中..."):
                    # 进行批改
                    grading_result = grade_answer(selected_question, student_answer)
                    st.session_state['grading_result'] = grading_result
                    st.session_state['current_question'] = selected_question
                    st.rerun()
            else:
                st.warning("请先输入答案")
    
    with col2:
        if st.button("👀 查看参考答案", use_container_width=True):
            st.session_state['show_reference'] = True
            st.rerun()
    
    # 显示批改结果
    if st.session_state.get('grading_result'):
        render_grading_result(
            st.session_state['grading_result'],
            st.session_state['current_question']
        )
    
    # 显示参考答案
    if st.session_state.get('show_reference'):
        st.markdown("---")
        st.markdown("### 📖 参考答案")
        st.success(selected_question['answer'])
        
        if st.button("❌ 关闭参考答案"):
            st.session_state['show_reference'] = False
            st.rerun()


def grade_answer(question, student_answer):
    """AI批改答案"""
    # 这里应该调用AI API进行批改
    # 目前使用简单的关键词匹配模拟
    
    scoring_points = question.get('scoring_points', [])
    total_score = 100
    earned_score = 0
    
    # 检查要点覆盖
    covered_points = []
    missing_points = []
    
    for point in scoring_points:
        if point in student_answer:
            covered_points.append(point)
            earned_score += (total_score / len(scoring_points))
        else:
            missing_points.append(point)
    
    # 分析答题质量
    quality_analysis = analyze_answer_quality(student_answer, question)
    
    # 生成评语
    comments = generate_comments(covered_points, missing_points, quality_analysis)
    
    return {
        'score': int(earned_score),
        'total': total_score,
        'covered_points': covered_points,
        'missing_points': missing_points,
        'quality': quality_analysis,
        'comments': comments
    }


def analyze_answer_quality(answer, question):
    """分析答案质量"""
    quality = {}
    
    # 1. 字数分析
    word_count = len(answer)
    if word_count < 50:
        quality['length'] = {'score': 60, 'comment': '答案较简略，建议充分展开'}
    elif word_count < 150:
        quality['length'] = {'score': 80, 'comment': '字数适中'}
    else:
        quality['length'] = {'score': 95, 'comment': '答案详细充实'}
    
    # 2. 分点情况
    has_numbering = any(char in answer for char in ['①', '②', '③', '1.', '2.', '3.', '（1）', '（2）'])
    if has_numbering:
        quality['structure'] = {'score': 90, 'comment': '答案结构清晰，分点作答'}
    else:
        quality['structure'] = {'score': 70, 'comment': '建议分点作答，结构更清晰'}
    
    # 3. 史料引用
    has_material_ref = '材料' in answer or '如材料所示' in answer or '材料中' in answer
    if has_material_ref:
        quality['material_use'] = {'score': 95, 'comment': '善于引用材料论证观点'}
    else:
        quality['material_use'] = {'score': 75, 'comment': '建议适当引用材料内容'}
    
    # 4. 学科术语
    keywords = question.get('keywords', [])
    term_count = sum(1 for kw in keywords if kw in answer)
    if term_count >= len(keywords) * 0.6:
        quality['terminology'] = {'score': 90, 'comment': '学科术语使用准确'}
    else:
        quality['terminology'] = {'score': 75, 'comment': '建议使用更多历史学科术语'}
    
    return quality


def generate_comments(covered_points, missing_points, quality):
    """生成评语"""
    comments = []
    
    # 要点覆盖评语
    if covered_points:
        comments.append(f"✅ **做得好：** 准确回答了{len(covered_points)}个要点：{', '.join(covered_points[:3])}")
    
    if missing_points:
        comments.append(f"⚠️ **可改进：** 遗漏了以下要点：{', '.join(missing_points)}")
    
    # 质量评语
    for aspect, data in quality.items():
        if data['score'] < 85:
            comments.append(f"💡 **{data['comment']}**")
    
    return comments


def render_grading_result(result, question):
    """渲染批改结果"""
    st.markdown("---")
    st.markdown("### 📊 批改结果")
    
    # 分数展示
    score_col1, score_col2, score_col3 = st.columns(3)
    
    with score_col1:
        st.metric("得分", f"{result['score']}", help="满分100分")
    
    with score_col2:
        coverage_rate = len(result['covered_points']) / len(question['scoring_points']) * 100
        st.metric("要点覆盖率", f"{int(coverage_rate)}%")
    
    with score_col3:
        avg_quality = sum(q['score'] for q in result['quality'].values()) / len(result['quality'])
        st.metric("答题质量", f"{int(avg_quality)}", help="综合评分")
    
    # 详细分析
    st.markdown("---")
    
    # 要点分析
    with st.expander("📋 要点覆盖分析", expanded=True):
        if result['covered_points']:
            st.success(f"✅ 已覆盖的要点（{len(result['covered_points'])}个）：")
            for point in result['covered_points']:
                st.markdown(f"- {point}")
        
        if result['missing_points']:
            st.warning(f"❌ 遗漏的要点（{len(result['missing_points'])}个）：")
            for point in result['missing_points']:
                st.markdown(f"- {point}")
    
    # 质量分析
    with st.expander("🎯 答题质量分析", expanded=True):
        quality_data = []
        for aspect, data in result['quality'].items():
            aspect_name = {
                'length': '字数充实度',
                'structure': '结构清晰度',
                'material_use': '史料运用',
                'terminology': '术语规范性'
            }.get(aspect, aspect)
            
            quality_data.append({
                '评估维度': aspect_name,
                '得分': data['score'],
                '评语': data['comment']
            })
        
        import pandas as pd
        df = pd.DataFrame(quality_data)
        st.dataframe(df, use_container_width=True, hide_index=True)
    
    # 总评
    st.markdown("---")
    st.markdown("### 💬 总体评价")
    
    for comment in result['comments']:
        st.info(comment)
    
    # 提升建议
    st.markdown("---")
    st.markdown("### 💡 提升建议")
    
    st.markdown("""
    <div class="highlight-box">
        <strong>材料题答题技巧：</strong>
        <ol style="margin-top: 10px; line-height: 1.8;">
            <li><strong>读材料：</strong> 仔细阅读材料，提取关键信息</li>
            <li><strong>看问题：</strong> 明确题目要求，确定答题方向</li>
            <li><strong>定要点：</strong> 结合所学知识，确定答题要点</li>
            <li><strong>巧组织：</strong> 分点作答，逻辑清晰，语言规范</li>
            <li><strong>再检查：</strong> 检查是否遗漏要点，表达是否准确</li>
        </ol>
    </div>
    """, unsafe_allow_html=True)
    
    # 保存到批改记录
    if 'grading_history' not in st.session_state:
        st.session_state['grading_history'] = []
    
    # 避免重复保存
    if not any(h['question_id'] == question['id'] and h['score'] == result['score'] 
               for h in st.session_state['grading_history']):
        st.session_state['grading_history'].append({
            'question_id': question['id'],
            'question_text': question['question'][:50] + '...',
            'score': result['score'],
            'date': '2026-01-07'
        })


def render_grading_history():
    """渲染批改记录"""
    st.markdown("### 📊 我的批改记录")
    
    if not st.session_state.get('grading_history'):
        st.info("还没有批改记录，快去练习吧！")
        return
    
    # 显示记录
    import pandas as pd
    df = pd.DataFrame(st.session_state['grading_history'])
    
    st.dataframe(df, use_container_width=True, hide_index=True)
    
    # 统计分析
    st.markdown("---")
    st.markdown("### 📈 学习统计")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("练习总数", len(st.session_state['grading_history']))
    
    with col2:
        avg_score = sum(h['score'] for h in st.session_state['grading_history']) / len(st.session_state['grading_history'])
        st.metric("平均分", f"{int(avg_score)}")
    
    with col3:
        max_score = max(h['score'] for h in st.session_state['grading_history'])
        st.metric("最高分", max_score)

"""
学习追踪与报告模块
追踪学生学习行为，生成个性化报告
"""

import streamlit as st
from modules.ai_service import get_ai_service
from datetime import datetime
import json


def init_learning_tracker():
    """初始化学习追踪器"""
    if 'learning_records' not in st.session_state:
        st.session_state.learning_records = {
            'page_visits': [],        # 页面访问记录
            'questions_attempted': [],  # 做过的题目
            'questions_correct': [],   # 做对的题目
            'questions_wrong': [],     # 做错的题目（错题本）
            'search_history': [],      # 搜索历史
            'knowledge_viewed': [],    # 查看过的知识点
            'session_start': datetime.now().isoformat()
        }
    
    if 'weak_points' not in st.session_state:
        st.session_state.weak_points = {}  # 薄弱知识点统计


def track_page_visit(page_name):
    """记录页面访问"""
    init_learning_tracker()
    st.session_state.learning_records['page_visits'].append({
        'page': page_name,
        'time': datetime.now().isoformat()
    })


def track_question_attempt(question, is_correct, user_answer, correct_answer, topic=None, options=None):
    """记录做题情况"""
    init_learning_tracker()
    
    record = {
        'question': question[:100] if len(question) > 100 else question,
        'user_answer': user_answer,
        'correct_answer': correct_answer,
        'is_correct': is_correct,
        'topic': topic,
        'options': options,  # 保存选项
        'time': datetime.now().isoformat()
    }
    
    st.session_state.learning_records['questions_attempted'].append(record)
    
    if is_correct:
        st.session_state.learning_records['questions_correct'].append(record)
    else:
        # 检查是否已经存在相同题目（去重）
        existing = False
        for existing_q in st.session_state.learning_records['questions_wrong']:
            if existing_q['question'] == record['question']:
                existing = True
                break
        
        if not existing:
            st.session_state.learning_records['questions_wrong'].append(record)
        
        # 更新薄弱知识点统计
        if topic:
            if topic not in st.session_state.weak_points:
                st.session_state.weak_points[topic] = 0
            st.session_state.weak_points[topic] += 1


def track_search(keyword):
    """记录搜索历史"""
    init_learning_tracker()
    st.session_state.learning_records['search_history'].append({
        'keyword': keyword,
        'time': datetime.now().isoformat()
    })


def track_knowledge_view(knowledge_point):
    """记录知识点查看"""
    init_learning_tracker()
    st.session_state.learning_records['knowledge_viewed'].append({
        'knowledge': knowledge_point,
        'time': datetime.now().isoformat()
    })


def get_wrong_questions():
    """获取错题本"""
    init_learning_tracker()
    return st.session_state.learning_records.get('questions_wrong', [])


def remove_wrong_question(question_text, topic=None):
    """删除已解决的错题"""
    init_learning_tracker()
    
    # 从错题列表中删除
    wrong_questions = st.session_state.learning_records['questions_wrong']
    st.session_state.learning_records['questions_wrong'] = [
        q for q in wrong_questions if q['question'] != question_text
    ]
    
    # 减少该专题的薄弱点计数
    if topic and topic in st.session_state.weak_points:
        st.session_state.weak_points[topic] -= 1
        if st.session_state.weak_points[topic] <= 0:
            del st.session_state.weak_points[topic]


def get_weak_points():
    """获取薄弱知识点（按错误次数排序）"""
    init_learning_tracker()
    weak = st.session_state.weak_points
    # 按错误次数排序
    sorted_weak = sorted(weak.items(), key=lambda x: x[1], reverse=True)
    return sorted_weak


def get_learning_summary():
    """获取学习总结"""
    init_learning_tracker()
    records = st.session_state.learning_records
    
    total_questions = len(records['questions_attempted'])
    correct_count = len(records['questions_correct'])
    wrong_count = len(records['questions_wrong'])
    accuracy = correct_count / total_questions * 100 if total_questions > 0 else 0
    
    return {
        'total_questions': total_questions,
        'correct_count': correct_count,
        'wrong_count': wrong_count,
        'accuracy': accuracy,
        'pages_visited': len(records['page_visits']),
        'searches': len(records['search_history']),
        'knowledge_viewed': len(records['knowledge_viewed']),
        'weak_points': get_weak_points()[:5]  # 前5个薄弱点
    }


# ============ 错题本页面 ============
def render_wrong_questions():
    """渲染错题本页面"""
    st.title("📕 AI错题本")
    
    init_learning_tracker()
    ai_service = get_ai_service()
    
    wrong_questions = get_wrong_questions()
    
    if not wrong_questions:
        st.info("🎉 太棒了！你还没有做错过题目，继续保持！")
        st.markdown("""
        ### 💡 提示
        - 当你在**题目解析**、**专题练习**等模块做错题目时，会自动收录到这里
        - 错题本会帮助你针对性地复习薄弱环节
        """)
        return
    
    st.markdown(f"""
    <div style='background: linear-gradient(135deg, #ff6b6b 0%, #ee5a5a 100%); 
                padding: 20px; border-radius: 12px; margin-bottom: 20px;'>
        <h3 style='color: white; margin: 0;'>📊 错题统计</h3>
        <p style='color: white; margin: 10px 0 0 0;'>
            共收录 <strong>{len(wrong_questions)}</strong> 道错题，
            点击可查看详情和AI解析
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # 打印和导出功能
    col_print, col_export = st.columns(2)
    
    with col_print:
        if st.button("🖨️ 打印错题本", use_container_width=True, type="primary"):
            # 生成可打印的HTML内容
            print_html = generate_printable_html(wrong_questions)
            st.session_state['print_html'] = print_html
            st.session_state['show_print_preview'] = True
            st.rerun()
    
    with col_export:
        # 生成文本格式的错题，用于下载
        export_text = generate_export_text(wrong_questions)
        st.download_button(
            label="📥 下载错题（TXT）",
            data=export_text,
            file_name="错题本.txt",
            mime="text/plain",
            use_container_width=True
        )
    
    # 显示打印预览
    if st.session_state.get('show_print_preview', False):
        st.markdown("---")
        st.markdown("### 🖨️ 打印预览")
        st.info("💡 点击下方按钮打印，或按 Ctrl+P 直接打印当前页面")
        
        # 打印按钮（使用JavaScript）
        print_js = """
        <script>
        function printContent() {
            var printWindow = window.open('', '_blank');
            printWindow.document.write(document.getElementById('print-content').innerHTML);
            printWindow.document.close();
            printWindow.print();
        }
        </script>
        <button onclick="printContent()" style="background: #667eea; color: white; padding: 10px 20px; 
                border: none; border-radius: 8px; cursor: pointer; font-size: 16px; margin: 10px 0;">
            🖨️ 点击打印
        </button>
        """
        st.markdown(print_js, unsafe_allow_html=True)
        
        # 显示打印内容预览
        st.markdown(f"""
        <div id="print-content" style="background: white; padding: 20px; border: 1px solid #ddd; border-radius: 8px;">
            {st.session_state.get('print_html', '')}
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("❌ 关闭预览"):
            st.session_state['show_print_preview'] = False
            st.rerun()
        
        st.markdown("---")
    
    # 按专题分组显示
    topics_dict = {}
    for q in wrong_questions:
        topic = q.get('topic', '未分类')
        if topic not in topics_dict:
            topics_dict[topic] = []
        topics_dict[topic].append(q)
    
    # 显示各专题错题
    for topic, questions in topics_dict.items():
        with st.expander(f"📁 {topic} ({len(questions)}道错题)", expanded=True):
            for i, q in enumerate(questions):
                st.markdown(f"**第{i+1}题：** {q['question']}")
                
                # 显示选项（如果有）
                if q.get('options'):
                    st.markdown("**选项：**")
                    options = q['options']
                    if isinstance(options, dict):
                        for key, value in options.items():
                            # 标记正确答案和用户选择
                            if key.upper() == q['correct_answer'].upper():
                                st.markdown(f"✅ {key}. {value} ← **正确答案**")
                            elif key.upper() == q['user_answer'].upper():
                                st.markdown(f"❌ {key}. {value} ← **你的答案**")
                            else:
                                st.markdown(f"{key}. {value}")
                    else:
                        for opt in options:
                            st.markdown(f"- {opt}")
                
                col1, col2 = st.columns(2)
                with col1:
                    st.error(f"❌ 你的答案：{q['user_answer']}")
                with col2:
                    st.success(f"✅ 正确答案：{q['correct_answer']}")
                
                # 按钮行：AI解析 + 已解决
                btn_col1, btn_col2 = st.columns([3, 1])
                
                with btn_col1:
                    # AI解析按钮
                    if st.button(f"🤖 AI解析这道题", key=f"explain_{topic}_{i}"):
                        with st.spinner("AI正在分析..."):
                            prompt = f"""请分析这道历史题目：
题目：{q['question']}
学生答案：{q['user_answer']}
正确答案：{q['correct_answer']}

请：
1. 解释为什么学生答错了
2. 讲解正确答案的原因
3. 给出记忆技巧
4. 推荐相关知识点复习"""
                            
                            messages = [
                                {"role": "system", "content": "你是一位耐心的高中历史老师，擅长帮助学生分析错题。"},
                                {"role": "user", "content": prompt}
                            ]
                            explanation = ai_service.call_api(messages)
                            
                            if explanation:
                                st.markdown("""
                                <div style='background: #f8f9fa; padding: 15px 15px 5px 15px; border-radius: 10px; 
                                            border-left: 4px solid #667eea; margin: 10px 0;'>
                                    <strong>🤖 AI错题分析：</strong>
                                </div>
                                """, unsafe_allow_html=True)
                                # 使用st.markdown正确渲染Markdown格式
                                st.markdown(explanation)
                
                with btn_col2:
                    # 已学会按钮
                    if st.button("✅ 已学会", key=f"solved_{topic}_{i}", type="primary"):
                        remove_wrong_question(q['question'], topic)
                        st.success("🎉 太棒了！该题已从错题本移除！")
                        st.rerun()
                
                st.markdown("---")


# ============ 学习报告页面 ============
def render_learning_report():
    """渲染学习报告页面"""
    st.title("📊 AI学习报告")
    
    init_learning_tracker()
    ai_service = get_ai_service()
    
    summary = get_learning_summary()
    
    # 统计卡片
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    padding: 20px; border-radius: 12px; text-align: center;'>
            <h2 style='color: white; margin: 0;'>{summary['total_questions']}</h2>
            <p style='color: white; margin: 5px 0 0 0;'>做题总数</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%); 
                    padding: 20px; border-radius: 12px; text-align: center;'>
            <h2 style='color: white; margin: 0;'>{summary['correct_count']}</h2>
            <p style='color: white; margin: 5px 0 0 0;'>答对数量</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, #ff6b6b 0%, #ee5a5a 100%); 
                    padding: 20px; border-radius: 12px; text-align: center;'>
            <h2 style='color: white; margin: 0;'>{summary['wrong_count']}</h2>
            <p style='color: white; margin: 5px 0 0 0;'>答错数量</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        accuracy_color = "#11998e" if summary['accuracy'] >= 70 else "#ff6b6b"
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, {accuracy_color} 0%, {accuracy_color}99 100%); 
                    padding: 20px; border-radius: 12px; text-align: center;'>
            <h2 style='color: white; margin: 0;'>{summary['accuracy']:.1f}%</h2>
            <p style='color: white; margin: 5px 0 0 0;'>正确率</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # 学习行为统计
    col_a, col_b = st.columns(2)
    
    with col_a:
        st.markdown("### 📈 学习行为")
        st.markdown(f"""
        - 📄 访问页面：**{summary['pages_visited']}** 次
        - 🔍 搜索知识：**{summary['searches']}** 次
        - 📚 查看知识点：**{summary['knowledge_viewed']}** 个
        """)
    
    with col_b:
        st.markdown("### ⚠️ 薄弱知识点")
        if summary['weak_points']:
            for topic, count in summary['weak_points']:
                st.markdown(f"- **{topic}**：错误 {count} 次")
        else:
            st.success("暂无明显薄弱点，继续保持！")
    
    st.markdown("---")
    
    # AI生成个性化报告
    st.markdown("### 🤖 AI个性化学习建议")
    
    if st.button("📝 生成AI学习报告", type="primary", use_container_width=True):
        with st.spinner("🤖 AI正在分析你的学习情况..."):
            prompt = f"""请为这位学生生成一份个性化学习报告：

【学习数据】
- 做题总数：{summary['total_questions']}道
- 答对数量：{summary['correct_count']}道
- 答错数量：{summary['wrong_count']}道
- 正确率：{summary['accuracy']:.1f}%
- 访问页面：{summary['pages_visited']}次
- 搜索次数：{summary['searches']}次
- 查看知识点：{summary['knowledge_viewed']}个

【薄弱知识点】
{chr(10).join([f"- {topic}：错误{count}次" for topic, count in summary['weak_points']]) if summary['weak_points'] else "暂无明显薄弱点"}

请生成报告，包含：
1. 学习情况总结（2-3句话）
2. 优点分析（至少2条）
3. 需要改进的地方（至少2条）
4. 针对薄弱知识点的具体学习建议
5. 下一步学习计划建议
"""
            
            messages = [
                {"role": "system", "content": "你是一位专业的高中历史学习顾问，擅长分析学生学习数据并给出针对性建议。"},
                {"role": "user", "content": prompt}
            ]
            report = ai_service.call_api(messages)
            
            if report:
                st.markdown(f"""
                <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                            padding: 25px; border-radius: 12px 12px 0 0;'>
                    <h3 style='color: white; margin: 0;'>📋 你的个性化学习报告</h3>
                </div>
                """, unsafe_allow_html=True)
                # 使用st.markdown正确渲染Markdown格式
                st.markdown(report)


# ============ 重点注意页面 ============
def render_focus_points():
    """渲染重点注意页面 - 分析频繁出错的知识点"""
    st.title("⚠️ 重点注意")
    
    init_learning_tracker()
    ai_service = get_ai_service()
    
    weak_points = get_weak_points()
    
    if not weak_points:
        st.info("🎉 目前没有发现需要重点注意的知识点！继续保持良好的学习状态。")
        st.markdown("""
        ### 💡 什么是"重点注意"？
        - 当你在同一类知识点上**多次出错**时，系统会自动识别
        - 这些知识点会被标记为"重点注意"，帮助你集中突破薄弱环节
        - AI会为你分析出错原因，并提供针对性的学习建议
        """)
        return
    
    st.markdown(f"""
    <div style='background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); 
                padding: 20px; border-radius: 12px; margin-bottom: 20px;'>
        <h3 style='color: white; margin: 0;'>🎯 薄弱知识点分析</h3>
        <p style='color: white; margin: 10px 0 0 0;'>
            系统检测到你在以下 <strong>{len(weak_points)}</strong> 个知识点上需要加强练习
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # 显示薄弱知识点列表
    for i, (topic, error_count) in enumerate(weak_points):
        severity = "🔴" if error_count >= 3 else "🟡" if error_count >= 2 else "🟢"
        
        with st.expander(f"{severity} {topic} - 错误{error_count}次", expanded=(i==0)):
            st.markdown(f"**错误次数：** {error_count} 次")
            
            # 获取该知识点的错题
            wrong_in_topic = [q for q in get_wrong_questions() if q.get('topic') == topic]
            
            if wrong_in_topic:
                st.markdown("**相关错题：**")
                for j, q in enumerate(wrong_in_topic[:3]):  # 最多显示3道
                    st.markdown(f"{j+1}. {q['question'][:50]}...")
            
            # AI分析按钮
            if st.button(f"🤖 AI深度分析「{topic}」", key=f"analyze_{topic}"):
                with st.spinner("AI正在分析..."):
                    # 收集该知识点的错题信息
                    wrong_details = "\n".join([
                        f"题目：{q['question'][:80]}... 学生答：{q['user_answer']} 正确答案：{q['correct_answer']}"
                        for q in wrong_in_topic[:5]
                    ])
                    
                    prompt = f"""请分析学生在「{topic}」这个知识点上的薄弱情况：

【错误统计】
错误次数：{error_count}次

【典型错题】
{wrong_details if wrong_details else "暂无具体错题记录"}

请：
1. 分析学生可能存在的认知误区
2. 解释该知识点的核心要点
3. 提供记忆技巧和学习方法
4. 推荐具体的复习步骤
5. 给出2-3道巩固练习题（含答案）
"""
                    
                    messages = [
                        {"role": "system", "content": "你是一位资深高中历史老师，擅长诊断学生的学习问题并给出针对性指导。"},
                        {"role": "user", "content": prompt}
                    ]
                    analysis = ai_service.call_api(messages)
                    
                    if analysis:
                        st.markdown(f"""
                        <div style='background: #fff3cd; padding: 15px 15px 5px 15px; border-radius: 12px; 
                                    border-left: 5px solid #ffc107; margin: 15px 0;'>
                            <h4 style='color: #856404; margin: 0;'>🎓 AI诊断报告：{topic}</h4>
                        </div>
                        """, unsafe_allow_html=True)
                        # 使用st.markdown正确渲染Markdown格式
                        st.markdown(analysis)


# ============ AI学习助手页面 ============
def render_ai_learning_assistant():
    """渲染AI学习助手页面 - 自由问答"""
    st.title("🤖 AI学习助手")
    
    ai_service = get_ai_service()
    
    st.markdown("""
    <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                padding: 20px; border-radius: 12px; margin-bottom: 20px;'>
        <h3 style='color: white; margin: 0;'>💬 有问题随时问我！</h3>
        <p style='color: white; margin: 10px 0 0 0;'>
            我是你的AI历史学习助手，可以回答历史问题、解释知识点、帮你复习备考
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # 初始化聊天历史
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    
    # 显示聊天历史
    chat_container = st.container()
    with chat_container:
        for msg in st.session_state.chat_history:
            if msg['role'] == 'user':
                st.markdown(f"""
                <div style='background: #e3f2fd; padding: 15px; border-radius: 12px; 
                            margin: 10px 0; text-align: right;'>
                    <strong>🧑‍🎓 你：</strong> {msg['content']}
                </div>
                """, unsafe_allow_html=True)
            else:
                # AI回复使用单独的容器，让Markdown正常渲染
                st.markdown("""
                <div style='background: #f8f9fa; padding: 15px 15px 5px 15px; border-radius: 12px; 
                            margin: 10px 0; border-left: 4px solid #667eea;'>
                    <strong>🤖 AI助手：</strong>
                </div>
                """, unsafe_allow_html=True)
                # 使用st.markdown渲染内容，这样Markdown格式会被正确处理
                st.markdown(msg['content'])
    
    # 输入区域
    st.markdown("---")
    
    # 快捷问题按钮
    st.markdown("**💡 快捷问题：**")
    quick_cols = st.columns(4)
    quick_questions = [
        "帮我复习一下洋务运动",
        "辛亥革命的意义是什么",
        "如何记忆历史年份",
        "材料题答题技巧"
    ]
    
    for i, q in enumerate(quick_questions):
        with quick_cols[i]:
            if st.button(q, key=f"quick_{i}", use_container_width=True):
                st.session_state.pending_question = q
                st.rerun()
    
    # 处理快捷问题
    if 'pending_question' in st.session_state:
        question = st.session_state.pending_question
        del st.session_state.pending_question
        
        st.session_state.chat_history.append({'role': 'user', 'content': question})
        
        with st.spinner("🤖 AI正在思考..."):
            messages = [
                {"role": "system", "content": "你是一位友善、专业的高中历史老师，用通俗易懂的语言帮助学生学习历史。回答要简洁、重点突出。"},
                {"role": "user", "content": question}
            ]
            response = ai_service.call_api(messages)
            
            if response:
                st.session_state.chat_history.append({'role': 'assistant', 'content': response})
        
        st.rerun()
    
    # 自定义输入
    user_input = st.text_input("输入你的问题：", placeholder="例如：请帮我分析一下抗日战争胜利的原因...")
    
    col1, col2 = st.columns([1, 4])
    with col1:
        send_btn = st.button("📤 发送", type="primary", use_container_width=True)
    with col2:
        if st.button("🗑️ 清空对话", use_container_width=True):
            st.session_state.chat_history = []
            st.rerun()
    
    if send_btn and user_input:
        st.session_state.chat_history.append({'role': 'user', 'content': user_input})
        
        with st.spinner("🤖 AI正在思考..."):
            # 构建带历史的对话
            messages = [
                {"role": "system", "content": "你是一位友善、专业的高中历史老师，用通俗易懂的语言帮助学生学习历史。回答要简洁、重点突出。"}
            ]
            
            # 添加最近的对话历史（最多5轮）
            recent_history = st.session_state.chat_history[-10:]
            for msg in recent_history:
                messages.append({"role": msg['role'], "content": msg['content']})
            
            response = ai_service.call_api(messages)
            
            if response:
                st.session_state.chat_history.append({'role': 'assistant', 'content': response})
        
        st.rerun()

# ============ 打印和导出功能 ============
def generate_printable_html(wrong_questions):
    """生成可打印的HTML格式错题本"""
    from datetime import datetime
    
    # 按专题分组
    topics_dict = {}
    for q in wrong_questions:
        topic = q.get('topic', '未分类')
        if topic not in topics_dict:
            topics_dict[topic] = []
        topics_dict[topic].append(q)
    
    html = f"""
    <html>
    <head>
        <meta charset="UTF-8">
        <style>
            body {{ font-family: "Microsoft YaHei", sans-serif; padding: 20px; }}
            h1 {{ color: #333; text-align: center; border-bottom: 2px solid #667eea; padding-bottom: 10px; }}
            h2 {{ color: #667eea; margin-top: 30px; }}
            .question-box {{ 
                border: 1px solid #ddd; 
                padding: 15px; 
                margin: 10px 0; 
                border-radius: 8px;
                page-break-inside: avoid;
            }}
            .question {{ font-weight: bold; font-size: 16px; margin-bottom: 10px; }}
            .options {{ margin: 10px 0; padding-left: 20px; }}
            .option {{ margin: 5px 0; }}
            .correct {{ color: #28a745; }}
            .wrong {{ color: #dc3545; }}
            .answer-row {{ display: flex; margin-top: 10px; }}
            .answer-box {{ flex: 1; padding: 8px; margin: 0 5px; border-radius: 5px; }}
            .user-answer {{ background: #ffebee; border: 1px solid #f44336; }}
            .correct-answer {{ background: #e8f5e9; border: 1px solid #4caf50; }}
            .footer {{ margin-top: 30px; text-align: center; color: #666; font-size: 12px; }}
            @media print {{
                .no-print {{ display: none; }}
                body {{ padding: 10px; }}
            }}
        </style>
    </head>
    <body>
        <h1>📕 高中历史错题本</h1>
        <p style="text-align: center; color: #666;">打印日期：{datetime.now().strftime('%Y年%m月%d日')}</p>
        <p style="text-align: center; color: #666;">共 {len(wrong_questions)} 道错题</p>
    """
    
    question_num = 1
    for topic, questions in topics_dict.items():
        html += f'<h2>📁 {topic}（{len(questions)}道）</h2>'
        
        for q in questions:
            html += f'''
            <div class="question-box">
                <div class="question">第{question_num}题：{q['question']}</div>
            '''
            
            # 显示选项
            if q.get('options'):
                html += '<div class="options">'
                options = q['options']
                if isinstance(options, dict):
                    for key, value in options.items():
                        if key.upper() == q['correct_answer'].upper():
                            html += f'<div class="option correct">✓ {key}. {value}（正确答案）</div>'
                        elif key.upper() == q['user_answer'].upper():
                            html += f'<div class="option wrong">✗ {key}. {value}（你的答案）</div>'
                        else:
                            html += f'<div class="option">{key}. {value}</div>'
                html += '</div>'
            
            html += f'''
                <div class="answer-row">
                    <div class="answer-box user-answer">❌ 你的答案：{q['user_answer']}</div>
                    <div class="answer-box correct-answer">✅ 正确答案：{q['correct_answer']}</div>
                </div>
            </div>
            '''
            question_num += 1
    
    html += '''
        <div class="footer">
            <p>📚 高中历史自适应学习系统 - 错题本打印版</p>
            <p>💡 温馨提示：多复习，常练习，历史学习更轻松！</p>
        </div>
    </body>
    </html>
    '''
    
    return html


def generate_export_text(wrong_questions):
    """生成文本格式的错题本，用于下载"""
    from datetime import datetime
    
    # 按专题分组
    topics_dict = {}
    for q in wrong_questions:
        topic = q.get('topic', '未分类')
        if topic not in topics_dict:
            topics_dict[topic] = []
        topics_dict[topic].append(q)
    
    lines = []
    lines.append("=" * 50)
    lines.append("📕 高中历史错题本")
    lines.append("=" * 50)
    lines.append(f"导出日期：{datetime.now().strftime('%Y年%m月%d日 %H:%M')}")
    lines.append(f"错题总数：{len(wrong_questions)} 道")
    lines.append("=" * 50)
    lines.append("")
    
    question_num = 1
    for topic, questions in topics_dict.items():
        lines.append(f"\n【{topic}】（{len(questions)}道）")
        lines.append("-" * 40)
        
        for q in questions:
            lines.append(f"\n第{question_num}题：")
            lines.append(f"题目：{q['question']}")
            
            # 显示选项
            if q.get('options'):
                lines.append("选项：")
                options = q['options']
                if isinstance(options, dict):
                    for key, value in options.items():
                        marker = ""
                        if key.upper() == q['correct_answer'].upper():
                            marker = " ← 正确答案"
                        elif key.upper() == q['user_answer'].upper():
                            marker = " ← 你的答案"
                        lines.append(f"  {key}. {value}{marker}")
            
            lines.append(f"你的答案：{q['user_answer']}")
            lines.append(f"正确答案：{q['correct_answer']}")
            lines.append("")
            question_num += 1
    
    lines.append("\n" + "=" * 50)
    lines.append("📚 高中历史自适应学习系统 - 错题本")
    lines.append("💡 温馨提示：多复习，常练习！")
    lines.append("=" * 50)
    
    return "\n".join(lines)
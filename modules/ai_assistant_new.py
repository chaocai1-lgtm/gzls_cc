"""
AI助手模块 - 升级版
提供深度智能问答和个性化学习辅导
"""

import streamlit as st
from modules.ai_service import get_ai_service
from data.history_knowledge_graph import search_knowledge_by_keyword

def render_ai_assistant():
    """渲染AI助手页面"""
    st.title("🤖 AI学习助手 - 史老师")
    
    # 获取AI服务
    ai_service = get_ai_service()
    
    st.markdown("""
    <div class="info-box">
        <h3>💡 双模式学习助手</h3>
        <p><strong>⚡ 快速模式</strong>：直接给出要点，高效学习</p>
        <p><strong>🤖 AI深度模式</strong>：详细讲解、引导思考、举一反三</p>
        <p>你可以根据需要灵活切换！</p>
    </div>
    """, unsafe_allow_html=True)
    
    # 学生信息（用于个性化）
    if 'student_context' not in st.session_state:
        st.session_state.student_context = {
            'weak_points': [],
            'recent_topics': [],
            'interaction_count': 0
        }
    
    # 快速问题按钮
    st.subheader("⚡ 快速提问")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**📖 历史知识**")
        if st.button("辛亥革命的意义", use_container_width=True):
            st.session_state['quick_action'] = ('quick', '辛亥革命', '辛亥革命的历史意义')
        if st.button("洋务运动为何失败", use_container_width=True):
            st.session_state['quick_action'] = ('quick', '洋务运动', '洋务运动失败原因')
        if st.button("戊戌变法的内容", use_container_width=True):
            st.session_state['quick_action'] = ('quick', '戊戌变法', '戊戌变法的主要内容')
    
    with col2:
        st.markdown("**🎓 学习方法**")
        if st.button("如何记忆历史年代", use_container_width=True):
            st.session_state['quick_action'] = ('method', '记忆方法', '如何快速记忆历史年代')
        if st.button("材料题答题技巧", use_container_width=True):
            st.session_state['quick_action'] = ('method', '答题技巧', '材料分析题答题技巧')
        if st.button("生成练习题", use_container_width=True):
            st.session_state['quick_action'] = ('generate', '练习题', '')
    
    # 处理快速操作
    if 'quick_action' in st.session_state:
        action_type, topic, question = st.session_state.quick_action
        process_quick_action(ai_service, action_type, topic, question)
        del st.session_state['quick_action']
    
    # 对话区域
    st.subheader("💬 深度交流")
    
    # 初始化对话历史
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
        # 欢迎消息
        st.session_state.chat_history.append({
            'role': 'assistant',
            'content': "你好！我是史老师👋 有什么历史问题困扰你吗？或者想深入了解某个历史事件？尽管问我！"
        })
    
    # 显示对话历史（添加滚动容器）
    chat_container = st.container()
    with chat_container:
        for i, msg in enumerate(st.session_state.chat_history):
            if msg['role'] == 'user':
                st.markdown(f"""
                <div style='background-color: #e3f2fd; padding: 10px; border-radius: 10px; margin: 5px 0;'>
                    <strong>🙋 你：</strong> {msg['content']}
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div style='background-color: #fff3e0; padding: 10px; border-radius: 10px; margin: 5px 0;'>
                    <strong>👨‍🏫 史老师：</strong><br>{msg['content']}
                </div>
                """, unsafe_allow_html=True)
                
                # 如果有AI详细讲解选项
                if msg.get('has_ai_detail') and not msg.get('ai_expanded'):
                    if st.button(f"🤖 AI深度讲解", key=f"ai_detail_{i}", use_container_width=True):
                        with st.spinner("🤔 AI老师正在准备深度讲解..."):
                            detail_response = ai_service.explain_concept(
                                msg.get('ai_topic', ''),
                                level='detailed'
                            )
                            if detail_response:
                                st.session_state.chat_history[i]['ai_expanded'] = True
                                st.session_state.chat_history.insert(i+1, {
                                    'role': 'assistant',
                                    'content': f"### 🤖 AI深度讲解\n\n{detail_response}"
                                })
                                st.rerun()
                            else:
                                st.warning("AI暂时无法响应，请稍后重试")
    
    # 用户输入
    st.markdown("---")
    col1, col2 = st.columns([4, 1])
    
    with col1:
        user_input = st.text_area(
            "💭 请输入你的问题：",
            height=80,
            placeholder="例如：为什么说辛亥革命成功了又失败了？"
        )
    
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        send_btn = st.button("📤 发送", type="primary", use_container_width=True)
        clear_btn = st.button("🗑️ 清空", use_container_width=True)
    
    if send_btn and user_input:
        # 添加用户消息
        st.session_state.chat_history.append({
            'role': 'user',
            'content': user_input
        })
        
        # 更新学生上下文
        st.session_state.student_context['interaction_count'] += 1
        
        # 搜索相关知识点
        related_knowledge = search_knowledge_by_keyword(user_input[:20])
        context_info = ""
        if related_knowledge:
            context_info = f"相关知识点：{', '.join([e['name'] for e in related_knowledge[:3]])}"
        
        # 生成AI回复
        with st.spinner("🤔 史老师正在思考..."):
            # 准备对话历史（最近5轮）
            recent_history = []
            for msg in st.session_state.chat_history[-10:]:  # 最近5轮对话
                recent_history.append({
                    "role": msg['role'],
                    "content": msg['content']
                })
            
            response = ai_service.chat_with_teacher(
                user_message=user_input,
                chat_history=recent_history[:-1],  # 不包括当前消息
                context=context_info
            )
            
            if response:
                st.session_state.chat_history.append({
                    'role': 'assistant',
                    'content': response
                })
            else:
                # 降级方案：显示相关知识点
                fallback_msg = "抱歉，AI老师暂时无法回答。"
                if related_knowledge:
                    fallback_msg += f"\n\n📚 为你找到相关知识点：\n"
                    for i, event in enumerate(related_knowledge[:3], 1):
                        fallback_msg += f"\n{i}. **{event['name']}** ({event['year']}年)\n   {event.get('description', '')[:100]}"
                    fallback_msg += "\n\n💡 你可以在历史时间轴中查看更多详情，或稍后重试提问。"
                else:
                    fallback_msg += "\n\n💡 建议：\n- 检查网络连接\n- 稍后重试\n- 或在历史时间轴、闪卡复习中查找相关内容"
                
                st.session_state.chat_history.append({
                    'role': 'assistant',
                    'content': fallback_msg
                })
        
        st.rerun()
    
    if clear_btn:
        st.session_state.chat_history = []
        st.session_state.student_context = {
            'weak_points': [],
            'recent_topics': [],
            'interaction_count': 0
        }
        st.rerun()
    
    # 侧边栏：AI生成功能
    with st.sidebar:
        st.markdown("### 🎯 AI专属服务")
        
        st.markdown("**📝 生成练习题**")
        topic = st.text_input("知识点", placeholder="如：洋务运动")
        
        col_diff, col_type = st.columns(2)
        with col_diff:
            difficulty = st.selectbox("难度", ["easy", "medium", "hard"], 
                                     format_func=lambda x: {"easy": "简单", "medium": "中等", "hard": "困难"}[x])
        with col_type:
            question_type = st.selectbox("题型", ["选择题", "材料题", "混合"])
        
        count = st.slider("题目数量", 1, 5, 2)
        
        if st.button("生成题目", type="primary", use_container_width=True):
            if topic:
                with st.spinner("AI正在出题..."):
                    questions = ai_service.generate_questions(
                        knowledge_points=[topic],
                        difficulty=difficulty,
                        count=count,
                        question_type=question_type
                    )
                    
                    if questions:
                        st.session_state['generated_questions'] = questions
                        st.success(f"成功生成{len(questions)}道题目！")
                        st.rerun()
        
        # 显示生成的题目
        if 'generated_questions' in st.session_state:
            st.markdown("---")
            st.markdown("**📋 生成的题目**")
            for i, q in enumerate(st.session_state.generated_questions, 1):
                with st.expander(f"📝 题目 {i}"):
                    st.markdown(f"**{q.get('question', '')}**")
                    
                    # 显示选项（如果有）
                    if 'options' in q:
                        st.markdown("**选项：**")
                        for key, value in q['options'].items():
                            st.write(f"{key}. {value}")
                    
                    # 查看答案按钮
                    if st.button(f"查看答案", key=f"sidebar_ans_{i}"):
                        st.success(f"✅ 答案：{q.get('answer', '')}")
                        if 'explanation' in q:
                            st.info(f"💡 解析：{q['explanation']}")


def process_quick_action(ai_service, action_type, topic, question):
    """处理快速操作"""
    if action_type == 'quick':
        # 快速回答模式
        quick_answer = get_quick_answer(topic, question)
        
        st.session_state.chat_history.append({
            'role': 'user',
            'content': question
        })
        
        # 显示快速回答
        st.session_state.chat_history.append({
            'role': 'assistant',
            'content': quick_answer,
            'has_ai_detail': True,
            'ai_topic': topic
        })
    
    elif action_type == 'method':
        # 学习方法 - 也用快速+AI详细模式
        quick_answer = get_method_answer(topic)
        
        st.session_state.chat_history.append({
            'role': 'user',
            'content': question
        })
        
        st.session_state.chat_history.append({
            'role': 'assistant',
            'content': quick_answer,
            'has_ai_detail': True,
            'ai_topic': question
        })
    
    elif action_type == 'generate':
        st.info("请使用右侧边栏的「AI生成练习题」功能")


def get_quick_answer(topic, question):
    """获取快速回答"""
    quick_answers = {
        '辛亥革命': """**辛亥革命的历史意义**：

**1. 政治方面** 🏛️
- 推翻了清朝统治，结束了2000多年的君主专制制度
- 建立了中华民国，使民主共和观念深入人心

**2. 思想方面** 💭
- 极大冲击了封建思想，解放了人们的思想
- 为新文化运动的兴起创造了条件

**3. 经济方面** 💰
- 为民族资本主义发展创造了有利条件
- 促进了近代工业的发展

**4. 社会方面** 👥
- 推动了社会风俗的改革
- 促进了社会的进步

**局限性**：
没有改变中国半殖民地半封建社会的性质，没有完成反帝反封建的任务。

---
💡 想了解更深入的分析？点击下方「AI深度讲解」""",
        
        '洋务运动': """**洋务运动失败的原因**：

**根本原因** ⭐
没有触动封建制度的根基，只是在维护封建制度的前提下学习西方技术

**具体原因**：
1. **指导思想落后** 💭
   - "中体西用"，只学技术不改制度
   
2. **缺乏完整规划** 📋
   - 各自为政，没有统一部署
   
3. **内部阻力大** ⚔️
   - 顽固派反对，经费不足
   
4. **外部环境恶劣** 🌍
   - 列强不愿看到中国强大
   
**失败标志**：
甲午战争中北洋水师全军覆没（1894年）

---
💡 想看对比分析（日本明治维新为何成功）？点击「AI深度讲解」""",
        
        '戊戌变法': """**戊戌变法的主要内容**：

**政治方面** 🏛️
- 改革政府机构，裁撤冗员
- 允许官民上书言事
- 开放言论，准许创办报刊

**经济方面** 💰
- 保护和奖励农工商业
- 改革财政，编制国家预算

**文化教育** 📚
- 废除八股，改试策论
- 开办京师大学堂
- 设立译书局，翻译外国书籍
- 派人出国留学

**军事方面** ⚔️
- 训练新式陆海军
- 裁减旧军，精练兵队

**时间**：1898年6月-9月（103天）

---
💡 想知道变法为什么失败？点击「AI深度讲解」"""
    }
    
    return quick_answers.get(topic, f"**{question}**\n\n这是一个重要的历史问题。\n\n💡 点击下方「AI深度讲解」获取详细分析")


def get_method_answer(topic):
    """获取学习方法的快速回答"""
    methods = {
        '记忆方法': """**历史年代快速记忆法**：

**1. 口诀记忆法** 🎵
- 例：一八四零鸦片战，一八九四甲午战
- 自己编顺口溜，朗朗上口

**2. 联想记忆法** 🔗
- 1949建国 → "四九年解放"
- 1911辛亥革命 → "双11购物？不，是革命！"

**3. 时间轴记忆法** 📊
- 画一条线，标注重要事件
- 看清历史发展脉络

**4. 对比记忆法** ⚖️
- 中日改革对比记忆
- 两次世界大战对比记忆

**5. 理解记忆法** 💡
- 理解为什么发生，比死记年份更重要
- 知道前因后果，自然记住时间

---
💡 想要更多具体例子和技巧？点击「AI深度讲解」""",
        
        '答题技巧': """**材料分析题答题技巧**：

**第一步：审题** 🔍
- 看清问什么（原因/影响/评价）
- 注意限定词（时间、地点、角度）

**第二步：读材料** 📖
- 圈关键词（时间、人物、事件）
- 理解材料主旨

**第三步：组织答案** ✍️
- **分点答**：1、2、3...条理清晰
- **总分总**：先总述再分点，最后总结
- **引材料**：原文关键句要引用

**第四步：规范表达** 📝
- 使用历史术语
- 语言简洁准确
- 字数适当（不少于150字）

**常见失分点** ❌
- 没有分点
- 没有结合材料
- 要点不全
- 表述不规范

---
💡 想看具体例题和答题示范？点击「AI深度讲解」"""
    }
    
    return methods.get(topic, "学习方法整理中...\n\n💡 点击「AI深度讲解」获取详细指导")

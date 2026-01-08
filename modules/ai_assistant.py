"""
AI历史小助手功能模块
对话式问答和学习指导
"""

import streamlit as st
from data.history_knowledge_graph import search_knowledge_by_keyword
from data.history_questions import search_questions


def render_ai_assistant():
    """渲染AI历史助手页面"""
    
    st.markdown("""
    <div class="module-header">
        <div class="module-title">
            <span>🤖</span> AI历史小助手
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="content-panel">
        <div class="panel-header">💡 我能帮你做什么</div>
        <ul style="color: #6b7280; line-height: 1.8;">
            <li>📚 回答历史问题，提供结构化答案</li>
            <li>💭 分析历史事件的原因和影响</li>
            <li>🎯 传授答题技巧和记忆方法</li>
            <li>🔗 关联相关知识点，构建知识网络</li>
            <li>💬 像朋友一样聊天，轻松学历史</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    # 初始化对话历史
    if 'chat_history' not in st.session_state:
        st.session_state['chat_history'] = [
            {
                'role': 'assistant',
                'content': '你好！我是AI历史小助手 🤖\n\n有什么历史问题想问我吗？比如：\n- 为什么洋务运动最后失败了？\n- 辛亥革命的意义是什么？\n- 如何记忆中国古代朝代顺序？'
            }
        ]
    
    # 显示对话历史
    st.markdown("### 💬 对话区")
    
    chat_container = st.container()
    
    with chat_container:
        for message in st.session_state['chat_history']:
            if message['role'] == 'user':
                st.markdown(f"""
                <div style="display: flex; justify-content: flex-end; margin: 15px 0;">
                    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                                color: white; padding: 15px 20px; border-radius: 18px 18px 4px 18px; 
                                max-width: 70%; text-align: left;">
                        {message['content']}
                    </div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div style="display: flex; justify-content: flex-start; margin: 15px 0;">
                    <div style="background: #f3f4f6; padding: 15px 20px; border-radius: 18px 18px 18px 4px; 
                                max-width: 70%; text-align: left; color: #1f2937; line-height: 1.8; white-space: pre-wrap;">
                        {message['content']}
                    </div>
                </div>
                """, unsafe_allow_html=True)
    
    # 输入区
    st.markdown("---")
    
    # 快捷问题按钮
    st.markdown("**💡 快捷提问：**")
    quick_questions = [
        "洋务运动为什么失败？",
        "辛亥革命的意义",
        "鸦片战争的影响",
        "如何记忆朝代顺序？"
    ]
    
    cols = st.columns(len(quick_questions))
    for i, question in enumerate(quick_questions):
        with cols[i]:
            if st.button(question, key=f"quick_{i}", use_container_width=True):
                # 添加用户问题
                st.session_state['chat_history'].append({
                    'role': 'user',
                    'content': question
                })
                
                # 生成AI回答
                answer = generate_ai_response(question)
                st.session_state['chat_history'].append({
                    'role': 'assistant',
                    'content': answer
                })
                
                st.rerun()
    
    # 用户输入
    col1, col2 = st.columns([5, 1])
    
    with col1:
        user_input = st.text_input(
            "输入你的问题",
            placeholder="例如：为什么要进行改革开放？",
            label_visibility="collapsed",
            key="user_input"
        )
    
    with col2:
        send_button = st.button("发送 📤", type="primary", use_container_width=True)
    
    if send_button and user_input:
        # 添加用户问题
        st.session_state['chat_history'].append({
            'role': 'user',
            'content': user_input
        })
        
        # 生成AI回答
        with st.spinner("AI正在思考..."):
            answer = generate_ai_response(user_input)
            st.session_state['chat_history'].append({
                'role': 'assistant',
                'content': answer
            })
        
        st.rerun()
    
    # 清除对话按钮
    if len(st.session_state.get('chat_history', [])) > 1:
        if st.button("🗑️ 清除对话历史"):
            st.session_state['chat_history'] = [{
                'role': 'assistant',
                'content': '对话已清除，有什么新的问题吗？😊'
            }]
            st.rerun()


def generate_ai_response(question):
    """生成AI回答（实际应调用AI API）"""
    # 这里应该调用实际的AI API（如DeepSeek等）
    # 目前使用规则匹配模拟
    
    question_lower = question.lower()
    
    # 关于洋务运动
    if '洋务运动' in question and ('失败' in question or '为什么' in question):
        return """我来帮你从三个角度分析洋务运动失败的原因：

**1️⃣ 根本原因：封建制度的束缚**
洋务运动只学习西方的技术和器物，没有改变封建制度和政治体制。就像一座房子地基腐朽了，光装修表面是救不了房子的。

**2️⃣ 直接原因：甲午战争失败**
1894年甲午战争中，洋务派苦心经营30年的北洋水师全军覆没，标志着洋务运动的破产。

**3️⃣ 指导思想的局限：中体西用**
"中体西用"只想保留封建统治的"体"，学习西方技术的"用"。但西方的先进技术是建立在资本主义制度基础上的，不改变制度只学技术，是行不通的。

**💡 记忆技巧：**
用"根本-直接-主观"三层框架，这个方法可以套用到其他改革运动的失败原因分析哦！

**🔗 相关知识点：**
- 百日维新（戊戌变法）
- 辛亥革命
- 新文化运动"""

    # 关于辛亥革命
    elif '辛亥革命' in question and '意义' in question:
        return """辛亥革命的历史意义可以从这几个方面理解：

**✅ 政治方面：**
1. 推翻了清朝统治，结束了中国两千多年的君主专制制度
2. 建立了资产阶级共和国，使民主共和观念深入人心

**✅ 社会方面：**
3. 沉重打击了帝国主义侵略势力
4. 为中国的进步打开了闸门，促进了思想解放

**❗ 局限性：**
没有改变中国半殖民地半封建社会的性质，革命果实被袁世凯窃取

**💡 答题技巧：**
回答"意义"类问题，要从政治、经济、思想文化等多角度分析，既要说积极影响，也可以提及局限性，这样答案更全面。

**🎯 相关事件：**
- 武昌起义（1911年）
- 中华民国成立（1912年）
- 袁世凯称帝失败"""

    # 关于鸦片战争
    elif '鸦片战争' in question and '影响' in question:
        return """鸦片战争对中国社会产生了深远影响：

**🔴 社会性质的变化（最重要）：**
中国开始从封建社会逐步沦为半殖民地半封建社会。

**📉 主权受损：**
- 领土主权：割让香港岛
- 关税主权：协定关税
- 司法主权：领事裁判权（后来条约中规定）

**⚔️ 社会矛盾的变化：**
外国资本主义与中华民族的矛盾成为主要矛盾，激发了中国人民的反抗斗争。

**📚 历史地位：**
鸦片战争是中国近代史的开端。

**💡 记忆方法：**
用"性质-主权-矛盾-地位"四步记忆法，简洁清晰！

**🔗 后续影响：**
- 引发了太平天国运动
- 推动了洋务运动的开展"""

    # 关于记忆方法
    elif '记忆' in question or '背' in question:
        if '朝代' in question:
            return """教你几个记忆中国古代朝代顺序的方法：

**📝 口诀记忆法：**
"夏商周秦汉，
魏晋南北隋，
唐宋元明清。"

**📊 时间节点记忆法：**
- 夏：约前2070年
- 秦：前221年（统一）
- 汉：前202年（西汉）
- 唐：618年
- 宋：960年
- 元：1271年
- 明：1368年
- 清：1636年

**🎯 特征记忆法：**
- 秦：第一个统一的中央集权国家
- 汉：丝绸之路开通
- 唐：最繁荣的朝代
- 宋：经济文化高度发达
- 元：疆域最大
- 明：郑和下西洋
- 清：最后一个封建王朝

**💡 小技巧：**
多做历史时间轴练习，把重大事件和朝代对应起来，自然就记住了！"""
        else:
            return """历史知识的记忆方法很多，我推荐这几种：

**1️⃣ 理解记忆：**
不要死记硬背，理解了历史事件的因果关系，自然就记住了。

**2️⃣ 归纳记忆：**
把相似的知识点归类，比如"中国古代选官制度的演变"、"近代中国的救亡图存运动"等。

**3️⃣ 对比记忆：**
对比相似事件的异同，如"洋务运动vs戊戌变法vs辛亥革命"。

**4️⃣ 图表记忆：**
画思维导图、时间轴，让知识可视化。

**5️⃣ 联想记忆：**
用有趣的联想帮助记忆，比如"商鞅变法→商人变法"。

需要哪方面的具体记忆方法，可以继续问我哦！"""

    # 关于改革开放
    elif '改革开放' in question:
        return """关于改革开放，我来详细讲解：

**⏰ 时间节点：**
1978年12月，十一届三中全会召开，标志着改革开放的开始。

**🎯 主要内容：**
1. **农村改革：** 家庭联产承包责任制（大包干）
2. **城市改革：** 国有企业改革，发展多种所有制经济
3. **对外开放：** 经济特区→沿海开放城市→全方位开放

**✨ 重大意义：**
- 是决定当代中国命运的关键抉择
- 使中国实现了从站起来到富起来的伟大飞跃
- 开辟了中国特色社会主义道路

**📍 重要标志：**
- 1980年：深圳等经济特区建立
- 1992年：邓小平南方谈话，改革开放进入新阶段
- 2001年：中国加入WTO

**💡 答题要点：**
回答改革开放问题时，要突出"历史转折""富起来""中国特色社会主义"这些关键词。

有具体想了解的方面吗？"""

    # 默认回答
    else:
        # 尝试搜索相关知识点
        knowledge_results = search_knowledge_by_keyword(question)
        
        if knowledge_results:
            response = f"我找到了与'{question}'相关的知识点：\n\n"
            for i, knowledge in enumerate(knowledge_results[:2], 1):
                response += f"**{i}. {knowledge['name']}**\n"
                response += f"关键词：{', '.join(knowledge['keywords'][:5])}\n\n"
            
            response += "💡 你可以具体问我这些知识点的某个方面，比如原因、影响、意义等。"
            return response
        else:
            return """这是一个很好的问题！不过我暂时还不太确定如何回答。

你可以试试这样问：
- 具体的历史事件（如"鸦片战争的影响"）
- 历史人物的贡献
- 制度、运动的特点和意义
- 答题方法和记忆技巧

也欢迎你翻看教材，然后问我不理解的地方！📚"""

"""
材料题批改模块 - AI增强版
提供智能批改和深度反馈
"""

import streamlit as st
from modules.ai_service import get_ai_service
from data.history_questions import get_questions_by_type
import json

# 预设材料题库
PRESET_MATERIAL_QUESTIONS = {
    "近代化探索": [
        {
            "material": """材料一：19世纪60年代起，清政府开始兴办近代军事工业。1861年，曾国藩在安庆创办了安庆内军械所；1865年，李鸿章在上海创办江南制造总局。此后又兴办了福州船政局、天津机器局等。

材料二：19世纪70年代后，洋务派开始创办民用企业。1872年，李鸿章在上海创办轮船招商局；1880年，李鸿章创办开平矿务局；张之洞创办汉阳铁厂、湖北织布局等。

材料三：洋务派还创办了京师同文馆等新式学堂，选派留学生出国深造。""",
            "questions": [
                {
                    "question": "（1）根据材料一、二，概括洋务运动在经济方面的主要举措。",
                    "answer": "①兴办近代军事工业（安庆内军械所、江南制造总局、福州船政局等）；②创办民用企业（轮船招商局、开平矿务局、汉阳铁厂、湖北织布局等）。"
                },
                {
                    "question": "（2）结合所学知识，分析洋务运动的历史作用。",
                    "answer": "积极作用：①引进了西方先进技术和设备，刺激了中国民族资本主义的产生和发展；②培养了一批近代科技人才（创办新式学堂、派遣留学生）；③在一定程度上抵制了外国经济侵略，对外国侵略势力起到了一些抵制作用。\n局限性：①没有改变封建制度，不能使中国走上富强道路；②最终在甲午战争中失败。"
                }
            ]
        },
        {
            "material": """材料一：戊戌变法历时仅103天，以慈禧太后发动政变、光绪帝被囚、维新派遭到镇压而告终。谭嗣同等六君子被杀害，康有为、梁启超逃亡海外。

材料二：变法期间，维新派缺乏实权，光绪帝权力受限。慈禧太后实际控制朝政，守旧势力强大。维新派试图依靠没有实权的光绪帝和极少数帝党官僚推行变法。

材料三：维新派脱离广大人民群众，仅在上层推动改革，未能获得基层力量支持。""",
            "questions": [
                {
                    "question": "（1）根据材料一，指出戊戌变法的结局。",
                    "answer": "历时103天即告失败；慈禧太后发动政变，光绪帝被囚；维新派遭到镇压（谭嗣同等六君子被杀害，康有为、梁启超逃亡海外）。"
                },
                {
                    "question": "（2）根据材料二、三，分析戊戌变法失败的原因。",
                    "answer": "①根本原因：资产阶级力量薄弱，维新派缺乏实权；②直接原因：以慈禧太后为首的守旧势力强大，反对变法；③主观原因：维新派脱离人民群众，仅依靠没有实权的光绪帝；④客观原因：封建势力强大，资本主义经济基础薄弱。"
                },
                {
                    "question": "（3）戊戌变法虽然失败，但有何历史意义？",
                    "answer": "①是一次爱国救亡的政治运动；②是近代中国第一次思想解放潮流；③促进了中国人民的觉醒；④为辛亥革命的发生奠定了思想基础。"
                }
            ]
        }
    ],
    "抗日战争": [
        {
            "material": """材料一：1945年8月15日，日本宣布无条件投降。中国人民经过14年艰苦卓绝的斗争，取得了抗日战争的伟大胜利。

材料二：抗日战争是近代以来中国反抗外敌入侵第一次取得完全胜利的民族解放战争。台湾及其附属岛屿回归祖国，结束了日本50年的殖民统治。

材料三：中国战场是世界反法西斯战争的东方主战场，中国人民的抗战牵制和消灭了日军主力，为世界反法西斯战争的胜利作出了重大贡献。""",
            "questions": [
                {
                    "question": "（1）根据材料一、二，指出中国抗日战争胜利的时间及其在中国近代史上的地位。",
                    "answer": "时间：1945年8月15日。\n地位：近代以来中国反抗外敌入侵第一次取得完全胜利的民族解放战争。"
                },
                {
                    "question": "（2）根据材料二，说明抗战胜利对解决台湾问题的意义。",
                    "answer": "台湾及其附属岛屿回归祖国，结束了日本50年的殖民统治，维护了国家主权和领土完整。"
                },
                {
                    "question": "（3）根据材料三并结合所学知识，说明中国抗日战争胜利的国际意义。",
                    "answer": "①中国战场是世界反法西斯战争的东方主战场；②中国人民的抗战牵制和消灭了日军主力，减轻了其他战场的压力；③为世界反法西斯战争的胜利作出了重大贡献；④提高了中国的国际地位。"
                }
            ]
        }
    ],
    "新中国成立": [
        {
            "material": """材料一：1949年10月1日，毛泽东在天安门城楼向全世界庄严宣告：中华人民共和国中央人民政府今天成立了！

材料二：新中国的成立，结束了中国百年来受帝国主义压迫奴役的历史，中国人民从此站起来了，成为国家的主人。

材料三：新中国的成立，壮大了世界和平民主和社会主义力量，鼓舞了世界被压迫民族和人民争取解放的斗争。""",
            "questions": [
                {
                    "question": "（1）根据材料一，写出新中国成立的时间、标志性事件。",
                    "answer": "时间：1949年10月1日。\n标志：毛泽东在天安门城楼宣告中华人民共和国中央人民政府成立。"
                },
                {
                    "question": "（2）根据材料二，说明新中国成立对中国人民的意义。",
                    "answer": "①结束了百年来受帝国主义压迫奴役的历史；②结束了半殖民地半封建社会；③中国人民从此站起来了，成为国家的主人；④实现了民族独立和人民解放。"
                },
                {
                    "question": "（3）根据材料三并结合所学知识，概括新中国成立的国际影响。",
                    "answer": "①改变了世界政治格局；②壮大了世界和平民主和社会主义力量；③鼓舞了世界被压迫民族和人民争取解放的斗争；④提高了中国的国际地位。"
                }
            ]
        }
    ],
    "改革开放": [
        {
            "material": """材料一：1980年，我国在深圳、珠海、汕头、厦门设立经济特区。1984年，开放14个沿海港口城市。

材料二：1985年以后，在长江三角洲、珠江三角洲、闽南三角区等地建立了沿海经济开放区。1990年，中央决定开发开放上海浦东。

材料三：逐步形成了经济特区—沿海开放城市—沿海经济开放区—内地的全方位、多层次、宽领域的对外开放格局。""",
            "questions": [
                {
                    "question": "（1）根据材料一，指出我国对外开放的起步措施。",
                    "answer": "1980年设立深圳、珠海、汕头、厦门四个经济特区；1984年开放14个沿海港口城市。"
                },
                {
                    "question": "（2）根据材料一、二，概括我国对外开放格局的形成过程。",
                    "answer": "①1980年：设立四个经济特区；②1984年：开放14个沿海港口城市；③1985年后：建立沿海经济开放区（长三角、珠三角、闽南三角区）；④1990年：开发开放上海浦东；⑤形成由沿海到内地、全方位多层次的对外开放格局。"
                },
                {
                    "question": "（3）结合所学知识，分析对外开放对我国发展的意义。",
                    "answer": "①促进了我国经济快速发展，引进外资和先进技术；②推动了社会主义市场经济体制的建立和完善；③加快了我国现代化建设步伐；④提高了我国的国际竞争力和国际地位；⑤丰富了人民物质文化生活。"
                }
            ]
        }
    ]
}

def render_essay_grading():
    """渲染材料题批改页面 - 全屏三种模式"""
    st.title("📝 材料题分析与批改")
    
    # 获取AI服务
    ai_service = get_ai_service()
    
    # 初始化答题记录
    if 'essay_records' not in st.session_state:
        st.session_state.essay_records = []
    
    # 三种模式选择
    st.markdown("### 🎯 选择使用模式")
    mode = st.radio(
        "请选择你要使用的功能",
        ["📚 按专题选择材料题", "✨ AI生成材料题", "📋 自定义材料解析"],
        horizontal=True,
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    
    # ========== 模式1：按专题选择材料题 ==========
    if mode == "📚 按专题选择材料题":
        render_topic_mode(ai_service)
    
    # ========== 模式2：AI生成材料题 ==========
    elif mode == "✨ AI生成材料题":
        render_ai_generate_mode(ai_service)
    
    # ========== 模式3：自定义材料解析 ==========
    else:
        render_custom_mode(ai_service)


def render_topic_mode(ai_service):
    """模式1：按专题选择材料题"""
    st.markdown("## 📚 按专题选择材料题")
    
    # 使用预设题库
    topics = list(PRESET_MATERIAL_QUESTIONS.keys())
    
    # 选择专题和题目
    col1, col2 = st.columns([2, 1])
    with col1:
        selected_topic = st.selectbox(
            "选择历史专题",
            topics,
            format_func=lambda x: f"{x}专题"
        )
    
    # 获取该专题下的题目
    topic_questions = PRESET_MATERIAL_QUESTIONS[selected_topic]
    
    with col2:
        question_idx = st.selectbox(
            "选择题目",
            range(len(topic_questions)),
            format_func=lambda x: f"第{x+1}题"
        )
    
    selected_question = topic_questions[question_idx]
    
    # 直接显示材料和题目
    st.markdown("---")
    st.markdown("## 📖 材料与问题")
    
    # 先显示材料
    st.markdown(f"""
    <div style='background: #fff3cd; padding: 25px; border-radius: 12px; 
                border-left: 5px solid #ffc107; margin: 15px 0;'>
        <h4 style='color: #856404; margin: 0 0 15px 0;'>📄 阅读材料</h4>
        <div style='color: #856404; font-size: 15px; line-height: 1.8;'>
            {selected_question['material'].replace(chr(10), '<br>')}
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # 后显示题目（多个小问）
    st.markdown(f"""
    <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                padding: 25px; border-radius: 15px; margin: 15px 0;'>
        <h4 style='color: white; margin: 0 0 15px 0;'>📝 请回答以下问题</h4>
    </div>
    """, unsafe_allow_html=True)
    
    # 显示所有小问
    for i, q in enumerate(selected_question['questions']):
        st.markdown(f"""
        <div style='background: #f8f9fa; padding: 15px 20px; border-radius: 8px; 
                    border-left: 4px solid #667eea; margin: 10px 0;'>
            <p style='color: #333; font-size: 16px; line-height: 1.8; margin: 0;'>
                {q['question']}
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    # 学生作答区
    st.markdown("---")
    st.markdown("## ✍️ 你的答案")
    
    student_answer = st.text_area(
        "请在此作答（多个问题请分别作答，标注序号）：",
        height=250,
        placeholder="提示：\n1. 多个小问请分别标注（1）（2）（3）\n2. 分点作答，条理清晰\n3. 结合材料，言之有据\n4. 使用历史术语\n5. 注意字数要求",
        key=f"answer_{selected_topic}_{question_idx}"
    )
    
    # 提交批改按钮
    submit_btn = st.button("📤 提交批改", type="primary", use_container_width=True)
    
    # AI批改
    if submit_btn and student_answer:
        with st.spinner("🤖 AI老师正在批改，请稍候..."):
            # 合并所有小问和答案用于批改
            full_question = "\n".join([q['question'] for q in selected_question['questions']])
            full_answer = "\n\n".join([f"{q['question']}\n{q['answer']}" for q in selected_question['questions']])
            grading_result = grade_answer(ai_service, full_question, student_answer, full_answer)
            if grading_result:
                display_grading_result(grading_result)
                
                # 检查是否低分，如果低于60分则收录到错题本
                score = extract_score_from_text(grading_result)
                if score < 60:
                    # 收录到错题本
                    from modules.learning_tracker import track_question_attempt
                    topic = extract_topic_from_question(full_question)
                    track_question_attempt(
                        full_question[:200],  # 截取前200字符
                        False,  # 低分视为"错误"
                        f"得分{score}分",
                        "参考答案",
                        f"材料题-{topic}",
                        None  # 材料题没有选项
                    )
                    st.warning(f"📝 此题得分较低（{score}分），已收录到错题本便于复习！")
    
    # 查看参考答案和AI深度解读
    st.markdown("---")
    col_a, col_b = st.columns(2)
    
    if 'show_ref_answer' not in st.session_state:
        st.session_state.show_ref_answer = False
    if 'show_ai_analysis' not in st.session_state:
        st.session_state.show_ai_analysis = False
    
    with col_a:
        if st.button("👁️ 查看参考答案", use_container_width=True, type="secondary"):
            st.session_state.show_ref_answer = not st.session_state.show_ref_answer
            st.rerun()
    
    with col_b:
        if st.button("🤖 AI深度解读", use_container_width=True, type="secondary"):
            st.session_state.show_ai_analysis = not st.session_state.show_ai_analysis
            st.rerun()
    
    # 显示参考答案
    if st.session_state.show_ref_answer:
        st.markdown("""
        <div style='background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%); 
                    padding: 25px; border-radius: 12px 12px 0 0; margin: 20px 0 0 0;'>
            <h4 style='color: white; margin: 0;'>✅ 参考答案</h4>
        </div>
        """, unsafe_allow_html=True)
        
        for i, q in enumerate(selected_question['questions']):
            st.markdown(f"""
            <div style='background: {'#f0fdf4' if i % 2 == 0 else '#f8fafc'}; 
                        padding: 20px; border-left: 4px solid #11998e; 
                        margin: 0; {'border-radius: 0 0 12px 12px;' if i == len(selected_question['questions'])-1 else ''}'>
                <p style='color: #166534; font-weight: bold; margin: 0 0 10px 0;'>{q['question']}</p>
                <div style='color: #15803d; font-size: 15px; line-height: 1.8;'>
                    {q['answer'].replace(chr(10), '<br>')}
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    # AI深度解读
    if st.session_state.show_ai_analysis:
        with st.spinner("🤖 AI正在生成深度解读..."):
            # 合并所有问题和答案
            full_content = f"材料：{selected_question.get('material', '')}\n\n"
            for q in selected_question['questions']:
                full_content += f"{q['question']}\n答案：{q['answer']}\n\n"
            
            explanation = ai_service.explain_concept(
                full_content,
                level='detailed'
            )
            if explanation:
                st.markdown(f"""
                <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                            padding: 25px; border-radius: 12px 12px 0 0;'>
                    <h3 style='color: white; margin: 0;'>🤖 AI深度解读</h3>
                </div>
                """, unsafe_allow_html=True)
                # 使用st.markdown正确渲染Markdown格式
                st.markdown(explanation)


def render_ai_generate_mode(ai_service):
    """模式2：AI生成材料题"""
    st.markdown("## ✨ AI生成材料题")
    st.info("💡 根据你的需求，AI会自动生成一道材料分析题和详细解析")
    
    # 用户输入需求
    st.markdown("### 📝 描述你的需求")
    
    col1, col2 = st.columns(2)
    with col1:
        topic_input = st.text_input("主题或专题", placeholder="例如：辛亥革命、抗日战争、改革开放等")
    with col2:
        difficulty = st.selectbox("难度级别", ["基础", "中等", "较难", "高考难度"])
    
    requirements = st.text_area(
        "详细要求（可选）",
        height=100,
        placeholder="例如：\n- 侧重考查原因分析\n- 包含图片材料\n- 题目字数400字左右\n- 要求对比分析两个历史事件"
    )
    
    if st.button("🚀 生成材料题", type="primary", use_container_width=True):
        if not topic_input:
            st.error("❌ 请至少输入主题")
            return
        
        with st.spinner("🤖 AI正在生成材料题，请稍候..."):
            # 构建提示词
            prompt = f"""请生成一道高中历史材料分析题，要求如下：
主题：{topic_input}
难度：{difficulty}
额外要求：{requirements if requirements else '无'}

请按照以下格式生成：
【题目】
[在这里写题目正文，包括问题]

【材料】
[在这里写材料内容]

【参考答案】
[在这里写详细的参考答案]

【解析】
[在这里写解题思路和知识点讲解]
"""
            
            messages = [
                {"role": "system", "content": "你是一位经验丰富的高中历史老师，擅长设计高质量的材料分析题。"},
                {"role": "user", "content": prompt}
            ]
            response = ai_service.call_api(messages)
            
            if response:
                st.session_state.generated_question = response
                st.rerun()
    
    # 显示生成的题目
    if 'generated_question' in st.session_state:
        st.markdown("---")
        st.markdown("### 📖 生成的题目")
        
        content = st.session_state.generated_question
        
        # 显示生成内容
        st.markdown(f"""
        <div style='background: #f8f9fa; padding: 25px; border-radius: 12px; 
                    border-left: 5px solid #667eea; line-height: 1.8;'>
            {content.replace(chr(10), '<br>')}
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        st.markdown("### ✍️ 在此作答")
        
        student_answer = st.text_area(
            "你的答案",
            height=200,
            placeholder="请根据上面的题目作答..."
        )
        
        if st.button("📤 提交批改", type="primary", use_container_width=True):
            if student_answer:
                with st.spinner("🤖 AI正在批改..."):
                    grading_result = grade_answer(ai_service, content, student_answer, "")
                    display_grading_result(grading_result)
                    
                    # 检查是否低分，如果低于60分则收录到错题本
                    score = extract_score_from_text(grading_result)
                    if score < 60:
                        from modules.learning_tracker import track_question_attempt
                        topic = extract_topic_from_question(content)
                        track_question_attempt(
                            content[:200],
                            False,
                            f"得分{score}分",
                            "参考答案",
                            f"材料题-{topic}",
                            None
                        )
                        st.warning(f"📝 此题得分较低（{score}分），已收录到错题本便于复习！")


def render_custom_mode(ai_service):
    """模式3：自定义材料解析"""
    st.markdown("## 📋 自定义材料解析")
    st.info("💡 粘贴你自己的材料，AI会按照材料分析的标准流程进行解析")
    
    # 用户粘贴材料
    st.markdown("### 📄 粘贴材料内容")
    
    material_input = st.text_area(
        "材料内容",
        height=200,
        placeholder="请粘贴你的材料内容（文字材料）...\n\n提示：\n- 可以是历史文献、数据表格、图片描述等\n- 越详细越好，AI会据此进行深度分析"
    )
    
    question_input = st.text_input(
        "问题（可选）",
        placeholder="如果有具体问题，请在此输入，例如：请概括材料反映的主要问题"
    )
    
    if st.button("🔍 AI解析材料", type="primary", use_container_width=True):
        if not material_input:
            st.error("❌ 请先粘贴材料内容")
            return
        
        with st.spinner("🤖 AI正在分析材料..."):
            # AI解析材料
            prompt = f"""请按照高中历史材料分析的标准流程，对以下材料进行全面解析：

【材料内容】
{material_input}

{f"【问题】{question_input}" if question_input else ""}

请按照以下结构进行解析：
1. 材料概述：概括材料的主要内容和历史背景
2. 关键信息提取：列出材料中的重要时间、人物、事件等
3. 深层分析：分析材料反映的历史现象、原因、影响等
4. 史学价值：说明这份材料在历史研究中的意义
{f"5. 问题解答：针对问题给出详细答案" if question_input else ""}
6. 拓展思考：相关的历史背景和延伸知识点
"""
            
            messages = [
                {"role": "system", "content": "你是一位经验丰富的高中历史老师，擅长材料分析和史料解读。"},
                {"role": "user", "content": prompt}
            ]
            analysis = ai_service.call_api(messages)
            
            if analysis:
                st.markdown("---")
                st.markdown("## 🎯 AI材料解析结果")
                
                st.markdown(f"""
                <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                            padding: 25px; border-radius: 12px 12px 0 0;'>
                    <h3 style='color: white; margin: 0;'>📊 专业材料解析</h3>
                </div>
                """, unsafe_allow_html=True)
                # 使用st.markdown正确渲染Markdown格式
                st.markdown(analysis)


def render_question_and_answer(question, ai_service):
    """渲染题目和作答区（全屏模式）"""
    st.markdown("---")
    st.markdown("## 📖 题目详情")
    
    # 显示题目
    st.markdown(f"""
    <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                padding: 25px; border-radius: 15px; margin: 15px 0;'>
        <h4 style='color: white; margin: 0 0 15px 0;'>📝 题目</h4>
        <p style='color: white; font-size: 16px; line-height: 1.8; margin: 0;'>
            {question['question'].replace(chr(10), '<br>')}
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # 显示材料（如果有）
    if 'material' in question and question['material']:
        st.markdown(f"""
        <div style='background: #fff3cd; padding: 20px; border-radius: 12px; 
                    border-left: 5px solid #ffc107; margin: 15px 0;'>
            <h4 style='color: #856404; margin: 0 0 10px 0;'>📄 材料</h4>
            <div style='color: #856404; font-size: 15px; line-height: 1.8;'>
                {question['material'].replace(chr(10), '<br>')}
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # 查看答案和AI解读按钮
    st.markdown("---")
    col_a, col_b = st.columns(2)
    
    if 'show_material_answer' not in st.session_state:
        st.session_state.show_material_answer = False
    if 'show_material_ai' not in st.session_state:
        st.session_state.show_material_ai = False
    
    with col_a:
        if st.button("👁️ 查看参考答案", use_container_width=True, type="primary"):
            st.session_state.show_material_answer = not st.session_state.show_material_answer
            st.rerun()
    
    with col_b:
        if st.button("🤖 AI深度解读", use_container_width=True):
            st.session_state.show_material_ai = not st.session_state.show_material_ai
            st.rerun()
    
    # 显示参考答案
    if st.session_state.show_material_answer:
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%); 
                    padding: 25px; border-radius: 12px; margin: 20px 0;'>
            <h4 style='color: white; margin: 0 0 15px 0;'>✅ 参考答案要点</h4>
            <div style='color: white; font-size: 16px; line-height: 1.8;'>
                {question.get('answer', '').replace(chr(10), '<br>')}
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # AI深度解读
    if st.session_state.show_material_ai:
        with st.spinner("🤖 AI正在生成深度解读..."):
            explanation = ai_service.explain_concept(
                f"题目：{question['question']}\n材料：{question.get('material', '')}\n答案：{question.get('answer', '')}",
                level='detailed'
            )
            if explanation:
                st.markdown(f"""
                <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                            padding: 25px; border-radius: 12px 12px 0 0;'>
                    <h3 style='color: white; margin: 0;'>🤖 AI深度解读</h3>
                </div>
                <div style='background: #f8f9fa; padding: 30px; border-radius: 0 0 12px 12px; 
                            border: 2px solid #667eea; border-top: none; line-height: 1.8;'>
                    {explanation}
                </div>
                """, unsafe_allow_html=True)
    
    # 学生作答区
    st.markdown("---")
    st.markdown("## ✍️ 你的答案")
    
    student_answer = st.text_area(
        "请在此作答：",
        height=200,
        placeholder="提示：\n1. 分点作答，条理清晰\n2. 结合材料，言之有据\n3. 使用历史术语\n4. 注意字数要求",
        key="student_answer_input"
    )
    
    col1, col2 = st.columns([1, 3])
    
    with col1:
        submit_btn = st.button("📤 提交批改", type="primary", use_container_width=True)
    
    with col2:
        if st.button("💡 查看答题提示", use_container_width=True):
            with st.expander("💭 答题技巧", expanded=True):
                st.markdown("""
                **材料题答题技巧：**
                1. 审题：看清楚问什么，注意时间、地点限定
                2. 读材料：找关键词，理解材料主旨
                3. 组织答案：
                   - 先总后分或先分后总
                   - 分点答，每点一句话概括+展开
                   - 引用材料支撑观点
                4. 使用术语：规范的历史表述
                5. 检查：要点是否齐全，逻辑是否清晰
                """)
    
    # AI批改
    if submit_btn and student_answer:
        with st.spinner("🤖 AI老师正在批改，请稍候..."):
            grading_result = grade_answer(ai_service, question['question'], student_answer, question.get('answer', ''))
            if grading_result:
                display_grading_result(grading_result)
                
                # 检查是否低分，如果低于60分则收录到错题本
                score = extract_score_from_text(grading_result)
                if score < 60:
                    from modules.learning_tracker import track_question_attempt
                    topic = extract_topic_from_question(question['question'])
                    track_question_attempt(
                        question['question'][:200],
                        False,
                        f"得分{score}分",
                        "参考答案",
                        f"材料题-{topic}",
                        None
                    )
                    st.warning(f"📝 此题得分较低（{score}分），已收录到错题本便于复习！")


def grade_answer(ai_service, question_text, student_answer, reference_answer):
    """AI批改答案"""
    prompt = f"""请作为高中历史老师，对学生的材料题答案进行批改。

【题目】
{question_text}

【参考答案】
{reference_answer if reference_answer else '无参考答案'}

【学生答案】
{student_answer}

请从以下几个维度进行评分和点评：
1. 内容要点（40分）：是否答全了要点，是否准确
2. 材料运用（20分）：是否结合材料，引用是否恰当
3. 逻辑结构（20分）：层次是否清晰，论述是否有条理
4. 历史术语（10分）：是否使用规范的历史表述
5. 文字表达（10分）：语言是否通顺，书写是否规范

请给出：
- 总分（满分100分）
- 各维度得分和具体点评
- 优点（至少2条）
- 不足（至少2条）
- 改进建议（具体可操作的）
- 参考改进版本（可选）
"""
    
    messages = [
        {"role": "system", "content": "你是一位严谨专业的高中历史老师，擅长批改材料分析题。"},
        {"role": "user", "content": prompt}
    ]
    result = ai_service.call_api(messages)
    return result


def display_grading_result(result):
    """显示批改结果"""
    st.markdown("---")
    st.markdown("## 📊 批改结果")
    
    st.markdown(f"""
    <div style='background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); 
                padding: 25px; border-radius: 12px 12px 0 0;'>
        <h3 style='color: white; margin: 0;'>🎯 AI批改反馈</h3>
    </div>
    """, unsafe_allow_html=True)
    # 使用st.markdown正确渲染Markdown格式
    st.markdown(result)


def extract_score_from_text(text):
    """从AI批改文本中提取分数"""
    import re
    # 匹配 "总分：XX分" 或 "总分（满分100分）：XX分"
    match = re.search(r'总分[：:]\s*(\d+)', text)
    if match:
        return int(match.group(1))
    return 0


def extract_topic_from_question(question):
    """从题目中提取主题"""
    # 简单实现：提取前20个字符或第一句话
    if '？' in question:
        return question.split('？')[0][:20]
    elif '。' in question:
        return question.split('。')[0][:20]
    else:
        return question[:20]


"""
专题练习模块 - 按章节/专题生成题目
支持选择题、填空题、材料分析题
"""

import streamlit as st
from modules.ai_service import get_ai_service
from data.history_questions import get_questions_by_chapter, get_questions_by_type, HISTORY_QUESTIONS
import random

# 章节定义 - 与知识库高度对应
CHAPTERS = {
    "中国古代史": [
        "中国古代的农业经济",
        "先秦时期",
        "秦朝：大一统帝国的建立",
        "汉朝：大一统帝国的巩固",
        "三国两晋南北朝",
        "隋唐：大一统帝国的繁荣",
        "宋元：多元文化的碰撞",
        "明清：大一统帝国的延续",
        "古代中国的民族融合",
        "古代政治制度演变"
    ],
    "中国近代史": [
        "鸦片战争与第一次鸦片战争后的中国",
        "第二次鸦片战争与洋务运动",
        "戊戌变法与八国联军",
        "辛亥革命与民国建立",
        "新民主主义革命的兴起（五四运动）",
        "中共一大与革命的开始",
        "大革命时期（1924-1927）",
        "土地革命时期（1927-1937）",
        "抗日战争（1937-1945）",
        "解放战争与新中国成立"
    ],
    "中国现代史": [
        "新中国的建立与过渡",
        "社会主义建设初期（1953-1966）",
        "文革十年（1966-1976）",
        "徘徊中的探索（1976-1978）",
        "改革开放初期（1978-1992）",
        "建立社会主义市场经济体制（1992-2002）",
        "科学发展观指导下的发展（2002-2012）",
        "新时代的中国（2012至今）",
        "中国外交政策的演变",
        "民族区域自治与民族关系"
    ],
    "世界近代史": [
        "欧洲文艺复兴与宗教改革",
        "新航路开辟与欧洲殖民扩张",
        "启蒙运动",
        "美国独立战争与美国的建立",
        "法国大革命与拿破仑战争",
        "欧洲工业革命与社会变化",
        "资本主义制度在欧美的确立与发展"
    ],
    "世界现代史": [
        "第一次世界大战与战后国际关系",
        "苏联建立与社会主义建设",
        "1920-1930年代的欧美与亚洲",
        "第二次世界大战",
        "美苏冷战的开始",
        "两个超级大国的对峙",
        "第三世界的兴起与发展",
        "冷战后的世界局势"
    ]
}

# 专题定义 - 跨越古今的主题
TOPICS = {
    "政治制度": [
        "中央集权制度",
        "民主革命运动",
        "政治体制改革",
        "国家权力结构",
        "法律制度演变",
        "国共关系与政党制度",
        "宪法与民主制度",
        "统一多民族国家治理"
    ],
    "经济与社会": [
        "农业与农村发展",
        "手工业与商业贸易",
        "近代工业兴起",
        "社会主义工业化建设",
        "对外贸易与经济开放",
        "经济体制改革",
        "社会阶级与社会结构",
        "人民生活与消费变化"
    ],
    "文化与思想": [
        "儒家思想发展",
        "中国传统文化",
        "马克思主义传入与发展",
        "新文化运动",
        "科学与教育制度",
        "民族优秀文化继承",
        "中外文化交融",
        "意识形态与思想解放"
    ],
    "对外关系与外交": [
        "古代丝绸之路",
        "鸦片战争与列强入侵",
        "近代外交与条约体系",
        "抗日战争中的国际关系",
        "新中国外交政策",
        "两极世界的形成",
        "国际组织与国际事务",
        "和平发展与互利共赢"
    ],
    "科技与日常生活": [
        "农业生产技术",
        "交通运输革新",
        "通信技术发展",
        "工业技术进步",
        "医疗卫生发展",
        "教育制度变化",
        "文化生活丰富",
        "生活方式现代化"
    ],
    "战争与军事": [
        "冷兵器时代的战争",
        "火药武器的使用",
        "鸦片战争军事失败",
        "甲午中日战争",
        "辛亥革命武装起义",
        "抗日战争军事斗争",
        "解放战争与三大战役",
        "现代战争理论"
    ],
    "民族与宗教": [
        "汉族与少数民族融合",
        "宗教信仰发展",
        "民族区域自治制度",
        "民族团结与和谐",
        "佛教与道教传播",
        "伊斯兰教传入",
        "基督教在华发展",
        "民族矛盾与民族问题"
    ],
    "人物与事件": [
        "帝王将相故事",
        "农民起义领袖",
        "近代改革家思想家",
        "革命先驱与英雄",
        "科学家与教育家",
        "文学家与艺术家",
        "重大历史事件分析",
        "历史人物评价"
    ]
}

# 题型定义 - 更加详细
QUESTION_TYPES = {
    "选择题": ["单选题", "多选题", "单选+多选混合"],
    "填空题": ["单空填空", "多空填空", "混合型填空"],
    "材料分析题": ["史料分析", "图表分析", "综合材料分析"],
    "简答题": ["简述型", "对比型", "评价型"],
    "论述题": ["历史意义分析", "历史影响分析", "历史演变过程"],
    "混合题型": ["全部题型混合练习"]
}

def render_topic_practice():
    """渲染专题练习页面"""
    st.title("🎯 专题练习生成器")
    
    # 初始化session state
    if 'show_answers' not in st.session_state:
        st.session_state.show_answers = {}
    if 'show_ai_explanation' not in st.session_state:
        st.session_state.show_ai_explanation = {}
    
    st.markdown("""
    <div class="info-box">
        <h3>💡 智能练习系统</h3>
        <p><strong>📚 按章节</strong>：选择课本章节，系统自动生成配套练习</p>
        <p><strong>🎯 按专题</strong>：选择专题类型，深度练习某一主题</p>
        <p><strong>📝 选题型</strong>：选择题/填空题/材料分析题，自由搭配</p>
        <p><strong>✨ 预设+AI</strong>：先显示预设题，可生成更多AI题目</p>
    </div>
    """, unsafe_allow_html=True)
    
    # 初始化会话状态
    if 'generated_practice' not in st.session_state:
        st.session_state.generated_practice = []
    if 'show_answers' not in st.session_state:
        st.session_state.show_answers = {}
    
    # 获取AI服务
    ai_service = get_ai_service()
    
    st.markdown("---")
    
    # 选择生成方式
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📚 选择范围")
        
        range_type = st.radio(
            "按什么生成？",
            ["按章节", "按专题"],
            horizontal=True
        )
        
        if range_type == "按章节":
            period = st.selectbox("选择历史时期", list(CHAPTERS.keys()), 
                                 help="选择中国古代史、近代史、现代史或世界历史")
            chapters_in_period = CHAPTERS[period]
            chapter = st.selectbox("选择具体章节", chapters_in_period,
                                  help=f"{period}中的详细章节，共{len(chapters_in_period)}个")
            selected_range = f"{period}-{chapter}"
        else:
            topic_category = st.selectbox("选择专题类别", list(TOPICS.keys()),
                                         help="选择8大类跨越古今的历史主题")
            topics_in_category = TOPICS[topic_category]
            topic = st.selectbox("选择具体专题", topics_in_category,
                                help=f"{topic_category}下的专项内容，共{len(topics_in_category)}个")
            selected_range = f"{topic_category}-{topic}"
    
    with col2:
        st.markdown("### 📝 题型与难度")
        
        question_type = st.selectbox(
            "题型",
            list(QUESTION_TYPES.keys()),
            help="选择题型：从单纯选择题到混合题型应有尽有"
        )
        
        if question_type != "混合题型":
            sub_types = QUESTION_TYPES[question_type]
            if len(sub_types) > 1:
                sub_type = st.selectbox(
                    f"{question_type}小类",
                    sub_types,
                    help=f"{question_type}的具体分类"
                )
            else:
                sub_type = sub_types[0]
        else:
            sub_type = "全部题型"
        
        st.markdown("---")
        
        difficulty_map = {
            "简单": "基础记忆与理解",
            "中等": "综合分析与应用", 
            "困难": "深度思考与创新"
        }
        difficulty = st.select_slider(
            "难度",
            options=["简单", "中等", "困难"],
            value="中等",
            help="简单：基础知识点  中等：综合分析  困难：深度思考"
        )
        st.caption(f"📌 {difficulty_map[difficulty]}")
        
        count = st.slider("题目数量", 3, 20, 8, 
                         help="一次练习的题目数量，建议8-10题为一组")
    
    # 生成按钮
    st.markdown("---")
    col_btn1, col_btn2, col_btn3 = st.columns(3)
    
    with col_btn1:
        if st.button("📚 显示预设题目", use_container_width=True, type="primary"):
            # 从题库中筛选预设题目
            preset_questions = get_preset_questions(selected_range, question_type, difficulty, count)
            st.session_state.generated_practice = preset_questions
            st.session_state.show_answers = {}
            st.success(f"✅ 已加载 {len(preset_questions)} 道预设题目")
            st.rerun()
    
    with col_btn2:
        if st.button("🤖 AI生成更多题目", use_container_width=True):
            if not st.session_state.generated_practice:
                st.warning("请先显示预设题目，AI会基于现有题目生成相似题")
            else:
                with st.spinner("🤔 AI正在生成题目..."):
                    # 使用AI生成额外题目
                    ai_questions = generate_ai_questions(
                        ai_service, 
                        selected_range, 
                        question_type, 
                        difficulty,
                        count
                    )
                    if ai_questions:
                        st.session_state.generated_practice.extend(ai_questions)
                        st.success(f"✅ AI生成了 {len(ai_questions)} 道新题目")
                        st.rerun()
    
    with col_btn3:
        if st.button("🔄 清空重新开始", use_container_width=True):
            st.session_state.generated_practice = []
            st.session_state.show_answers = {}
            st.rerun()
    
    # 显示生成的题目
    if st.session_state.generated_practice:
        st.markdown("---")
        st.markdown(f"## 📝 练习题目（共 {len(st.session_state.generated_practice)} 道）")
        
        for i, q in enumerate(st.session_state.generated_practice, 1):
            render_question_card(q, i, ai_service)


def get_preset_questions(selected_range, question_type, difficulty, count):
    """从题库获取预设题目"""
    # 根据范围筛选题目
    if "近代史" in selected_range:
        # 按章节筛选
        if "洋务运动" in selected_range:
            filtered = [q for q in HISTORY_QUESTIONS if "洋务运动" in str(q.get('keywords', []))]
        elif "辛亥革命" in selected_range:
            filtered = [q for q in HISTORY_QUESTIONS if "辛亥革命" in str(q.get('keywords', []))]
        elif "中共成立" in selected_range or "中国共产党" in selected_range:
            filtered = [q for q in HISTORY_QUESTIONS if "中国共产党" in str(q.get('keywords', []))]
        else:
            filtered = [q for q in HISTORY_QUESTIONS if q.get('chapter_id', '').startswith('chapter')]
    else:
        filtered = HISTORY_QUESTIONS
    
    # 按题型筛选
    if question_type == "选择题":
        filtered = [q for q in filtered if q.get('type') == 'choice']
    elif question_type == "材料分析题":
        filtered = [q for q in filtered if q.get('type') == 'material']
    
    # 按难度筛选
    difficulty_map = {"简单": "easy", "中等": "medium", "困难": "hard"}
    filtered = [q for q in filtered if q.get('difficulty') == difficulty_map.get(difficulty, 'medium')]
    
    # 随机选择指定数量
    if len(filtered) > count:
        return random.sample(filtered, count)
    else:
        return filtered


def generate_ai_questions(ai_service, selected_range, question_type, difficulty, count):
    """使用AI生成题目"""
    # 解析范围信息
    range_parts = selected_range.split('-')
    topic_desc = range_parts[-1] if len(range_parts) > 1 else selected_range
    
    difficulty_map = {"简单": "easy", "中等": "medium", "困难": "hard"}
    
    questions = ai_service.generate_questions(
        knowledge_points=[topic_desc],
        difficulty=difficulty_map.get(difficulty, 'medium'),
        count=count,
        question_type=question_type
    )
    
    return questions if questions else []


def render_question_card(question, index, ai_service):
    """渲染单个题目卡片"""
    # 初始化该题的作答状态
    answer_key = f"user_answer_{index}"
    if answer_key not in st.session_state:
        st.session_state[answer_key] = None
    
    with st.container():
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    padding: 15px 25px; border-radius: 12px 12px 0 0; margin-top: 20px;'>
            <h3 style='color: white; margin: 0;'>题目 {index}</h3>
        </div>
        <div style='background: #f8f9fa; padding: 25px; border-radius: 0 0 12px 12px; 
                    border: 2px solid #667eea; border-top: none;'>
        """, unsafe_allow_html=True)
        
        # 显示题目
        st.markdown(f"**{question.get('question', '')}**")
        
        # 如果是选择题，使用radio按钮让用户点击选择
        if 'options' in question:
            options = question['options']
            
            # 构建选项列表
            if isinstance(options, dict):
                option_list = [f"{key}. {value}" for key, value in options.items()]
                option_keys = list(options.keys())
            else:
                option_list = options
                option_keys = [opt.split('.')[0] if '.' in opt else opt[0] for opt in options]
            
            # 使用radio让用户选择
            user_choice = st.radio(
                "请选择你的答案：",
                option_list,
                key=f"choice_{index}",
                index=None,
                label_visibility="collapsed"
            )
            
            # 如果用户选择了答案
            if user_choice:
                selected_key = user_choice.split('.')[0]
                correct_answer = question.get('answer', '')
                
                # 判断是否正确
                is_correct = selected_key.upper() == correct_answer.upper()
                
                if is_correct:
                    st.success(f"✅ 正确！答案是 {correct_answer}")
                else:
                    st.error(f"❌ 错误！你选的是 {selected_key}，正确答案是 {correct_answer}")
                
                # 记录到学习追踪
                from modules.learning_tracker import track_question_attempt
                topic = question.get('keywords', ['未分类'])[0] if question.get('keywords') else '未分类'
                track_question_attempt(
                    question.get('question', ''),
                    is_correct,
                    selected_key,
                    correct_answer,
                    topic,
                    options  # 传入选项
                )
                
                # 显示解析
                if 'explanation' in question:
                    st.info(f"💡 **解析：** {question['explanation']}")
        
        # 如果是材料题，显示材料和输入框
        elif question.get('type') == 'material':
            if 'material' in question:
                st.markdown("**📄 材料：**")
                st.info(question['material'])
            
            # 提供输入框
            user_answer = st.text_area(
                "请输入你的答案：",
                key=f"material_answer_{index}",
                height=150
            )
            
            if st.button(f"📤 提交答案", key=f"submit_{index}"):
                if user_answer:
                    st.session_state.show_answers[index] = True
                    st.rerun()
        
        # 查看答案按钮（非选择题用）
        if 'options' not in question:
            col1, col2 = st.columns([1, 1])
            
            with col1:
                if st.button(f"👁️ 查看答案", key=f"show_ans_{index}"):
                    st.session_state.show_answers[index] = not st.session_state.show_answers.get(index, False)
                    st.rerun()
            
            with col2:
                if st.button(f"🤖 AI详细讲解", key=f"ai_explain_{index}"):
                    st.session_state.show_ai_explanation[index] = not st.session_state.show_ai_explanation.get(index, False)
                    st.rerun()
        else:
            # 选择题也可以请求AI讲解
            if st.button(f"🤖 AI详细讲解", key=f"ai_explain_{index}"):
                st.session_state.show_ai_explanation[index] = not st.session_state.show_ai_explanation.get(index, False)
                st.rerun()
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # 显示答案（非选择题）
        if st.session_state.show_answers.get(index, False) and 'options' not in question:
            st.markdown(f"""
            <div style='background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%); 
                        padding: 20px; border-radius: 10px; margin: 10px 0;'>
                <h4 style='color: white; margin: 0 0 10px 0;'>✅ 参考答案</h4>
                <p style='color: white; font-size: 16px; margin: 0; line-height: 1.8;'>{question.get('answer', '').replace(chr(10), '<br>')}</p>
            </div>
            """, unsafe_allow_html=True)
            
            if 'explanation' in question:
                st.info(f"💡 **解析：** {question['explanation']}")
        
        # AI详细讲解
        if st.session_state.show_ai_explanation.get(index, False):
            with st.spinner("AI正在准备讲解..."):
                explanation = ai_service.explain_concept(
                    f"题目：{question.get('question', '')}\n答案：{question.get('answer', '')}",
                    level='detailed'
                )
                if explanation:
                    # 使用st.markdown直接渲染，让Markdown格式生效
                    st.markdown(f"""
                    <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                                padding: 20px; border-radius: 12px 12px 0 0; margin: 15px 0 0 0;'>
                        <h3 style='color: white; margin: 0;'>🤖 AI详细讲解</h3>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # 用st.markdown渲染，保留Markdown格式
                    st.markdown(explanation)


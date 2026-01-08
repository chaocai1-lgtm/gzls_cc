"""
历史题目解析模块 (GZLS) - 拍照/输入题目，智能解析+关联知识点
支持图片上传识别和文字输入，提供基础解析和AI深度讲解
"""

import streamlit as st
import json
from pathlib import Path
import sys
import base64
from PIL import Image
import io
import re

sys.path.append(str(Path(__file__).parent.parent))

# 导入AI服务
from modules.ai_service import AIService
from modules.question_solver_gzls_v2 import generate_more_questions_with_ai, ai_analyze_single_question


class GZLSQuestionSolver:
    """GZLS历史题目解析器"""
    
    def __init__(self):
        self.tag = "gzls"
        self.data_dir = Path(__file__).parent.parent / "data" / "parsed"
        
        # 加载数据
        try:
            self.lessons = self._load_json("lessons.json")
            self.events = self._load_json("historical_events.json")
            self.figures = self._load_json("historical_figures.json")
            self.units = self._load_json("units.json")
            
            self.connected = True
        except Exception as e:
            st.error(f"❌ 数据加载失败: {e}")
            self.connected = False
            self.lessons = []
            self.events = []
            self.figures = []
            self.units = []
    
    def _load_json(self, filename):
        """加载JSON文件"""
        file_path = self.data_dir / filename
        if file_path.exists():
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []
    
    def extract_keywords(self, text):
        """从题目中提取关键词 - 改进版"""
        keywords = []
        
        # 1. 提取年份（包括公元前）
        years = re.findall(r'(?:公元前)?\d{1,4}年', text)
        keywords.extend(years)
        
        # 2. 提取朝代名称
        dynasties = ['夏朝', '商朝', '周朝', '秦朝', '汉朝', '唐朝', '宋朝', '元朝', '明朝', '清朝', 
                     '西周', '东周', '春秋', '战国', '西汉', '东汉', '三国', '西晋', '东晋', 
                     '南北朝', '隋朝', '五代', '北宋', '南宋', '辽', '金', '元', '明', '清',
                     '中华民国', '新中国']
        for dynasty in dynasties:
            if dynasty in text:
                keywords.append(dynasty)
        
        # 3. 提取常见历史术语和制度名称
        terms = ['中央集权', '郡县制', '分封制', '科举制', '三省六部', '行省制度',
                '洋务运动', '戊戌变法', '辛亥革命', '新文化运动', '五四运动',
                '抗日战争', '解放战争', '改革开放', '一国两制',
                '丝绸之路', '大运河', '郑和下西洋', '闭关锁国',
                '鸦片战争', '甲午战争', '八国联军', '义和团',
                '维新变法', '君主立宪', '民主共和', '三民主义']
        for term in terms:
            if term in text:
                keywords.append(term)
        
        # 4. 从数据库中匹配历史人物
        for figure in self.figures[:100]:
            figure_name = figure.get('figure', '')
            if figure_name and len(figure_name) >= 2 and figure_name in text:
                keywords.append(figure_name)
        
        # 5. 从数据库中匹配历史事件
        for event in self.events[:150]:
            event_name = event.get('event', '')
            if event_name and len(event_name) >= 3 and event_name in text:
                keywords.append(event_name)
        
        # 6. 提取题目中的关键短语（使用简单的NLP）
        # 提取"的"字前的词组
        phrases = re.findall(r'[\u4e00-\u9fa5]{2,8}(?=的)', text)
        keywords.extend([p for p in phrases if len(p) >= 3])
        
        return list(set(keywords))  # 去重
    
    def find_related_knowledge(self, keywords):
        """根据关键词查找相关知识点（修复字段名）"""
        related = {
            'events': [],
            'figures': [],
            'lessons': [],
            'units': []
        }
        
        if not keywords:
            return related
        
        # 搜索相关事件 - 使用正确的字段名
        for event in self.events:
            # 正确的字段是 description，没有event字段
            event_text = f"{event.get('description', '')} {event.get('year', '')}"
            # 只要有1个关键词匹配就加入
            if any(kw in event_text for kw in keywords):
                # 补充event字段方便后续使用
                event_copy = event.copy()
                if 'event' not in event_copy:
                    event_copy['event'] = event.get('description', '历史事件')[:20]
                related['events'].append(event_copy)
                if len(related['events']) >= 15:
                    break
        
        # 搜索相关人物 - 使用正确的字段名
        for figure in self.figures:
            # 正确的字段是 name 和 description
            figure_text = f"{figure.get('name', '')} {figure.get('description', '')}"
            if any(kw in figure_text for kw in keywords):
                # 补充figure字段方便后续使用
                figure_copy = figure.copy()
                if 'figure' not in figure_copy:
                    figure_copy['figure'] = figure.get('name', '历史人物')
                if 'introduction' not in figure_copy:
                    figure_copy['introduction'] = figure.get('description', '')
                related['figures'].append(figure_copy)
                if len(related['figures']) >= 15:
                    break
        
        # 搜索相关课文 - 只需要1个关键词匹配
        for lesson in self.lessons:
            lesson_text = f"{lesson.get('title', '')} {lesson.get('content', '')[:1000]}"
            if any(kw in lesson_text for kw in keywords):
                related['lessons'].append(lesson)
                if len(related['lessons']) >= 8:
                    break
        
        # 搜索相关单元 - 只需要1个关键词匹配
        for unit in self.units:
            unit_text = f"{unit.get('title', '')} {unit.get('description', '')}"
            if any(kw in unit_text for kw in keywords):
                related['units'].append(unit)
                if len(related['units']) >= 5:
                    break
        
        return related
    
    def basic_analysis(self, question_text):
        """基础解析 - 不调用AI，基于知识库"""
        # 提取关键词
        keywords = self.extract_keywords(question_text)
        
        # 查找相关知识
        related = self.find_related_knowledge(keywords)
        
        # 判断题目类型
        question_type = self._identify_question_type(question_text)
        
        # 生成基础解析
        analysis = {
            'question_type': question_type,
            'keywords': keywords,
            'related_knowledge': related,
            'answer_hints': self._generate_answer_hints(question_text, question_type, related)
        }
        
        return analysis
    
    def _identify_question_type(self, text):
        """识别题目类型"""
        if '材料' in text or '根据材料' in text:
            return '材料分析题'
        elif any(x in text for x in ['简述', '论述', '分析', '评价']):
            return '主观题'
        elif '选择' in text or any(f'{x}.' in text for x in ['A', 'B', 'C', 'D']):
            return '选择题'
        elif '填空' in text or '______' in text:
            return '填空题'
        else:
            return '综合题'
    
    def _generate_answer_hints(self, question_text, question_type, related):
        """使用AI动态生成答题提示 - 针对具体题目给出思路"""
        hints = []
        
        # 先显示相关知识点（作为背景信息）
        if related['events']:
            event_list = [e.get('event', '') for e in related['events'][:5]]
            hints.append(f"💡 **相关历史事件：** {' | '.join(event_list)}")
        
        if related['figures']:
            figure_list = [f.get('figure', '') for f in related['figures'][:5]]
            hints.append(f"👤 **相关历史人物：** {' | '.join(figure_list)}")
        
        if related['lessons']:
            lesson = related['lessons'][0]
            hints.append(f"📖 **教材章节：** {lesson.get('title', '')}（{lesson.get('book_name', '')}）")
        
        # 使用AI根据具体题目生成答题提示
        try:
            from modules.ai_service import AIService
            ai_service = AIService()
            
            # 构建上下文信息
            context_info = []
            if related['events']:
                context_info.append(f"相关事件：{', '.join([e.get('event', '') for e in related['events'][:3]])}")
            if related['figures']:
                context_info.append(f"相关人物：{', '.join([f.get('figure', '') for f in related['figures'][:3]])}")
            if related['lessons']:
                context_info.append(f"相关章节：{related['lessons'][0].get('title', '')}")
            
            context_str = "\\n".join(context_info) if context_info else "无明确知识点匹配"
            
            prompt = f"""你是一位历史老师，学生向你请教一道题目。请针对这道具体题目，给出解题思路和方法提示（不要直接给答案）。

**题目：**
{question_text}

**题型：** {question_type}

**相关知识背景：**
{context_str}

**请提供：**
1. **审题要点** - 这道题在考什么？关键信息有哪些？
2. **思路引导** - 应该从哪几个角度思考？
3. **方法提示** - 这类题有什么答题技巧？
4. **注意事项** - 容易忽略或出错的地方

要求：
- 针对这道具体题目，不要用通用模板
- 不直接说答案，而是引导思考方向
- 语言简洁清晰，200字左右
- 用Markdown格式，使用emoji图标"""
            
            messages = [
                {"role": "system", "content": "你是一位善于启发学生的历史老师。"},
                {"role": "user", "content": prompt}
            ]
            
            ai_hint = ai_service.call_api(messages, params={"temperature": 0.7, "max_tokens": 500})
            if ai_hint:
                hints.append(ai_hint)
            else:
                # AI不可用时的基础提示
                hints.append(f"💡 **答题思路：** 这是一道{question_type}，建议从题目关键词入手，结合相关历史知识进行分析。")
        except Exception as e:
            # AI生成失败时，给出基础提示
            hints.append(f"💡 **答题思路：** 这是一道{question_type}，建议从题目关键词入手，结合相关历史知识进行分析。")
        
        return hints
    
    def generate_similar_questions(self, keywords, question_type):
        """根据关键词生成3道类似题目"""
        similar = []
        
        # 从数据库中找相关题目（这里是示例，实际应该从题库中查询）
        if keywords:
            main_keyword = keywords[0] if keywords else "历史"
            
            # 示例题目模板
            if '秦朝' in str(keywords) or '中央集权' in str(keywords):
                similar = [
                    {
                        'question': '秦朝为加强中央集权，在地方推行的制度是（  ）',
                        'options': {'A': '分封制', 'B': '郡县制', 'C': '行省制', 'D': '科举制'},
                        'type': '选择题',
                        'difficulty': '简单',
                        'answer': 'B',
                        'explanation': '秦朝统一后，废除分封制，在全国推行郡县制。郡县制是中央集权制度的重要组成部分，郡县长官由皇帝任免，有利于加强中央对地方的控制。'
                    },
                    {
                        'question': '简述秦朝中央集权制度的影响',
                        'type': '简答题',
                        'difficulty': '中等',
                        'answer': '积极影响：①加强了国家统一，巩固了多民族国家；②提高了行政效率，有利于经济文化发展；③形成了中央垂直管理体系。消极影响：①皇权过度集中，易导致暴政；②官僚体系庞大，容易腐败。',
                        'explanation': '要从积极和消极两个方面分析，注意联系秦朝的实际情况。'
                    },
                    {
                        'question': '比较秦朝的郡县制与西周的分封制有何不同？',
                        'type': '比较题',
                        'difficulty': '较难',
                        'answer': '不同点：①性质：分封制是贵族政治，郡县制是官僚政治；②传承：分封制世袭，郡县制由皇帝任免；③权力：分封制诸侯权力大，郡县制地方官听命于中央；④影响：分封制易导致分裂，郡县制有利于统一。',
                        'explanation': '抓住两种制度的本质区别：世袭与任命、分权与集权。'
                    }
                ]
            elif '洋务运动' in str(keywords):
                similar = [
                    {
                        'question': '洋务运动的指导思想是（  ）',
                        'options': {'A': '师夷长技以制夷', 'B': '中体西用', 'C': '民主科学', 'D': '实业救国'},
                        'type': '选择题',
                        'difficulty': '简单',
                        'answer': 'B',
                        'explanation': '洋务运动的指导思想是"中体西用"，即以中国传统文化为本体，学习西方先进技术为用。这反映了洋务派在维护封建统治的前提下，试图通过引进西方技术来富国强兵。'
                    },
                    {
                        'question': '分析洋务运动失败的原因',
                        'type': '分析题',
                        'difficulty': '中等',
                        'answer': '根本原因：没有触动封建制度，只学技术不改制度。主观原因：①指导思想保守；②顽固派阻挠；③管理腐败。客观原因：①列强侵略；②资金技术不足；③缺乏群众基础。',
                        'explanation': '分析失败原因要抓住根本原因，再从主客观方面展开。'
                    },
                    {
                        'question': '洋务运动对中国近代化的影响如何？',
                        'type': '评价题',
                        'difficulty': '较难',
                        'answer': '积极影响：①引进西方技术，创办近代企业，开启中国近代化进程；②培养科技人才；③刺激民族资本主义产生；④客观上抵制了外国经济侵略。局限性：①未改变半殖民地半封建性质；②未使中国走上富强之路。',
                        'explanation': '评价要一分为二，既看到进步作用，也要指出历史局限。'
                    }
                ]
            else:
                # 默认推荐通用题目
                similar = [
                    {
                        'question': f'关于{main_keyword}的历史意义，下列说法正确的是（  ）',
                        'options': {'A': '促进了社会进步', 'B': '阻碍了历史发展', 'C': '没有实际影响', 'D': '具有双重性'},
                        'type': '选择题',
                        'difficulty': '中等',
                        'answer': '请结合具体内容判断',
                        'explanation': '历史意义通常从政治、经济、文化等多角度分析，注意一分为二地评价。'
                    },
                    {
                        'question': f'简述{main_keyword}的背景和过程',
                        'type': '简答题',
                        'difficulty': '中等',
                        'answer': '背景：分析国内外形势、阶级矛盾、经济基础等。过程：按时间顺序梳理关键事件和转折点。',
                        'explanation': '回答背景和过程类问题要注意时间线索和因果关系。'
                    },
                    {
                        'question': f'评价{main_keyword}的历史作用',
                        'type': '论述题',
                        'difficulty': '较难',
                        'answer': '从进步性和局限性两方面评价。进步性：对当时社会的积极影响。局限性：受历史条件制约的不足之处。',
                        'explanation': '评价类问题要坚持一分为二原则，既肯定积极作用，也要指出历史局限。'
                    }
                ]
        
        return similar[:3]
    
    def ai_deep_analysis(self, question_text, basic_analysis):
        """AI深度解析 - 给解题思路，不直接给答案"""
        try:
            ai_service = AIService()
            
            # 构建提示词 - 强调不直接给答案
            keywords_str = '、'.join(basic_analysis['keywords']) if basic_analysis['keywords'] else '未识别到'
            
            prompt = f"""你是一位耐心的历史老师，学生向你请教一道题目。请你**不要直接给出答案**，而是通过启发式提问和思路引导，帮助学生自己思考出答案。

**学生的题目：**
{question_text}

**题型：** {basic_analysis['question_type']}
**识别到的关键词：** {keywords_str}

**你的任务：**
1. **审题引导** - 帮学生分析题目在问什么，有哪些关键信息
2. **知识激活** - 提示相关的历史知识点，但不直接说答案
3. **思路点拨** - 用"你可以想想...""从哪个角度考虑..."等方式引导
4. **方法总结** - 告诉学生这类题的一般解题方法

**注意：**
- ❌ 不要直接说"答案是XX"
- ✅ 要说"你可以从XX角度思考"
- ✅ 用苏格拉底式提问引导思考
- ✅ 给出答题框架和思路
- ✅ 最后可以提示："想好了可以自己尝试作答，有疑问再来问老师"

请用亲切、鼓励的语气，像和学生面对面交流一样。"""
            
            # 调用AI
            messages = [
                {"role": "system", "content": "你是一位善于启发学生思考的历史老师，不直接给答案，而是引导学生自己找到答案。"},
                {"role": "user", "content": prompt}
            ]
            
            response = ai_service.call_api(messages, params={
                "temperature": 0.8,
                "max_tokens": 1500
            })
            
            return response if response else "AI服务暂时不可用，请使用基础解析功能。"
            
        except Exception as e:
            return f"AI解析出现问题：{str(e)}\n\n💡 建议：请先使用基础解析查看知识点，或直接查看教材相关章节。"


def render_question_solver():
    """渲染题目解析界面"""
    st.title("📝 历史题目智能解析")
    st.markdown("---")
    
    # 初始化解析器
    if 'gzls_solver' not in st.session_state:
        st.session_state.gzls_solver = GZLSQuestionSolver()
    
    solver = st.session_state.gzls_solver
    
    if not solver.connected:
        st.error("❌ 数据加载失败，无法使用解析功能")
        return
    
    # 选择输入方式
    input_method = st.radio(
        "选择输入方式",
        ["📝 文字输入", "📷 图片上传"],
        horizontal=True,
        key="gzls_input_method"
    )
    
    question_text = ""
    
    if input_method == "📝 文字输入":
        question_text = st.text_area(
            "请输入或粘贴题目内容",
            height=200,
            placeholder="例如：\n1. 简述秦朝中央集权制度的特点\n2. 材料一：……\n   问题：根据材料分析……",
            key="gzls_question_text"
        )
    
    else:  # 图片上传
        uploaded_file = st.file_uploader(
            "上传题目图片（支持 JPG、PNG）",
            type=['jpg', 'jpeg', 'png'],
            key="gzls_question_image"
        )
        
        if uploaded_file:
            # 显示图片
            image = Image.open(uploaded_file)
            st.image(image, caption="上传的题目图片", use_container_width=True)
            
            # OCR识别提示
            st.info("🔄 图片已上传。由于未配置OCR服务，请手动输入题目内容，或使用文字输入方式。")
            
            # 提供手动输入框
            question_text = st.text_area(
                "请根据图片手动输入题目内容",
                height=150,
                key="gzls_manual_input_from_image"
            )
    
    # 解析按钮
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🔍 基础解析", type="primary", use_container_width=True):
            if question_text.strip():
                with st.spinner("正在分析题目..."):
                    analysis = solver.basic_analysis(question_text)
                    st.session_state.gzls_current_analysis = analysis
                    st.session_state.gzls_current_question = question_text
                    st.rerun()
            else:
                st.warning("请先输入题目内容")
    
    with col2:
        if st.button("🤖 AI思路引导", type="secondary", use_container_width=True):
            if question_text.strip():
                # 先进行基础解析
                basic_analysis = solver.basic_analysis(question_text)
                
                with st.spinner("AI老师正在思考如何引导你..."):
                    ai_response = solver.ai_deep_analysis(question_text, basic_analysis)
                    
                    st.session_state.gzls_ai_analysis = ai_response
                    st.session_state.gzls_current_analysis = basic_analysis
                    st.session_state.gzls_current_question = question_text
                    st.rerun()
            else:
                st.warning("请先输入题目内容")
    
    st.markdown("---")
    
    # 显示基础解析结果
    if 'gzls_current_analysis' in st.session_state:
        analysis = st.session_state.gzls_current_analysis
        
        st.subheader("📊 基础解析")
        
        # 题型和关键词
        col1, col2 = st.columns(2)
        with col1:
            st.metric("题目类型", analysis['question_type'])
        with col2:
            st.metric("关键词数量", len(analysis['keywords']))
        
        if analysis['keywords']:
            st.write("🔑 **识别到的关键词：**")
            st.write(" · ".join(analysis['keywords']))
        
        # 答题提示
        if analysis['answer_hints']:
            st.write("### 💡 答题提示")
            for hint in analysis['answer_hints']:
                st.info(hint)
        
        # 相关知识点 - 添加知识图谱可视化
        related = analysis['related_knowledge']
        
        # 提取核心知识点（从关键词中提取）
        core_concept = ""
        keywords = analysis.get('keywords', [])
        if keywords:
            # 优先使用历史术语作为核心概念
            historical_terms = ['中央集权', '郡县制', '分封制', '科举制', '洋务运动', '戊戌变法', 
                              '辛亥革命', '新文化运动', '五四运动', '国共合作', '抗日战争', 
                              '解放战争', '改革开放', '一国两制', '民族区域自治']
            for term in historical_terms:
                if term in str(keywords):
                    core_concept = term
                    break
            
            # 如果没有匹配到术语，使用第一个关键词
            if not core_concept and len(keywords) > 0:
                core_concept = keywords[0]
        
        if any([related['events'], related['figures'], related['lessons']]):
            st.write("### 📚 相关知识点")
            
            # 调试：显示数据统计
            with st.expander("🔍 数据匹配情况", expanded=False):
                st.write(f"- 关键词: {analysis.get('keywords', [])}")
                st.write(f"- 匹配到的单元: {len(related['units'])}个")
                st.write(f"- 匹配到的课程: {len(related['lessons'])}个")
                st.write(f"- 匹配到的事件: {len(related['events'])}个")
                st.write(f"- 匹配到的人物: {len(related['figures'])}个")
                if related['events']:
                    st.write("事件样例:", [e.get('event') for e in related['events'][:3]])
                if related['figures']:
                    st.write("人物样例:", [f.get('figure') for f in related['figures'][:3]])
            
            # 只显示知识图谱
            try:
                from modules.knowledge_graph_visual import render_knowledge_graph_visual
                render_knowledge_graph_visual(
                    related,
                    solver.events,
                    solver.figures,
                    solver.lessons,
                    solver.units,
                    core_concept  # 传递核心概念
                )
            except Exception as e:
                st.error(f"❌ 知识图谱加载失败：{str(e)}")
                import traceback
                st.code(traceback.format_exc())
        
        # 推荐类似题目
        st.markdown("---")
        st.write("### 📚 推荐练习：巩固提升")
        
        similar_questions = solver.generate_similar_questions(
            analysis['keywords'], 
            analysis['question_type']
        )
        
        if similar_questions:
            st.info("💡 做完这道题后，可以尝试以下类似题目，加深理解！")
            
            for i, q in enumerate(similar_questions, 1):
                with st.expander(f"第{i}题 · {q['type']} · 难度：{q['difficulty']}", expanded=False):
                    st.markdown(f"**题目：** {q['question']}")
                    
                    # 显示选项 - 如果是选择题，使用radio让用户点击选择
                    if 'options' in q and q['options']:
                        options = q['options']
                        
                        # 构建选项列表
                        if isinstance(options, dict):
                            option_list = [f"{key}. {value}" for key, value in options.items()]
                        elif isinstance(options, list):
                            option_list = [f"{chr(65+idx)}. {opt}" for idx, opt in enumerate(options)]
                        else:
                            option_list = []
                        
                        if option_list:
                            # 使用radio让用户选择
                            user_choice = st.radio(
                                "请选择你的答案：",
                                option_list,
                                key=f"similar_choice_{i}",
                                index=None,
                                label_visibility="collapsed"
                            )
                            
                            # 如果用户选择了答案
                            if user_choice:
                                selected_key = user_choice.split('.')[0].strip()
                                correct_answer = str(q.get('answer', '')).strip().upper()
                                
                                # 判断是否正确
                                is_correct = selected_key.upper() == correct_answer
                                
                                if is_correct:
                                    st.success(f"✅ 正确！答案是 {correct_answer}")
                                else:
                                    st.error(f"❌ 错误！你选的是 {selected_key}，正确答案是 {correct_answer}")
                                    
                                    # 收录到错题本
                                    from modules.learning_tracker import track_question_attempt
                                    topic = q.get('knowledge_point', '推荐练习题')
                                    track_question_attempt(
                                        q.get('question', ''),
                                        is_correct,
                                        selected_key,
                                        correct_answer,
                                        topic,
                                        options
                                    )
                                
                                # 显示解析
                                if 'explanation' in q and q['explanation']:
                                    st.info(f"💡 **解析：** {q['explanation']}")
                    
                    # 添加查看解析和AI解析按钮
                    col_a, col_b = st.columns(2)
                    with col_a:
                        if st.button(f"📖 查看标准解析", key=f"similar_exp_{i}", use_container_width=True):
                            st.session_state[f'show_explanation_{i}'] = True
                            st.rerun()
                    
                    with col_b:
                        if st.button(f"🤖 AI深度讲解", key=f"similar_ai_{i}", use_container_width=True):
                            with st.spinner("AI老师正在准备讲解..."):
                                ai_analysis = ai_analyze_single_question(q)
                                st.session_state[f'ai_explanation_{i}'] = ai_analysis
                                st.rerun()
                    
                    # 显示标准解析
                    if st.session_state.get(f'show_explanation_{i}', False):
                        st.markdown("---")
                        st.markdown("**📖 标准解析：**")
                        if 'answer' in q and q['answer']:
                            st.success(f"**✅ 正确答案：** {q['answer']}")
                        if 'explanation' in q and q['explanation']:
                            st.info(f"**💡 解析：** {q['explanation']}")
                        if not q.get('answer') and not q.get('explanation'):
                            st.warning("提示：这是预设题目，可点击'AI深度讲解'获取详细分析")
                    
                    # 显示AI解析
                    if st.session_state.get(f'ai_explanation_{i}'):
                        st.markdown("---")
                        st.markdown("**🤖 AI深度讲解：**")
                        st.markdown(st.session_state[f'ai_explanation_{i}'])
        
        # AI生成更多题目 - 改进UI交互
        st.markdown("---")
        st.markdown("### 🤖 AI智能生成练习题")
        
        col1, col2, col3, col4 = st.columns([2, 2, 1, 2])
        
        with col1:
            question_type_gen = st.selectbox(
                "题型",
                options=["选择题", "材料分析题", "简答题", "评价题", "比较题", "综合题"],
                index=0,
                key="gen_type"
            )
        
        with col2:
            difficulty_gen = st.selectbox(
                "难度",
                options=["easy", "medium", "hard"],
                format_func=lambda x: {"easy": "简单", "medium": "中等", "hard": "较难"}[x],
                index=1,
                key="gen_difficulty"
            )
        
        with col3:
            count_gen = st.selectbox(
                "数量",
                options=[1, 2, 3, 4, 5],
                index=2,
                key="gen_count"
            )
        
        with col4:
            if st.button("🚀 立即生成", type="primary", use_container_width=True):
                with st.spinner(f"AI正在生成{count_gen}道{question_type_gen}..."):
                    new_questions = generate_more_questions_with_ai(
                        analysis['keywords'], 
                        question_type_gen,
                        difficulty=difficulty_gen,
                        count=count_gen
                    )
                    if new_questions:
                        st.session_state['generated_questions'] = new_questions
                        st.session_state['generated_difficulty'] = difficulty_gen
                        st.session_state['generated_type'] = question_type_gen
                        st.success(f"✅ 成功生成{len(new_questions)}道题目！")
                        st.rerun()
        
        # 显示AI生成的题目
        if 'generated_questions' in st.session_state:
            st.markdown("---")
            difficulty_label = {'easy': '简单', 'medium': '中等', 'hard': '较难'}
            diff = st.session_state.get('generated_difficulty', 'medium')
            gen_type = st.session_state.get('generated_type', '题目')
            st.write(f"### 📝 {gen_type} · {difficulty_label[diff]}难度")
            
            generated_qs = st.session_state['generated_questions']
            for j, gq in enumerate(generated_qs, 1):
                with st.expander(f"第{j}题 · {gq.get('type', '未知')}", expanded=True):
                    st.markdown(f"**题目：** {gq.get('question', '')}")
                    
                    # 显示选项 - 如果是选择题，使用radio让用户点击选择
                    if 'options' in gq and gq['options']:
                        options = gq['options']
                        
                        # 构建选项列表
                        if isinstance(options, dict):
                            option_list = [f"{key}. {value}" for key, value in options.items()]
                        elif isinstance(options, list):
                            option_list = [f"{chr(65+idx)}. {opt}" for idx, opt in enumerate(options)]
                        else:
                            option_list = []
                        
                        if option_list:
                            # 使用radio让用户选择
                            user_choice = st.radio(
                                "请选择你的答案：",
                                option_list,
                                key=f"gen_choice_{j}",
                                index=None,
                                label_visibility="collapsed"
                            )
                            
                            # 如果用户选择了答案
                            if user_choice:
                                selected_key = user_choice.split('.')[0].strip()
                                correct_answer = str(gq.get('answer', '')).strip().upper()
                                
                                # 判断是否正确
                                is_correct = selected_key.upper() == correct_answer
                                
                                if is_correct:
                                    st.success(f"✅ 正确！答案是 {correct_answer}")
                                else:
                                    st.error(f"❌ 错误！你选的是 {selected_key}，正确答案是 {correct_answer}")
                                    
                                    # 收录到错题本
                                    from modules.learning_tracker import track_question_attempt
                                    topic = gq.get('knowledge_points', ['AI生成题'])[0] if gq.get('knowledge_points') else 'AI生成题'
                                    track_question_attempt(
                                        gq.get('question', ''),
                                        is_correct,
                                        selected_key,
                                        correct_answer,
                                        topic,
                                        options
                                    )
                                
                                # 显示解析
                                if 'explanation' in gq:
                                    st.info(f"💡 **解析：** {gq['explanation']}")
                    else:
                        # 非选择题，显示题目即可
                        pass
                    
                    # 显示知识点
                    if 'knowledge_points' in gq and gq['knowledge_points']:
                        st.markdown(f"📌 **考查知识点：** {' | '.join(gq['knowledge_points'])}")
                    
                    # 按钮：查看答案和AI分析
                    col_ans, col_ai = st.columns(2)
                    with col_ans:
                        if st.button(f"📖 查看答案与解析", key=f"gen_ans_{j}", use_container_width=True):
                            st.session_state[f'show_gen_ans_{j}'] = True
                            st.rerun()
                    
                    with col_ai:
                        if st.button(f"🤖 AI深度讲解", key=f"gen_ai_{j}", use_container_width=True):
                            with st.spinner("AI老师正在准备讲解..."):
                                ai_analysis = ai_analyze_single_question(gq)
                                st.session_state[f'gen_ai_explanation_{j}'] = ai_analysis
                                st.rerun()
                    
                    # 显示答案和解析
                    if st.session_state.get(f'show_gen_ans_{j}', False):
                        st.markdown("---")
                        if 'answer' in gq:
                            st.success(f"**✅ 答案：** {gq['answer']}")
                        if 'explanation' in gq:
                            st.info(f"**💡 解析：** {gq['explanation']}")
                    
                    # 显示AI深度讲解
                    if st.session_state.get(f'gen_ai_explanation_{j}'):
                        st.markdown("---")
                        st.markdown("**🤖 AI深度讲解：**")
                        st.markdown(st.session_state[f'gen_ai_explanation_{j}'])
            
            # 清除生成的题目
            if st.button("🗑️ 清除生成的题目"):
                # 清除所有相关session state
                keys_to_delete = [k for k in st.session_state.keys() if k.startswith('show_gen_ans_') or k.startswith('gen_ai_explanation_')]
                for key in keys_to_delete:
                    del st.session_state[key]
                if 'generated_questions' in st.session_state:
                    del st.session_state['generated_questions']
                if 'generated_difficulty' in st.session_state:
                    del st.session_state['generated_difficulty']
                if 'generated_type' in st.session_state:
                    del st.session_state['generated_type']
                st.rerun()
    
    # 显示AI思路引导
    if 'gzls_ai_analysis' in st.session_state:
        st.markdown("---")
        st.subheader("🤖 AI老师的思路引导")
        
        # 提示框
        st.success("💡 老师不会直接告诉你答案，而是引导你自己思考出来！")
        
        st.markdown(st.session_state.gzls_ai_analysis)
        
        # 操作按钮
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔄 重新获取引导", use_container_width=True):
                solver = st.session_state.gzls_solver
                question = st.session_state.gzls_current_question
                basic = st.session_state.gzls_current_analysis
                
                with st.spinner("AI老师正在重新思考..."):
                    new_response = solver.ai_deep_analysis(question, basic)
                    st.session_state.gzls_ai_analysis = new_response
                    st.rerun()
        
        with col2:
            if st.button("✅ 我理解了", use_container_width=True):
                del st.session_state.gzls_ai_analysis
                st.success("很好！继续加油 💪")
                st.rerun()

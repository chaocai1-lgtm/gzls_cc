"""
AI服务核心模块
封装DeepSeek API调用
"""

import requests
import json
import streamlit as st
import time
from config.ai_config import *

class AIService:
    """AI服务封装类"""
    
    def __init__(self):
        self.api_key = DEEPSEEK_API_KEY
        self.api_base = DEEPSEEK_API_BASE
        self.model = DEEPSEEK_MODEL
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    def call_api(self, messages, params=None, max_retries=3):
        """
        调用DeepSeek API（带重试机制）
        
        Args:
            messages: 对话消息列表
            params: API参数（可选）
            max_retries: 最大重试次数
        
        Returns:
            API响应内容
        """
        if params is None:
            params = API_PARAMS
        
        url = f"{self.api_base}/chat/completions"
        
        payload = {
            "model": self.model,
            "messages": messages,
            **params
        }
        
        # 重试机制
        for attempt in range(max_retries):
            try:
                # 增加超时时间到60秒
                response = requests.post(
                    url,
                    headers=self.headers,
                    json=payload,
                    timeout=60
                )
                response.raise_for_status()
                
                result = response.json()
                return result['choices'][0]['message']['content']
            
            except requests.exceptions.Timeout:
                if attempt < max_retries - 1:
                    st.warning(f"⏰ 请求超时，正在重试 ({attempt + 1}/{max_retries})...")
                    continue
                else:
                    st.error("❌ API请求超时。可能原因：\n- 网络连接不稳定\n- API服务器响应慢\n\n建议：请稍后重试或检查网络连接")
                    return None
            
            except requests.exceptions.ConnectionError:
                if attempt < max_retries - 1:
                    st.warning(f"🔌 网络连接失败，正在重试 ({attempt + 1}/{max_retries})...")
                    continue
                else:
                    st.error("❌ 无法连接到API服务器。请检查：\n- 网络连接是否正常\n- 是否可以访问 api.deepseek.com")
                    return None
            
            except requests.exceptions.HTTPError as e:
                if e.response.status_code == 429:
                    st.error("⚠️ API调用频率超限，请稍后再试")
                elif e.response.status_code == 401:
                    st.error("❌ API Key无效，请检查配置")
                elif e.response.status_code == 500:
                    st.error("❌ API服务器错误，请稍后重试")
                else:
                    st.error(f"❌ HTTP错误 {e.response.status_code}: {str(e)}")
                return None
            
            except requests.exceptions.RequestException as e:
                st.error(f"❌ API调用失败: {str(e)}")
                return None
            
            except Exception as e:
                st.error(f"❌ 处理响应失败: {str(e)}")
                return None
        
        return None
    
    def chat_with_teacher(self, user_message, chat_history=None, context=None):
        """
        与AI历史老师对话
        
        Args:
            user_message: 用户消息
            chat_history: 对话历史
            context: 上下文信息（知识点、学生历史记录等）
        
        Returns:
            AI回复
        """
        messages = [
            {"role": "system", "content": HISTORY_TEACHER_PROMPT}
        ]
        
        # 添加上下文
        if context:
            context_msg = f"学生背景信息：{context}"
            messages.append({"role": "system", "content": context_msg})
        
        # 添加历史对话
        if chat_history:
            messages.extend(chat_history)
        
        # 添加当前消息
        messages.append({"role": "user", "content": user_message})
        
        return self.call_api(messages, CHAT_PARAMS)
    
    def grade_essay(self, question, student_answer, reference_answer=None, history_records=None):
        """
        批改材料题
        
        Args:
            question: 题目内容
            student_answer: 学生答案
            reference_answer: 参考答案
            history_records: 学生历史答题记录
        
        Returns:
            批改结果
        """
        prompt = f"""请批改以下材料分析题：

【题目】
{question}

【学生答案】
{student_answer}

{"【参考答案】" + reference_answer if reference_answer else ""}

{"【学生历史记录】" + history_records if history_records else ""}

请按照以下格式批改：

## 📊 总体评价
[给出总分和总体评价]

## ✓ 答题亮点
[列出学生答案的优点，给予肯定]

## ✗ 存在问题
[逐条指出问题，要具体到某句话或某个要点]

## 💡 改进建议
[针对性的提升建议]

## 📝 范文参考
[基于参考答案，给出标准答题示范]

## 🎯 知识点巩固
[这道题考查的核心知识点，帮助学生复习]
"""
        
        messages = [
            {"role": "system", "content": ESSAY_GRADER_PROMPT},
            {"role": "user", "content": prompt}
        ]
        
        return self.call_api(messages, GRADING_PARAMS)
    
    def generate_questions(self, knowledge_points=None, difficulty='medium', weak_points=None, count=3, question_type='选择题'):
        """
        生成练习题（优先生成选择题）
        
        Args:
            knowledge_points: 知识点列表
            difficulty: 难度等级（easy/medium/hard）
            weak_points: 学生薄弱点
            count: 生成题目数量
            question_type: 题型（'选择题'/'材料题'/'混合'）
        
        Returns:
            题目列表（JSON格式）
        """
        difficulty_map = {
            'easy': '简单（基础记忆）',
            'medium': '中等（理解分析）',
            'hard': '困难（综合应用）'
        }
        
        # 题型描述
        if question_type == '选择题':
            type_desc = "**全部生成单选题或多选题**（单选题70%，多选题30%）"
        elif question_type == '材料题':
            type_desc = "生成材料分析题"
        else:
            type_desc = "选择题为主（80%），材料题为辅（20%）"
        
        topic = ', '.join(knowledge_points) if knowledge_points else '近代史'
        
        prompt = f"""请生成{count}道关于"{topic}"的历史练习题。

【要求】
- 难度等级：{difficulty_map.get(difficulty, '中等')}
- 题型：{type_desc}
{"- 重点考查：" + weak_points if weak_points else ""}

【输出格式】（必须是有效的JSON数组）
```json
[
  {{
    "question": "洋务运动的根本目的是（  ）",
    "options": {{
      "A": "学习西方先进技术",
      "B": "发展资本主义",
      "C": "维护清朝统治",
      "D": "抵抗外国侵略"
    }},
    "answer": "C",
    "explanation": "洋务运动是在不改变封建制度的前提下学习西方技术，其根本目的是维护清朝封建统治。A项是表面现象，B项不是目的，D项虽是动机之一但不是根本目的。",
    "knowledge_point": "洋务运动",
    "difficulty": "medium",
    "type": "single_choice"
  }},
  {{
    "question": "下列关于戊戌变法的表述正确的有（  ）（多选）",
    "options": {{
      "A": "主张实行君主立宪制",
      "B": "废除科举制度",
      "C": "开办京师大学堂",
      "D": "训练新式军队"
    }},
    "answer": "ACD",
    "explanation": "戊戌变法主张君主立宪（A正确），创办京师大学堂（C正确），训练新军（D正确）。但变法只是改革科举内容（废八股改策论），并未废除科举制度，科举真正废除是在1905年（B错误）。",
    "knowledge_point": "戊戌变法",
    "difficulty": "hard",
    "type": "multiple_choice"
  }}
]
```

**重要提示**：
1. 选择题选项用对象格式 {{"A": "...", "B": "...", ...}}
2. 单选题答案是单个字母（如"C"），多选题答案是多个字母（如"ACD"）
3. 题目要标注是单选还是多选
4. 解析要详细说明为什么选这个，其他选项为什么错
5. 选项要有干扰性，不能一眼看出答案
"""
        
        messages = [
            {"role": "system", "content": QUESTION_GENERATOR_PROMPT},
            {"role": "user", "content": prompt}
        ]
        
        response = self.call_api(messages, QUESTION_PARAMS)
        
        if response:
            try:
                # 提取JSON部分
                json_start = response.find('[')
                json_end = response.rfind(']') + 1
                if json_start != -1 and json_end > json_start:
                    json_str = response[json_start:json_end]
                    questions = json.loads(json_str)
                    return questions
            except json.JSONDecodeError:
                st.error("AI生成的题目格式有误，请重试")
                return None
        
        return None
    
    def explain_concept(self, concept, level='detailed', related_concepts=None):
        """
        讲解知识点
        
        Args:
            concept: 要讲解的概念/事件
            level: 讲解深度（simple/detailed/advanced）
            related_concepts: 相关概念列表
        
        Returns:
            讲解内容
        """
        level_map = {
            'simple': '简单讲解（适合初学者）',
            'detailed': '详细讲解（深入理解）',
            'advanced': '深度分析（历史规律）'
        }
        
        prompt = f"""请讲解历史概念：{concept}

【讲解要求】
- 深度：{level_map.get(level, '详细讲解')}
- 讲解方式：故事化、生动化，避免枯燥
{"- 关联概念：" + "、".join(related_concepts) if related_concepts else ""}

【讲解结构】
## 📖 是什么（基本概念）
[用1-2句话说清楚]

## ⏰ 时间背景
[发生在什么时代？当时的社会环境是怎样的？]

## 🎯 为什么（原因分析）
[为什么会发生？背后的深层原因]

## 📊 主要内容/过程
[具体讲讲发生了什么，用故事的方式]

## 💡 历史意义
[产生了什么影响？为什么重要？]

## 🔗 知识关联
[与其他事件的关系，帮助学生建立知识网络]

## 💭 思考延伸
[提出1-2个引导性问题，让学生思考]
"""
        
        messages = [
            {"role": "system", "content": HISTORY_TEACHER_PROMPT},
            {"role": "user", "content": prompt}
        ]
        
        return self.call_api(messages, CHAT_PARAMS)
    
    def analyze_learning_data(self, student_records):
        """
        分析学生学习数据，生成个性化建议
        
        Args:
            student_records: 学生学习记录（dict格式）
        
        Returns:
            分析报告
        """
        prompt = f"""请分析学生的学习数据，给出个性化学习建议：

【学习数据】
{json.dumps(student_records, ensure_ascii=False, indent=2)}

请生成：

## 📊 学习情况总览
[总体评价]

## 🎯 优势分析
[学生擅长的部分]

## ⚠️ 薄弱环节
[需要加强的知识点，具体到章节]

## 📈 进步追踪
[与之前相比的进步]

## 🎓 学习建议
[针对性的学习计划和方法建议]

## 📚 推荐学习路径
[按优先级推荐接下来应该学习的内容]
"""
        
        messages = [
            {"role": "system", "content": HISTORY_TEACHER_PROMPT},
            {"role": "user", "content": prompt}
        ]
        
        return self.call_api(messages, CHAT_PARAMS)
    
    def generate_memory_tips(self, content, student_confusion=None):
        """
        生成记忆技巧
        
        Args:
            content: 需要记忆的内容
            student_confusion: 学生容易混淆的地方
        
        Returns:
            记忆技巧
        """
        prompt = f"""学生需要记住以下历史内容：

{content}

{"学生容易混淆：" + student_confusion if student_confusion else ""}

请生成易于记忆的方法：

## 🎯 记忆口诀
[编一个朗朗上口的口诀]

## 🔗 联想记忆
[建立有趣的联想]

## 📊 对比记忆
[如果有容易混淆的，做对比表格]

## 💡 理解记忆
[从理解角度帮助记忆，而不是死记硬背]
"""
        
        messages = [
            {"role": "system", "content": HISTORY_TEACHER_PROMPT},
            {"role": "user", "content": prompt}
        ]
        
        return self.call_api(messages, CHAT_PARAMS)


# 创建全局AI服务实例
@st.cache_resource
def get_ai_service():
    """获取AI服务实例（缓存）"""
    return AIService()

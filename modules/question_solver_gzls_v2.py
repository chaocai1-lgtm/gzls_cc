"""
题目解析模块 - AI生成题目功能
"""
from modules.ai_service import AIService
import json
import streamlit as st


def generate_more_questions_with_ai(keywords, question_type, difficulty="medium", count=3):
    """用AI生成更多类似题目"""
    try:
        ai_service = AIService()
        
        keywords_str = '、'.join(keywords[:5]) if keywords else "历史知识"
        
        # 构建提示词
        prompt = f"""你是一位历史题目设计专家。请根据以下信息生成{count}道高质量的历史练习题。

**关键词：** {keywords_str}
**题型参考：** {question_type}
**难度：** {difficulty}

**要求：**
1. **题型优先级：** 70%单选题，20%多选题，10%主观题
2. 题目要有针对性，围绕关键词设计
3. 难度要{difficulty}（easy=基础记忆, medium=理解应用, hard=综合分析）
4. 每道题必须包含详细解析
5. 选择题要有4个选项，干扰项要有迷惑性

**输出格式（JSON）：**
```json
[
  {{
    "question": "题目内容",
    "type": "单选题/多选题/简答题",
    "options": {{"A": "选项A", "B": "选项B", "C": "选项C", "D": "选项D"}},
    "answer": "正确答案（单选一个字母，多选多个字母）",
    "explanation": "详细解析（200字左右）",
    "difficulty": "easy/medium/hard",
    "knowledge_points": ["知识点1", "知识点2"]
  }},
  ...
]
```

**注意：**
- 单选题和多选题必须有options和answer
- 主观题不需要options，answer写"见解析"
- 解析要详细，说明为什么选这个，其他选项为什么错
- 只返回JSON，不要其他文字

请生成{count}道题目："""

        # 调用AI
        messages = [
            {"role": "system", "content": "你是历史题目设计专家，擅长生成高质量练习题。只返回JSON格式，不要其他文字。"},
            {"role": "user", "content": prompt}
        ]
        
        response = ai_service.call_api(messages, params={
            "temperature": 0.8,
            "max_tokens": 2000
        })
        
        if not response:
            return None
        
        # 解析JSON
        try:
            # 提取JSON部分（可能包含```json```标记）
            json_str = response
            if "```json" in response:
                json_str = response.split("```json")[1].split("```")[0]
            elif "```" in response:
                json_str = response.split("```")[1].split("```")[0]
            
            questions = json.loads(json_str.strip())
            return questions
        except json.JSONDecodeError as e:
            st.error(f"解析AI生成的题目失败：{str(e)}")
            st.code(response)
            return None
            
    except Exception as e:
        st.error(f"AI生成题目失败：{str(e)}")
        return None


def ai_analyze_single_question(question_data):
    """对单个题目进行AI深度解析"""
    try:
        ai_service = AIService()
        
        question_text = question_data['question']
        question_type = question_data.get('type', '未知')
        
        # 构建提示词
        if 'options' in question_data:
            # 选择题
            options = question_data.get('options', {})
            # 处理options可能是list或dict的情况
            if isinstance(options, dict):
                options_text = "\n".join([f"{k}. {v}" for k, v in options.items()])
            elif isinstance(options, list):
                options_text = "\n".join([f"{i+1}. {opt}" for i, opt in enumerate(options)])
            else:
                options_text = str(options)
            prompt = f"""请作为历史老师，深度解析这道选择题：

**题目：**
{question_text}

**选项：**
{options_text}

**请提供：**
1. **审题要点** - 这道题在考什么知识点？关键词是什么？
2. **逐项分析** - 每个选项为什么对或为什么错
3. **解题思路** - 用什么方法最快解决（时间排除法/因果法等）
4. **知识拓展** - 相关的历史知识串联
5. **易错提示** - 学生容易在哪里出错

用清晰的结构呈现，帮助学生理解透彻。"""
        else:
            # 主观题
            prompt = f"""请作为历史老师，深度解析这道主观题：

**题目：**
{question_text}

**请提供：**
1. **审题分析** - 题目要求我们回答什么？有哪些限定词？
2. **答题框架** - 应该从哪几个角度作答？
3. **要点提示** - 必须包含哪些核心内容？
4. **答案示例** - 给出一个标准答案
5. **评分标准** - 如何给分？重点在哪？
6. **提升建议** - 如何把这道题答得更好？

用清晰的结构呈现。"""
        
        # 调用AI
        messages = [
            {"role": "system", "content": "你是一位经验丰富的历史老师，擅长深入浅出地讲解题目。"},
            {"role": "user", "content": prompt}
        ]
        
        response = ai_service.call_api(messages, params={
            "temperature": 0.7,
            "max_tokens": 1500
        })
        
        return response if response else "AI解析暂时不可用"
        
    except Exception as e:
        return f"解析失败：{str(e)}"

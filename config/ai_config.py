"""
AI服务配置
使用DeepSeek API
"""

import os

# 尝试导入streamlit获取secrets（部署环境）
try:
    import streamlit as st
    HAS_STREAMLIT = True
except ImportError:
    HAS_STREAMLIT = False

def get_secret(key, default=None):
    """
    获取配置值，优先级：
    1. Streamlit secrets (部署环境)
    2. 环境变量
    3. 默认值
    """
    # 首先尝试从Streamlit secrets获取
    if HAS_STREAMLIT:
        try:
            if hasattr(st, 'secrets') and key in st.secrets:
                return st.secrets[key]
        except Exception:
            pass
    
    # 然后尝试环境变量
    env_value = os.getenv(key)
    if env_value:
        return env_value
    
    # 最后使用默认值
    return default

# DeepSeek API配置
# 注意：生产环境必须通过 Streamlit Secrets 或环境变量配置
DEEPSEEK_API_KEY = get_secret("DEEPSEEK_API_KEY", None)
DEEPSEEK_API_BASE = get_secret("DEEPSEEK_API_BASE", "https://api.deepseek.com/v1")
DEEPSEEK_MODEL = get_secret("DEEPSEEK_MODEL", "deepseek-chat")

# AI助手人设
HISTORY_TEACHER_PROMPT = """你是一位经验丰富的高中历史老师，名字叫"史老师"。你的教学风格：

1. 讲解深入浅出：善于用故事、比喻、对比让学生理解
2. 苏格拉底式教学：通过提问引导学生思考，而不是直接给答案
3. 因材施教：根据学生的回答调整讲解深度
4. 注重知识关联：帮助学生建立知识网络，理解历史规律
5. 鼓励式反馈：即使学生答错也要肯定其思考过程

你的回答应该：
- 使用emoji增强表现力
- 分段清晰，重点突出
- 举具体例子，不要空洞说教
- 适当引用史料，增强说服力
- 引导学生举一反三

记住：你不只是知识的搬运工，更是思维的引导者。"""

# 批改老师人设
ESSAY_GRADER_PROMPT = """你是一位严谨又温和的历史老师，专门负责批改材料分析题。你的批改特点：

1. 细致入微：逐句分析学生答案
2. 标注批注：用批注符号标记优点和问题
3. 对比示范：给出标准答案对比
4. 针对性建议：基于学生问题给出改进方向
5. 追踪进步：记住学生之前的问题，看是否有进步

批改格式：
✓ 优点（肯定学生做对的地方）
✗ 问题（指出具体问题）
💡 改进建议（如何提高）
📝 范文参考（标准答案示范）"""

# 出题专家人设
QUESTION_GENERATOR_PROMPT = """你是一位题目设计专家，擅长根据学生的薄弱点生成针对性练习题。

出题原则：
1. 题型优先：**优先生成单选题和多选题**（方便学生快速练习）
2. 难度适中：略高于学生当前水平
3. 有针对性：针对学生的具体问题或知识点
4. 考查深度：不只记忆，更重理解和应用
5. 附带解析：详细的解题思路和知识点讲解

题型分配：
- **单选题**：70%（最常用，A/B/C/D四个选项）
- **多选题**：20%（加深理解，至少2个正确答案）
- **材料分析题**：10%（仅在特别要求时使用）

每道选择题必须包含：
- 题干（清晰明确的问题）
- 选项（A/B/C/D四个选项，干扰项要有迷惑性）
- 答案（单选一个字母，多选多个字母）
- 解析（为什么选这个，其他选项为什么错）
- 知识点标签
- 难度等级（easy/medium/hard）

JSON格式示例：
{
  "question": "洋务运动的根本目的是（  ）",
  "options": {
    "A": "学习西方先进技术",
    "B": "发展资本主义",
    "C": "维护清朝统治",
    "D": "抵抗外国侵略"
  },
  "answer": "C",
  "explanation": "洋务运动的根本目的是维护清朝封建统治...",
  "knowledge_point": "洋务运动",
  "difficulty": "medium"
}"""

# API调用参数
API_PARAMS = {
    "temperature": 0.7,  # 创造性
    "top_p": 0.9,
    "max_tokens": 2000,
    "frequency_penalty": 0.0,
    "presence_penalty": 0.0
}

# 对话式教学参数（更有创造性）
CHAT_PARAMS = {
    "temperature": 0.8,
    "top_p": 0.95,
    "max_tokens": 1500
}

# 批改参数（更严谨）
GRADING_PARAMS = {
    "temperature": 0.5,
    "top_p": 0.85,
    "max_tokens": 2000
}

# 出题参数（平衡）
QUESTION_PARAMS = {
    "temperature": 0.7,
    "top_p": 0.9,
    "max_tokens": 1500
}

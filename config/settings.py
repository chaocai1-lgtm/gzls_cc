"""
配置文件
存储数据库连接信息和API密钥
支持本地开发和Streamlit Cloud部署
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

# Neo4j配置 - 阿里云私有版 (高分子课程)
# 注意：生产环境必须通过 Streamlit Secrets 或环境变量配置，不要使用默认值
NEO4J_URI = get_secret("NEO4J_URI", None)
NEO4J_USERNAME = get_secret("NEO4J_USERNAME", None)
NEO4J_PASSWORD = get_secret("NEO4J_PASSWORD", None)

# Elasticsearch配置
# 注意：生产环境必须通过 Streamlit Secrets 或环境变量配置
ELASTICSEARCH_CLOUD_ID = get_secret("ELASTICSEARCH_CLOUD_ID", None)
ELASTICSEARCH_USERNAME = get_secret("ELASTICSEARCH_USERNAME", None)
ELASTICSEARCH_PASSWORD = get_secret("ELASTICSEARCH_PASSWORD", None)

# DeepSeek API配置
# 注意：生产环境必须通过 Streamlit Secrets 或环境变量配置
DEEPSEEK_API_KEY = get_secret("DEEPSEEK_API_KEY", None)
DEEPSEEK_BASE_URL = "https://api.deepseek.com/v1"

# 应用配置 (高分子课程)
APP_TITLE_GFZ = "高分子自适应学习系统"
APP_ICON_GFZ = "🧪"

# Neo4j标签 - 高分子课程数据库标签（添加gfz前缀）
# 注意：数据库中使用的是 gfz_Module, gfz_Chapter, gfz_KnowledgePoint 等标签
NEO4J_LABEL_MODULE_GFZ = "gfz_Module"
NEO4J_LABEL_CHAPTER_GFZ = "gfz_Chapter"  # 数据库中的Chapter对应章节
NEO4J_LABEL_KNOWLEDGE_GFZ = "gfz_KnowledgePoint"
NEO4J_LABEL_STUDENT_GFZ = "gfz_Student"
NEO4J_LABEL_ACTIVITY_GFZ = "gfz_SearchLog"  # 学习活动日志
NEO4J_LABEL_DANMU_GFZ = "gfz_Log_Danmu"  # 弹幕日志

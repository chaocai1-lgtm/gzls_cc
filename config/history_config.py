"""
高中历史学习系统 - 配置文件
包含 Elasticsearch 和 Neo4j 连接配置
"""

# Elasticsearch 配置
ES_CLOUD_ID = "41ed8f6c58a942fb9aea8f6804841099:dXMtY2VudHJhbDEuZ2NwLmNsb3VkLmVzLmlvOjQ0MyQ1ZTRhNGI5ZGNlZjc0NDI4YjI3MWEzZDg3YzRmZjY2OCRlZjhhODRlYjliNzc0YjM3ODk0NWQ3ZTQ3OWVkOWRkNQ=="
ES_USERNAME = "elastic"
ES_PASSWORD = "x5ZwEPmZewPZlnZIn1Fy3XoQ"

# Neo4j 配置
NEO4J_URI = "bolt://47.110.83.32:11005"
NEO4J_USERNAME = "neo4j"
NEO4J_PASSWORD = "mima030303"

# DeepSeek API 配置
DEEPSEEK_API_KEY = "sk-bdf96d7f1aa74a53a83ff167f7f2f5a9"

# Elasticsearch 索引名称
ES_INDEX_KNOWLEDGE = "history_knowledge_points"  # 知识点索引
ES_INDEX_LESSONS = "history_lessons"  # 课文内容索引
ES_INDEX_QUESTIONS = "history_questions"  # 题目索引
ES_INDEX_EVENTS = "history_events"  # 历史事件索引

# 教材配置
TEXTBOOKS = {
    "bixiu_shang": {
        "name": "必修 中外历史纲要（上）",
        "file": "普通高中教科书 历史 必修 中外历史纲要（上）_1756191818507_raw.txt",
        "type": "必修",
        "description": "从中华文明起源到社会主义现代化建设新时代"
    },
    "bixiu_xia": {
        "name": "必修 中外历史纲要（下）",
        "file": "普通高中教科书 历史 必修 中外历史纲要（下）_1737864037123_raw.txt",
        "type": "必修",
        "description": "古代文明产生到当代世界发展"
    },
    "xuanxiu1": {
        "name": "选择性必修1 国家制度与社会治理",
        "file": "普通高中教科书 历史 选择性必修1 国家制度与社会治理_1756191819457_raw.txt",
        "type": "选择性必修",
        "description": "政治制度、官员选拔、法律教化等专题"
    },
    "xuanxiu2": {
        "name": "选择性必修2 经济与社会生活",
        "file": "普通高中教科书 历史 选择性必修2 经济与社会生活_1756191816942_raw.txt",
        "type": "选择性必修",
        "description": "食物生产、工具劳作、商业贸易等专题"
    },
    "xuanxiu3": {
        "name": "选择性必修3 文化交流与传播",
        "file": "普通高中教科书 历史 选择性必修3 文化交流与传播_1756191817723_raw.txt",
        "type": "选择性必修",
        "description": "中华文化、世界文化、文化交流等专题"
    }
}

# 知识点分类
KNOWLEDGE_CATEGORIES = {
    "政治": ["政治制度", "国家制度", "官员制度", "法律制度", "民族关系", "外交关系"],
    "经济": ["农业", "手工业", "商业", "对外贸易", "经济政策", "货币税收"],
    "文化": ["思想", "科技", "教育", "文学艺术", "宗教", "文化交流"],
    "军事": ["战争", "军事制度", "军事技术"],
    "社会": ["社会结构", "社会生活", "民族融合", "人口迁徙", "城市发展"]
}

# 时代分期
TIME_PERIODS = {
    "中国古代": {
        "先秦": {"start": -2070, "end": -221, "description": "从夏朝到秦统一前"},
        "秦汉": {"start": -221, "end": 220, "description": "秦朝和汉朝"},
        "魏晋南北朝": {"start": 220, "end": 589, "description": "三国两晋南北朝时期"},
        "隋唐": {"start": 589, "end": 907, "description": "隋朝和唐朝"},
        "五代辽宋夏金元": {"start": 907, "end": 1368, "description": "五代十国到元朝"},
        "明清": {"start": 1368, "end": 1912, "description": "明朝和清朝"}
    },
    "中国近代": {
        "晚清": {"start": 1840, "end": 1912, "description": "鸦片战争到辛亥革命"},
        "民国": {"start": 1912, "end": 1949, "description": "中华民国时期"}
    },
    "中国现代": {
        "新中国成立和社会主义建设": {"start": 1949, "end": 1978, "description": "建国到改革开放前"},
        "改革开放": {"start": 1978, "end": 2012, "description": "改革开放新时期"},
        "新时代": {"start": 2012, "end": 2024, "description": "中国特色社会主义新时代"}
    },
    "世界古代": {
        "上古": {"start": -3500, "end": 476, "description": "古代文明到西罗马灭亡"},
        "中古": {"start": 476, "end": 1500, "description": "中世纪时期"}
    },
    "世界近代": {
        "早期": {"start": 1500, "end": 1640, "description": "新航路开辟到英国资产阶级革命"},
        "中期": {"start": 1640, "end": 1870, "description": "资产阶级革命到第二次工业革命"},
        "晚期": {"start": 1870, "end": 1918, "description": "第二次工业革命到一战结束"}
    },
    "世界现代": {
        "战间期": {"start": 1918, "end": 1945, "description": "一战到二战"},
        "冷战": {"start": 1945, "end": 1991, "description": "二战后到苏联解体"},
        "后冷战": {"start": 1991, "end": 2024, "description": "当代世界"}
    }
}

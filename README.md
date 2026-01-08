# 高中历史自适应学习系统 📚

基于知识图谱的高中历史智能学习系统（GZLS增强版），提供AI助教、题目解析、材料批改、知识图谱可视化等功能。

## ✨ 核心功能

- 📚 **知识图谱可视化**：展示高中历史知识结构和关系（5本教科书，101课）
- 🔍 **智能搜索引擎**：基于Elasticsearch的历史资料检索
- 🤖 **AI智能助教**：DeepSeek驱动的"史老师"，苏格拉底式教学
- ✍️ **材料题批改**：自动批改历史材料分析题，提供详细反馈
- 📝 **题目解析系统**：智能解析历史选择题和材料题
- 📊 **学习追踪分析**：错题本、学习报告、重点注意
- 👨‍🏫 **教师仪表盘**：班级数据分析和教学管理

## 🚀 快速开始

### 本地运行

1. **克隆仓库**
```bash
git clone https://github.com/chaocai1-lgtm/gzls_cc.git
cd 高中历史自适应学习系统
```

2. **安装依赖**
```bash
pip install -r requirements.txt
```

3. **配置密钥**

复制 `.env.example` 为 `.env` 并填入真实配置：
```bash
cp .env.example .env
# 编辑 .env 文件，填入你的数据库和API密钥
```

4. **运行应用**
```bash
streamlit run app_chuzhong_backup.py
# 或使用批处理文件（Windows）
启动GZLS系统.bat
```

### Streamlit Cloud 部署

1. Fork 本仓库到你的GitHub账号
2. 登录 [Streamlit Cloud](https://streamlit.io/cloud)
3. 新建应用，选择你的仓库
4. 主文件路径设置为：`高中历史自适应学习系统/app_chuzhong_backup.py`
5. 在 Settings -> Secrets 中添加配置（参考 `STREAMLIT_SECRETS.md`）

详细部署说明参见仓库根目录下的 `STREAMLIT_SECRETS.md`

## 🔧 技术栈

- **前端框架**：Streamlit
- **数据库**：Neo4j (知识图谱), Elasticsearch (搜索引擎)
- **AI 模型**：DeepSeek API (deepseek-chat)
- **可视化**：Vis.js, Plotly

## 📦 项目结构

```
高中历史自适应学习系统/
├── app_chuzhong_backup.py  # 主应用入口
├── requirements.txt        # 依赖列表
├── .env.example            # 环境变量模板
├── config/                 # 配置文件
│   ├── settings.py         # 数据库配置
│   ├── ai_config.py        # AI配置
│   └── history_config.py   # 历史课程配置
├── modules/                # 功能模块
│   ├── photo_search_gzls_simple.py   # 搜索引擎
│   ├── question_solver_gzls.py       # 题目解析
│   ├── essay_grading_new.py          # 材料批改
│   ├── knowledge_graph_browser.py    # 知识图谱
│   ├── learning_tracker.py           # 学习追踪
│   └── teacher_dashboard.py          # 教师仪表盘
├── data/                   # 数据文件
│   ├── history_questions.py          # 题库
│   ├── history_knowledge_graph.py    # 知识图谱数据
│   └── history_flashcards.py         # 闪卡数据
└── scripts/                # 初始化脚本
    ├── init_neo4j.py       # Neo4j初始化
    └── init_elasticsearch.py # ES初始化
```

## 👥 测试账户

- 教师账号：`teacher` / `admin888`
- 学生账号：`student1` / `123456`

## ⚠️ 注意事项

- ✅ 本项目为个人使用，需自行提供数据库和API密钥
- ✅ **请勿将密钥文件**（`.env`, `配置.txt`）**提交到Git**
- ✅ 部署前请确保在Streamlit Secrets中正确填写所有配置
- ✅ 建议将GitHub仓库设为私有（如包含敏感数据）

## 📄 环境变量说明

系统需要以下环境变量（通过`.env`或Streamlit Secrets配置）：

- `NEO4J_URI`: Neo4j数据库连接URI
- `NEO4J_USERNAME`: Neo4j用户名
- `NEO4J_PASSWORD`: Neo4j密码
- `ELASTICSEARCH_CLOUD_ID`: Elasticsearch Cloud ID
- `ELASTICSEARCH_USERNAME`: Elasticsearch用户名
- `ELASTICSEARCH_PASSWORD`: Elasticsearch密码
- `DEEPSEEK_API_KEY`: DeepSeek API密钥

详细配置说明参见 `STREAMLIT_SECRETS.md`

## 📄 许可

本项目仅供学习和研究使用。

---

💡 如有问题，请参考 `STREAMLIT_SECRETS.md` 或查看代码注释。

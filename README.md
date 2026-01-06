# 高分子自适应学习系统 🧪

基于知识图谱的高分子物理课程智能学习系统，提供个性化学习路径推荐、案例库检索、课堂互动等功能。

## ✨ 核心功能

- 📚 **知识图谱可视化**：展示高分子物理知识结构和关系
- 🎯 **能力推荐系统**：基于学习数据智能推荐学习内容
- 📖 **案例库检索**：快速查找相关教学案例
- 💬 **课堂互动**：实时弹幕交流和 AI 助教
- 📊 **学习分析**：可视化学习进度和效果
- 📝 **报告生成**：自动生成学习报告和教学设计

## 🚀 快速开始

### 本地运行

1. **克隆仓库**
```bash
git clone <your-repo-url>
cd 高分子自适应学习系统
```

2. **安装依赖**
```bash
pip install -r requirements.txt
```

3. **配置密钥**
```bash
# 复制配置模板
cp .streamlit/secrets.toml.example .streamlit/secrets.toml

# 编辑 .streamlit/secrets.toml，填入真实的数据库和 API 密钥
```

4. **运行应用**
```bash
streamlit run app.py
```

### Streamlit Cloud 部署

详见 [DEPLOYMENT.md](DEPLOYMENT.md)

## 🔧 技术栈

- **前端框架**：Streamlit
- **数据库**：Neo4j (知识图谱), Elasticsearch (案例检索)
- **AI 模型**：DeepSeek API
- **可视化**：Plotly, PyVis

## 📦 项目结构

```
高分子自适应学习系统/
├── app.py                 # 主应用入口
├── requirements.txt       # 依赖列表
├── DEPLOYMENT.md          # 部署指南
├── config/               # 配置文件
│   └── settings.py       # 环境配置
├── modules/              # 功能模块
│   ├── knowledge_graph.py      # 知识图谱
│   ├── ability_recommender.py  # 能力推荐
│   ├── case_library.py         # 案例库
│   ├── classroom_interaction.py # 课堂互动
│   ├── analytics.py            # 数据分析
│   ├── report_generator.py     # 报告生成
│   └── teaching_design.py      # 教学设计
├── data/                 # 数据文件
└── .streamlit/           # Streamlit 配置
    ├── config.toml       # 应用配置
    ├── secrets.toml      # 密钥（不提交）
    └── secrets.toml.example # 密钥模板
```

## 🧪 部署前测试

运行测试脚本确保配置正确：
```bash
python test_deployment.py
```

## 👥 测试账户

- 教师账号：`teacher` / `admin888`
- 学生账号：`student1` / `123456`

## ⚠️ 注意事项

- 本项目配置为个人使用，需自行提供数据库和 API 密钥
- **请勿将密钥文件**（`.streamlit/secrets.toml`）**提交到 Git**
- 部署前请确保所有配置正确填写
- 建议将 GitHub 仓库设为私有

## 📄 许可

本项目仅供学习和研究使用。

---

💡 如有问题，请参考 [DEPLOYMENT.md](DEPLOYMENT.md)。

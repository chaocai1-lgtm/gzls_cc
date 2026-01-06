# 部署指南

本项目为**个人使用**的高分子自适应学习系统，使用 Streamlit Cloud 部署。

## 🚀 快速部署到 Streamlit Cloud

### 1. 准备 GitHub 仓库

```bash
# 确保代码已推送到 GitHub
git add .
git commit -m "准备部署"
git push origin main
```

### 2. 配置 Streamlit Cloud

1. 访问 [share.streamlit.io](https://share.streamlit.io)
2. 使用 GitHub 账号登录
3. 点击 "New app"
4. 选择你的 GitHub 仓库和分支
5. 主文件路径设置为：`高分子自适应学习系统/app.py`

### 3. 配置 Secrets（重要！）

在 Streamlit Cloud 应用管理页面：

1. 点击 "Settings" → "Secrets"
2. 粘贴以下内容（**替换为你的实际密钥**）：

```toml
# Neo4j 数据库配置
NEO4J_URI = "bolt://your-neo4j-host:port"
NEO4J_USERNAME = "your-username"
NEO4J_PASSWORD = "your-password"

# Elasticsearch 配置
ELASTICSEARCH_CLOUD_ID = "your-cloud-id"
ELASTICSEARCH_USERNAME = "your-username"
ELASTICSEARCH_PASSWORD = "your-password"

# DeepSeek API 配置
DEEPSEEK_API_KEY = "sk-xxxxxxxxxxxxxxxxxxxxxxxx"
```

### 4. 部署完成

保存配置后，Streamlit 会自动部署应用。几分钟后即可访问。

---

## 🔒 安全说明

- **secrets.toml** 文件已被 `.gitignore` 排除，不会上传到 GitHub
- **config/settings.py** 中的默认值仅用于本地开发，部署时会被 Streamlit Secrets 覆盖
- 建议定期更换密钥，尤其是在怀疑泄露时

---

## 📝 本地开发

1. 克隆仓库后，复制密钥模板：
   ```bash
   cd 高分子自适应学习系统
   cp .streamlit/secrets.toml.example .streamlit/secrets.toml
   ```

2. 编辑 `.streamlit/secrets.toml` 填入真实密钥

3. 安装依赖并运行：
   ```bash
   pip install -r requirements.txt
   streamlit run app.py
   ```

---

## ⚠️ 注意事项

1. **私有仓库**：建议将 GitHub 仓库设为私有，避免代码泄露
2. **访问控制**：Streamlit Cloud 免费版的应用是公开的，任何知道链接的人都能访问
3. **资源限制**：免费版有资源限制，如遇性能问题可考虑升级

---

## 🔧 故障排查

### 应用无法连接数据库
- 检查 Streamlit Cloud Secrets 是否正确配置
- 确认 Neo4j 数据库允许外网访问
- 检查防火墙和安全组设置

### 页面加载缓慢
- 可能是数据库查询较慢
- 检查 Neo4j 数据库性能
- 考虑添加缓存机制

### API 调用失败
- 检查 DEEPSEEK_API_KEY 是否有效
- 确认 API 额度是否充足

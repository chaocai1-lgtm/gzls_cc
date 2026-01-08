@echo off
chcp 65001 >nul
echo ========================================
echo 启动GZLS历史学习系统
echo History Learning System with GZLS
echo ========================================
echo.
echo 🚀 系统特色：
echo   - 📚 5本高中历史教科书 (101课)
echo   - 🗺️ Neo4j知识图谱
echo   - 🔍 Elasticsearch智能搜索
echo   - 🤖 DeepSeek AI助手
echo.
echo 正在启动系统...
echo.

cd /d "%~dp0"
streamlit run app_chuzhong_backup.py --server.port 8501

pause

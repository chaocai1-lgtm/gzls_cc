"""
高中历史自适应学习系统 - 主应用 (GZLS增强版)
History Adaptive Learning System - AI Enhanced with GZLS
GZLS = 高中历史 (GaoZhong LiShi) - 基于JSON文件的完整知识体系（无需Neo4j/ES）
"""

import streamlit as st
# 导入GZLS简化模块（基于JSON，无需数据库）
from modules.photo_search_gzls_simple import render_photo_search  # GZLS搜索引擎
from modules.knowledge_graph_browser import render_knowledge_graph  # 知识图谱浏览器（新版）
from modules.question_solver_gzls import render_question_solver  # GZLS题目解析
# 导入其他双模式AI模块
from modules.essay_grading_new import render_essay_grading
from modules.topic_practice import render_topic_practice
# 导入学习追踪与报告模块
from modules.learning_tracker import (
    render_wrong_questions,      # 错题本
    render_learning_report,       # 学习报告
    render_focus_points,          # 重点注意
    render_ai_learning_assistant, # AI学习助手
    init_learning_tracker         # 初始化追踪器
)
# 导入教师端模块
from modules.teacher_dashboard import (
    render_login_page,           # 登录页面
    render_teacher_dashboard,    # 教师仪表盘
    check_login_status,          # 检查登录状态
    get_user_role,               # 获取用户角色
    logout                       # 退出登录
)

# 页面配置
st.set_page_config(
    page_title="历史AI学习系统 (GZLS增强版)",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 🎨 历史主题 UI - 古典书卷风格
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Noto Serif SC', 'STSong', serif;
    }
    
    /* 禁用动画 */
    *, *::before, *::after { transition: none !important; animation: none !important; }
    
    /* 古典书卷背景 */
    .stApp {
        background: linear-gradient(180deg, #fdfbf7 0%, #f8f6f0 50%, #f5f3ed 100%);
        min-height: 100vh;
    }
    
    [data-testid="stSidebar"] { display: none !important; }
    
    /* 顶部导航 - 古典卷轴风格 */
    .top-nav {
        background: linear-gradient(135deg, #8b7355 0%, #6b5444 100%);
        border-radius: 16px;
        padding: 20px 30px;
        margin: 15px 0 30px 0;
        box-shadow: 0 8px 30px rgba(107, 84, 68, 0.3);
        border: 3px solid #d4af37;
    }
    
    .logo-section {
        display: flex;
        align-items: center;
        gap: 16px;
    }
    
    .logo-icon {
        font-size: 42px;
        filter: drop-shadow(0 2px 4px rgba(0,0,0,0.3));
    }
    
    .logo-text {
        font-size: 24px;
        font-weight: 700;
        color: #ffd700;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        letter-spacing: 2px;
    }
    
    .logo-subtitle {
        font-size: 11px;
        color: #d4af37;
        letter-spacing: 3px;
        margin-top: 4px;
    }
    
    /* 用户信息 */
    .user-info {
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 10px 24px;
        background: rgba(255, 255, 255, 0.15);
        border-radius: 30px;
        border: 2px solid rgba(212, 175, 55, 0.5);
    }
    
    .user-avatar {
        width: 40px;
        height: 40px;
        border-radius: 50%;
        background: #ffd700;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 20px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.2);
    }
    
    .user-name {
        color: #fff;
        font-weight: 700;
        font-size: 15px;
    }
    
    .user-role {
        color: #d4af37;
        font-size: 12px;
    }
    
    /* 功能卡片 - 竹简风格 */
    .feature-card {
        background: linear-gradient(135deg, #f5f3ed 0%, #ebe8dd 100%);
        border-radius: 20px;
        padding: 35px 25px;
        text-align: center;
        cursor: pointer;
        height: 260px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        box-shadow: 0 8px 25px rgba(107, 84, 68, 0.15);
        border: 2px solid #d4c5b0;
        position: relative;
        overflow: hidden;
    }
    
    .feature-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, #8b7355, #d4af37, #8b7355);
    }
    
    .feature-card:hover {
        box-shadow: 0 15px 40px rgba(107, 84, 68, 0.25);
        transform: translateY(-4px);
        border-color: #d4af37;
    }
    
    .feature-icon {
        font-size: 64px;
        margin-bottom: 20px;
        filter: drop-shadow(0 4px 6px rgba(107, 84, 68, 0.2));
    }
    
    .feature-title {
        color: #3e2723;
        font-size: 20px;
        font-weight: 700;
        margin-bottom: 12px;
    }
    
    .feature-desc {
        color: #6b5444;
        font-size: 13px;
        line-height: 1.8;
    }
    
    /* 统计卡片 */
    .stat-card {
        background: linear-gradient(135deg, #f5f3ed 0%, #ebe8dd 100%);
        border-radius: 18px;
        padding: 30px 20px;
        text-align: center;
        box-shadow: 0 6px 20px rgba(107, 84, 68, 0.12);
        border: 2px solid #d4c5b0;
    }
    
    .stat-number {
        font-size: 44px;
        font-weight: 800;
        color: #8b7355;
        line-height: 1;
    }
    
    .stat-label {
        color: #6b5444;
        font-size: 14px;
        margin-top: 12px;
        font-weight: 600;
    }
    
    /* 按钮 - 古典印章风格 */
    .stButton>button {
        background: linear-gradient(135deg, #8b7355 0%, #6b5444 100%);
        color: #ffd700 !important;
        border: 2px solid #d4af37;
        border-radius: 12px;
        padding: 12px 24px;
        font-weight: 700;
        box-shadow: 0 4px 15px rgba(107, 84, 68, 0.3);
        font-family: 'Noto Serif SC', serif;
    }
    
    .stButton>button:hover {
        box-shadow: 0 6px 20px rgba(107, 84, 68, 0.4);
        transform: translateY(-2px);
        border-color: #ffd700;
    }
    
    /* 输入框 */
    .stTextInput>div>div>input,
    .stTextArea>div>div>textarea {
        background: #fdfbf7 !important;
        border: 2px solid #d4c5b0 !important;
        border-radius: 12px !important;
        color: #3e2723 !important;
        font-family: 'Noto Serif SC', serif !important;
    }
    
    .stTextInput>div>div>input:focus,
    .stTextArea>div>div>textarea:focus {
        border-color: #8b7355 !important;
        box-shadow: 0 0 0 3px rgba(139, 115, 85, 0.1) !important;
    }
    
    /* 内容面板 */
    .content-panel {
        background: linear-gradient(135deg, #fdfbf7 0%, #f8f6f0 100%);
        border-radius: 18px;
        padding: 28px;
        margin: 20px 0;
        box-shadow: 0 6px 20px rgba(107, 84, 68, 0.1);
        border: 2px solid #e8e4dc;
    }
    
    .panel-header {
        font-size: 18px;
        font-weight: 700;
        color: #3e2723;
        padding-bottom: 16px;
        border-bottom: 2px solid #d4c5b0;
        margin-bottom: 20px;
    }
    
    /* 模块标题 */
    .module-header {
        background: linear-gradient(135deg, #8b7355 0%, #6b5444 100%);
        border-radius: 18px;
        padding: 25px 35px;
        margin-bottom: 30px;
        box-shadow: 0 8px 25px rgba(107, 84, 68, 0.2);
        border: 3px solid #d4af37;
    }
    
    .module-title {
        font-size: 26px;
        font-weight: 800;
        color: #ffd700;
        display: flex;
        align-items: center;
        gap: 14px;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    /* 欢迎横幅 */
    .welcome-banner {
        background: linear-gradient(135deg, #f5f3ed 0%, #ebe8dd 100%);
        border-radius: 24px;
        padding: 40px 45px;
        margin-bottom: 35px;
        box-shadow: 0 10px 35px rgba(107, 84, 68, 0.15);
        border: 3px solid #d4af37;
        position: relative;
        overflow: hidden;
    }
    
    .welcome-banner::before {
        content: '📜';
        position: absolute;
        font-size: 180px;
        right: -30px;
        top: -40px;
        opacity: 0.08;
    }
    
    .welcome-title {
        font-size: 28px;
        font-weight: 800;
        color: #3e2723;
        margin-bottom: 12px;
    }
    
    .welcome-subtitle {
        color: #6b5444;
        font-size: 16px;
    }
    
    /* 标签页 */
    .stTabs [data-baseweb="tab-list"] {
        background: #ebe8dd;
        border-radius: 12px;
        padding: 6px;
        gap: 6px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        color: #6b5444;
        border-radius: 10px;
        font-weight: 600;
        font-family: 'Noto Serif SC', serif;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #8b7355 0%, #6b5444 100%) !important;
        color: #ffd700 !important;
        box-shadow: 0 4px 12px rgba(107, 84, 68, 0.3);
    }
    
    /* 消息框 */
    .stSuccess {
        background: #f0f9f4 !important;
        border: 2px solid #86efac !important;
        color: #166534 !important;
        border-radius: 12px;
    }
    
    .stWarning {
        background: #fffbeb !important;
        border: 2px solid #fde047 !important;
        color: #92400e !important;
        border-radius: 12px;
    }
    
    .stError {
        background: #fef2f2 !important;
        border: 2px solid #fca5a5 !important;
        color: #991b1b !important;
        border-radius: 12px;
    }
    
    .stInfo {
        background: #eff6ff !important;
        border: 2px solid #93c5fd !important;
        color: #1e40af !important;
        border-radius: 12px;
    }
    
    /* 度量指标 */
    [data-testid="metric-container"] {
        background: #fdfbf7;
        border-radius: 16px;
        padding: 24px;
        border: 2px solid #e8e4dc;
        box-shadow: 0 4px 12px rgba(107, 84, 68, 0.08);
    }
    
    [data-testid="metric-container"] label {
        color: #6b5444 !important;
        font-weight: 600;
    }
    
    [data-testid="metric-container"] [data-testid="stMetricValue"] {
        color: #8b7355 !important;
        font-weight: 800;
    }
    
    /* 徽章 */
    .badge {
        display: inline-block;
        padding: 6px 14px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 700;
    }
    
    .badge-primary {
        background: #fff8e1;
        color: #8b7355;
        border: 1px solid #d4c5b0;
    }
    
    .badge-success {
        background: #f0f9f4;
        color: #166534;
        border: 1px solid #86efac;
    }
    
    .badge-warning {
        background: #fffbeb;
        color: #92400e;
        border: 1px solid #fde047;
    }
    
    /* 高亮框 */
    .highlight-box {
        background: linear-gradient(135deg, rgba(139,115,85,0.08), rgba(212,175,55,0.08));
        border-radius: 16px;
        padding: 24px;
        border-left: 4px solid #8b7355;
        margin: 15px 0;
    }
    
    /* 页脚 */
    .footer-info {
        text-align: center;
        color: #9ca3af;
        font-size: 12px;
        margin-top: 50px;
        padding: 20px;
    }
    
    footer { visibility: hidden; }
    #MainMenu { visibility: hidden; }
    header[data-testid="stHeader"] { background: transparent; }
</style>
""", unsafe_allow_html=True)


def main():
    # 初始化session_state
    init_session_state()
    
    # 检查登录状态
    if not check_login_status():
        # 未登录，显示登录页面
        render_login_page()
        return
    
    # 已登录，根据角色显示不同页面
    user_role = get_user_role()
    
    if user_role == 'teacher':
        # 教师端
        render_teacher_navigation()
        render_teacher_dashboard()
    else:
        # 学生端
        # 初始化学习追踪器
        init_learning_tracker()
        
        # 顶部导航栏
        render_navigation()
        
        # 根据当前页面渲染内容
        current_page = st.session_state.get('current_page', 'home')
        
        if current_page == 'home':
            render_home_page()
        elif current_page == 'question_solver':
            render_question_solver()
        elif current_page == 'photo_search':
            render_photo_search()
        elif current_page == 'timeline':
            render_knowledge_graph()  # 使用新的知识图谱代替旧的时间轴
        elif current_page == 'essay_grading':
            render_essay_grading()
        elif current_page == 'topic_practice':
            render_topic_practice()
        elif current_page == 'wrong_questions':
            render_wrong_questions()  # 错题本
        elif current_page == 'learning_report':
            render_learning_report()  # 学习报告
        elif current_page == 'focus_points':
            render_focus_points()     # 重点注意
        elif current_page == 'ai_assistant':
            render_ai_learning_assistant()  # AI学习助手
        else:
            render_home_page()


def render_teacher_navigation():
    """渲染教师端导航栏"""
    st.markdown(f"""
    <div class="top-nav">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <div class="logo-section">
                <span class="logo-icon">📚</span>
                <div>
                    <div class="logo-text">高中历史自适应学习系统</div>
                    <div class="logo-subtitle">教师数据分析中心</div>
                </div>
            </div>
            <div class="user-info">
                <div class="user-avatar">👨‍🏫</div>
                <div>
                    <div class="user-name">管理员</div>
                    <div class="user-role">教师端</div>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # 退出登录按钮
    col1, col2, col3 = st.columns([6, 1, 1])
    with col3:
        if st.button("🚪 退出登录", key="logout_btn"):
            logout()
            st.rerun()


def init_session_state():
    """初始化session_state"""
    if 'current_page' not in st.session_state:
        st.session_state['current_page'] = 'home'
    if 'user_name' not in st.session_state:
        st.session_state['user_name'] = '学生'


def render_navigation():
    """渲染导航栏"""
    user_name = st.session_state.get('user_name', '学生')
    student_name = st.session_state.get('student_name', user_name)
    
    st.markdown(f"""
    <div class="top-nav">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <div class="logo-section">
                <span class="logo-icon">📚</span>
                <div>
                    <div class="logo-text">高中历史自适应学习系统</div>
                    <div class="logo-subtitle">HISTORY ADAPTIVE LEARNING SYSTEM</div>
                </div>
            </div>
            <div class="user-info">
                <div class="user-avatar">👨‍🎓</div>
                <div>
                    <div class="user-name">{student_name}</div>
                    <div class="user-role">学生</div>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # 退出登录按钮
    col1, col2, col3 = st.columns([6, 1, 1])
    with col3:
        if st.button("🚪 退出", key="student_logout"):
            logout()
            st.rerun()
    
    # 导航按钮 - 分两行设计
    st.markdown("##### 🧭 功能导航")
    
    # 第一行：核心学习功能（6个）
    nav_row1 = st.columns(6)
    
    with nav_row1[0]:
        if st.button("🏠 首页", use_container_width=True):
            st.session_state['current_page'] = 'home'
            st.rerun()
    
    with nav_row1[1]:
        if st.button("📝 题目解析", use_container_width=True):
            st.session_state['current_page'] = 'question_solver'
            st.rerun()
    
    with nav_row1[2]:
        if st.button("🔍 智能搜索", use_container_width=True):
            st.session_state['current_page'] = 'photo_search'
            st.rerun()
    
    with nav_row1[3]:
        if st.button("🗺️ 知识图谱", use_container_width=True):
            st.session_state['current_page'] = 'timeline'
            st.rerun()
    
    with nav_row1[4]:
        if st.button("✍️ 材料题批改", use_container_width=True):
            st.session_state['current_page'] = 'essay_grading'
            st.rerun()
    
    with nav_row1[5]:
        if st.button("🎯 专题练习", use_container_width=True):
            st.session_state['current_page'] = 'topic_practice'
            st.rerun()
    
    # 第二行：AI辅助功能（4个）
    nav_row2 = st.columns(4)
    
    with nav_row2[0]:
        if st.button("📕 错题本", use_container_width=True):
            st.session_state['current_page'] = 'wrong_questions'
            st.rerun()
    
    with nav_row2[1]:
        if st.button("📊 学习报告", use_container_width=True):
            st.session_state['current_page'] = 'learning_report'
            st.rerun()
    
    with nav_row2[2]:
        if st.button("⚠️ 重点注意", use_container_width=True):
            st.session_state['current_page'] = 'focus_points'
            st.rerun()
    
    with nav_row2[3]:
        if st.button("🤖 AI学习助手", use_container_width=True):
            st.session_state['current_page'] = 'ai_assistant'
            st.rerun()
    
    st.markdown("<br>", unsafe_allow_html=True)


def render_home_page():
    """渲染首页"""
    user_name = st.session_state.get('student_name', st.session_state.get('user_name', '同学'))
    
    # 欢迎横幅 (GZLS)
    st.markdown(f"""
    <div class="welcome-banner">
        <div class="welcome-title">👋 欢迎回来，{user_name}！</div>
        <div class="welcome-subtitle">📚 基于5本高中历史教科书完整知识体系的智能学习系统</div>
    </div>
    """, unsafe_allow_html=True)
    
    # 统计数据 (GZLS真实数据)
    stat_cols = st.columns(5)
    
    with stat_cols[0]:
        st.markdown("""
        <div class="stat-card">
            <div class="stat-number">5本</div>
            <div class="stat-label">📚 教科书</div>
        </div>
        """, unsafe_allow_html=True)
    
    with stat_cols[1]:
        st.markdown("""
        <div class="stat-card">
            <div class="stat-number">101课</div>
            <div class="stat-label">📖 完整课文</div>
        </div>
        """, unsafe_allow_html=True)
    
    with stat_cols[2]:
        st.markdown("""
        <div class="stat-card">
            <div class="stat-number">500+</div>
            <div class="stat-label">⚡ 历史事件</div>
        </div>
        """, unsafe_allow_html=True)
    
    with stat_cols[3]:
        st.markdown("""
        <div class="stat-card">
            <div class="stat-number">300+</div>
            <div class="stat-label">👤 历史人物</div>
        </div>
        """, unsafe_allow_html=True)
    
    with stat_cols[4]:
        st.markdown("""
        <div class="stat-card">
            <div class="stat-number">AI</div>
            <div class="stat-label">🤖 DeepSeek</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # 功能模块
    st.markdown("""
    <div style="text-align: center; margin: 30px 0;">
        <h2 style="color: #3e2723; font-weight: 800;">🚀 选择学习模块</h2>
        <p style="color: #6b5444; font-size: 16px;">点击下方卡片开始你的历史学习之旅</p>
    </div>
    """, unsafe_allow_html=True)
    
    # 第一行：3个功能卡片
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <span class="feature-icon">📝</span>
            <div class="feature-title">题目解析</div>
            <div class="feature-desc">图片/文字上传<br>AI深度讲解<br>关联知识点</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("进入解析", key="btn_solver", use_container_width=True):
            st.session_state['current_page'] = 'question_solver'
            st.rerun()
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <span class="feature-icon">🔍</span>
            <div class="feature-title">智能搜索</div>
            <div class="feature-desc">全文搜索引擎<br>课文/事件/知识点<br>秒速定位答案</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("进入搜索", key="btn_search", use_container_width=True):
            st.session_state['current_page'] = 'photo_search'
            st.rerun()
    
    with col3:
        st.markdown("""
        <div class="feature-card">
            <span class="feature-icon">🗺️</span>
            <div class="feature-title">知识图谱</div>
            <div class="feature-desc">教科书知识网络<br>课文完整内容<br>系统学习历史</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("进入图谱", key="btn_timeline", use_container_width=True):
            st.session_state['current_page'] = 'timeline'
            st.rerun()
    
    # 第二行：3个功能卡片
    col4, col5, col6 = st.columns(3)
    
    with col4:
        st.markdown("""
        <div class="feature-card">
            <span class="feature-icon">✍️</span>
            <div class="feature-title">材料题批改</div>
            <div class="feature-desc">预设题目练习<br>AI智能批改<br>详细答案解析</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("进入批改", key="btn_essay", use_container_width=True):
            st.session_state['current_page'] = 'essay_grading'
            st.rerun()
    
    with col5:
        st.markdown("""
        <div class="feature-card">
            <span class="feature-icon">🎯</span>
            <div class="feature-title">专题练习</div>
            <div class="feature-desc">按章节专题练习<br>多题型全覆盖<br>AI生成题目</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("进入练习", key="btn_topic", use_container_width=True):
            st.session_state['current_page'] = 'topic_practice'
            st.rerun()
    
    with col6:
        st.markdown("""
        <div class="feature-card">
            <span class="feature-icon">📕</span>
            <div class="feature-title">错题本</div>
            <div class="feature-desc">自动收集错题<br>AI智能解析<br>针对性复习</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("查看错题", key="btn_wrong", use_container_width=True):
            st.session_state['current_page'] = 'wrong_questions'
            st.rerun()
    
    # 第三行：3个功能卡片
    col7, col8, col9 = st.columns(3)
    
    with col7:
        st.markdown("""
        <div class="feature-card">
            <span class="feature-icon">📊</span>
            <div class="feature-title">学习报告</div>
            <div class="feature-desc">学习数据统计<br>AI分析诊断<br>个性化建议</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("查看报告", key="btn_report", use_container_width=True):
            st.session_state['current_page'] = 'learning_report'
            st.rerun()
    
    with col8:
        st.markdown("""
        <div class="feature-card">
            <span class="feature-icon">⚠️</span>
            <div class="feature-title">重点注意</div>
            <div class="feature-desc">薄弱知识点<br>频繁出错分析<br>AI专项辅导</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("查看重点", key="btn_focus", use_container_width=True):
            st.session_state['current_page'] = 'focus_points'
            st.rerun()
    
    with col9:
        st.markdown("""
        <div class="feature-card">
            <span class="feature-icon">🤖</span>
            <div class="feature-title">AI学习助手</div>
            <div class="feature-desc">自由问答<br>知识点讲解<br>学习策略指导</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("开始对话", key="btn_ai", use_container_width=True):
            st.session_state['current_page'] = 'ai_assistant'
            st.rerun()
    
    # 页脚
    st.markdown("""
    <div class="footer-info">
        <div style="margin-bottom: 15px;">
            <span style="padding: 8px 16px; background: #8b7355; color: #ffd700; border-radius: 20px; margin: 0 5px;">📚 知识图谱</span>
            <span style="padding: 8px 16px; background: #8b7355; color: #ffd700; border-radius: 20px; margin: 0 5px;">🤖 AI辅导</span>
            <span style="padding: 8px 16px; background: #8b7355; color: #ffd700; border-radius: 20px; margin: 0 5px;">📊 数据分析</span>
            <span style="padding: 8px 16px; background: #8b7355; color: #ffd700; border-radius: 20px; margin: 0 5px;">⚡ 智能推荐</span>
        </div>
        © 2026 高中历史自适应学习系统 · 以史为鉴，知古鉴今
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()

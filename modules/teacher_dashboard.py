"""
教师端数据分析仪表盘
"""

import streamlit as st
import json
import random
from datetime import datetime, timedelta
from modules.ai_service import get_ai_service


# ============ 模拟学生数据（实际应用中应从数据库获取）============
def generate_mock_students():
    """生成模拟学生数据"""
    if 'mock_students' in st.session_state:
        return st.session_state.mock_students
    
    # 历史专题列表
    topics = [
        "中华文明起源", "夏商周", "春秋战国", "秦汉", "三国两晋南北朝",
        "隋唐", "宋元", "明清", "晚清", "辛亥革命", "新民主主义革命",
        "抗日战争", "解放战争", "新中国成立", "改革开放",
        "世界古代史", "资本主义兴起", "工业革命", "两次世界大战", "当代世界"
    ]
    
    # 生成30个学生数据
    students = []
    names = ["张伟", "王芳", "李娜", "刘洋", "陈静", "杨帆", "赵敏", "黄磊", 
             "周杰", "吴昊", "徐明", "孙悦", "马超", "朱婷", "胡涛", "郭靖",
             "林黛", "何雨", "高飞", "罗兰", "梁山", "宋江", "唐琳", "韩梅",
             "冯雪", "董卿", "萧峰", "段誉", "虚竹", "王语嫣"]
    
    for i, name in enumerate(names):
        student_id = f"2024{str(i+1).zfill(3)}"
        
        # 随机生成学习数据
        total_questions = random.randint(20, 150)
        correct_rate = random.uniform(0.4, 0.95)
        correct_count = int(total_questions * correct_rate)
        wrong_count = total_questions - correct_count
        
        # 生成各专题的错题分布
        wrong_by_topic = {}
        remaining_wrong = wrong_count
        selected_topics = random.sample(topics, min(8, len(topics)))
        for j, topic in enumerate(selected_topics):
            if j == len(selected_topics) - 1:
                wrong_by_topic[topic] = remaining_wrong
            else:
                count = random.randint(0, remaining_wrong // 2)
                wrong_by_topic[topic] = count
                remaining_wrong -= count
        
        # 生成页面访问记录
        pages = ["首页", "题目解析", "智能搜索", "知识图谱", "材料题批改", "专题练习"]
        page_visits = {page: random.randint(1, 30) for page in pages}
        
        # 学习时长（分钟）
        study_time = random.randint(30, 300)
        
        # 最近活跃时间
        last_active = datetime.now() - timedelta(hours=random.randint(0, 72))
        
        students.append({
            'id': student_id,
            'name': name,
            'total_questions': total_questions,
            'correct_count': correct_count,
            'wrong_count': wrong_count,
            'accuracy': round(correct_rate * 100, 1),
            'wrong_by_topic': wrong_by_topic,
            'page_visits': page_visits,
            'study_time': study_time,
            'last_active': last_active.isoformat(),
            'searches': random.randint(5, 50),
            'knowledge_viewed': random.randint(10, 80)
        })
    
    st.session_state.mock_students = students
    return students


def get_class_statistics(students):
    """计算班级整体统计"""
    if not students:
        return {}
    
    total_students = len(students)
    avg_accuracy = sum(s['accuracy'] for s in students) / total_students
    avg_questions = sum(s['total_questions'] for s in students) / total_students
    avg_study_time = sum(s['study_time'] for s in students) / total_students
    
    # 统计所有专题的错题
    all_wrong_topics = {}
    for s in students:
        for topic, count in s['wrong_by_topic'].items():
            if topic not in all_wrong_topics:
                all_wrong_topics[topic] = 0
            all_wrong_topics[topic] += count
    
    # 按错题数排序，找出共性薄弱点
    weak_topics = sorted(all_wrong_topics.items(), key=lambda x: x[1], reverse=True)[:5]
    
    return {
        'total_students': total_students,
        'avg_accuracy': round(avg_accuracy, 1),
        'avg_questions': round(avg_questions, 1),
        'avg_study_time': round(avg_study_time, 1),
        'weak_topics': weak_topics,
        'all_wrong_topics': all_wrong_topics
    }


# ============ 教师登录验证 ============
def verify_teacher_password(password):
    """验证教师密码"""
    return password == "admin888"


# ============ 教师端主页面 ============
def render_teacher_dashboard():
    """渲染教师端仪表盘"""
    st.markdown("""
    <h1 style='text-align: center; color: #1a1a2e; margin-bottom: 30px;'>
        👨‍🏫 教师数据分析中心
    </h1>
    """, unsafe_allow_html=True)
    
    students = generate_mock_students()
    stats = get_class_statistics(students)
    ai_service = get_ai_service()
    
    # ========== 顶部统计卡片 ==========
    st.markdown("### 📊 班级数据总览")
    
    # 第一行：4个核心指标
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    padding: 25px; border-radius: 16px; text-align: center; box-shadow: 0 8px 25px rgba(102,126,234,0.3);'>
            <h1 style='color: white; margin: 0; font-size: 42px;'>{stats['total_students']}</h1>
            <p style='color: rgba(255,255,255,0.9); margin: 8px 0 0 0; font-size: 16px;'>👥 学生总数</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        # 正确率颜色：绑色>70%，黄色50-70%，红色<50%
        acc = stats['avg_accuracy']
        if acc >= 70:
            bg_color = "linear-gradient(135deg, #11998e 0%, #38ef7d 100%)"
        elif acc >= 50:
            bg_color = "linear-gradient(135deg, #f7971e 0%, #ffd200 100%)"
        else:
            bg_color = "linear-gradient(135deg, #ff416c 0%, #ff4b2b 100%)"
        
        st.markdown(f"""
        <div style='background: {bg_color}; 
                    padding: 25px; border-radius: 16px; text-align: center; box-shadow: 0 8px 25px rgba(17,153,142,0.3);'>
            <h1 style='color: white; margin: 0; font-size: 42px;'>{stats['avg_accuracy']}%</h1>
            <p style='color: rgba(255,255,255,0.9); margin: 8px 0 0 0; font-size: 16px;'>📈 平均正确率</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); 
                    padding: 25px; border-radius: 16px; text-align: center; box-shadow: 0 8px 25px rgba(240,147,251,0.3);'>
            <h1 style='color: white; margin: 0; font-size: 42px;'>{stats['avg_questions']:.0f}</h1>
            <p style='color: rgba(255,255,255,0.9); margin: 8px 0 0 0; font-size: 16px;'>📝 平均做题量</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); 
                    padding: 25px; border-radius: 16px; text-align: center; box-shadow: 0 8px 25px rgba(79,172,254,0.3);'>
            <h1 style='color: white; margin: 0; font-size: 42px;'>{stats['avg_study_time']:.0f}</h1>
            <p style='color: rgba(255,255,255,0.9); margin: 8px 0 0 0; font-size: 16px;'>⏱️ 平均时长(分钟)</p>
        </div>
        """, unsafe_allow_html=True)
    
    # 第二行：更多详细指标
    st.markdown("<br>", unsafe_allow_html=True)
    col5, col6, col7, col8 = st.columns(4)
    
    # 计算更多统计数据
    high_performers = len([s for s in students if s['accuracy'] >= 80])
    medium_performers = len([s for s in students if 60 <= s['accuracy'] < 80])
    low_performers = len([s for s in students if s['accuracy'] < 60])
    total_wrong = sum(s['wrong_count'] for s in students)
    
    with col5:
        st.markdown(f"""
        <div style='background: #f8f9fa; padding: 20px; border-radius: 12px; text-align: center; 
                    border: 2px solid #28a745;'>
            <h2 style='color: #28a745; margin: 0;'>{high_performers}人</h2>
            <p style='color: #666; margin: 5px 0 0 0;'>🌟 优秀学生(≥80%)</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col6:
        st.markdown(f"""
        <div style='background: #f8f9fa; padding: 20px; border-radius: 12px; text-align: center; 
                    border: 2px solid #ffc107;'>
            <h2 style='color: #e6a700; margin: 0;'>{medium_performers}人</h2>
            <p style='color: #666; margin: 5px 0 0 0;'>📊 中等学生(60-79%)</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col7:
        st.markdown(f"""
        <div style='background: #f8f9fa; padding: 20px; border-radius: 12px; text-align: center; 
                    border: 2px solid #dc3545;'>
            <h2 style='color: #dc3545; margin: 0;'>{low_performers}人</h2>
            <p style='color: #666; margin: 5px 0 0 0;'>⚠️ 需关注(&lt;60%)</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col8:
        st.markdown(f"""
        <div style='background: #f8f9fa; padding: 20px; border-radius: 12px; text-align: center; 
                    border: 2px solid #6f42c1;'>
            <h2 style='color: #6f42c1; margin: 0;'>{total_wrong}道</h2>
            <p style='color: #666; margin: 5px 0 0 0;'>❌ 班级错题总数</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("---")
    
    # ========== 功能模块选择 ==========
    st.markdown("### 🎯 选择分析模块")
    
    # 使用4列按钮代替tab
    btn_col1, btn_col2, btn_col3, btn_col4 = st.columns(4)
    
    if 'teacher_view' not in st.session_state:
        st.session_state.teacher_view = 'student_list'
    
    with btn_col1:
        if st.button("👥 学生列表", use_container_width=True, 
                     type="primary" if st.session_state.teacher_view == 'student_list' else "secondary"):
            st.session_state.teacher_view = 'student_list'
            st.rerun()
    
    with btn_col2:
        if st.button("📊 数据可视化", use_container_width=True,
                     type="primary" if st.session_state.teacher_view == 'visualization' else "secondary"):
            st.session_state.teacher_view = 'visualization'
            st.rerun()
    
    with btn_col3:
        if st.button("🎯 专题分析", use_container_width=True,
                     type="primary" if st.session_state.teacher_view == 'topic_analysis' else "secondary"):
            st.session_state.teacher_view = 'topic_analysis'
            st.rerun()
    
    with btn_col4:
        if st.button("🤖 AI智能诊断", use_container_width=True,
                     type="primary" if st.session_state.teacher_view == 'ai_diagnosis' else "secondary"):
            st.session_state.teacher_view = 'ai_diagnosis'
            st.rerun()
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # 根据选择渲染内容
    if st.session_state.teacher_view == 'student_list':
        render_student_list(students)
    elif st.session_state.teacher_view == 'visualization':
        render_data_visualization(students, stats)
    elif st.session_state.teacher_view == 'topic_analysis':
        render_topic_analysis(students, stats)
    elif st.session_state.teacher_view == 'ai_diagnosis':
        render_ai_diagnosis(students, stats, ai_service)


def render_student_list(students):
    """渲染学生列表"""
    st.markdown("### 👥 学生学习情况一览")
    
    # 搜索和筛选
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        search_term = st.text_input("🔍 搜索学生（学号或姓名）", placeholder="输入学号或姓名...")
    with col2:
        sort_by = st.selectbox("排序方式", ["正确率", "做题数", "学习时长", "学号"])
    with col3:
        order = st.selectbox("排序顺序", ["降序", "升序"])
    
    # 筛选和排序
    filtered_students = students
    if search_term:
        filtered_students = [s for s in students if search_term in s['id'] or search_term in s['name']]
    
    sort_key = {
        "正确率": "accuracy",
        "做题数": "total_questions", 
        "学习时长": "study_time",
        "学号": "id"
    }[sort_by]
    
    filtered_students = sorted(filtered_students, key=lambda x: x[sort_key], reverse=(order == "降序"))
    
    # 显示学生表格
    for i, student in enumerate(filtered_students):
        with st.expander(f"**{student['name']}** ({student['id']}) - 正确率: {student['accuracy']}%", expanded=False):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("做题总数", student['total_questions'])
                st.metric("正确数", student['correct_count'])
            
            with col2:
                st.metric("错题数", student['wrong_count'])
                st.metric("学习时长", f"{student['study_time']}分钟")
            
            with col3:
                st.metric("搜索次数", student['searches'])
                st.metric("查看知识点", student['knowledge_viewed'])
            
            # 错题分布
            if student['wrong_by_topic']:
                st.markdown("**❌ 错题分布（按专题）：**")
                for topic, count in sorted(student['wrong_by_topic'].items(), key=lambda x: x[1], reverse=True):
                    if count > 0:
                        st.markdown(f"- {topic}: {count}道")
            
            # 查看详情按钮
            if st.button(f"📊 查看 {student['name']} 详细分析", key=f"detail_{student['id']}"):
                st.session_state.selected_student = student
                st.session_state.show_student_detail = True


def render_data_visualization(students, stats):
    """渲染数据可视化"""
    st.markdown("### 📊 数据可视化分析")
    
    import pandas as pd
    
    # 1. 正确率分布
    st.markdown("#### 1️⃣ 班级正确率分布")
    accuracy_ranges = {
        "90-100%": 0, "80-89%": 0, "70-79%": 0, 
        "60-69%": 0, "50-59%": 0, "50%以下": 0
    }
    for s in students:
        acc = s['accuracy']
        if acc >= 90: accuracy_ranges["90-100%"] += 1
        elif acc >= 80: accuracy_ranges["80-89%"] += 1
        elif acc >= 70: accuracy_ranges["70-79%"] += 1
        elif acc >= 60: accuracy_ranges["60-69%"] += 1
        elif acc >= 50: accuracy_ranges["50-59%"] += 1
        else: accuracy_ranges["50%以下"] += 1
    
    df_accuracy = pd.DataFrame({
        "正确率区间": list(accuracy_ranges.keys()),
        "学生人数": list(accuracy_ranges.values())
    })
    st.bar_chart(df_accuracy.set_index("正确率区间"))
    
    # 2. 学习时长分布
    st.markdown("#### 2️⃣ 学习时长分布")
    time_ranges = {
        "30分钟以下": 0, "30-60分钟": 0, "1-2小时": 0,
        "2-3小时": 0, "3小时以上": 0
    }
    for s in students:
        t = s['study_time']
        if t < 30: time_ranges["30分钟以下"] += 1
        elif t < 60: time_ranges["30-60分钟"] += 1
        elif t < 120: time_ranges["1-2小时"] += 1
        elif t < 180: time_ranges["2-3小时"] += 1
        else: time_ranges["3小时以上"] += 1
    
    df_time = pd.DataFrame({
        "学习时长": list(time_ranges.keys()),
        "学生人数": list(time_ranges.values())
    })
    st.bar_chart(df_time.set_index("学习时长"))
    
    # 3. 做题量 vs 正确率 散点图
    st.markdown("#### 3️⃣ 做题量与正确率关系")
    df_scatter = pd.DataFrame({
        "学生": [s['name'] for s in students],
        "做题量": [s['total_questions'] for s in students],
        "正确率": [s['accuracy'] for s in students]
    })
    st.scatter_chart(df_scatter.set_index("学生")[["做题量", "正确率"]])
    
    # 4. 班级Top10排行
    st.markdown("#### 4️⃣ 班级正确率排行榜")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**🏆 Top 10 学霸**")
        top10 = sorted(students, key=lambda x: x['accuracy'], reverse=True)[:10]
        for i, s in enumerate(top10):
            medal = ["🥇", "🥈", "🥉"][i] if i < 3 else f"{i+1}."
            st.markdown(f"{medal} {s['name']} - {s['accuracy']}%")
    
    with col2:
        st.markdown("**⚠️ 需关注学生**")
        bottom10 = sorted(students, key=lambda x: x['accuracy'])[:10]
        for i, s in enumerate(bottom10):
            st.markdown(f"⚠️ {s['name']} - {s['accuracy']}%")


def render_topic_analysis(students, stats):
    """渲染专题分析 - 丰富的数据维度"""
    st.markdown("### 🎯 专题知识点深度分析")
    
    import pandas as pd
    
    all_topics = stats['all_wrong_topics']
    
    # ========== 第一部分：总览数据 ==========
    st.markdown("#### 📊 专题数据总览")
    
    total_topics = len(all_topics)
    total_wrong = sum(all_topics.values())
    avg_wrong_per_topic = round(total_wrong / total_topics, 1) if total_topics > 0 else 0
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("涉及专题数", f"{total_topics}个")
    with col2:
        st.metric("错题总数", f"{total_wrong}道")
    with col3:
        st.metric("平均每专题错题", f"{avg_wrong_per_topic}道")
    with col4:
        high_risk = len([t for t, c in all_topics.items() if c > avg_wrong_per_topic * 1.5])
        st.metric("高风险专题", f"{high_risk}个", delta="需重点关注", delta_color="inverse")
    
    st.markdown("---")
    
    # ========== 第二部分：班级薄弱点排行 ==========
    st.markdown("#### 🔥 班级薄弱点排行")
    
    if stats['weak_topics']:
        # 用表格展示更多信息
        weak_data = []
        for i, (topic, count) in enumerate(stats['weak_topics']):
            # 计算该专题涉及学生数
            affected_students = len([s for s in students if topic in s['wrong_by_topic'] and s['wrong_by_topic'][topic] > 0])
            risk_level = "🔴 高" if count > avg_wrong_per_topic * 1.5 else ("🟡 中" if count > avg_wrong_per_topic else "🟢 低")
            weak_data.append({
                "排名": i + 1,
                "专题名称": topic,
                "错题总数": count,
                "涉及学生": f"{affected_students}人",
                "风险等级": risk_level
            })
        
        df_weak = pd.DataFrame(weak_data)
        st.dataframe(df_weak, use_container_width=True, hide_index=True)
        
        # 可视化柱状图
        weak_df = pd.DataFrame({
            "专题": [t[0][:8] + "..." if len(t[0]) > 8 else t[0] for t in stats['weak_topics']],
            "错题数": [t[1] for t in stats['weak_topics']]
        })
        st.bar_chart(weak_df.set_index("专题"))
    
    st.markdown("---")
    
    # ========== 第三部分：各专题详细分析 ==========
    st.markdown("#### 📋 各专题详细分析")
    
    if all_topics:
        sorted_topics = sorted(all_topics.items(), key=lambda x: x[1], reverse=True)
        
        # 创建更丰富的数据表
        topic_details = []
        for topic, count in sorted_topics:
            # 统计该专题相关学生
            affected = [s for s in students if topic in s['wrong_by_topic'] and s['wrong_by_topic'][topic] > 0]
            
            if affected:
                avg_wrong = round(sum(s['wrong_by_topic'][topic] for s in affected) / len(affected), 1)
                max_wrong = max(s['wrong_by_topic'][topic] for s in affected)
                worst_student = [s['name'] for s in affected if s['wrong_by_topic'][topic] == max_wrong][0]
            else:
                avg_wrong = 0
                max_wrong = 0
                worst_student = "-"
            
            topic_details.append({
                "专题": topic,
                "错题总数": count,
                "涉及人数": len(affected),
                "人均错题": avg_wrong,
                "最多错题": max_wrong,
                "最需关注": worst_student
            })
        
        df_details = pd.DataFrame(topic_details)
        st.dataframe(df_details, use_container_width=True, hide_index=True)
    
    st.markdown("---")
    
    # ========== 第四部分：难度分级 ==========
    st.markdown("#### 🎚️ 专题难度分级")
    
    col1, col2, col3 = st.columns(3)
    
    # 根据错题数分级
    high_difficulty = [t for t, c in all_topics.items() if c > avg_wrong_per_topic * 1.5]
    medium_difficulty = [t for t, c in all_topics.items() if avg_wrong_per_topic * 0.5 <= c <= avg_wrong_per_topic * 1.5]
    low_difficulty = [t for t, c in all_topics.items() if c < avg_wrong_per_topic * 0.5]
    
    with col1:
        st.markdown("""
        <div style='background: #ffebee; padding: 15px; border-radius: 10px; border-left: 4px solid #f44336;'>
            <h4 style='color: #c62828; margin: 0;'>🔴 高难度专题</h4>
            <p style='color: #666; margin: 5px 0;'>错题数高于平均50%以上</p>
        </div>
        """, unsafe_allow_html=True)
        for t in high_difficulty[:5]:
            st.markdown(f"• {t}")
        if not high_difficulty:
            st.info("暂无")
    
    with col2:
        st.markdown("""
        <div style='background: #fff8e1; padding: 15px; border-radius: 10px; border-left: 4px solid #ff9800;'>
            <h4 style='color: #ef6c00; margin: 0;'>🟡 中等难度专题</h4>
            <p style='color: #666; margin: 5px 0;'>错题数接近平均水平</p>
        </div>
        """, unsafe_allow_html=True)
        for t in medium_difficulty[:5]:
            st.markdown(f"• {t}")
        if not medium_difficulty:
            st.info("暂无")
    
    with col3:
        st.markdown("""
        <div style='background: #e8f5e9; padding: 15px; border-radius: 10px; border-left: 4px solid #4caf50;'>
            <h4 style='color: #2e7d32; margin: 0;'>🟢 低难度专题</h4>
            <p style='color: #666; margin: 5px 0;'>错题数低于平均50%</p>
        </div>
        """, unsafe_allow_html=True)
        for t in low_difficulty[:5]:
            st.markdown(f"• {t}")
        if not low_difficulty:
            st.info("暂无")
    
    st.markdown("---")
    
    # ========== 第五部分：教学建议 ==========
    st.markdown("#### 💡 针对性教学建议")
    
    if stats['weak_topics']:
        for i, (topic, count) in enumerate(stats['weak_topics'][:3]):
            affected_count = len([s for s in students if topic in s['wrong_by_topic'] and s['wrong_by_topic'][topic] > 0])
            
            st.markdown(f"""
            <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                        padding: 20px; border-radius: 12px; margin: 10px 0;'>
                <h4 style='color: white; margin: 0;'>📌 重点专题 {i+1}：{topic}</h4>
                <p style='color: rgba(255,255,255,0.9); margin: 10px 0 0 0;'>
                    累计错题 <strong>{count}</strong> 道 | 涉及学生 <strong>{affected_count}</strong> 人 | 
                    建议：安排专项复习课，重点讲解易错点
                </p>
            </div>
            """, unsafe_allow_html=True)


def render_ai_diagnosis(students, stats, ai_service):
    """渲染AI智能诊断"""
    st.markdown("### 🤖 AI智能诊断分析")
    
    # 选择分析类型
    analysis_type = st.radio(
        "选择分析类型：",
        ["📊 班级整体分析", "👤 个人学情诊断", "🎯 专题教学建议", "📈 学习趋势预测"],
        horizontal=True
    )
    
    if analysis_type == "📊 班级整体分析":
        if st.button("🔍 生成班级整体分析报告", type="primary"):
            with st.spinner("AI正在分析班级数据..."):
                weak_topics_str = ", ".join([f"{t[0]}({t[1]}道错题)" for t in stats['weak_topics']])
                
                prompt = f"""作为一位资深教育数据分析专家，请分析以下班级学习数据并给出专业建议：

班级概况：
- 学生总数：{stats['total_students']}人
- 平均正确率：{stats['avg_accuracy']}%
- 平均做题数：{stats['avg_questions']}道
- 平均学习时长：{stats['avg_study_time']}分钟

共性薄弱点（错题最多的专题）：
{weak_topics_str}

请从以下几个方面进行分析：
1. 整体学情评估（优势与不足）
2. 薄弱专题的原因分析
3. 针对性教学策略建议
4. 分层教学建议（学优生、中等生、待提升生）
5. 下阶段重点教学内容建议"""

                messages = [
                    {"role": "system", "content": "你是一位资深的教育数据分析专家，擅长根据学习数据给出专业的教学建议。"},
                    {"role": "user", "content": prompt}
                ]
                
                result = ai_service.call_api(messages)
                if result:
                    st.markdown(result)
    
    elif analysis_type == "👤 个人学情诊断":
        # 选择学生
        student_names = [f"{s['name']} ({s['id']})" for s in students]
        selected = st.selectbox("选择要分析的学生：", student_names)
        
        if selected and st.button("🔍 生成个人学情报告", type="primary"):
            student_name = selected.split(" (")[0]
            student = next((s for s in students if s['name'] == student_name), None)
            
            if student:
                with st.spinner(f"AI正在分析 {student['name']} 的学习数据..."):
                    wrong_topics_str = ", ".join([f"{t}({c}道)" for t, c in student['wrong_by_topic'].items() if c > 0])
                    
                    prompt = f"""作为一位教育专家，请分析以下学生的学习数据并给出个性化建议：

学生信息：
- 姓名：{student['name']}
- 学号：{student['id']}
- 做题总数：{student['total_questions']}道
- 正确率：{student['accuracy']}%
- 错题数：{student['wrong_count']}道
- 学习时长：{student['study_time']}分钟
- 搜索次数：{student['searches']}次
- 查看知识点数：{student['knowledge_viewed']}个

错题分布（按专题）：
{wrong_topics_str}

班级平均正确率：{stats['avg_accuracy']}%

请提供：
1. 学习状态评估
2. 优势与不足分析
3. 薄弱知识点针对性建议
4. 学习方法改进建议
5. 下阶段学习计划建议"""

                    messages = [
                        {"role": "system", "content": "你是一位专业的教育顾问，擅长根据学生数据给出个性化学习建议。"},
                        {"role": "user", "content": prompt}
                    ]
                    
                    result = ai_service.call_api(messages)
                    if result:
                        st.markdown(result)
    
    elif analysis_type == "🎯 专题教学建议":
        # 选择专题
        all_topics = list(stats['all_wrong_topics'].keys())
        selected_topic = st.selectbox("选择要分析的专题：", all_topics)
        
        if selected_topic and st.button("🔍 生成专题教学建议", type="primary"):
            error_count = stats['all_wrong_topics'].get(selected_topic, 0)
            
            with st.spinner(f"AI正在分析 {selected_topic} 专题..."):
                prompt = f"""作为一位高中历史教学专家，请针对以下专题给出教学建议：

专题名称：{selected_topic}
班级错题数：{error_count}道
班级总人数：{stats['total_students']}人

请提供：
1. 该专题的核心知识点梳理
2. 学生常见误区分析
3. 重难点突破策略
4. 推荐教学方法和活动设计
5. 配套练习题设计建议（3-5道）
6. 与其他专题的关联和拓展"""

                messages = [
                    {"role": "system", "content": "你是一位资深高中历史老师，擅长专题教学设计和知识点讲解。"},
                    {"role": "user", "content": prompt}
                ]
                
                result = ai_service.call_api(messages)
                if result:
                    st.markdown(result)
    
    elif analysis_type == "📈 学习趋势预测":
        if st.button("🔍 生成学习趋势分析", type="primary"):
            with st.spinner("AI正在分析学习趋势..."):
                # 模拟趋势数据
                high_performers = len([s for s in students if s['accuracy'] >= 80])
                medium_performers = len([s for s in students if 60 <= s['accuracy'] < 80])
                low_performers = len([s for s in students if s['accuracy'] < 60])
                
                prompt = f"""作为一位教育数据分析师，请根据以下数据预测班级学习趋势：

当前班级状况：
- 优秀学生（正确率≥80%）：{high_performers}人 ({round(high_performers/len(students)*100,1)}%)
- 中等学生（60-79%）：{medium_performers}人 ({round(medium_performers/len(students)*100,1)}%)
- 待提升学生（<60%）：{low_performers}人 ({round(low_performers/len(students)*100,1)}%)
- 平均学习时长：{stats['avg_study_time']}分钟
- 平均做题量：{stats['avg_questions']}道

请分析：
1. 班级整体学习趋势预测
2. 不同层次学生的发展预期
3. 可能出现的问题预警
4. 教学调整建议
5. 期末考试成绩预测及提升策略"""

                messages = [
                    {"role": "system", "content": "你是一位教育数据分析师，擅长根据学习数据预测趋势和给出预警建议。"},
                    {"role": "user", "content": prompt}
                ]
                
                result = ai_service.call_api(messages)
                if result:
                    st.markdown(result)


# ============ 登录页面 ============
def render_login_page():
    """渲染登录页面"""
    st.markdown("""
    <style>
    .login-container {
        max-width: 500px;
        margin: 50px auto;
        padding: 40px;
        background: white;
        border-radius: 20px;
        box-shadow: 0 10px 40px rgba(0,0,0,0.1);
    }
    .login-title {
        text-align: center;
        color: #333;
        margin-bottom: 30px;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div style='text-align: center; padding: 30px 0;'>
        <h1>📚 高中历史自适应学习系统</h1>
        <p style='color: #666; font-size: 18px;'>请选择登录身份</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        # 登录类型选择
        login_type = st.radio("选择登录身份：", ["🧑‍🎓 学生登录", "👨‍🏫 教师登录"], horizontal=True)
        
        st.markdown("---")
        
        if login_type == "🧑‍🎓 学生登录":
            st.markdown("### 学生登录")
            
            input_type = st.radio("选择登录方式：", ["学号", "姓名"], horizontal=True)
            
            if input_type == "学号":
                student_id = st.text_input("请输入学号：", placeholder="例如：2024001")
            else:
                student_name = st.text_input("请输入姓名：", placeholder="例如：张伟")
            
            if st.button("🚀 进入学习", type="primary", use_container_width=True):
                # 记录学生信息
                if input_type == "学号":
                    st.session_state.student_id = student_id if student_id else "guest"
                    st.session_state.student_name = "同学"
                else:
                    st.session_state.student_name = student_name if student_name else "同学"
                    st.session_state.student_id = "guest"
                
                st.session_state.logged_in = True
                st.session_state.user_role = "student"
                st.rerun()
        
        else:
            st.markdown("### 教师登录")
            
            password = st.text_input("请输入管理密码：", type="password", placeholder="请输入密码")
            
            if st.button("🔐 登录管理后台", type="primary", use_container_width=True):
                if verify_teacher_password(password):
                    st.session_state.logged_in = True
                    st.session_state.user_role = "teacher"
                    st.success("✅ 登录成功！正在跳转...")
                    st.rerun()
                else:
                    st.error("❌ 密码错误，请重试")
        
        st.markdown("---")
        st.markdown("""
        <div style='text-align: center; color: #999; font-size: 12px;'>
            © 2026 高中历史自适应学习系统
        </div>
        """, unsafe_allow_html=True)


def check_login_status():
    """检查登录状态"""
    return st.session_state.get('logged_in', False)


def get_user_role():
    """获取用户角色"""
    return st.session_state.get('user_role', None)


def logout():
    """退出登录"""
    if 'logged_in' in st.session_state:
        del st.session_state.logged_in
    if 'user_role' in st.session_state:
        del st.session_state.user_role
    if 'student_id' in st.session_state:
        del st.session_state.student_id
    if 'student_name' in st.session_state:
        del st.session_state.student_name

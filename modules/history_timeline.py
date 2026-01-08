"""
历史地图时间轴功能模块
实现交互式历史地图和时间轴展示
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from data.history_knowledge_graph import HISTORY_KNOWLEDGE_GRAPH, get_all_events
from datetime import datetime


def render_history_timeline():
    """渲染历史地图时间轴页面"""
    
    st.markdown("""
    <div class="module-header">
        <div class="module-title">
            <span>🗺️</span> 历史地图时间轴
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="content-panel">
        <div class="panel-header">💡 功能说明</div>
        <ul style="color: #6b7280; line-height: 1.8;">
            <li>📅 交互式时间轴展示重大历史事件</li>
            <li>🗺️ 地图标注事件发生地点</li>
            <li>🔍 点击事件查看详细信息</li>
            <li>🎯 按朝代/专题/地区筛选</li>
            <li>💡 理清历史脉络，强化时空观念</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    # 创建标签页：时间轴视图 / 地图视图
    tab1, tab2, tab3 = st.tabs(["📅 时间轴视图", "🗺️ 地图视图", "📊 专题视图"])
    
    with tab1:
        render_timeline_view()
    
    with tab2:
        render_map_view()
    
    with tab3:
        render_topic_view()


def render_timeline_view():
    """渲染时间轴视图"""
    st.markdown("### 📅 中国历史大事年表")
    
    # 筛选选项
    col1, col2 = st.columns(2)
    
    with col1:
        selected_module = st.selectbox(
            "选择历史时期",
            options=["全部"] + [m['name'] for m in HISTORY_KNOWLEDGE_GRAPH['modules']],
            key="timeline_module"
        )
    
    with col2:
        selected_period = st.selectbox(
            "选择具体时期",
            options=["全部", "先秦时期", "秦汉时期", "魏晋南北朝", "隋唐时期", "宋元时期", "明清时期", "近代时期", "现代时期"],
            key="timeline_period"
        )
    
    # 获取所有事件
    all_events = get_all_events()
    
    # 筛选事件
    filtered_events = []
    for event in all_events:
        if selected_module != "全部" and event['module'] != selected_module:
            continue
        if selected_period != "全部" and event['period'] != selected_period:
            continue
        filtered_events.append(event)
    
    if not filtered_events:
        st.info("没有找到符合条件的事件")
        return
    
    # 创建时间轴图表
    fig = create_timeline_chart(filtered_events)
    st.plotly_chart(fig, use_container_width=True)
    
    # 显示事件列表
    st.markdown("---")
    st.markdown("### 📋 事件详情")
    
    # 按时间排序显示
    for i, event in enumerate(filtered_events):
        with st.expander(f"{event['year']} - {event['name']}", expanded=False):
            cols = st.columns([1, 2])
            with cols[0]:
                st.markdown(f"""
                **⏰ 时间：** {event['year']}  
                **📍 地点：** {event['location']}  
                **📚 所属章节：** {event['chapter']}
                """)
            with cols[1]:
                st.markdown(f"**📖 历史时期：** {event['period']}")
                st.markdown(f"**🏛️ 模块：** {event['module']}")


def create_timeline_chart(events):
    """创建时间轴图表"""
    # 准备数据
    years = []
    names = []
    locations = []
    descriptions = []
    
    for event in events:
        # 提取年份数字（简单处理）
        year_str = event['year']
        try:
            # 处理公元前
            if '前' in year_str:
                year = -int(''.join(filter(str.isdigit, year_str)))
            else:
                year = int(''.join(filter(str.isdigit, year_str)))
        except:
            year = 0
        
        years.append(year)
        names.append(event['name'])
        locations.append(event['location'])
        descriptions.append(f"{event['year']} - {event['name']}<br>地点: {event['location']}")
    
    # 创建散点图
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=years,
        y=[1] * len(years),  # 所有点在同一水平线上
        mode='markers+text',
        marker=dict(
            size=12,
            color=years,
            colorscale='Viridis',
            showscale=True,
            colorbar=dict(title="年份")
        ),
        text=names,
        textposition="top center",
        hovertext=descriptions,
        hoverinfo="text"
    ))
    
    fig.update_layout(
        title="历史事件时间轴",
        xaxis_title="年份",
        yaxis_visible=False,
        height=400,
        hovermode='closest',
        showlegend=False
    )
    
    return fig


def render_map_view():
    """渲染地图视图"""
    st.markdown("### 🗺️ 历史事件地图")
    
    st.info("💡 地图功能开发中，将展示历史事件的地理位置分布")
    
    # 筛选选项
    selected_event_type = st.selectbox(
        "选择事件类型",
        options=["全部事件", "战争", "变法改革", "起义", "建立政权", "外交事件"],
        key="map_event_type"
    )
    
    # 这里可以集成地图库（如folium、plotly地图等）
    # 显示中国地图，标注历史事件发生地
    
    st.markdown("""
    <div class="content-panel">
        <h4>📍 重要历史地点</h4>
        <ul style="color: #6b7280;">
            <li><strong>北京：</strong> 元大都、明清两代首都、五四运动、新中国成立</li>
            <li><strong>南京：</strong> 明朝首都、太平天国、中华民国、南京大屠杀</li>
            <li><strong>西安（长安）：</strong> 西周、秦、汉、唐都城、西安事变</li>
            <li><strong>开封：</strong> 北宋都城、清明上河图</li>
            <li><strong>洛阳：</strong> 东周、东汉、隋唐东都</li>
            <li><strong>上海：</strong> 中共一大、五口通商、租界</li>
            <li><strong>武汉：</strong> 辛亥革命武昌起义</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)


def render_topic_view():
    """渲染专题视图"""
    st.markdown("### 📊 专题历史梳理")
    
    # 选择专题
    topics = [
        "中国古代政治制度演变",
        "中国古代经济发展",
        "中国古代思想文化",
        "近代中国反侵略斗争",
        "近代中国的近代化探索",
        "新民主主义革命",
        "社会主义建设与改革开放"
    ]
    
    selected_topic = st.selectbox("选择专题", topics)
    
    if selected_topic == "中国古代政治制度演变":
        render_political_system_topic()
    elif selected_topic == "近代中国反侵略斗争":
        render_anti_aggression_topic()
    elif selected_topic == "社会主义建设与改革开放":
        render_socialist_construction_topic()
    else:
        st.info(f"【{selected_topic}】专题内容开发中")


def render_political_system_topic():
    """渲染中国古代政治制度演变专题"""
    st.markdown("#### 📜 中国古代政治制度演变")
    
    timeline_data = [
        {"period": "西周", "system": "分封制、宗法制", "feature": "血缘关系维系统治"},
        {"period": "秦朝", "system": "专制主义中央集权制度", "feature": "皇帝制、三公九卿、郡县制"},
        {"period": "汉朝", "system": "中央集权强化", "feature": "推恩令、察举制、刺史制度"},
        {"period": "隋唐", "system": "三省六部制", "feature": "科举制、完善的官僚体系"},
        {"period": "宋朝", "system": "中央集权进一步加强", "feature": "削弱相权、强化皇权"},
        {"period": "元朝", "system": "行省制", "feature": "地方行政制度创新"},
        {"period": "明清", "system": "君主专制达到顶峰", "feature": "废丞相、设内阁、军机处"}
    ]
    
    # 使用表格展示
    import pandas as pd
    df = pd.DataFrame(timeline_data)
    st.dataframe(df, use_container_width=True, hide_index=True)
    
    # 演变特点分析
    st.markdown("---")
    st.markdown("##### 🎯 演变特点")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        **总体趋势：**
        - 中央集权不断加强
        - 君主专制不断强化
        - 地方权力逐渐削弱
        - 制度日趋完善
        """)
    
    with col2:
        st.markdown("""
        **影响：**
        - ✅ 有利于国家统一和稳定
        - ✅ 有利于多民族国家发展
        - ❌ 后期阻碍社会进步
        - ❌ 压抑个性和创造力
        """)


def render_anti_aggression_topic():
    """渲染近代中国反侵略斗争专题"""
    st.markdown("#### ⚔️ 近代中国反侵略斗争")
    
    struggles = [
        {"time": "1840-1842", "event": "鸦片战争", "result": "失败", "treaty": "南京条约"},
        {"time": "1856-1860", "event": "第二次鸦片战争", "result": "失败", "treaty": "天津条约、北京条约"},
        {"time": "1894-1895", "event": "甲午战争", "result": "失败", "treaty": "马关条约"},
        {"time": "1900-1901", "event": "八国联军侵华", "result": "失败", "treaty": "辛丑条约"},
        {"time": "1937-1945", "event": "抗日战争", "result": "胜利", "treaty": "-"}
    ]
    
    import pandas as pd
    df = pd.DataFrame(struggles)
    st.dataframe(df, use_container_width=True, hide_index=True)
    
    st.markdown("---")
    st.success("**💡 历史规律：** 抗日战争是近代以来中国反抗外敌入侵第一次取得完全胜利的民族解放战争，关键在于全民族抗战和国共合作。")


def render_socialist_construction_topic():
    """渲染社会主义建设与改革开放专题"""
    st.markdown("#### 🇨🇳 社会主义建设与改革开放")
    
    st.markdown("##### 📊 发展阶段")
    
    stages = [
        {"stage": "过渡时期 (1949-1956)", "main_task": "社会主义三大改造", "achievement": "社会主义制度基本建立"},
        {"stage": "探索时期 (1956-1978)", "main_task": "探索社会主义建设道路", "achievement": "取得一定成就，但有严重失误"},
        {"stage": "改革开放 (1978-2012)", "main_task": "改革开放和现代化建设", "achievement": "综合国力大幅提升"},
        {"stage": "新时代 (2012-至今)", "main_task": "中国特色社会主义新时代", "achievement": "全面建成小康社会"}
    ]
    
    import pandas as pd
    df = pd.DataFrame(stages)
    st.dataframe(df, use_container_width=True, hide_index=True)
    
    st.markdown("---")
    st.markdown("##### 🎯 改革开放重大成就")
    
    achievements_col1, achievements_col2 = st.columns(2)
    
    with achievements_col1:
        st.markdown("""
        **经济建设：**
        - GDP世界第二
        - 人民生活水平提高
        - 基础设施完善
        - 科技创新发展
        """)
    
    with achievements_col2:
        st.markdown("""
        **对外开放：**
        - 加入WTO
        - 一带一路倡议
        - 构建人类命运共同体
        - 国际影响力提升
        """)

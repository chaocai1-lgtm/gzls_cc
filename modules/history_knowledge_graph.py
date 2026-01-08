"""
高中历史学习系统 - 知识图谱交互模块
基于Neo4j的历史知识网络可视化
"""
import streamlit as st
from neo4j import GraphDatabase
import plotly.graph_objects as go
import json
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parent.parent))

from config.history_config import NEO4J_URI, NEO4J_USERNAME, NEO4J_PASSWORD


class HistoryKnowledgeGraph:
    """历史知识图谱类"""
    
    def __init__(self):
        try:
            self.driver = GraphDatabase.driver(
                NEO4J_URI,
                auth=(NEO4J_USERNAME, NEO4J_PASSWORD)
            )
            self.connected = True
        except Exception as e:
            st.error(f"无法连接到Neo4j: {e}")
            self.connected = False
    
    def close(self):
        if self.connected:
            self.driver.close()
    
    def get_textbooks(self):
        """获取所有教科书"""
        if not self.connected:
            return []
        
        with self.driver.session() as session:
            result = session.run("""
                MATCH (b:Textbook)
                RETURN b.id as id, b.name as name, b.type as type
                ORDER BY b.id
            """)
            return [dict(record) for record in result]
    
    def get_units_by_book(self, book_id):
        """获取指定教科书的所有单元"""
        if not self.connected:
            return []
        
        with self.driver.session() as session:
            result = session.run("""
                MATCH (b:Textbook {id: $book_id})-[:HAS_UNIT]->(u:Unit)
                RETURN u.id as id, u.title as title, u.unit_number as number
                ORDER BY u.unit_number
            """, book_id=book_id)
            return [dict(record) for record in result]
    
    def get_lessons_by_unit(self, unit_id):
        """获取指定单元的所有课文"""
        if not self.connected:
            return []
        
        with self.driver.session() as session:
            result = session.run("""
                MATCH (u:Unit {id: $unit_id})-[:HAS_LESSON]->(l:Lesson)
                RETURN l.id as id, l.title as title, l.lesson_number as number,
                       l.content_preview as preview
                ORDER BY l.lesson_number
            """, unit_id=unit_id)
            return [dict(record) for record in result]
    
    def get_knowledge_by_lesson(self, lesson_id):
        """获取指定课文的知识点"""
        if not self.connected:
            return {"events": [], "figures": [], "concepts": []}
        
        with self.driver.session() as session:
            # 获取历史事件
            events = session.run("""
                MATCH (l:Lesson {id: $lesson_id})-[:MENTIONS_EVENT]->(e:HistoricalEvent)
                RETURN e.id as id, e.year as year, e.description as description
                ORDER BY e.year
            """, lesson_id=lesson_id)
            
            # 获取历史人物
            figures = session.run("""
                MATCH (l:Lesson {id: $lesson_id})-[:MENTIONS_FIGURE]->(f:HistoricalFigure)
                RETURN f.id as id, f.name as name, f.description as description
            """, lesson_id=lesson_id)
            
            # 获取概念
            concepts = session.run("""
                MATCH (l:Lesson {id: $lesson_id})-[:DEFINES_CONCEPT]->(c:Concept)
                RETURN c.id as id, c.term as term
            """, lesson_id=lesson_id)
            
            return {
                "events": [dict(r) for r in events],
                "figures": [dict(r) for r in figures],
                "concepts": [dict(r) for r in concepts]
            }
    
    def get_timeline_events(self, limit=50):
        """获取时间线上的历史事件"""
        if not self.connected:
            return []
        
        with self.driver.session() as session:
            result = session.run("""
                MATCH (e:HistoricalEvent)
                WHERE e.year IS NOT NULL
                RETURN e.year as year, e.description as description, e.id as id
                ORDER BY toInteger(e.year)
                LIMIT $limit
            """, limit=limit)
            return [dict(record) for record in result]
    
    def search_knowledge(self, keyword):
        """搜索知识点"""
        if not self.connected:
            return {"lessons": [], "events": [], "figures": [], "concepts": []}
        
        with self.driver.session() as session:
            # 搜索课文
            lessons = session.run("""
                MATCH (l:Lesson)
                WHERE l.title CONTAINS $keyword
                RETURN l.id as id, l.title as title, l.book_name as book
                LIMIT 10
            """, keyword=keyword)
            
            # 搜索历史事件
            events = session.run("""
                MATCH (e:HistoricalEvent)
                WHERE e.description CONTAINS $keyword
                RETURN e.id as id, e.year as year, e.description as description
                LIMIT 10
            """, keyword=keyword)
            
            # 搜索历史人物
            figures = session.run("""
                MATCH (f:HistoricalFigure)
                WHERE f.name CONTAINS $keyword OR f.description CONTAINS $keyword
                RETURN f.id as id, f.name as name, f.description as description
                LIMIT 10
            """, keyword=keyword)
            
            # 搜索概念
            concepts = session.run("""
                MATCH (c:Concept)
                WHERE c.term CONTAINS $keyword
                RETURN c.id as id, c.term as term
                LIMIT 10
            """, keyword=keyword)
            
            return {
                "lessons": [dict(r) for r in lessons],
                "events": [dict(r) for r in events],
                "figures": [dict(r) for r in figures],
                "concepts": [dict(r) for r in concepts]
            }
    
    def get_knowledge_graph_data(self, book_id=None, limit=100):
        """获取知识图谱数据用于可视化"""
        if not self.connected:
            return {"nodes": [], "edges": []}
        
        with self.driver.session() as session:
            # 根据是否指定教科书构建查询
            if book_id:
                query = """
                    MATCH (b:Textbook {id: $book_id})-[:HAS_UNIT]->(u:Unit)-[:HAS_LESSON]->(l:Lesson)
                    OPTIONAL MATCH (l)-[r]->(n)
                    WHERE n:HistoricalEvent OR n:HistoricalFigure OR n:Concept
                    RETURN u, l, r, n
                    LIMIT $limit
                """
                result = session.run(query, book_id=book_id, limit=limit)
            else:
                query = """
                    MATCH (u:Unit)-[:HAS_LESSON]->(l:Lesson)
                    OPTIONAL MATCH (l)-[r]->(n)
                    WHERE n:HistoricalEvent OR n:HistoricalFigure OR n:Concept
                    RETURN u, l, r, n
                    LIMIT $limit
                """
                result = session.run(query, limit=limit)
            
            nodes = {}
            edges = []
            
            for record in result:
                # 添加单元节点
                if record['u']:
                    unit = record['u']
                    unit_id = unit['id']
                    if unit_id not in nodes:
                        nodes[unit_id] = {
                            "id": unit_id,
                            "label": unit['title'],
                            "type": "unit",
                            "group": 1
                        }
                
                # 添加课文节点
                if record['l']:
                    lesson = record['l']
                    lesson_id = lesson['id']
                    if lesson_id not in nodes:
                        nodes[lesson_id] = {
                            "id": lesson_id,
                            "label": lesson['title'],
                            "type": "lesson",
                            "group": 2
                        }
                    
                    # 添加单元到课文的边
                    if record['u']:
                        edges.append({
                            "from": unit['id'],
                            "to": lesson_id,
                            "label": "包含"
                        })
                
                # 添加知识节点
                if record['n']:
                    knowledge = record['n']
                    node_id = knowledge['id']
                    
                    if node_id not in nodes:
                        # 确定节点类型
                        labels = list(knowledge.labels)
                        if 'HistoricalEvent' in labels:
                            node_type = "event"
                            label = f"{knowledge.get('year', '')}: {knowledge.get('description', '')[:20]}"
                            group = 3
                        elif 'HistoricalFigure' in labels:
                            node_type = "figure"
                            label = knowledge.get('name', '')
                            group = 4
                        elif 'Concept' in labels:
                            node_type = "concept"
                            label = knowledge.get('term', '')
                            group = 5
                        else:
                            continue
                        
                        nodes[node_id] = {
                            "id": node_id,
                            "label": label,
                            "type": node_type,
                            "group": group
                        }
                    
                    # 添加课文到知识的边
                    if record['l'] and record['r']:
                        relationship_type = record['r'].type
                        edges.append({
                            "from": lesson['id'],
                            "to": node_id,
                            "label": relationship_type
                        })
            
            return {
                "nodes": list(nodes.values()),
                "edges": edges
            }


def render_history_knowledge_graph():
    """渲染历史知识图谱页面"""
    st.markdown("""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                padding: 30px; border-radius: 16px; margin-bottom: 30px;">
        <h2 style="margin: 0; color: white;">🗺️ 历史知识图谱</h2>
        <p style="margin: 10px 0 0 0; color: rgba(255,255,255,0.9);">
            探索历史知识网络，理清知识脉络
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # 初始化知识图谱
    kg = HistoryKnowledgeGraph()
    
    if not kg.connected:
        st.error("⚠️ 无法连接到知识图谱数据库")
        st.info("请确保Neo4j服务正常运行，并检查配置文件")
        return
    
    # 创建标签页
    tab1, tab2, tab3, tab4 = st.tabs(["📚 按教材浏览", "🔍 搜索知识", "⏱️ 时间线", "🌐 图谱可视化"])
    
    with tab1:
        render_browse_by_textbook(kg)
    
    with tab2:
        render_knowledge_search(kg)
    
    with tab3:
        render_timeline(kg)
    
    with tab4:
        render_graph_visualization(kg)
    
    kg.close()


def render_browse_by_textbook(kg):
    """按教材浏览"""
    st.markdown("### 📖 选择教材")
    
    textbooks = kg.get_textbooks()
    
    if not textbooks:
        st.info("暂无教材数据")
        return
    
    # 选择教科书
    book_names = [f"{b['name']} ({b['type']})" for b in textbooks]
    selected_book_name = st.selectbox("选择教科书", book_names)
    
    if selected_book_name:
        selected_book = textbooks[book_names.index(selected_book_name)]
        book_id = selected_book['id']
        
        # 获取单元
        units = kg.get_units_by_book(book_id)
        
        st.markdown(f"### 📑 {selected_book['name']} - 单元列表")
        
        if not units:
            st.info("该教材暂无单元数据")
            return
        
        # 显示单元
        for unit in units:
            with st.expander(f"第{unit['number']}单元：{unit['title']}", expanded=False):
                # 获取课文
                lessons = kg.get_lessons_by_unit(unit['id'])
                
                if not lessons:
                    st.info("该单元暂无课文数据")
                    continue
                
                for lesson in lessons:
                    col1, col2 = st.columns([3, 1])
                    
                    with col1:
                        st.markdown(f"**第{lesson['number']}课：{lesson['title']}**")
                        if lesson.get('preview'):
                            st.caption(lesson['preview'][:100] + "...")
                    
                    with col2:
                        if st.button("查看详情", key=f"lesson_{lesson['id']}"):
                            st.session_state['selected_lesson'] = lesson['id']
                            st.session_state['view_detail'] = True
        
        # 显示课文详情
        if st.session_state.get('view_detail') and st.session_state.get('selected_lesson'):
            st.markdown("---")
            render_lesson_detail(kg, st.session_state['selected_lesson'])


def render_lesson_detail(kg, lesson_id):
    """渲染课文详情"""
    st.markdown("### 📝 课文详情")
    
    knowledge = kg.get_knowledge_by_lesson(lesson_id)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("#### 🎯 历史事件")
        if knowledge['events']:
            for event in knowledge['events']:
                st.markdown(f"- **{event['year']}年**：{event['description']}")
        else:
            st.info("暂无历史事件")
    
    with col2:
        st.markdown("#### 👤 历史人物")
        if knowledge['figures']:
            for figure in knowledge['figures']:
                st.markdown(f"- **{figure['name']}**")
                if figure.get('description'):
                    st.caption(figure['description'][:80] + "...")
        else:
            st.info("暂无历史人物")
    
    with col3:
        st.markdown("#### 💡 重要概念")
        if knowledge['concepts']:
            for concept in knowledge['concepts']:
                st.markdown(f"- {concept['term']}")
        else:
            st.info("暂无概念")


def render_knowledge_search(kg):
    """搜索知识"""
    st.markdown("### 🔍 搜索历史知识")
    
    keyword = st.text_input("输入关键词", placeholder="例如：秦始皇、辛亥革命、工业革命...")
    
    if keyword:
        with st.spinner("搜索中..."):
            results = kg.search_knowledge(keyword)
        
        # 显示结果
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 📚 相关课文")
            if results['lessons']:
                for lesson in results['lessons']:
                    st.markdown(f"- **{lesson['title']}** ({lesson['book']})")
            else:
                st.info("未找到相关课文")
            
            st.markdown("#### 🎯 相关事件")
            if results['events']:
                for event in results['events']:
                    st.markdown(f"- **{event['year']}**：{event['description']}")
            else:
                st.info("未找到相关事件")
        
        with col2:
            st.markdown("#### 👤 相关人物")
            if results['figures']:
                for figure in results['figures']:
                    st.markdown(f"- **{figure['name']}**")
                    if figure.get('description'):
                        st.caption(figure['description'][:80] + "...")
            else:
                st.info("未找到相关人物")
            
            st.markdown("#### 💡 相关概念")
            if results['concepts']:
                for concept in results['concepts']:
                    st.markdown(f"- {concept['term']}")
            else:
                st.info("未找到相关概念")


def render_timeline(kg):
    """渲染时间线"""
    st.markdown("### ⏱️ 历史事件时间线")
    
    limit = st.slider("显示事件数量", 10, 100, 50)
    
    events = kg.get_timeline_events(limit=limit)
    
    if not events:
        st.info("暂无时间线数据")
        return
    
    # 创建时间线图表
    fig = go.Figure()
    
    years = [int(e['year']) if e['year'].isdigit() else 0 for e in events]
    descriptions = [e['description'][:30] + "..." for e in events]
    
    fig.add_trace(go.Scatter(
        x=years,
        y=[1] * len(years),
        mode='markers+text',
        text=descriptions,
        textposition='top center',
        marker=dict(size=10, color='rgb(102, 126, 234)'),
        hovertext=[f"{e['year']}: {e['description']}" for e in events],
        hoverinfo='text'
    ))
    
    fig.update_layout(
        title="历史事件时间线",
        xaxis_title="年份",
        yaxis=dict(visible=False),
        height=600,
        showlegend=False
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # 显示事件列表
    st.markdown("### 📋 事件列表")
    
    for event in events:
        st.markdown(f"- **{event['year']}年**：{event['description']}")


def render_graph_visualization(kg):
    """渲染图谱可视化"""
    st.markdown("### 🌐 知识网络可视化")
    
    st.info("💡 提示：选择教材可以查看特定教材的知识网络")
    
    # 选择教科书（可选）
    textbooks = kg.get_textbooks()
    book_options = ["全部教材"] + [f"{b['name']}" for b in textbooks]
    selected_book_name = st.selectbox("选择教材范围", book_options)
    
    book_id = None
    if selected_book_name != "全部教材":
        book_id = textbooks[book_options.index(selected_book_name) - 1]['id']
    
    limit = st.slider("节点数量限制", 50, 200, 100)
    
    if st.button("生成知识图谱", type="primary"):
        with st.spinner("生成中..."):
            graph_data = kg.get_knowledge_graph_data(book_id=book_id, limit=limit)
        
        if not graph_data['nodes']:
            st.warning("暂无图谱数据")
            return
        
        st.success(f"✓ 已加载 {len(graph_data['nodes'])} 个节点，{len(graph_data['edges'])} 条边")
        
        # 显示图谱统计
        col1, col2, col3, col4 = st.columns(4)
        
        node_types = {}
        for node in graph_data['nodes']:
            node_type = node['type']
            node_types[node_type] = node_types.get(node_type, 0) + 1
        
        with col1:
            st.metric("单元", node_types.get('unit', 0))
        with col2:
            st.metric("课文", node_types.get('lesson', 0))
        with col3:
            st.metric("历史事件", node_types.get('event', 0))
        with col4:
            st.metric("人物+概念", node_types.get('figure', 0) + node_types.get('concept', 0))
        
        # 保存数据供前端使用
        st.session_state['graph_data'] = graph_data
        
        # 提示：这里需要前端JavaScript来渲染，Streamlit本身不支持复杂的网络图
        st.info("📊 图谱数据已准备就绪。在实际部署中，可以使用 vis.js 或 cytoscape.js 来渲染交互式知识图谱。")
        
        # 显示部分节点和边的信息
        with st.expander("查看图谱数据详情"):
            st.json({"nodes": graph_data['nodes'][:10], "edges": graph_data['edges'][:10]})


if __name__ == "__main__":
    render_history_knowledge_graph()

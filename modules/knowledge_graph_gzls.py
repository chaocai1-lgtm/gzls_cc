"""
历史知识图谱模块 (GZLS增强版) - 基于Neo4j的交互式可视化
GZLS = 高中历史 (GaoZhong LiShi)
使用Neo4j数据库存储5本高中历史教科书的完整知识体系
"""

import streamlit as st
from pyvis.network import Network
import streamlit.components.v1 as components
from neo4j import GraphDatabase
import json
from pathlib import Path
import sys
import tempfile
import os

sys.path.append(str(Path(__file__).parent.parent))

from config.history_config import (
    NEO4J_URI, NEO4J_USERNAME, NEO4J_PASSWORD,
    TEXTBOOKS, KNOWLEDGE_CATEGORIES, TIME_PERIODS
)


# GZLS 配色方案 - 历史书卷风格
GZLS_COLORS = {
    "必修": "#8b7355",  # 古典棕色
    "选择性必修": "#6b5444",  # 深棕色
    "事件": "#d4af37",  # 金色
    "人物": "#cd853f",  # 秘鲁色
    "概念": "#daa520",  # 金棒色
    "单元": "#a0826d",  # 浅棕色
    "课文": "#c19a6b",  # 驼色
}


class GZLSKnowledgeGraph:
    """GZLS历史知识图谱类 - 连接Neo4j数据库"""
    
    def __init__(self):
        self.tag = "gzls"  # GZLS标签
        try:
            self.driver = GraphDatabase.driver(
                NEO4J_URI,
                auth=(NEO4J_USERNAME, NEO4J_PASSWORD)
            )
            # 测试连接
            with self.driver.session() as session:
                session.run("RETURN 1")
            self.connected = True
            st.success("✅ GZLS知识图谱已连接到Neo4j数据库")
        except Exception as e:
            st.error(f"❌ 无法连接到Neo4j (GZLS): {e}")
            self.connected = False
    
    def close(self):
        """关闭数据库连接"""
        if self.connected and self.driver:
            self.driver.close()
    
    def get_textbooks(self):
        """获取所有教科书 (GZLS)"""
        if not self.connected:
            return []
        
        try:
            with self.driver.session() as session:
                result = session.run("""
                    MATCH (b:Textbook)
                    RETURN b.id as id, b.name as name, b.type as type
                    ORDER BY b.id
                """)
                books = [dict(record) for record in result]
                return books
        except Exception as e:
            st.error(f"获取教科书失败 (GZLS): {e}")
            return []
    
    def get_units_by_book(self, book_id):
        """获取指定教科书的所有单元 (GZLS)"""
        if not self.connected:
            return []
        
        try:
            with self.driver.session() as session:
                result = session.run("""
                    MATCH (b:Textbook {id: $book_id})-[:HAS_UNIT]->(u:Unit)
                    RETURN u.id as id, u.name as name, u.order as order
                    ORDER BY u.order
                """, book_id=book_id)
                return [dict(record) for record in result]
        except Exception as e:
            st.error(f"获取单元失败 (GZLS): {e}")
            return []
    
    def get_lessons_by_unit(self, unit_id):
        """获取指定单元的所有课文 (GZLS)"""
        if not self.connected:
            return []
        
        try:
            with self.driver.session() as session:
                result = session.run("""
                    MATCH (u:Unit {id: $unit_id})-[:HAS_LESSON]->(l:Lesson)
                    RETURN l.id as id, l.name as name, l.order as order
                    ORDER BY l.order
                """, unit_id=unit_id)
                return [dict(record) for record in result]
        except Exception as e:
            st.error(f"获取课文失败 (GZLS): {e}")
            return []
    
    def get_lesson_details(self, lesson_id):
        """获取课文详细内容 (GZLS)"""
        if not self.connected:
            return None
        
        try:
            with self.driver.session() as session:
                result = session.run("""
                    MATCH (l:Lesson {id: $lesson_id})
                    OPTIONAL MATCH (l)-[:HAS_EVENT]->(e:Event)
                    OPTIONAL MATCH (l)-[:HAS_FIGURE]->(f:Figure)
                    OPTIONAL MATCH (l)-[:HAS_CONCEPT]->(c:Concept)
                    RETURN l.name as name, l.content as content,
                           collect(DISTINCT {id: e.id, name: e.name, year: e.year, description: e.description}) as events,
                           collect(DISTINCT {id: f.id, name: f.name, role: f.role, description: f.description}) as figures,
                           collect(DISTINCT {id: c.id, name: c.name, category: c.category, description: c.description}) as concepts
                """, lesson_id=lesson_id)
                record = result.single()
                if record:
                    return dict(record)
                return None
        except Exception as e:
            st.error(f"获取课文详情失败 (GZLS): {e}")
            return None
    
    def search_knowledge(self, keyword, node_type="全部"):
        """搜索知识点 (GZLS)"""
        if not self.connected:
            return []
        
        try:
            with self.driver.session() as session:
                if node_type == "全部":
                    query = """
                        MATCH (n)
                        WHERE n.name CONTAINS $keyword OR n.description CONTAINS $keyword
                        RETURN labels(n)[0] as type, n.id as id, n.name as name, 
                               n.description as description
                        LIMIT 50
                    """
                else:
                    query = f"""
                        MATCH (n:{node_type})
                        WHERE n.name CONTAINS $keyword OR n.description CONTAINS $keyword
                        RETURN labels(n)[0] as type, n.id as id, n.name as name, 
                               n.description as description
                        LIMIT 50
                    """
                
                result = session.run(query, keyword=keyword)
                return [dict(record) for record in result]
        except Exception as e:
            st.error(f"搜索失败 (GZLS): {e}")
            return []
    
    def get_timeline_events(self, start_year=None, end_year=None):
        """获取时间线事件 (GZLS)"""
        if not self.connected:
            return []
        
        try:
            with self.driver.session() as session:
                if start_year and end_year:
                    query = """
                        MATCH (e:Event)
                        WHERE e.year >= $start_year AND e.year <= $end_year
                        RETURN e.id as id, e.name as name, e.year as year, 
                               e.description as description
                        ORDER BY e.year
                    """
                    result = session.run(query, start_year=start_year, end_year=end_year)
                else:
                    query = """
                        MATCH (e:Event)
                        WHERE e.year IS NOT NULL
                        RETURN e.id as id, e.name as name, e.year as year, 
                               e.description as description
                        ORDER BY e.year
                        LIMIT 100
                    """
                    result = session.run(query)
                
                return [dict(record) for record in result]
        except Exception as e:
            st.error(f"获取时间线失败 (GZLS): {e}")
            return []
    
    def get_knowledge_network(self, center_node_id, depth=2):
        """获取知识网络图 (GZLS) - 用于可视化"""
        if not self.connected:
            return {"nodes": [], "edges": []}
        
        try:
            with self.driver.session() as session:
                query = f"""
                    MATCH path = (center)-[*1..{depth}]-(connected)
                    WHERE center.id = $node_id
                    RETURN center, connected, relationships(path) as rels
                    LIMIT 100
                """
                
                result = session.run(query, node_id=center_node_id)
                
                nodes = {}
                edges = []
                
                for record in result:
                    center = record['center']
                    connected = record['connected']
                    rels = record['rels']
                    
                    # 添加中心节点
                    if center.element_id not in nodes:
                        nodes[center.element_id] = {
                            "id": center.element_id,
                            "label": center.get('name', 'Unknown'),
                            "type": list(center.labels)[0] if center.labels else "Unknown",
                            "properties": dict(center)
                        }
                    
                    # 添加连接节点
                    if connected.element_id not in nodes:
                        nodes[connected.element_id] = {
                            "id": connected.element_id,
                            "label": connected.get('name', 'Unknown'),
                            "type": list(connected.labels)[0] if connected.labels else "Unknown",
                            "properties": dict(connected)
                        }
                    
                    # 添加关系
                    for rel in rels:
                        edges.append({
                            "from": rel.start_node.element_id,
                            "to": rel.end_node.element_id,
                            "label": rel.type
                        })
                
                return {
                    "nodes": list(nodes.values()),
                    "edges": edges
                }
        except Exception as e:
            st.error(f"获取知识网络失败 (GZLS): {e}")
            return {"nodes": [], "edges": []}
    
    def get_statistics(self):
        """获取知识图谱统计信息 (GZLS)"""
        if not self.connected:
            return {}
        
        try:
            with self.driver.session() as session:
                stats = {}
                
                # 统计各类节点数量
                result = session.run("""
                    MATCH (n:Textbook) RETURN count(n) as count
                """)
                stats['textbooks'] = result.single()['count']
                
                result = session.run("""
                    MATCH (n:Unit) RETURN count(n) as count
                """)
                stats['units'] = result.single()['count']
                
                result = session.run("""
                    MATCH (n:Lesson) RETURN count(n) as count
                """)
                stats['lessons'] = result.single()['count']
                
                result = session.run("""
                    MATCH (n:Event) RETURN count(n) as count
                """)
                stats['events'] = result.single()['count']
                
                result = session.run("""
                    MATCH (n:Figure) RETURN count(n) as count
                """)
                stats['figures'] = result.single()['count']
                
                result = session.run("""
                    MATCH (n:Concept) RETURN count(n) as count
                """)
                stats['concepts'] = result.single()['count']
                
                # 统计关系数量
                result = session.run("""
                    MATCH ()-[r]->() RETURN count(r) as count
                """)
                stats['relationships'] = result.single()['count']
                
                return stats
        except Exception as e:
            st.error(f"获取统计信息失败 (GZLS): {e}")
            return {}


def render_knowledge_graph():
    """渲染GZLS知识图谱页面"""
    st.markdown("## 🗺️ 历史知识图谱 (GZLS)")
    st.markdown("**基于Neo4j的高中历史5本教科书完整知识体系**")
    
    # 初始化知识图谱
    if 'gzls_kg' not in st.session_state:
        st.session_state.gzls_kg = GZLSKnowledgeGraph()
    
    kg = st.session_state.gzls_kg
    
    if not kg.connected:
        st.error("❌ 知识图谱未连接，请检查Neo4j配置")
        st.info("💡 运行 `scripts/import_to_neo4j.py` 导入数据")
        return
    
    # 显示统计信息
    stats = kg.get_statistics()
    if stats:
        cols = st.columns(7)
        metrics = [
            ("📚 教科书", stats.get('textbooks', 0)),
            ("📑 单元", stats.get('units', 0)),
            ("📖 课文", stats.get('lessons', 0)),
            ("⚡ 历史事件", stats.get('events', 0)),
            ("👤 历史人物", stats.get('figures', 0)),
            ("💡 核心概念", stats.get('concepts', 0)),
            ("🔗 知识关系", stats.get('relationships', 0))
        ]
        for col, (label, value) in zip(cols, metrics):
            col.metric(label, value)
    
    st.markdown("---")
    
    # Tab切换
    tab1, tab2, tab3, tab4 = st.tabs([
        "📚 按教材浏览",
        "🔍 知识搜索",
        "⏱️ 历史时间线",
        "🕸️ 知识网络图"
    ])
    
    # Tab1: 按教材浏览
    with tab1:
        render_textbook_browser(kg)
    
    # Tab2: 知识搜索
    with tab2:
        render_knowledge_search(kg)
    
    # Tab3: 历史时间线
    with tab3:
        render_timeline(kg)
    
    # Tab4: 知识网络图
    with tab4:
        render_network_visualization(kg)


def render_textbook_browser(kg):
    """渲染教材浏览器 (GZLS)"""
    st.markdown("### 📚 浏览教材内容")
    
    # 获取教科书列表
    textbooks = kg.get_textbooks()
    
    if not textbooks:
        st.warning("⚠️ 暂无教科书数据，请先导入数据")
        st.code("cd scripts && python import_all_data.py", language="bash")
        return
    
    # 选择教科书
    book_options = {book['name']: book['id'] for book in textbooks}
    selected_book_name = st.selectbox(
        "选择教科书",
        list(book_options.keys()),
        key="gzls_book_select"
    )
    
    if selected_book_name:
        book_id = book_options[selected_book_name]
        
        # 获取单元列表
        units = kg.get_units_by_book(book_id)
        
        if units:
            unit_options = {unit['name']: unit['id'] for unit in units}
            selected_unit_name = st.selectbox(
                "选择单元",
                list(unit_options.keys()),
                key="gzls_unit_select"
            )
            
            if selected_unit_name:
                unit_id = unit_options[selected_unit_name]
                
                # 获取课文列表
                lessons = kg.get_lessons_by_unit(unit_id)
                
                if lessons:
                    lesson_options = {lesson['name']: lesson['id'] for lesson in lessons}
                    selected_lesson_name = st.selectbox(
                        "选择课文",
                        list(lesson_options.keys()),
                        key="gzls_lesson_select"
                    )
                    
                    if selected_lesson_name:
                        lesson_id = lesson_options[selected_lesson_name]
                        
                        # 显示课文详情
                        details = kg.get_lesson_details(lesson_id)
                        
                        if details:
                            st.markdown(f"## 📖 {details['name']}")
                            
                            # 课文内容
                            if details.get('content'):
                                with st.expander("📄 课文内容", expanded=True):
                                    st.markdown(details['content'])
                            
                            # 历史事件
                            events = [e for e in details.get('events', []) if e.get('id')]
                            if events:
                                with st.expander(f"⚡ 历史事件 ({len(events)}个)", expanded=True):
                                    for event in events:
                                        st.markdown(f"**{event['name']}** ({event.get('year', '未知年份')})")
                                        if event.get('description'):
                                            st.markdown(f"> {event['description']}")
                                        st.markdown("---")
                            
                            # 历史人物
                            figures = [f for f in details.get('figures', []) if f.get('id')]
                            if figures:
                                with st.expander(f"👤 历史人物 ({len(figures)}位)", expanded=True):
                                    for figure in figures:
                                        st.markdown(f"**{figure['name']}** - {figure.get('role', '未知')}")
                                        if figure.get('description'):
                                            st.markdown(f"> {figure['description']}")
                                        st.markdown("---")
                            
                            # 核心概念
                            concepts = [c for c in details.get('concepts', []) if c.get('id')]
                            if concepts:
                                with st.expander(f"💡 核心概念 ({len(concepts)}个)", expanded=True):
                                    for concept in concepts:
                                        st.markdown(f"**{concept['name']}** ({concept.get('category', '未分类')})")
                                        if concept.get('description'):
                                            st.markdown(f"> {concept['description']}")
                                        st.markdown("---")
                        else:
                            st.info("暂无详细内容")
                else:
                    st.info("该单元暂无课文")
        else:
            st.info("该教科书暂无单元")


def render_knowledge_search(kg):
    """渲染知识搜索 (GZLS)"""
    st.markdown("### 🔍 搜索历史知识")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        keyword = st.text_input(
            "输入关键词",
            placeholder="例如：鸦片战争、孔子、科举制度...",
            key="gzls_search_keyword"
        )
    
    with col2:
        node_type = st.selectbox(
            "搜索类型",
            ["全部", "Event", "Figure", "Concept", "Lesson"],
            key="gzls_search_type"
        )
    
    if st.button("🔍 搜索", key="gzls_search_btn"):
        if keyword:
            with st.spinner("搜索中..."):
                results = kg.search_knowledge(keyword, node_type)
                
                if results:
                    st.success(f"找到 {len(results)} 个相关结果")
                    
                    for result in results:
                        with st.expander(f"{result['type']} - {result['name']}"):
                            st.markdown(f"**ID:** {result['id']}")
                            if result.get('description'):
                                st.markdown(f"**描述:** {result['description']}")
                else:
                    st.warning("未找到相关结果")
        else:
            st.warning("请输入搜索关键词")


def render_timeline(kg):
    """渲染历史时间线 (GZLS)"""
    st.markdown("### ⏱️ 历史时间线")
    
    col1, col2 = st.columns(2)
    
    with col1:
        start_year = st.number_input(
            "起始年份",
            value=-2070,
            step=100,
            key="gzls_timeline_start"
        )
    
    with col2:
        end_year = st.number_input(
            "结束年份",
            value=2024,
            step=100,
            key="gzls_timeline_end"
        )
    
    if st.button("📊 生成时间线", key="gzls_timeline_btn"):
        with st.spinner("加载历史事件..."):
            events = kg.get_timeline_events(start_year, end_year)
            
            if events:
                st.success(f"共 {len(events)} 个历史事件")
                
                # 按时间顺序显示
                for event in events:
                    year_display = f"{abs(event['year'])}年{'前' if event['year'] < 0 else ''}"
                    
                    col_year, col_content = st.columns([1, 4])
                    
                    with col_year:
                        st.markdown(f"### {year_display}")
                    
                    with col_content:
                        st.markdown(f"**{event['name']}**")
                        if event.get('description'):
                            st.markdown(event['description'])
                    
                    st.markdown("---")
            else:
                st.warning("该时间段暂无历史事件")


def render_network_visualization(kg):
    """渲染知识网络图 (GZLS)"""
    st.markdown("### 🕸️ 知识关系网络图")
    st.info("💡 输入节点ID查看其知识网络关系")
    
    node_id = st.text_input(
        "节点ID",
        placeholder="例如：bixiu_shang_01_01",
        key="gzls_network_node_id"
    )
    
    depth = st.slider("关系深度", 1, 3, 2, key="gzls_network_depth")
    
    if st.button("🕸️ 生成网络图", key="gzls_network_btn"):
        if node_id:
            with st.spinner("生成知识网络..."):
                network_data = kg.get_knowledge_network(node_id, depth)
                
                if network_data['nodes']:
                    # 使用pyvis创建网络图
                    net = Network(height="600px", width="100%", bgcolor="#fdfbf7", font_color="#333")
                    
                    # 添加节点
                    for node in network_data['nodes']:
                        color = GZLS_COLORS.get(node['type'], "#95a5a6")
                        net.add_node(
                            node['id'],
                            label=node['label'],
                            title=f"{node['type']}: {node['label']}",
                            color=color
                        )
                    
                    # 添加边
                    for edge in network_data['edges']:
                        net.add_edge(edge['from'], edge['to'], label=edge.get('label', ''))
                    
                    # 设置物理布局
                    net.set_options("""
                    {
                        "physics": {
                            "enabled": true,
                            "barnesHut": {
                                "gravitationalConstant": -8000,
                                "springLength": 150,
                                "springConstant": 0.04
                            }
                        }
                    }
                    """)
                    
                    # 保存并显示
                    try:
                        with tempfile.NamedTemporaryFile(delete=False, suffix='.html', mode='w', encoding='utf-8') as f:
                            net.save_graph(f.name)
                            with open(f.name, 'r', encoding='utf-8') as html_file:
                                source_code = html_file.read()
                            components.html(source_code, height=620, scrolling=True)
                            os.unlink(f.name)
                    except Exception as e:
                        st.error(f"生成网络图失败: {e}")
                else:
                    st.warning("未找到该节点或其关系")
        else:
            st.warning("请输入节点ID")


if __name__ == "__main__":
    render_knowledge_graph()

"""
历史知识图谱模块 (GZLS简化版) - 基于JSON文件的知识浏览
不需要Neo4j，直接读取解析好的JSON数据
"""

import streamlit as st
import json
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parent.parent))


class GZLSKnowledgeGraphSimple:
    """GZLS历史知识图谱类 - 基于JSON文件"""
    
    def __init__(self):
        self.tag = "gzls_simple"
        self.data_dir = Path(__file__).parent.parent / "data" / "parsed"
        
        # 加载数据
        try:
            self.units = self._load_json("units.json")
            self.lessons = self._load_json("lessons.json")
            self.events = self._load_json("historical_events.json")
            self.figures = self._load_json("historical_figures.json")
            
            self.connected = True
            st.success(f"✅ GZLS知识图谱已加载：{len(self.units)}个单元，{len(self.lessons)}课，{len(self.events)}个事件，{len(self.figures)}位人物")
        except Exception as e:
            st.error(f"❌ 数据加载失败: {e}")
            self.connected = False
            self.units = []
            self.lessons = []
            self.events = []
            self.figures = []
    
    def _load_json(self, filename):
        """加载JSON文件"""
        file_path = self.data_dir / filename
        if file_path.exists():
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []
    
    def get_textbooks(self):
        """获取所有教科书"""
        textbooks = {}
        for unit in self.units:
            book_id = unit.get('book_id')
            book_name = unit.get('book_name')
            if book_id and book_id not in textbooks:
                textbooks[book_id] = {
                    'id': book_id,
                    'name': book_name,
                    'type': '必修' if 'bixiu' in book_id else '选择性必修'
                }
        return list(textbooks.values())
    
    def get_units_by_book(self, book_id):
        """获取指定教科书的所有单元"""
        units = [u for u in self.units if u.get('book_id') == book_id]
        # 按order排序
        units.sort(key=lambda x: x.get('order', 999))
        return units
    
    def get_lessons_by_unit(self, unit_id):
        """获取指定单元的所有课文"""
        lessons = [l for l in self.lessons if l.get('unit_id') == unit_id]
        # 按order排序
        lessons.sort(key=lambda x: x.get('order', 999))
        return lessons
    
    def get_lesson_details(self, lesson_id):
        """获取课文详细内容"""
        lesson = next((l for l in self.lessons if l.get('id') == lesson_id), None)
        if not lesson:
            return None
        
        # 获取该课的事件
        lesson_events = [e for e in self.events if e.get('lesson_id') == lesson_id]
        
        # 获取该课的人物
        lesson_figures = [f for f in self.figures if f.get('lesson_id') == lesson_id]
        
        return {
            'title': lesson.get('title', ''),
            'textbook_name': lesson.get('book_name', ''),
            'lesson_number': lesson.get('lesson_number', ''),
            'content': lesson.get('content', ''),
            'events': lesson_events,
            'figures': lesson_figures
        }
    
    def search_knowledge(self, keyword, node_type="全部"):
        """搜索知识点"""
        results = []
        
        if node_type in ["全部", "Lesson"]:
            for lesson in self.lessons:
                if keyword.lower() in lesson.get('title', '').lower() or \
                   keyword.lower() in lesson.get('content', '').lower():
                    results.append({
                        'type': 'Lesson',
                        'id': lesson.get('id'),
                        'name': lesson.get('title'),
                        'description': lesson.get('content', '')[:200]
                    })
        
        if node_type in ["全部", "Event"]:
            for event in self.events:
                if keyword.lower() in event.get('event', '').lower() or \
                   keyword.lower() in event.get('description', '').lower():
                    results.append({
                        'type': 'Event',
                        'id': event.get('id'),
                        'name': event.get('event'),
                        'description': event.get('description', '')
                    })
        
        if node_type in ["全部", "Figure"]:
            for figure in self.figures:
                if keyword.lower() in figure.get('name', '').lower() or \
                   keyword.lower() in figure.get('role', '').lower():
                    results.append({
                        'type': 'Figure',
                        'id': figure.get('id'),
                        'name': figure.get('name'),
                        'description': figure.get('role', '')
                    })
        
        return results[:50]
    
    def get_timeline_events(self, start_year=None, end_year=None):
        """获取时间线事件"""
        filtered_events = []
        
        for event in self.events:
            year = event.get('year')
            if year is None:
                continue
            
            try:
                year = int(year)
            except:
                continue
            
            if start_year and year < start_year:
                continue
            if end_year and year > end_year:
                continue
            
            filtered_events.append({
                'id': event.get('id'),
                'name': event.get('event'),
                'year': year,
                'description': event.get('description', '')
            })
        
        # 按年份排序
        filtered_events.sort(key=lambda x: x['year'])
        return filtered_events[:100]
    
    def get_statistics(self):
        """获取统计信息"""
        textbooks = self.get_textbooks()
        return {
            'textbooks': len(textbooks),
            'units': len(self.units),
            'lessons': len(self.lessons),
            'events': len(self.events),
            'figures': len(self.figures),
            'concepts': 0,
            'relationships': 0
        }


def render_knowledge_graph():
    """渲染GZLS知识图谱页面（简化版）"""
    st.markdown("## 🗺️ 历史知识图谱 (GZLS)")
    st.markdown("**基于5本高中历史教科书的完整知识体系（JSON版）**")
    
    # 初始化知识图谱
    if 'gzls_kg_simple' not in st.session_state:
        st.session_state.gzls_kg_simple = GZLSKnowledgeGraphSimple()
    
    kg = st.session_state.gzls_kg_simple
    
    if not kg.connected:
        st.error("❌ 数据未加载")
        st.info("💡 请确保已运行教科书解析：`python scripts/parse_textbooks.py`")
        return
    
    # 显示统计信息
    stats = kg.get_statistics()
    cols = st.columns(6)
    metrics = [
        ("📚 教科书", stats.get('textbooks', 0)),
        ("📑 单元", stats.get('units', 0)),
        ("📖 课文", stats.get('lessons', 0)),
        ("⚡ 历史事件", stats.get('events', 0)),
        ("👤 历史人物", stats.get('figures', 0)),
        ("💡 核心概念", stats.get('concepts', 0))
    ]
    for col, (label, value) in zip(cols, metrics):
        col.metric(label, value)
    
    st.markdown("---")
    
    # Tab切换
    tab1, tab2, tab3 = st.tabs([
        "📚 按教材浏览",
        "🔍 知识搜索",
        "⏱️ 历史时间线"
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


def render_textbook_browser(kg):
    """渲染教材浏览器"""
    st.markdown("### 📚 浏览教材内容")
    
    textbooks = kg.get_textbooks()
    
    if not textbooks:
        st.warning("⚠️ 暂无数据")
        return
    
    # 选择教科书
    book_options = {book['name']: book['id'] for book in textbooks}
    selected_book_name = st.selectbox(
        "选择教科书",
        list(book_options.keys()),
        key="gzls_simple_book_select"
    )
    
    if selected_book_name:
        book_id = book_options[selected_book_name]
        
        # 获取单元列表
        units = kg.get_units_by_book(book_id)
        
        if units:
            unit_options = {unit['title']: unit['id'] for unit in units}
            selected_unit_name = st.selectbox(
                "选择单元",
                list(unit_options.keys()),
                key="gzls_simple_unit_select"
            )
            
            if selected_unit_name:
                unit_id = unit_options[selected_unit_name]
                
                # 获取课文列表
                lessons = kg.get_lessons_by_unit(unit_id)
                
                if lessons:
                    lesson_options = {lesson['title']: lesson['id'] for lesson in lessons}
                    selected_lesson_name = st.selectbox(
                        "选择课文",
                        list(lesson_options.keys()),
                        key="gzls_simple_lesson_select"
                    )
                    
                    if selected_lesson_name:
                        lesson_id = lesson_options[selected_lesson_name]
                        
                        # 显示课文详情
                        details = kg.get_lesson_details(lesson_id)
                        
                        if details:
                            st.markdown(f"## 📖 {details['title']}")
                            
                            # 教材信息
                            col1, col2 = st.columns(2)
                            with col1:
                                st.info(f"📚 教材：{details.get('textbook_name', '未知')}")
                            with col2:
                                st.info(f"📑 课程编号：第{details.get('lesson_number', '?')}课")
                            
                            # 课文内容 - 完整显示
                            if details.get('content'):
                                content = details['content']
                                with st.expander("📄 课文内容（完整版）", expanded=False):
                                    # 使用文本框显示完整内容，可滚动
                                    st.text_area(
                                        "课文内容",
                                        value=content,
                                        height=600,
                                        label_visibility="collapsed"
                                    )
                                    st.info(f"字数：约{len(content)}字")
                            
                            # 历史事件
                            events = details.get('events', [])
                            if events:
                                with st.expander(f"⚡ 历史事件 ({len(events)}个)", expanded=True):
                                    for event in events[:20]:  # 增加显示数量
                                        st.markdown(f"**{event.get('event', '未知')}** ({event.get('year', '未知年份')})")
                                        if event.get('description'):
                                            st.markdown(f"> {event['description']}")
                                        st.markdown("---")
                            
                            # 历史人物
                            figures = details.get('figures', [])
                            if figures:
                                with st.expander(f"👤 历史人物 ({len(figures)}位)", expanded=True):
                                    for figure in figures[:20]:  # 增加显示数量
                                        st.markdown(f"**{figure.get('figure', '未知')}**")
                                        if figure.get('description'):
                                            st.markdown(f"> {figure['description'][:300]}...")
                                        st.markdown("---")
                        else:
                            st.info("暂无详细内容")
                else:
                    st.info("该单元暂无课文")
        else:
            st.info("该教科书暂无单元")


def render_knowledge_search(kg):
    """渲染知识搜索"""
    st.markdown("### 🔍 搜索历史知识")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        keyword = st.text_input(
            "输入关键词",
            placeholder="例如：鸦片战争、孔子、科举制度...",
            key="gzls_simple_search_keyword"
        )
    
    with col2:
        node_type = st.selectbox(
            "搜索类型",
            ["全部", "Event", "Figure", "Lesson"],
            key="gzls_simple_search_type"
        )
    
    if st.button("🔍 搜索", key="gzls_simple_search_btn"):
        if keyword:
            with st.spinner("搜索中..."):
                results = kg.search_knowledge(keyword, node_type)
                
                if results:
                    st.success(f"找到 {len(results)} 个相关结果")
                    
                    for result in results[:20]:
                        with st.expander(f"{result['type']} - {result['name']}"):
                            st.markdown(f"**ID:** {result['id']}")
                            if result.get('description'):
                                st.markdown(f"**描述:** {result['description'][:500]}")
                else:
                    st.warning("未找到相关结果")
        else:
            st.warning("请输入搜索关键词")


def render_timeline(kg):
    """渲染历史时间线"""
    st.markdown("### ⏱️ 历史时间线")
    
    col1, col2 = st.columns(2)
    
    with col1:
        start_year = st.number_input(
            "起始年份",
            value=-2070,
            step=100,
            key="gzls_simple_timeline_start"
        )
    
    with col2:
        end_year = st.number_input(
            "结束年份",
            value=2024,
            step=100,
            key="gzls_simple_timeline_end"
        )
    
    if st.button("📊 生成时间线", key="gzls_simple_timeline_btn"):
        with st.spinner("加载历史事件..."):
            events = kg.get_timeline_events(start_year, end_year)
            
            if events:
                st.success(f"共 {len(events)} 个历史事件")
                
                for event in events:
                    year_display = f"{abs(event['year'])}年{'前' if event['year'] < 0 else ''}"
                    
                    col_year, col_content = st.columns([1, 4])
                    
                    with col_year:
                        st.markdown(f"### {year_display}")
                    
                    with col_content:
                        st.markdown(f"**{event['name']}**")
                        if event.get('description'):
                            st.markdown(event['description'][:300])
                    
                    st.markdown("---")
            else:
                st.warning("该时间段暂无历史事件")


if __name__ == "__main__":
    render_knowledge_graph()

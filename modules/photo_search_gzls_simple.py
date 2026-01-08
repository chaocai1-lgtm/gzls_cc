"""
历史智能搜索模块 (GZLS简化版) - 基于JSON文件的搜索
不需要Elasticsearch，直接搜索JSON数据
"""

import streamlit as st
import json
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parent.parent))


class GZLSSearchEngineSimple:
    """GZLS历史搜索引擎类 - 基于JSON文件"""
    
    def __init__(self):
        self.tag = "gzls_simple"
        self.data_dir = Path(__file__).parent.parent / "data" / "parsed"
        
        # 加载数据
        try:
            self.lessons = self._load_json("lessons.json")
            self.events = self._load_json("historical_events.json")
            self.figures = self._load_json("historical_figures.json")
            
            self.connected = True
            st.success(f"✅ GZLS搜索引擎已加载：{len(self.lessons)}课，{len(self.events)}个事件")
        except Exception as e:
            st.error(f"❌ 数据加载失败: {e}")
            self.connected = False
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
    
    def search_lessons(self, query, textbook=None, size=20):
        """搜索课文内容"""
        results = []
        query_lower = query.lower()
        
        for lesson in self.lessons:
            # 检查标题和内容
            title_match = query_lower in lesson.get('title', '').lower()
            content_match = query_lower in lesson.get('content', '').lower()
            
            # 教科书筛选
            if textbook and lesson.get('book_name') != textbook:
                continue
            
            if title_match or content_match:
                # 提取匹配片段
                content = lesson.get('content', '')
                highlights = []
                if content_match:
                    idx = content.lower().find(query_lower)
                    if idx >= 0:
                        start = max(0, idx - 50)
                        end = min(len(content), idx + len(query) + 50)
                        highlights.append(content[start:end])
                
                results.append({
                    'title': lesson.get('title'),
                    'textbook_name': lesson.get('book_name'),
                    'unit_name': lesson.get('unit_name', '未知'),
                    'content': content,
                    'highlights': highlights,
                    'score': 2.0 if title_match else 1.0
                })
        
        # 按相关度排序
        results.sort(key=lambda x: x['score'], reverse=True)
        return results[:size]
    
    def search_events(self, query, start_year=None, end_year=None, size=20):
        """搜索历史事件"""
        results = []
        query_lower = query.lower()
        
        for event in self.events:
            # 检查事件描述（数据中只有description字段，没有event字段）
            description = event.get('description', '')
            desc_match = query_lower in description.lower()
            
            if not desc_match:
                continue
            
            # 年份范围筛选
            year = event.get('year')
            if year is not None:
                try:
                    year = int(year)
                    if start_year is not None and year < start_year:
                        continue
                    if end_year is not None and year > end_year:
                        continue
                except:
                    pass
            
            # 使用description作为事件名称（截取前30字）
            event_name = description[:30] + '...' if len(description) > 30 else description
            
            results.append({
                'name': event_name,
                'year': year,
                'description': description,
                'textbook_name': event.get('book_name'),
                'lesson_name': event.get('lesson_title', ''),
                'score': 1.0
            })
        
        # 按年份排序
        results.sort(key=lambda x: (x.get('year') or 0))
        return results[:size]
    
    def search_knowledge_points(self, query, category=None, size=20):
        """搜索知识点（人物）"""
        results = []
        query_lower = query.lower()
        
        for figure in self.figures:
            # 检查人物名称和描述（数据中只有name和description字段，没有role字段）
            name_match = query_lower in figure.get('name', '').lower()
            desc_match = query_lower in figure.get('description', '').lower()
            
            if not (name_match or desc_match):
                continue
            
            results.append({
                'name': figure.get('name'),
                'category': '历史人物',
                'description': figure.get('description', ''),
                'textbook_name': figure.get('book_name'),
                'highlights': [],
                'score': 2.0 if name_match else 1.0
            })
        
        # 按相关度排序
        results.sort(key=lambda x: x['score'], reverse=True)
        return results[:size]
    
    def get_index_stats(self):
        """获取索引统计信息"""
        return {
            'history_lessons': len(self.lessons),
            'history_events': len(self.events),
            'history_knowledge_points': len(self.figures)
        }


def render_photo_search():
    """渲染GZLS智能搜索页面（简化版）- 统一搜索"""
    st.markdown("## 🔍 智能历史搜索")
    st.markdown("**基于5本高中历史教科书的全文搜索 - 涵盖课文、事件、人物**")
    
    # 初始化搜索引擎
    if 'gzls_search_simple' not in st.session_state:
        st.session_state.gzls_search_simple = GZLSSearchEngineSimple()
    
    search_engine = st.session_state.gzls_search_simple
    
    if not search_engine.connected:
        st.error("❌ 搜索引擎未加载")
        st.info("💡 请确保已运行教科书解析：`python scripts/parse_textbooks.py`")
        return
    
    # 显示索引统计
    stats = search_engine.get_index_stats()
    cols = st.columns(3)
    metrics = [
        ("📖 课文", stats.get('history_lessons', 0)),
        ("⚡ 事件", stats.get('history_events', 0)),
        ("👤 人物", stats.get('history_knowledge_points', 0))
    ]
    for col, (label, value) in zip(cols, metrics):
        col.metric(label, value)
    
    st.markdown("---")
    
    # 统一搜索框
    st.markdown("### 🔎 输入关键词搜索")
    
    col1, col2 = st.columns([4, 1])
    
    with col1:
        query = st.text_input(
            "搜索历史内容",
            placeholder="例如：秦始皇、辛亥革命、改革开放、中央集权...",
            key="gzls_unified_search_query",
            label_visibility="collapsed"
        )
    
    with col2:
        search_btn = st.button("🔍 搜索", key="gzls_unified_search_btn", use_container_width=True)
    
    if search_btn and query:
        with st.spinner("正在搜索全部内容..."):
            # 同时搜索所有类型
            lessons = search_engine.search_lessons(query, size=10)
            events = search_engine.search_events(query, size=15)
            figures = search_engine.search_knowledge_points(query, size=10)
            
            total_results = len(lessons) + len(events) + len(figures)
            
            if total_results == 0:
                st.warning("😔 未找到相关内容，请尝试其他关键词")
                return
            
            st.success(f"✅ 找到 {total_results} 条相关结果（课文 {len(lessons)} 条、事件 {len(events)} 条、人物 {len(figures)} 条）")
            
            # 显示人物结果
            if figures:
                st.markdown("### 👤 相关历史人物")
                for idx, result in enumerate(figures, 1):
                    with st.expander(f"{idx}. {result.get('name', '未命名')} ", expanded=(idx<=2)):
                        if result.get('description'):
                            st.markdown(f"**简介:** {result['description']}")
                        if result.get('textbook_name'):
                            st.caption(f"📚 来源: {result['textbook_name']}")
                st.markdown("---")
            
            # 显示事件结果
            if events:
                st.markdown("### ⚡ 相关历史事件")
                for idx, result in enumerate(events, 1):
                    year = result.get('year')
                    year_display = f"{abs(year)}年{'前' if year and year < 0 else ''}" if year else "未知年份"
                    
                    col_year, col_content = st.columns([1, 5])
                    
                    with col_year:
                        st.markdown(f"**{year_display}**")
                    
                    with col_content:
                        with st.expander(f"{idx}. {result.get('name', '未命名')}", expanded=(idx<=3)):
                            if result.get('description'):
                                st.markdown(result['description'][:400] + ('...' if len(result.get('description', '')) > 400 else ''))
                            if result.get('textbook_name'):
                                st.caption(f"📚 来源: {result['textbook_name']}")
                
                st.markdown("---")
            
            # 显示课文结果
            if lessons:
                st.markdown("### 📖 相关课文内容")
                for idx, result in enumerate(lessons, 1):
                    with st.expander(f"{idx}. {result.get('title', '未命名')}", expanded=(idx<=2)):
                        st.markdown(f"**教科书:** {result.get('textbook_name', '未知')}")
                        st.markdown(f"**单元:** {result.get('unit_name', '未知')}")
                        
                        # 显示高亮片段
                        if result.get('highlights'):
                            st.markdown("**相关内容片段:**")
                            for highlight in result['highlights'][:2]:
                                st.markdown(f"> ...{highlight}...")
                        
                        # 显示部分内容
                        content = result.get('content', '')
                        if content:
                            st.markdown("**内容预览:**")
                            st.markdown(content[:400] + ('...' if len(content) > 400 else ''))
    
    elif search_btn and not query:
        st.warning("⚠️ 请输入搜索关键词")


if __name__ == "__main__":
    render_photo_search()

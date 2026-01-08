"""
高中历史学习系统 - 智能搜索模块
基于Elasticsearch的全文搜索
"""
import streamlit as st
from elasticsearch import Elasticsearch
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from config.history_config import (
    ES_CLOUD_ID, ES_USERNAME, ES_PASSWORD,
    ES_INDEX_KNOWLEDGE, ES_INDEX_LESSONS, ES_INDEX_EVENTS
)


class HistorySearchEngine:
    """历史搜索引擎类"""
    
    def __init__(self):
        try:
            self.es = Elasticsearch(
                cloud_id=ES_CLOUD_ID,
                basic_auth=(ES_USERNAME, ES_PASSWORD)
            )
            
            if not self.es.ping():
                raise Exception("无法连接到Elasticsearch")
            
            self.connected = True
        except Exception as e:
            st.error(f"无法连接到Elasticsearch: {e}")
            self.connected = False
    
    def search_lessons(self, query, size=10):
        """搜索课文内容"""
        if not self.connected:
            return []
        
        try:
            result = self.es.search(
                index=ES_INDEX_LESSONS,
                body={
                    "query": {
                        "multi_match": {
                            "query": query,
                            "fields": ["title^3", "content"],
                            "fuzziness": "AUTO"
                        }
                    },
                    "highlight": {
                        "fields": {
                            "content": {
                                "fragment_size": 150,
                                "number_of_fragments": 3
                            }
                        }
                    },
                    "size": size
                }
            )
            
            hits = []
            for hit in result['hits']['hits']:
                source = hit['_source']
                highlights = hit.get('highlight', {}).get('content', [])
                
                hits.append({
                    "id": source['id'],
                    "title": source['title'],
                    "book_name": source['book_name'],
                    "lesson_number": source.get('lesson_number', 0),
                    "score": hit['_score'],
                    "highlights": highlights
                })
            
            return hits
        except Exception as e:
            st.error(f"搜索课文失败: {e}")
            return []
    
    def search_events(self, query, year_range=None, size=20):
        """搜索历史事件"""
        if not self.connected:
            return []
        
        try:
            # 构建查询
            must_queries = [
                {
                    "match": {
                        "description": {
                            "query": query,
                            "fuzziness": "AUTO"
                        }
                    }
                }
            ]
            
            # 添加年份范围过滤
            if year_range:
                must_queries.append({
                    "range": {
                        "year": {
                            "gte": str(year_range[0]),
                            "lte": str(year_range[1])
                        }
                    }
                })
            
            result = self.es.search(
                index=ES_INDEX_EVENTS,
                body={
                    "query": {
                        "bool": {
                            "must": must_queries
                        }
                    },
                    "sort": [
                        {"year": {"order": "asc"}}
                    ],
                    "size": size
                }
            )
            
            hits = []
            for hit in result['hits']['hits']:
                source = hit['_source']
                hits.append({
                    "id": source['id'],
                    "year": source['year'],
                    "description": source['description'],
                    "lesson_id": source.get('lesson_id', ''),
                    "score": hit['_score']
                })
            
            return hits
        except Exception as e:
            st.error(f"搜索历史事件失败: {e}")
            return []
    
    def search_knowledge(self, query, category=None, size=20):
        """搜索知识点（人物、概念等）"""
        if not self.connected:
            return []
        
        try:
            # 构建查询
            must_queries = [
                {
                    "multi_match": {
                        "query": query,
                        "fields": ["term^2", "description"],
                        "fuzziness": "AUTO"
                    }
                }
            ]
            
            # 添加分类过滤
            if category and category != "全部":
                must_queries.append({
                    "term": {
                        "category": category
                    }
                })
            
            result = self.es.search(
                index=ES_INDEX_KNOWLEDGE,
                body={
                    "query": {
                        "bool": {
                            "must": must_queries
                        }
                    },
                    "size": size
                }
            )
            
            hits = []
            for hit in result['hits']['hits']:
                source = hit['_source']
                hits.append({
                    "id": source['id'],
                    "term": source['term'],
                    "description": source.get('description', ''),
                    "category": source.get('category', ''),
                    "lesson_id": source.get('lesson_id', ''),
                    "score": hit['_score']
                })
            
            return hits
        except Exception as e:
            st.error(f"搜索知识点失败: {e}")
            return []
    
    def aggregate_events_by_year(self):
        """按年份聚合历史事件"""
        if not self.connected:
            return {}
        
        try:
            result = self.es.search(
                index=ES_INDEX_EVENTS,
                body={
                    "size": 0,
                    "aggs": {
                        "events_per_year": {
                            "terms": {
                                "field": "year",
                                "size": 100,
                                "order": {"_key": "asc"}
                            }
                        }
                    }
                }
            )
            
            buckets = result['aggregations']['events_per_year']['buckets']
            return {bucket['key']: bucket['doc_count'] for bucket in buckets}
        except Exception as e:
            st.error(f"聚合统计失败: {e}")
            return {}


def render_history_search():
    """渲染历史搜索页面"""
    st.markdown("""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                padding: 30px; border-radius: 16px; margin-bottom: 30px;">
        <h2 style="margin: 0; color: white;">🔍 智能搜索</h2>
        <p style="margin: 10px 0 0 0; color: rgba(255,255,255,0.9);">
            全文检索历史知识，快速找到你需要的内容
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # 初始化搜索引擎
    search_engine = HistorySearchEngine()
    
    if not search_engine.connected:
        st.error("⚠️ 无法连接到搜索引擎")
        st.info("请确保Elasticsearch服务正常运行，并检查配置文件")
        return
    
    # 创建标签页
    tab1, tab2, tab3, tab4 = st.tabs(["📚 搜索课文", "🎯 搜索事件", "💡 搜索知识点", "📊 事件统计"])
    
    with tab1:
        render_lesson_search(search_engine)
    
    with tab2:
        render_event_search(search_engine)
    
    with tab3:
        render_knowledge_search(search_engine)
    
    with tab4:
        render_event_statistics(search_engine)


def render_lesson_search(search_engine):
    """搜索课文"""
    st.markdown("### 📖 课文全文搜索")
    
    st.info("💡 提示：支持模糊搜索，可以搜索课文标题或内容")
    
    query = st.text_input("输入搜索关键词", placeholder="例如：秦始皇统一六国、辛亥革命背景...")
    
    col1, col2 = st.columns([3, 1])
    with col1:
        size = st.slider("显示结果数量", 5, 20, 10)
    with col2:
        search_button = st.button("🔍 搜索", type="primary", use_container_width=True)
    
    if search_button and query:
        with st.spinner("搜索中..."):
            results = search_engine.search_lessons(query, size=size)
        
        if results:
            st.success(f"找到 {len(results)} 条相关课文")
            
            for i, result in enumerate(results, 1):
                with st.container():
                    st.markdown(f"#### {i}. {result['title']}")
                    st.caption(f"📚 {result['book_name']} · 第{result['lesson_number']}课 · 相关度: {result['score']:.2f}")
                    
                    # 显示高亮片段
                    if result['highlights']:
                        st.markdown("**相关内容：**")
                        for highlight in result['highlights']:
                            st.markdown(f"> {highlight}")
                    
                    st.markdown("---")
        else:
            st.warning("未找到相关课文，请尝试其他关键词")


def render_event_search(search_engine):
    """搜索历史事件"""
    st.markdown("### 🎯 历史事件搜索")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        query = st.text_input("输入事件关键词", placeholder="例如：战争、改革、革命...")
    
    with col2:
        use_year_filter = st.checkbox("按年份筛选", value=False)
    
    year_range = None
    if use_year_filter:
        col_y1, col_y2 = st.columns(2)
        with col_y1:
            start_year = st.number_input("起始年份", value=-221, step=1)
        with col_y2:
            end_year = st.number_input("结束年份", value=2024, step=1)
        year_range = (start_year, end_year)
    
    size = st.slider("显示结果数量", 10, 50, 20)
    
    if st.button("🔍 搜索事件", type="primary"):
        if query:
            with st.spinner("搜索中..."):
                results = search_engine.search_events(query, year_range=year_range, size=size)
            
            if results:
                st.success(f"找到 {len(results)} 条历史事件")
                
                # 按年代分组显示
                current_century = None
                
                for result in results:
                    year_int = int(result['year']) if result['year'].isdigit() else 0
                    century = year_int // 100
                    
                    # 显示世纪标题
                    if century != current_century:
                        current_century = century
                        if year_int < 0:
                            st.markdown(f"### 公元前 {abs(century)}世纪")
                        else:
                            st.markdown(f"### {century}世纪")
                    
                    # 显示事件
                    col1, col2 = st.columns([1, 4])
                    with col1:
                        st.markdown(f"**{result['year']}年**")
                    with col2:
                        st.markdown(f"{result['description']}")
                
            else:
                st.warning("未找到相关事件，请尝试其他关键词或调整年份范围")
        else:
            st.warning("请输入搜索关键词")


def render_knowledge_search(search_engine):
    """搜索知识点"""
    st.markdown("### 💡 知识点搜索")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        query = st.text_input("输入知识点关键词", placeholder="例如：秦始皇、科举制度、工业革命...")
    
    with col2:
        category = st.selectbox("分类", ["全部", "历史人物", "概念"])
    
    size = st.slider("显示结果数量", 10, 30, 20)
    
    if st.button("🔍 搜索知识点", type="primary"):
        if query:
            with st.spinner("搜索中..."):
                results = search_engine.search_knowledge(query, category=category, size=size)
            
            if results:
                st.success(f"找到 {len(results)} 条知识点")
                
                # 按类别分组
                by_category = {}
                for result in results:
                    cat = result.get('category', '其他')
                    if cat not in by_category:
                        by_category[cat] = []
                    by_category[cat].append(result)
                
                # 显示结果
                for cat, items in by_category.items():
                    st.markdown(f"#### {cat} ({len(items)})")
                    
                    for item in items:
                        with st.expander(f"📌 {item['term']}"):
                            if item['description']:
                                st.markdown(item['description'])
                            st.caption(f"相关度: {item['score']:.2f}")
            else:
                st.warning("未找到相关知识点，请尝试其他关键词")
        else:
            st.warning("请输入搜索关键词")


def render_event_statistics(search_engine):
    """事件统计"""
    st.markdown("### 📊 历史事件统计")
    
    st.info("💡 显示数据库中各年份的历史事件数量分布")
    
    if st.button("📈 生成统计", type="primary"):
        with st.spinner("统计中..."):
            stats = search_engine.aggregate_events_by_year()
        
        if stats:
            st.success(f"统计了 {len(stats)} 个年份的数据")
            
            # 创建图表
            import plotly.graph_objects as go
            
            years = sorted([int(y) if y.isdigit() else 0 for y in stats.keys()])
            counts = [stats[str(y)] for y in years]
            
            fig = go.Figure()
            fig.add_trace(go.Bar(
                x=years,
                y=counts,
                marker_color='rgb(102, 126, 234)',
                text=counts,
                textposition='outside'
            ))
            
            fig.update_layout(
                title="历史事件年份分布",
                xaxis_title="年份",
                yaxis_title="事件数量",
                height=500,
                showlegend=False
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # 显示前10个事件最多的年份
            st.markdown("### 🏆 事件最多的年份 Top 10")
            
            sorted_stats = sorted(stats.items(), key=lambda x: x[1], reverse=True)[:10]
            
            for i, (year, count) in enumerate(sorted_stats, 1):
                col1, col2, col3 = st.columns([1, 3, 1])
                with col1:
                    st.markdown(f"**#{i}**")
                with col2:
                    st.markdown(f"**{year}年**")
                with col3:
                    st.metric("", f"{count} 个事件")
        else:
            st.warning("暂无统计数据")


if __name__ == "__main__":
    render_history_search()

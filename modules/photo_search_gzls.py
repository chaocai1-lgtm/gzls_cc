"""
历史智能搜索模块 (GZLS增强版) - 基于Elasticsearch的全文搜索
GZLS = 高中历史 (GaoZhong LiShi)
使用Elasticsearch存储和搜索5本高中历史教科书的完整内容
"""

import streamlit as st
from elasticsearch import Elasticsearch
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parent.parent))

from config.history_config import (
    ES_CLOUD_ID, ES_USERNAME, ES_PASSWORD,
    ES_INDEX_KNOWLEDGE, ES_INDEX_LESSONS, ES_INDEX_EVENTS
)


class GZLSSearchEngine:
    """GZLS历史搜索引擎类 - 连接Elasticsearch"""
    
    def __init__(self):
        self.tag = "gzls"  # GZLS标签
        try:
            self.es = Elasticsearch(
                cloud_id=ES_CLOUD_ID,
                basic_auth=(ES_USERNAME, ES_PASSWORD),
                request_timeout=30
            )
            
            # 测试连接
            if not self.es.ping():
                raise Exception("无法ping通Elasticsearch")
            
            self.connected = True
            st.success("✅ GZLS搜索引擎已连接到Elasticsearch")
        except Exception as e:
            st.error(f"❌ 无法连接到Elasticsearch (GZLS): {e}")
            self.connected = False
    
    def search_lessons(self, query, textbook=None, size=20):
        """搜索课文内容 (GZLS)"""
        if not self.connected:
            return []
        
        try:
            # 构建搜索条件
            must_conditions = [
                {
                    "multi_match": {
                        "query": query,
                        "fields": ["title^3", "content^2", "keywords"],
                        "fuzziness": "AUTO"
                    }
                }
            ]
            
            # 如果指定了教科书，添加过滤条件
            if textbook:
                must_conditions.append({
                    "term": {"textbook_id": textbook}
                })
            
            search_body = {
                "query": {
                    "bool": {
                        "must": must_conditions
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
            
            result = self.es.search(
                index=ES_INDEX_LESSONS,
                body=search_body
            )
            
            hits = []
            for hit in result['hits']['hits']:
                doc = hit['_source']
                doc['score'] = hit['_score']
                doc['highlights'] = hit.get('highlight', {}).get('content', [])
                hits.append(doc)
            
            return hits
        
        except Exception as e:
            st.error(f"搜索课文失败 (GZLS): {e}")
            return []
    
    def search_events(self, query, start_year=None, end_year=None, size=20):
        """搜索历史事件 (GZLS)"""
        if not self.connected:
            return []
        
        try:
            # 构建搜索条件
            must_conditions = [
                {
                    "multi_match": {
                        "query": query,
                        "fields": ["name^3", "description^2"],
                        "fuzziness": "AUTO"
                    }
                }
            ]
            
            # 年份范围过滤
            filter_conditions = []
            if start_year is not None or end_year is not None:
                range_query = {"year": {}}
                if start_year is not None:
                    range_query["year"]["gte"] = start_year
                if end_year is not None:
                    range_query["year"]["lte"] = end_year
                filter_conditions.append({"range": range_query})
            
            search_body = {
                "query": {
                    "bool": {
                        "must": must_conditions,
                        "filter": filter_conditions
                    }
                },
                "sort": [
                    {"year": {"order": "asc"}}
                ],
                "size": size
            }
            
            result = self.es.search(
                index=ES_INDEX_EVENTS,
                body=search_body
            )
            
            hits = []
            for hit in result['hits']['hits']:
                doc = hit['_source']
                doc['score'] = hit['_score']
                hits.append(doc)
            
            return hits
        
        except Exception as e:
            st.error(f"搜索事件失败 (GZLS): {e}")
            return []
    
    def search_knowledge_points(self, query, category=None, size=20):
        """搜索知识点 (GZLS)"""
        if not self.connected:
            return []
        
        try:
            # 构建搜索条件
            must_conditions = [
                {
                    "multi_match": {
                        "query": query,
                        "fields": ["name^3", "description^2", "category"],
                        "fuzziness": "AUTO"
                    }
                }
            ]
            
            # 分类过滤
            if category:
                must_conditions.append({
                    "term": {"category": category}
                })
            
            search_body = {
                "query": {
                    "bool": {
                        "must": must_conditions
                    }
                },
                "highlight": {
                    "fields": {
                        "description": {
                            "fragment_size": 150,
                            "number_of_fragments": 2
                        }
                    }
                },
                "size": size
            }
            
            result = self.es.search(
                index=ES_INDEX_KNOWLEDGE,
                body=search_body
            )
            
            hits = []
            for hit in result['hits']['hits']:
                doc = hit['_source']
                doc['score'] = hit['_score']
                doc['highlights'] = hit.get('highlight', {}).get('description', [])
                hits.append(doc)
            
            return hits
        
        except Exception as e:
            st.error(f"搜索知识点失败 (GZLS): {e}")
            return []
    
    def get_index_stats(self):
        """获取索引统计信息 (GZLS)"""
        if not self.connected:
            return {}
        
        try:
            stats = {}
            
            for index in [ES_INDEX_LESSONS, ES_INDEX_EVENTS, ES_INDEX_KNOWLEDGE]:
                try:
                    count = self.es.count(index=index)['count']
                    stats[index] = count
                except:
                    stats[index] = 0
            
            return stats
        
        except Exception as e:
            st.error(f"获取统计信息失败 (GZLS): {e}")
            return {}
    
    def suggest_related_terms(self, query, field="name", size=5):
        """智能推荐相关搜索词 (GZLS)"""
        if not self.connected:
            return []
        
        try:
            search_body = {
                "suggest": {
                    "text": query,
                    "simple_phrase": {
                        "phrase": {
                            "field": field,
                            "size": size,
                            "gram_size": 2,
                            "direct_generator": [{
                                "field": field,
                                "suggest_mode": "always"
                            }]
                        }
                    }
                }
            }
            
            result = self.es.search(
                index=ES_INDEX_KNOWLEDGE,
                body=search_body
            )
            
            suggestions = []
            for option in result.get('suggest', {}).get('simple_phrase', [{}])[0].get('options', []):
                suggestions.append(option['text'])
            
            return suggestions
        
        except Exception as e:
            return []


def render_photo_search():
    """渲染GZLS智能搜索页面"""
    st.markdown("## 🔍 智能历史搜索 (GZLS)")
    st.markdown("**基于Elasticsearch的5本高中历史教科书全文搜索**")
    
    # 初始化搜索引擎
    if 'gzls_search' not in st.session_state:
        st.session_state.gzls_search = GZLSSearchEngine()
    
    search_engine = st.session_state.gzls_search
    
    if not search_engine.connected:
        st.error("❌ 搜索引擎未连接，请检查Elasticsearch配置")
        st.info("💡 运行 `scripts/import_to_elasticsearch.py` 导入数据")
        return
    
    # 显示索引统计
    stats = search_engine.get_index_stats()
    if stats:
        cols = st.columns(3)
        metrics = [
            ("📖 课文索引", stats.get(ES_INDEX_LESSONS, 0)),
            ("⚡ 事件索引", stats.get(ES_INDEX_EVENTS, 0)),
            ("💡 知识点索引", stats.get(ES_INDEX_KNOWLEDGE, 0))
        ]
        for col, (label, value) in zip(cols, metrics):
            col.metric(label, value)
    
    st.markdown("---")
    
    # Tab切换
    tab1, tab2, tab3 = st.tabs([
        "📖 搜索课文",
        "⚡ 搜索历史事件",
        "💡 搜索知识点"
    ])
    
    # Tab1: 搜索课文
    with tab1:
        render_lesson_search(search_engine)
    
    # Tab2: 搜索历史事件
    with tab2:
        render_event_search(search_engine)
    
    # Tab3: 搜索知识点
    with tab3:
        render_knowledge_search(search_engine)


def render_lesson_search(search_engine):
    """渲染课文搜索 (GZLS)"""
    st.markdown("### 📖 搜索课文内容")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        query = st.text_input(
            "输入搜索关键词",
            placeholder="例如：辛亥革命、改革开放、文艺复兴...",
            key="gzls_lesson_query"
        )
    
    with col2:
        textbook = st.selectbox(
            "教科书筛选",
            ["全部", "必修上", "必修下", "选择性必修1", "选择性必修2", "选择性必修3"],
            key="gzls_lesson_textbook"
        )
    
    if st.button("🔍 搜索课文", key="gzls_lesson_search_btn"):
        if query:
            textbook_filter = None if textbook == "全部" else textbook
            
            with st.spinner("搜索中..."):
                results = search_engine.search_lessons(query, textbook_filter)
                
                if results:
                    st.success(f"找到 {len(results)} 个相关课文")
                    
                    for idx, result in enumerate(results, 1):
                        with st.expander(f"{idx}. {result.get('title', '未命名')} (相关度: {result['score']:.2f})", expanded=(idx==1)):
                            st.markdown(f"**教科书:** {result.get('textbook_name', '未知')}")
                            st.markdown(f"**单元:** {result.get('unit_name', '未知')}")
                            
                            # 显示高亮片段
                            if result.get('highlights'):
                                st.markdown("**相关内容片段:**")
                                for highlight in result['highlights']:
                                    st.markdown(f"> {highlight}")
                            
                            # 显示完整内容（可选）
                            if result.get('content'):
                                with st.expander("查看完整内容"):
                                    st.markdown(result['content'])
                else:
                    st.warning("未找到相关课文")
        else:
            st.warning("请输入搜索关键词")


def render_event_search(search_engine):
    """渲染历史事件搜索 (GZLS)"""
    st.markdown("### ⚡ 搜索历史事件")
    
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        query = st.text_input(
            "输入事件关键词",
            placeholder="例如：鸦片战争、五四运动、工业革命...",
            key="gzls_event_query"
        )
    
    with col2:
        start_year = st.number_input(
            "起始年份",
            value=None,
            step=100,
            key="gzls_event_start_year",
            format="%d"
        )
    
    with col3:
        end_year = st.number_input(
            "结束年份",
            value=None,
            step=100,
            key="gzls_event_end_year",
            format="%d"
        )
    
    if st.button("🔍 搜索事件", key="gzls_event_search_btn"):
        if query:
            with st.spinner("搜索中..."):
                results = search_engine.search_events(query, start_year, end_year)
                
                if results:
                    st.success(f"找到 {len(results)} 个相关事件")
                    
                    for idx, result in enumerate(results, 1):
                        year_display = f"{abs(result.get('year', 0))}年{'前' if result.get('year', 0) < 0 else ''}"
                        
                        col_year, col_content = st.columns([1, 4])
                        
                        with col_year:
                            st.markdown(f"### {year_display}")
                            st.caption(f"相关度: {result['score']:.2f}")
                        
                        with col_content:
                            st.markdown(f"**{result.get('name', '未命名')}**")
                            
                            if result.get('description'):
                                st.markdown(result['description'])
                            
                            if result.get('textbook_name'):
                                st.caption(f"📚 来源: {result['textbook_name']} - {result.get('lesson_name', '')}")
                        
                        st.markdown("---")
                else:
                    st.warning("未找到相关事件")
        else:
            st.warning("请输入搜索关键词")


def render_knowledge_search(search_engine):
    """渲染知识点搜索 (GZLS)"""
    st.markdown("### 💡 搜索知识点")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        query = st.text_input(
            "输入知识点关键词",
            placeholder="例如：科举制度、经济政策、文化交流...",
            key="gzls_knowledge_query"
        )
    
    with col2:
        category = st.selectbox(
            "知识分类",
            ["全部", "政治", "经济", "文化", "军事", "社会"],
            key="gzls_knowledge_category"
        )
    
    if st.button("🔍 搜索知识点", key="gzls_knowledge_search_btn"):
        if query:
            category_filter = None if category == "全部" else category
            
            with st.spinner("搜索中..."):
                results = search_engine.search_knowledge_points(query, category_filter)
                
                if results:
                    st.success(f"找到 {len(results)} 个相关知识点")
                    
                    for idx, result in enumerate(results, 1):
                        with st.expander(
                            f"{idx}. {result.get('name', '未命名')} - {result.get('category', '未分类')} (相关度: {result['score']:.2f})",
                            expanded=(idx==1)
                        ):
                            if result.get('description'):
                                st.markdown(result['description'])
                            
                            # 显示高亮片段
                            if result.get('highlights'):
                                st.markdown("**相关描述:**")
                                for highlight in result['highlights']:
                                    st.markdown(f"> {highlight}")
                            
                            if result.get('textbook_name'):
                                st.caption(f"📚 来源: {result['textbook_name']}")
                else:
                    st.warning("未找到相关知识点")
        else:
            st.warning("请输入搜索关键词")


if __name__ == "__main__":
    render_photo_search()

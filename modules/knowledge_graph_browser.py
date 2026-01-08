"""
历史知识图谱浏览器 - 3级节点结构，支持按课本和按专题两种模式
"""

import streamlit as st
import json
from pathlib import Path
from pyvis.network import Network
import streamlit.components.v1 as components
import tempfile
import os
import re


def extract_event_name(description, year=None):
    """从事件描述中智能提取事件名称"""
    if not description:
        return "历史事件"
    
    # 去除年份数字
    desc = re.sub(r'\d{1,4}年', '', description)
    desc = re.sub(r'公元前?\d+年', '', desc)
    
    # 提取第一个句子（以句号、问号、感叹号分割）
    sentences = re.split(r'[。！？\n]', desc)
    first_sentence = sentences[0].strip() if sentences else desc
    
    # 如果第一句太长，截取前30字
    if len(first_sentence) > 30:
        # 尝试提取关键部分（去除"在...""于..."等前缀）
        first_sentence = re.sub(r'^(在|于|当|到|自)\S{1,10}[，,]', '', first_sentence)
        first_sentence = first_sentence[:30].strip()
    
    # 如果太短，保留原始描述前25字
    if len(first_sentence) < 5:
        first_sentence = description[:25]
    
    return first_sentence.strip() or "历史事件"


class KnowledgeGraphBrowser:
    """知识图谱浏览器"""
    
    def __init__(self):
        self.data_dir = Path(__file__).parent.parent / "data" / "parsed"
        self.load_data()
        
        # 定义专题（基于5本教材的核心主题）
        self.topics = {
            "中央集权制度": {
                "description": "从秦朝到清朝中央集权制度的演变",
                "keywords": ["中央集权", "皇权", "郡县制", "三省六部", "军机处", "内阁", "秦始皇", "汉武帝"],
                "periods": ["古代", "近代"]
            },
            "改革与变法": {
                "description": "历代重大改革与变法运动",
                "keywords": ["商鞅变法", "王安石变法", "戊戌变法", "明治维新", "改革开放", "变法", "改革"],
                "periods": ["古代", "近代", "现代"]
            },
            "民族关系": {
                "description": "中国历史上的民族交流与融合",
                "keywords": ["民族", "汉族", "少数民族", "和亲", "文成公主", "昭君出塞", "胡汉融合"],
                "periods": ["古代", "近代", "现代"]
            },
            "对外交流": {
                "description": "中外文化交流与传播",
                "keywords": ["丝绸之路", "郑和下西洋", "遣唐使", "文化交流", "传播", "马可波罗"],
                "periods": ["古代", "近代"]
            },
            "近代侵略与抗争": {
                "description": "近代中国遭受侵略与民族抗争",
                "keywords": ["鸦片战争", "甲午战争", "八国联军", "抗日战争", "不平等条约", "侵略", "抗争"],
                "periods": ["近代"]
            },
            "革命运动": {
                "description": "近现代革命运动",
                "keywords": ["辛亥革命", "五四运动", "国民革命", "土地革命", "新民主主义革命", "孙中山", "毛泽东"],
                "periods": ["近代", "现代"]
            },
            "新中国建设": {
                "description": "新中国成立后的建设与发展",
                "keywords": ["新中国", "社会主义", "改革开放", "经济建设", "一五计划", "大跃进", "人民公社"],
                "periods": ["现代"]
            },
            "经济发展": {
                "description": "中国经济制度与发展历程",
                "keywords": ["经济", "农业", "手工业", "商业", "工业", "市场经济", "土地制度"],
                "periods": ["古代", "近代", "现代"]
            },
            "思想文化": {
                "description": "中国思想文化发展",
                "keywords": ["儒家", "道家", "佛教", "理学", "心学", "新文化运动", "孔子", "老子"],
                "periods": ["古代", "近代", "现代"]
            },
            "科技成就": {
                "description": "中国历代科技发明与成就",
                "keywords": ["四大发明", "造纸术", "印刷术", "火药", "指南针", "科技", "发明"],
                "periods": ["古代", "近代", "现代"]
            }
        }
    
    def load_data(self):
        """加载数据"""
        try:
            self.books = self._load_json("books.json") or []
            self.units = self._load_json("units.json") or []
            self.lessons = self._load_json("lessons.json") or []
            self.events = self._load_json("historical_events.json") or []
            self.figures = self._load_json("historical_figures.json") or []
            self.connected = True
        except Exception as e:
            st.error(f"❌ 数据加载失败: {e}")
            self.connected = False
            self.books = []
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
    
    def get_books(self):
        """获取所有教科书"""
        if self.books:
            return self.books
        # 从units中提取不同的book
        books_dict = {}
        for unit in self.units:
            book_id = unit.get('book_id')
            book_name = unit.get('book_name')
            if book_id and book_id not in books_dict:
                books_dict[book_id] = {
                    'id': book_id,
                    'name': book_name,
                    'type': '必修' if '必修' in book_name else '选择性必修'
                }
        return list(books_dict.values())
    
    def get_units_by_book(self, book_id):
        """获取指定教科书的所有单元"""
        units = [u for u in self.units if u.get('book_id') == book_id]
        units.sort(key=lambda x: x.get('order', 999))
        return units
    
    def get_lessons_by_unit(self, unit_id):
        """获取指定单元的所有课文"""
        lessons = [l for l in self.lessons if l.get('unit_id') == unit_id]
        lessons.sort(key=lambda x: x.get('order', 999))
        return lessons
    
    def get_events_by_lesson(self, lesson_id):
        """获取指定课文的所有事件"""
        return [e for e in self.events if e.get('lesson_id') == lesson_id]
    
    def get_figures_by_lesson(self, lesson_id):
        """获取指定课文的所有人物"""
        return [f for f in self.figures if f.get('lesson_id') == lesson_id]
    
    def search_by_topic(self, topic_name):
        """根据专题搜索相关内容"""
        topic_info = self.topics.get(topic_name, {})
        keywords = topic_info.get('keywords', [])
        
        if not keywords:
            return {'lessons': [], 'events': [], 'figures': []}
        
        matched_lessons = []
        matched_events = []
        matched_figures = []
        
        # 搜索课文
        for lesson in self.lessons:
            title = lesson.get('title', '').lower()
            content = lesson.get('content', '').lower()
            if any(kw.lower() in title or kw.lower() in content for kw in keywords):
                matched_lessons.append(lesson)
        
        # 搜索事件
        for event in self.events:
            desc = event.get('description', '').lower()
            if any(kw.lower() in desc for kw in keywords):
                matched_events.append(event)
        
        # 搜索人物
        for figure in self.figures:
            name = figure.get('name', '').lower()
            desc = figure.get('description', '').lower()
            if any(kw.lower() in name or kw.lower() in desc for kw in keywords):
                matched_figures.append(figure)
        
        return {
            'lessons': matched_lessons[:15],
            'events': matched_events[:20],
            'figures': matched_figures[:15]
        }
    
    def create_textbook_graph(self, book_id, unit_id=None, lesson_id=None):
        """创建按课本顺序的知识图谱（显示所有课程和知识点，内容丰富）"""
        net = Network(height="800px", width="100%", bgcolor="#ffffff", font_color="#333")
        
        net.barnes_hut(gravity=-2000, central_gravity=0.2, spring_length=180, damping=0.6)
        
        # 第1级：选中的教科书（中心节点）
        book = next((b for b in self.get_books() if b['id'] == book_id), None)
        if not book:
            return net
        
        # 如果选择了单元，只显示该单元
        if unit_id:
            unit = next((u for u in self.units if u.get('id') == unit_id), None)
            if not unit:
                return net
            
            # 中心节点：单元
            net.add_node(
                "center",
                label=f"📂 {unit.get('title', '')[:20]}",
                color="#FF6B6B",
                size=55,
                title=f"单元：{unit.get('title')}\n教材：{book['name']}",
                font={"size": 24, "bold": True}
            )
            
            # 显示该单元的所有课程
            lessons = self.get_lessons_by_unit(unit_id)
            for lesson in lessons:  # 显示所有课程
                lesson_id_str = f"lesson_{lesson.get('id')}"
                net.add_node(
                    lesson_id_str,
                    label=f"📖 {lesson.get('title', '')[:15]}",
                    color="#4ECDC4",
                    size=38,
                    title=f"课程：{lesson.get('title')}\n{lesson.get('content', '')[:100]}...",
                    font={"size": 16}
                )
                net.add_edge("center", lesson_id_str, color="#4ECDC4", width=2.5, smooth=False)
                
                # 该课程的所有事件（显示更多）
                events = self.get_events_by_lesson(lesson.get('id'))
                for i, event in enumerate(events[:8]):  # 每课最多8个事件
                    event_id_str = f"event_{lesson.get('id')}_{i}"
                    event_desc = event.get('description', '')
                    event_year = event.get('year', '')
                    # 使用智能提取函数获取事件名称
                    event_name = extract_event_name(event_desc, event_year)
                    event_label = event_name[:15] if len(event_name) > 15 else event_name
                    net.add_node(
                        event_id_str,
                        label=f"⚡ {event_label}",
                        color="#FFA07A",
                        size=24,
                        title=f"事件：{event_name}\n年份：{event_year}年\n详情：{event_desc}",
                        font={"size": 13}
                    )
                    net.add_edge(lesson_id_str, event_id_str, color="#ccc", width=1.5, smooth=False)
                
                # 该课程的所有人物（显示更多）
                figures = self.get_figures_by_lesson(lesson.get('id'))
                for i, figure in enumerate(figures[:5]):  # 每课最多5个人物
                    figure_id_str = f"figure_{lesson.get('id')}_{i}"
                    net.add_node(
                        figure_id_str,
                        label=f"👤 {figure.get('name', '')[:8]}",
                        color="#96CEB4",
                        size=22,
                        title=f"人物：{figure.get('name')}\n{figure.get('description', '')[:50]}...",
                        font={"size": 12}
                    )
                    net.add_edge(lesson_id_str, figure_id_str, color="#ccc", width=1.5, smooth=False)
        
        else:
            # 未选择单元，显示教材的所有单元
            net.add_node(
                "center",
                label=f"📚 {book['name'][:18]}",
                color="#FF6B6B",
                size=60,
                title=f"教科书：{book['name']}",
                font={"size": 26, "bold": True}
            )
            
            # 显示所有单元
            units = self.get_units_by_book(book_id)
            for unit in units:  # 显示所有单元
                unit_id_str = f"unit_{unit.get('id')}"
                net.add_node(
                    unit_id_str,
                    label=f"📂 {unit.get('title', '')[:15]}",
                    color="#4ECDC4",
                    size=42,
                    title=f"单元：{unit.get('title')}\n{unit.get('description', '')}",
                    font={"size": 18, "bold": True}
                )
                net.add_edge("center", unit_id_str, color="#4ECDC4", width=3, smooth=False)
                
                # 该单元的部分课程
                lessons = self.get_lessons_by_unit(unit.get('id'))
                for lesson in lessons[:4]:  # 每单元显示前4课
                    lesson_id_str = f"lesson_{unit.get('id')}_{lesson.get('id')}"
                    net.add_node(
                        lesson_id_str,
                        label=f"📖 {lesson.get('title', '')[:12]}",
                        color="#45B7D1",
                        size=30,
                        title=f"课程：{lesson.get('title')}",
                        font={"size": 14}
                    )
                    net.add_edge(unit_id_str, lesson_id_str, color="#999", width=2, smooth=False)
        
        # 配置交互选项（参考xjygraph.py）
        net.set_options("""
        {
            "nodes": {
                "font": {
                    "size": 20,
                    "face": "Microsoft YaHei, SimHei, sans-serif"
                }
            },
            "edges": {
                "smooth": false,
                "width": 1,
                "color": "#999999"
            },
            "interaction": {
                "hover": true,
                "navigationButtons": false,
                "keyboard": true,
                "dragNodes": true,
                "dragView": true,
                "zoomView": true
            },
            "physics": {
                "enabled": true,
                "barnesHut": {
                    "gravitationalConstant": -8000,
                    "centralGravity": 0.1,
                    "springLength": 300,
                    "springConstant": 0.01,
                    "avoidOverlap": 1
                },
                "stabilization": {
                    "enabled": true,
                    "iterations": 300,
                    "fit": true
                }
            }
        }
        """)
        
        return net
    
    def create_topic_graph(self, topic_name):
        """创建按专题的知识图谱（网状结构，避免重叠）"""
        net = Network(height="900px", width="100%", bgcolor="#ffffff", font_color="#333333")
        
        # 参考xjygraph.py的布局参数，防止节点重叠
        net.barnes_hut(
            gravity=-3000,
            central_gravity=0.3,
            spring_length=200
        )
        
        # 第1层：中心专题节点（参考原文件尺寸）
        topic_info = self.topics.get(topic_name, {})
        net.add_node(
            "topic",
            label=f"🎯 {topic_name}",
            color="#FF6B6B",
            size=70,
            font={"size": 160, "bold": True, "color": "#222222", "face": "Microsoft YaHei, SimHei, sans-serif"},
            borderWidth=3,
            borderWidthSelected=5
        )
        
        # 搜索相关内容
        results = self.search_by_topic(topic_name)
        
        # 第2层：大类别节点（课文、事件、人物）
        categories = []
        if results['lessons']:
            categories.append(('lessons', '📚 相关课文', '#4ECDC4', results['lessons']))
        if results['events']:
            categories.append(('events', '⚡ 相关事件', '#FFA07A', results['events']))
        if results['figures']:
            categories.append(('figures', '👤 相关人物', '#96CEB4', results['figures']))
        
        for cat_id, cat_label, cat_color, items in categories:
            cat_node_id = f"cat_{cat_id}"
            # 第2层类别节点
            net.add_node(
                cat_node_id,
                label=f"{cat_label}\n({len(items)}项)",
                color=cat_color,
                size=55,
                font={"size": 140, "bold": True, "color": "#222222", "face": "Microsoft YaHei, SimHei, sans-serif"},
                borderWidth=2,
                borderWidthSelected=5
            )
            # 中心到类别的连线（带箭头）
            net.add_edge("topic", cat_node_id, 
                        color="#999999", 
                        width=2, 
                        smooth=False,
                        arrows={"to": {"enabled": True, "scaleFactor": 0.5}})
            
            # 第3层：具体知识点（显示所有）
            for i, item in enumerate(items):
                item_id = f"{cat_id}_{i}"
                
                if cat_id == 'lessons':
                    label = f"📖 {item.get('title', '')[:10]}"
                    size = 30
                    item['_type'] = 'lesson'
                elif cat_id == 'events':
                    desc = item.get('description', '')
                    event_year = item.get('year', '')
                    event_name = extract_event_name(desc, event_year)
                    label = f"{event_name[:12]}"
                    size = 28
                    item['_type'] = 'event'
                    item['_year'] = event_year
                else:  # figures
                    label = f"{item.get('name', '')[:8]}"
                    size = 26
                    item['_type'] = 'figure'
                
                # 第3层知识点节点（参考原文件字体大小）
                net.add_node(
                    item_id,
                    label=label,
                    color=cat_color,
                    size=size,
                    font={"size": 120, "bold": True, "color": "#222222", "face": "Microsoft YaHei, SimHei, sans-serif"},
                    borderWidth=2,
                    borderWidthSelected=4
                )
                # 类别到知识点的连线（带箭头）
                net.add_edge(cat_node_id, item_id, 
                           color="#999999", 
                           width=1, 
                           smooth=False,
                           arrows={"to": {"enabled": True, "scaleFactor": 0.3}})
        
        # 添加横向关联：相同年份的事件之间建立连接
        events_by_year = {}
        for cat_id, cat_label, cat_color, items in categories:
            if cat_id == 'events':
                for i, item in enumerate(items):
                    year = item.get('year', '')
                    if year and year != '未知':
                        if year not in events_by_year:
                            events_by_year[year] = []
                        events_by_year[year].append(f"events_{i}")
        
        # 同年事件之间添加虚线连接
        for year, event_ids in events_by_year.items():
            if len(event_ids) > 1:
                for i in range(len(event_ids) - 1):
                    net.add_edge(
                        event_ids[i], 
                        event_ids[i+1],
                        color="#cccccc",
                        width=0.5,
                        dashes=True,
                        smooth=False,
                        arrows={"to": {"enabled": False}}
                    )
        
        net.set_options("""
        {
            "nodes": {
                "font": {
                    "size": 20,
                    "face": "Microsoft YaHei, SimHei, sans-serif"
                }
            },
            "edges": {
                "smooth": false,
                "width": 1,
                "color": "#999999"
            },
            "interaction": {
                "hover": true,
                "navigationButtons": false,
                "keyboard": true,
                "dragNodes": true,
                "dragView": true,
                "zoomView": true
            },
            "physics": {
                "enabled": true,
                "barnesHut": {
                    "gravitationalConstant": -8000,
                    "centralGravity": 0.1,
                    "springLength": 300,
                    "springConstant": 0.01,
                    "avoidOverlap": 1
                },
                "stabilization": {
                    "enabled": true,
                    "iterations": 300,
                    "fit": true
                }
            }
        }
        """)
        
        return net


def render_knowledge_graph():
    """渲染知识图谱浏览器"""
    st.markdown("## 🗺️ 历史知识图谱")
    st.markdown("**3级结构 • 支持按课本顺序和按专题浏览**")
    
    # 初始化
    if 'kg_browser' not in st.session_state:
        st.session_state.kg_browser = KnowledgeGraphBrowser()
    
    browser = st.session_state.kg_browser
    
    if not browser.connected:
        st.error("❌ 数据未加载")
        return
    
    # 显示统计
    cols = st.columns(5)
    cols[0].metric("📚 教科书", len(browser.get_books()))
    cols[1].metric("📂 单元", len(browser.units))
    cols[2].metric("📖 课文", len(browser.lessons))
    cols[3].metric("⚡ 事件", len(browser.events))
    cols[4].metric("👤 人物", len(browser.figures))
    
    st.markdown("---")
    
    # 只保留专题浏览模式
    render_topic_mode(browser)


def render_textbook_mode(browser):
    """渲染按课本顺序模式"""
    st.markdown("### 📚 按课本顺序浏览")
    st.info("💡 先选择教科书和单元，展示完整的知识图谱（课程 + 事件 + 人物）")
    
    # 第一步：选择教科书
    books = browser.get_books()
    book_names = [b['name'] for b in books]
    selected_book_name = st.selectbox(
        "**📚 第1步：选择教科书**",
        book_names,
        key="kg_book_select"
    )
    
    selected_book = next((b for b in books if b['name'] == selected_book_name), None)
    if not selected_book:
        return
    
    # 第二步：选择单元（必选）
    units = browser.get_units_by_book(selected_book['id'])
    if not units:
        st.warning("该教材暂无单元数据")
        return
    
    unit_options = [f"{u.get('title', '')}" for u in units]
    selected_unit_name = st.selectbox(
        "**📂 第2步：选择单元章节**",
        unit_options,
        key="kg_unit_select"
    )
    
    unit_id = next((u['id'] for u in units if u.get('title') == selected_unit_name), None)
    
    if not unit_id:
        st.warning("请选择单元")
        return
    
    # 统计该单元的内容
    lessons = browser.get_lessons_by_unit(unit_id)
    total_events = sum(len(browser.get_events_by_lesson(l.get('id'))) for l in lessons)
    total_figures = sum(len(browser.get_figures_by_lesson(l.get('id'))) for l in lessons)
    
    col1, col2, col3 = st.columns(3)
    col1.metric("📖 课程", len(lessons))
    col2.metric("⚡ 事件", total_events)
    col3.metric("👤 人物", total_figures)
    
    st.markdown("---")
    
    # 生成图谱
    if st.button("🗺️ 生成知识图谱", type="primary", key="kg_textbook_generate", use_container_width=True):
        with st.spinner("正在生成知识图谱..."):
            net = browser.create_textbook_graph(selected_book['id'], unit_id)
            
            # 准备节点数据
            nodes_data = {}
            for lesson in lessons:
                lesson_id = f"lesson_{lesson.get('id')}"
                nodes_data[lesson_id] = {
                    "type": "课程",
                    "title": lesson.get('title', ''),
                    "book_name": lesson.get('book_name', ''),
                    "content": lesson.get('content', '')
                }
                
                # 事件数据
                events = browser.get_events_by_lesson(lesson.get('id'))
                for i, event in enumerate(events[:8]):
                    event_id = f"event_{lesson.get('id')}_{i}"
                    event_desc = event.get('description', '')
                    event_year = event.get('year', '未知')
                    event_name = extract_event_name(event_desc, event_year)
                    nodes_data[event_id] = {
                        "type": "事件",
                        "name": event_name,
                        "year": event_year,
                        "description": event_desc
                    }
                
                # 人物数据
                figures = browser.get_figures_by_lesson(lesson.get('id'))
                for i, figure in enumerate(figures[:5]):
                    figure_id = f"figure_{lesson.get('id')}_{i}"
                    nodes_data[figure_id] = {
                        "type": "人物",
                        "name": figure.get('name', ''),
                        "description": figure.get('description', '')
                    }
            
            # 保存并显示
            with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.html', encoding='utf-8') as f:
                net.save_graph(f.name)
                graph_path = f.name
            
            with open(graph_path, 'r', encoding='utf-8') as f:
                html_content = f.read()
            
            # 注入点击事件处理
            import json
            nodes_json = json.dumps(nodes_data, ensure_ascii=False)
            
            click_handler = f"""
            <style>
            html, body {{
                height: 100%;
                overflow: hidden;
            }}
            #node-detail-panel {{
                position: absolute;
                top: 20px;
                right: 20px;
                width: 400px;
                height: 600px;
                background: rgba(255,255,255,0.98);
                padding: 20px;
                z-index: 9999;
                overflow-y: scroll !important;
                overflow-x: hidden;
                display: none;
                font-family: 'Microsoft YaHei', sans-serif;
                box-shadow: 0 4px 20px rgba(0,0,0,0.15);
                border-radius: 12px;
                border: 2px solid #4ECDC4;
            }}
            #node-detail-panel::-webkit-scrollbar {{
                width: 10px;
            }}
            #node-detail-panel::-webkit-scrollbar-track {{
                background: #f1f1f1;
                border-radius: 5px;
            }}
            #node-detail-panel::-webkit-scrollbar-thumb {{
                background: #4ECDC4;
                border-radius: 5px;
            }}
            #node-detail-panel::-webkit-scrollbar-thumb:hover {{
                background: #45B7D1;
            }}
            #node-detail-panel h3 {{
                margin: 0 0 15px 0;
                color: #1f77b4;
                font-size: 22px;
                padding-bottom: 12px;
                border-bottom: 3px solid #4ECDC4;
            }}
            #node-detail-panel .detail-row {{
                margin: 15px 0;
                font-size: 15px;
                line-height: 1.8;
            }}
            #node-detail-panel .detail-label {{
                font-weight: bold;
                color: #333;
                display: block;
                margin-bottom: 5px;
            }}
            #node-detail-panel .detail-value {{
                color: #555;
            }}
            #node-detail-panel .close-btn {{
                position: absolute;
                top: 15px;
                right: 20px;
                cursor: pointer;
                font-size: 28px;
                color: #999;
                font-weight: bold;
                transition: color 0.3s;
            }}
            #node-detail-panel .close-btn:hover {{
                color: #333;
            }}
            #node-detail-panel .type-badge {{
                display: inline-block;
                padding: 4px 12px;
                border-radius: 12px;
                font-size: 13px;
                font-weight: bold;
                margin-bottom: 10px;
            }}
            </style>
            
            <div id="node-detail-panel">
                <span class="close-btn" onclick="closeDetailPanel()">✕</span>
                <div id="detail-content"></div>
            </div>
            
            <script>
            var nodesData = {nodes_json};
            var networkRef = null;
            var originalColors = {{nodes: {{}}, edges: {{}}}};
            
            function closeDetailPanel() {{
                document.getElementById('node-detail-panel').style.display = 'none';
                if (networkRef) {{
                    restoreAllColors();
                }}
            }}
            
            function restoreAllColors() {{
                if (!networkRef) return;
                var nodeUpdates = [];
                var edgeUpdates = [];
                
                // 恢复节点颜色
                for (var nodeId in originalColors.nodes) {{
                    nodeUpdates.push({{id: nodeId, color: originalColors.nodes[nodeId], font: {{color: '#222222'}}}});
                }}
                // 恢复边颜色
                for (var edgeId in originalColors.edges) {{
                    edgeUpdates.push({{id: edgeId, color: originalColors.edges[edgeId]}});
                }}
                
                if (nodeUpdates.length > 0) {{
                    networkRef.body.data.nodes.update(nodeUpdates);
                }}
                if (edgeUpdates.length > 0) {{
                    networkRef.body.data.edges.update(edgeUpdates);
                }}
                originalColors = {{nodes: {{}}, edges: {{}}}};
            }}
            
            function highlightConnected(clickedNodeId) {{
                if (!networkRef) return;
                
                // 先恢复之前的颜色
                restoreAllColors();
                
                // 找出关联的节点和边
                var connectedNodes = new Set([clickedNodeId]);
                var connectedEdgeIds = new Set();
                
                var allEdges = networkRef.body.data.edges.get();
                allEdges.forEach(function(edge) {{
                    if (edge.from === clickedNodeId || edge.to === clickedNodeId) {{
                        connectedNodes.add(edge.from);
                        connectedNodes.add(edge.to);
                        connectedEdgeIds.add(edge.id);
                    }}
                }});
                
                // 保存原始颜色并设置新颜色
                var allNodes = networkRef.body.data.nodes.get();
                var nodeUpdates = [];
                var edgeUpdates = [];
                
                originalColors = {{nodes: {{}}, edges: {{}}}};
                
                allNodes.forEach(function(node) {{
                    originalColors.nodes[node.id] = node.color;
                    if (connectedNodes.has(node.id)) {{
                        // 关联节点保持原色
                        nodeUpdates.push({{id: node.id, font: {{color: '#222222'}}}});
                    }} else {{
                        // 非关联节点变灰
                        nodeUpdates.push({{id: node.id, color: '#dddddd', font: {{color: '#bbbbbb'}}}});
                    }}
                }});
                
                allEdges.forEach(function(edge) {{
                    originalColors.edges[edge.id] = edge.color;
                    if (connectedEdgeIds.has(edge.id)) {{
                        // 关联边高亮
                        edgeUpdates.push({{id: edge.id, color: '#FF6B6B', width: 4}});
                    }} else {{
                        // 非关联边变灰
                        edgeUpdates.push({{id: edge.id, color: '#eeeeee'}});
                    }}
                }});
                
                networkRef.body.data.nodes.update(nodeUpdates);
                networkRef.body.data.edges.update(edgeUpdates);
            }}
            
            window.onload = function() {{
                var attempts = 0;
                var maxAttempts = 20;
                
                function tryBindEvents() {{
                    attempts++;
                    var networkObj = null;
                    
                    if (typeof network !== 'undefined') {{
                        networkObj = network;
                    }} else if (typeof window.network !== 'undefined') {{
                        networkObj = window.network;
                    }}
                    
                    if (networkObj) {{
                        networkRef = networkObj;
                        
                        networkObj.on('stabilized', function() {{
                            networkObj.setOptions({{physics: {{enabled: false}}}});
                        }});
                        
                        networkObj.on('click', function(params) {{
                            if (params.nodes && params.nodes.length > 0) {{
                                var nodeId = params.nodes[0];
                                if (nodeId !== 'center') {{
                                    var node = nodesData[nodeId];
                                    if (node) {{
                                        showNodeDetail(node);
                                    }}
                                }}
                            }} else {{
                                closeDetailPanel();
                            }}
                        }});
                    }} else if (attempts < maxAttempts) {{
                        setTimeout(tryBindEvents, 300);
                    }}
                }}
                
                function showNodeDetail(node) {{
                    var panel = document.getElementById('node-detail-panel');
                    var content = document.getElementById('detail-content');
                    
                    var typeColors = {{
                        "课程": "#4ECDC4",
                        "事件": "#FFA07A",
                        "人物": "#96CEB4"
                    }};
                    var bgColor = typeColors[node.type] || "#999";
                    
                    var html = '<span class="type-badge" style="background:' + bgColor + ';color:white;">' + node.type + '</span>';
                    
                    if (node.type === "课程") {{
                        html += '<h3>' + (node.title || '课程') + '</h3>';
                        if (node.book_name) html += '<div class="detail-row"><span class="detail-label">📚 教材：</span><span class="detail-value">' + node.book_name + '</span></div>';
                        if (node.content) html += '<div class="detail-row"><span class="detail-label">📝 内容：</span><span class="detail-value">' + node.content + '</span></div>';
                    }} else if (node.type === "事件") {{
                        html += '<h3>⚡ ' + (node.name || '历史事件') + '</h3>';
                        if (node.year) {{
                            var yearText = String(node.year);
                            if (!yearText.includes('年')) yearText += '年';
                            html += '<div class="detail-row"><span class="detail-label">⏰ 时间：</span><span class="detail-value">' + yearText + '</span></div>';
                        }}
                        if (node.description) html += '<div class="detail-row"><span class="detail-label">💡 描述：</span><span class="detail-value">' + node.description + '</span></div>';
                    }} else if (node.type === "人物") {{
                        html += '<h3>👤 ' + (node.name || '历史人物') + '</h3>';
                        if (node.description) html += '<div class="detail-row"><span class="detail-label">📝 简介：</span><span class="detail-value">' + node.description + '</span></div>';
                    }}
                    
                    content.innerHTML = html;
                    panel.style.display = 'block';
                }}
                
                setTimeout(tryBindEvents, 500);
            }};
            </script>
            """
            
            html_content = html_content.replace("</body>", click_handler + "</body>")
            
            st.markdown("#### 📊 知识图谱可视化")
            st.caption("💡 拖动节点调整位置 • 滚轮缩放 • **点击节点查看详细信息卡片**")
            components.html(html_content, height=850, scrolling=False)
            
            try:
                os.unlink(graph_path)
            except:
                pass


def render_topic_mode(browser):
    """渲染按专题模式"""
    st.markdown("### 🎯 按专题浏览")
    st.info("💡 选择专题，展示跨教材的相关知识点（课文 + 事件 + 人物）")
    
    # 专题下拉选择
    topics = list(browser.topics.keys())
    selected_topic = st.selectbox(
        "**🎯 选择专题**",
        topics,
        key="kg_topic_select"
    )
    
    if selected_topic:
        topic_info = browser.topics[selected_topic]
        st.markdown(f"**专题描述：** {topic_info['description']}")
        
        # 预览统计
        results = browser.search_by_topic(selected_topic)
        col1, col2, col3 = st.columns(3)
        col1.metric("📖 相关课文", len(results['lessons']))
        col2.metric("⚡ 相关事件", len(results['events']))
        col3.metric("👤 相关人物", len(results['figures']))
        
        st.markdown("---")
        
        # 生成专题图谱
        if st.button("🗺️ 生成专题图谱", type="primary", key="kg_topic_generate", use_container_width=True):
            with st.spinner("正在生成专题知识图谱..."):
                net = browser.create_topic_graph(selected_topic)
                
                # 准备节点数据
                nodes_data = {}
                for i, lesson in enumerate(results['lessons']):
                    lesson_id = f"lessons_{i}"
                    nodes_data[lesson_id] = {
                        "type": "课程",
                        "title": lesson.get('title', ''),
                        "book_name": lesson.get('book_name', ''),
                        "content": lesson.get('content', '')
                    }
                
                for i, event in enumerate(results['events']):
                    event_id = f"events_{i}"
                    event_desc = event.get('description', '')
                    event_year = event.get('year', '未知')
                    event_name = extract_event_name(event_desc, event_year)
                    nodes_data[event_id] = {
                        "type": "事件",
                        "name": event_name,
                        "year": event_year,
                        "description": event_desc
                    }
                
                for i, figure in enumerate(results['figures']):
                    figure_id = f"figures_{i}"
                    nodes_data[figure_id] = {
                        "type": "人物",
                        "name": figure.get('name', ''),
                        "description": figure.get('description', '')
                    }
                
                # 保存并显示
                with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.html', encoding='utf-8') as f:
                    net.save_graph(f.name)
                    graph_path = f.name
                
                with open(graph_path, 'r', encoding='utf-8') as f:
                    html_content = f.read()
                
                # 注入点击事件处理
                import json
                nodes_json = json.dumps(nodes_data, ensure_ascii=False)
                
                click_handler = f"""
                <style>
                html, body {{
                    height: 100%;
                    overflow: hidden;
                }}
                #node-detail-panel {{
                    position: absolute;
                    top: 20px;
                    right: 20px;
                    width: 400px;
                    height: 600px;
                    background: rgba(255,255,255,0.98);
                    padding: 20px;
                    z-index: 9999;
                    overflow-y: scroll !important;
                    overflow-x: hidden;
                    display: none;
                    font-family: 'Microsoft YaHei', sans-serif;
                    box-shadow: 0 4px 20px rgba(0,0,0,0.15);
                    border-radius: 12px;
                    border: 2px solid #4ECDC4;
                }}
                #node-detail-panel::-webkit-scrollbar {{
                    width: 10px;
                }}
                #node-detail-panel::-webkit-scrollbar-track {{
                    background: #f1f1f1;
                    border-radius: 5px;
                }}
                #node-detail-panel::-webkit-scrollbar-thumb {{
                    background: #FFA07A;
                    border-radius: 5px;
                }}
                #node-detail-panel::-webkit-scrollbar-thumb:hover {{
                    background: #FF6B6B;
                }}
                #node-detail-panel h3 {{
                    margin: 0 0 15px 0;
                    color: #1f77b4;
                    font-size: 22px;
                    padding-bottom: 12px;
                    border-bottom: 3px solid #4ECDC4;
                }}
                #node-detail-panel .detail-row {{
                    margin: 15px 0;
                    font-size: 15px;
                    line-height: 1.8;
                }}
                #node-detail-panel .detail-label {{
                    font-weight: bold;
                    color: #333;
                    display: block;
                    margin-bottom: 5px;
                }}
                #node-detail-panel .detail-value {{
                    color: #555;
                }}
                #node-detail-panel .close-btn {{
                    position: absolute;
                    top: 15px;
                    right: 20px;
                    cursor: pointer;
                    font-size: 28px;
                    color: #999;
                    font-weight: bold;
                    transition: color 0.3s;
                }}
                #node-detail-panel .close-btn:hover {{
                    color: #333;
                }}
                #node-detail-panel .type-badge {{
                    display: inline-block;
                    padding: 4px 12px;
                    border-radius: 12px;
                    font-size: 13px;
                    font-weight: bold;
                    margin-bottom: 10px;
                }}
                </style>
                
                <div id="node-detail-panel">
                    <span class="close-btn" onclick="closeDetailPanel()">✕</span>
                    <div id="detail-content"></div>
                </div>
                
                <script>
                var nodesData = {nodes_json};
                var networkRef = null;
                var originalColors = {{nodes: {{}}, edges: {{}}}};
                
                function closeDetailPanel() {{
                    document.getElementById('node-detail-panel').style.display = 'none';
                    if (networkRef) {{
                        restoreAllColors();
                    }}
                }}
                
                function restoreAllColors() {{
                    if (!networkRef) return;
                    var nodeUpdates = [];
                    var edgeUpdates = [];
                    
                    for (var nodeId in originalColors.nodes) {{
                        nodeUpdates.push({{id: nodeId, color: originalColors.nodes[nodeId], font: {{color: '#222222'}}}});
                    }}
                    for (var edgeId in originalColors.edges) {{
                        edgeUpdates.push({{id: edgeId, color: originalColors.edges[edgeId], width: 2}});
                    }}
                    
                    if (nodeUpdates.length > 0) networkRef.body.data.nodes.update(nodeUpdates);
                    if (edgeUpdates.length > 0) networkRef.body.data.edges.update(edgeUpdates);
                    originalColors = {{nodes: {{}}, edges: {{}}}};
                }}
                
                function highlightConnected(clickedNodeId) {{
                    if (!networkRef) return;
                    restoreAllColors();
                    
                    var connectedNodes = new Set([clickedNodeId]);
                    var connectedEdgeIds = new Set();
                    
                    networkRef.body.data.edges.get().forEach(function(edge) {{
                        if (edge.from === clickedNodeId || edge.to === clickedNodeId) {{
                            connectedNodes.add(edge.from);
                            connectedNodes.add(edge.to);
                            connectedEdgeIds.add(edge.id);
                        }}
                    }});
                    
                    var nodeUpdates = [];
                    var edgeUpdates = [];
                    originalColors = {{nodes: {{}}, edges: {{}}}};
                    
                    networkRef.body.data.nodes.get().forEach(function(node) {{
                        originalColors.nodes[node.id] = node.color;
                        if (!connectedNodes.has(node.id)) {{
                            nodeUpdates.push({{id: node.id, color: '#dddddd', font: {{color: '#bbbbbb'}}}});
                        }}
                    }});
                    
                    networkRef.body.data.edges.get().forEach(function(edge) {{
                        originalColors.edges[edge.id] = edge.color;
                        if (connectedEdgeIds.has(edge.id)) {{
                            edgeUpdates.push({{id: edge.id, color: '#FF6B6B', width: 6}});
                        }} else {{
                            edgeUpdates.push({{id: edge.id, color: '#eeeeee', width: 1}});
                        }}
                    }});
                    
                    if (nodeUpdates.length > 0) networkRef.body.data.nodes.update(nodeUpdates);
                    if (edgeUpdates.length > 0) networkRef.body.data.edges.update(edgeUpdates);
                }}
                
                window.onload = function() {{
                    var attempts = 0;
                    var maxAttempts = 20;
                    
                    function tryBindEvents() {{
                        attempts++;
                        var networkObj = (typeof network !== 'undefined') ? network : (typeof window.network !== 'undefined' ? window.network : null);
                        
                        if (networkObj) {{
                            networkRef = networkObj;
                            networkObj.on('stabilized', function() {{
                                networkObj.setOptions({{physics: {{enabled: false}}}});
                            }});
                            
                            networkObj.on('click', function(params) {{
                                if (params.nodes && params.nodes.length > 0) {{
                                    var nodeId = params.nodes[0];
                                    if (nodeId !== 'topic' && !nodeId.startsWith('cat_')) {{
                                        var node = nodesData[nodeId];
                                        if (node) {{
                                            highlightConnected(nodeId);
                                            var panel = document.getElementById('node-detail-panel');
                                            var content = document.getElementById('detail-content');
                                            
                                            var typeColors = {{"课程": "#4ECDC4", "事件": "#FFA07A", "人物": "#96CEB4"}};
                                            var bgColor = typeColors[node.type] || "#999";
                                            
                                            var html = '<span class="type-badge" style="background:' + bgColor + ';color:white;">' + node.type + '</span>';
                                            
                                            if (node.type === "课程") {{
                                                html += '<h3>📖 ' + (node.title || '课程') + '</h3>';
                                                if (node.book_name) html += '<div class="detail-row"><span class="detail-label">📚 教材：</span><span class="detail-value">' + node.book_name + '</span></div>';
                                                if (node.content) html += '<div class="detail-row"><span class="detail-label">📝 内容：</span><span class="detail-value">' + node.content + '</span></div>';
                                            }} else if (node.type === "事件") {{
                                                html += '<h3>⚡ ' + (node.name || '历史事件') + '</h3>';
                                                if (node.year) {{
                                                    var yearText = String(node.year);
                                                    if (!yearText.includes('年')) yearText += '年';
                                                    html += '<div class="detail-row"><span class="detail-label">⏰ 时间：</span><span class="detail-value">' + yearText + '</span></div>';
                                                }}
                                                if (node.description) html += '<div class="detail-row"><span class="detail-label">💡 描述：</span><span class="detail-value">' + node.description + '</span></div>';
                                            }} else if (node.type === "人物") {{
                                                html += '<h3>👤 ' + (node.name || '历史人物') + '</h3>';
                                                if (node.description) html += '<div class="detail-row"><span class="detail-label">📝 简介：</span><span class="detail-value">' + node.description + '</span></div>';
                                            }}
                                            
                                            content.innerHTML = html;
                                            panel.style.display = 'block';
                                        }}
                                    }}
                                }} else {{
                                    closeDetailPanel();
                                }}
                            }});
                        }} else if (attempts < maxAttempts) {{
                            setTimeout(tryBindEvents, 300);
                        }}
                    }}
                    
                    setTimeout(tryBindEvents, 500);
                }};
                </script>
                """
                
                html_content = html_content.replace("</body>", click_handler + "</body>")
                
                st.markdown("#### 📊 知识图谱可视化")
                st.caption("💡 拖动节点调整位置 • 滚轮缩放 • **点击节点查看详细信息卡片**")
                components.html(html_content, height=850, scrolling=False)
                
                try:
                    os.unlink(graph_path)
                except:
                    pass
            
            # 显示统计
            results = browser.search_by_topic(selected_topic)
            col1, col2, col3 = st.columns(3)
            col1.metric("📖 相关课文", len(results['lessons']))
            col2.metric("⚡ 相关事件", len(results['events']))
            col3.metric("👤  相关人物", len(results['figures']))
            
            try:
                os.unlink(graph_path)
            except:
                pass


if __name__ == "__main__":
    render_knowledge_graph()

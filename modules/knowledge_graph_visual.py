"""
知识图谱可视化模块
使用Pyvis创建交互式知识图谱，展示题目相关的知识点关联
参考范各庄矿突水事故知识图谱的可视化样式
"""

import streamlit as st
import streamlit.components.v1 as components
from pyvis.network import Network
import os
import tempfile
import json


class KnowledgeGraphVisualizer:
    """知识图谱可视化器"""
    
    def __init__(self, events, figures, lessons, units):
        """
        初始化可视化器
        
        Args:
            events: 历史事件数据
            figures: 历史人物数据
            lessons: 课程数据
            units: 单元数据
        """
        self.events = events
        self.figures = figures
        self.lessons = lessons
        self.units = units
        
        # 类别颜色配置
        self.category_colors = {
            "单元": "#FF6B6B",
            "课程": "#4ECDC4",
            "事件": "#45B7D1",
            "人物": "#96CEB4",
            "其他": "#FFEAA7"
        }
    
    def create_knowledge_graph(self, related_knowledge, core_concept=""):
        """
        创建知识图谱 - 以核心知识点为中心的专题式图谱
        
        Args:
            related_knowledge: 相关知识点数据，包含events, figures, lessons, units
            core_concept: 核心概念/知识点
        
        Returns:
            Network: pyvis网络图对象
        """
        net = Network(
            height="750px",
            width="100%",
            bgcolor="#ffffff",
            font_color="#333333"
        )
        
        # 配置物理引擎
        net.barnes_hut(
            gravity=-5000,
            central_gravity=0.3,
            spring_length=180,
            damping=0.5,
            overlap=0.9
        )
        
        # 中心节点 - 核心知识点
        if not core_concept:
            core_concept = "核心知识点"
        
        net.add_node(
            "center",
            label=f"🎯 {core_concept}",
            color="#FF6B6B",
            size=60,
            title=f"核心概念：{core_concept}",
            borderWidth=4,
            font={"size": 26, "color": "#222", "face": "Microsoft YaHei", "bold": True}
        )
        
        # 添加单元节点 - 作为知识主题
        units = related_knowledge.get('units', [])[:3]
        for i, unit in enumerate(units):
            unit_id = f"unit_{i}"
            unit_title = unit.get('title', '相关单元')
            
            net.add_node(
                unit_id,
                label=f"📂 {unit_title[:18]}",
                color=self.category_colors["单元"],
                size=42,
                title=f"📂 单元主题：{unit_title}",
                borderWidth=3,
                font={"size": 17, "color": "#222", "face": "Microsoft YaHei", "bold": True}
            )
            net.add_edge("center", unit_id, 
                        color="#FF6B6B", 
                        width=3,
                        title="所属单元",
                        smooth=False)
            
            # 单元和课程的关系（直线）
            for j, lesson in enumerate(lessons):
                if lesson.get('unit_id') == unit.get('id'):
                    net.add_edge(unit_id, f"lesson_{j}",
                               color="#999",
                               width=1.5,
                               dashes=True,
                               title="包含课程",
                               smooth=False)
        
        # 添加课程节点 - 作为知识来源
        lessons = related_knowledge.get('lessons', [])[:5]
        for i, lesson in enumerate(lessons):
            lesson_id = f"lesson_{i}"
            lesson_title = lesson.get('title', '相关课程')
            book_name = lesson.get('book_name', '')
            
            net.add_node(
                lesson_id,
                label=f"📚 {lesson_title[:15]}",
                color=self.category_colors["课程"],
                size=36,
                title=f"📚 课程：{lesson_title}\\n📖 教材：{book_name}",
                borderWidth=2,
                font={"size": 16, "color": "#222", "face": "Microsoft YaHei"}
            )
            net.add_edge("center", lesson_id, 
                        color="#4ECDC4", 
                        width=2.5,
                        title="知识来源",
                        smooth=False)
        
        # 添加事件节点 - 围绕核心概念（去重）
        events = related_knowledge.get('events', [])[:10]
        added_events = set()  # 记录已添加的事件名称
        event_id_counter = 0
        for i, event in enumerate(events):
            # 使用event字段（已从description补充过来），如果没有就用description
            event_name = event.get('event', event.get('description', '历史事件'))
            event_year = event.get('year', '')
            event_desc = event.get('description', '')
            
            # 去重：检查事件名称是否已存在
            if event_name in added_events:
                continue
            added_events.add(event_name)
            
            event_id = f"event_{event_id_counter}"
            event_id_counter += 1
            
            net.add_node(
                event_id,
                label=f"📅 {event_name[:12]}",
                color=self.category_colors["事件"],
                size=32,
                title=f"📅 {event_name}\\n⏰ {event_year}年\\n💡 {event_desc[:50]}...",
                borderWidth=2,
                font={"size": 15, "color": "#222", "face": "Microsoft YaHei"}
            )
            
            # 直接连接到中心节点，表示与核心概念的关系（直线）
            net.add_edge("center", event_id, 
                        color="#45B7D1", 
                        width=2,
                        title="相关事件",
                        smooth=False)
        
        # 添加人物节点 - 围绕核心概念（去重）
        figures = related_knowledge.get('figures', [])[:10]
        added_figures = set()  # 记录已添加的人物名称
        figure_id_counter = 0
        for i, figure in enumerate(figures):
            # 使用figure字段（已从name补充过来），如果没有就用name
            figure_name = figure.get('figure', figure.get('name', '历史人物'))
            figure_intro = figure.get('introduction', figure.get('description', ''))[:40]
            
            # 去重：检查人物名称是否已存在
            if figure_name in added_figures:
                continue
            added_figures.add(figure_name)
            
            figure_id = f"figure_{figure_id_counter}"
            figure_id_counter += 1
            
            net.add_node(
                figure_id,
                label=f"👤 {figure_name[:8]}",
                color=self.category_colors["人物"],
                size=28,
                title=f"👤 {figure_name}\\n📝 {figure_intro}...",
                borderWidth=2,
                font={"size": 14, "color": "#222", "face": "Microsoft YaHei"}
            )
            
            # 直接连接到中心节点（直线）
            net.add_edge("center", figure_id, 
                        color="#96CEB4", 
                        width=2,
                        title="相关人物",
                        smooth=False)
        
        # 配置交互选项
        net.set_options("""
        {
            "nodes": {
                "font": {
                    "size": 16,
                    "face": "Microsoft YaHei, SimHei, sans-serif"
                }
            },
            "edges": {
                "smooth": {
                    "type": "continuous",
                    "roundness": 0.5
                },
                "width": 1,
                "color": "#999999"
            },
            "interaction": {
                "hover": true,
                "navigationButtons": true,
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
                    "springLength": 250,
                    "avoidOverlap": 1
                },
                "stabilization": {
                    "enabled": true,
                    "iterations": 200,
                    "fit": true
                }
            }
        }
        """)
        
        return net
    
    def render(self, related_knowledge, core_concept=""):
        """
        渲染知识图谱
        
        Args:
            related_knowledge: 相关知识点数据
            core_concept: 核心概念/知识点
        """
        st.markdown("### 🗺️ 知识关联图谱")
        
        # 统计信息
        total_nodes = (
            len(related_knowledge.get('units', [])) +
            len(related_knowledge.get('lessons', [])) +
            len(related_knowledge.get('events', [])) +
            len(related_knowledge.get('figures', []))
        )
        
        if total_nodes == 0:
            st.warning("📊 未找到足够的关联知识点来生成图谱")
            st.info("💡 提示：请尝试输入包含具体历史事件、人物或朝代名称的题目")
            return
        
        # 显示核心概念
        if core_concept:
            st.info(f"🎯 **核心知识点：** {core_concept}")
        
        # 显示统计信息
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("📚 单元", len(related_knowledge.get('units', [])))
        with col2:
            st.metric("📖 课程", len(related_knowledge.get('lessons', [])))
        with col3:
            st.metric("⚡ 事件", len(related_knowledge.get('events', [])))
        with col4:
            st.metric("👤 人物", len(related_knowledge.get('figures', [])))
        
        # 图例
        st.markdown("#### 📊 节点类型")
        legend_html = "<div style='display:flex;gap:10px;flex-wrap:wrap;'>"
        for cat, color in self.category_colors.items():
            legend_html += f"<span style='background:{color}33;border:2px solid {color};border-radius:6px;padding:4px 12px;font-size:13px;color:{color};font-weight:bold;'>{cat}</span>"
        legend_html += "</div>"
        st.markdown(legend_html, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # 创建图谱
        net = self.create_knowledge_graph(related_knowledge, core_concept)
        
        # 保存并显示HTML
        try:
            # 使用临时文件
            with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.html', encoding='utf-8') as f:
                net.save_graph(f.name)
                graph_path = f.name
            
            # 读取HTML内容
            with open(graph_path, 'r', encoding='utf-8') as f:
                html_content = f.read()
            
            # 准备节点数据供JavaScript使用
            nodes_data = {}
            
            # 添加单元节点数据
            for i, unit in enumerate(related_knowledge.get('units', [])[:5]):
                nodes_data[f"unit_{i}"] = {
                    "id": f"unit_{i}",
                    "label": unit.get('title', '相关单元'),
                    "type": "单元",
                    "title": unit.get('title', ''),
                    "description": unit.get('description', ''),
                    "book_name": unit.get('book_name', '')
                }
            
            # 添加课程节点数据
            for i, lesson in enumerate(related_knowledge.get('lessons', [])[:5]):
                nodes_data[f"lesson_{i}"] = {
                    "id": f"lesson_{i}",
                    "label": lesson.get('title', '相关课程'),
                    "type": "课程",
                    "title": lesson.get('title', ''),
                    "content": lesson.get('content', '')[:200] + '...' if lesson.get('content', '') else '',
                    "book_name": lesson.get('book_name', '')
                }
            
            # 添加事件节点数据
            for i, event in enumerate(related_knowledge.get('events', [])[:10]):
                event_name = event.get('event', event.get('description', '历史事件'))
                nodes_data[f"event_{i}"] = {
                    "id": f"event_{i}",
                    "label": event_name[:12],
                    "type": "事件",
                    "event": event_name,
                    "year": event.get('year', ''),
                    "description": event.get('description', '')
                }
            
            # 添加人物节点数据
            for i, figure in enumerate(related_knowledge.get('figures', [])[:10]):
                figure_name = figure.get('figure', figure.get('name', '历史人物'))
                nodes_data[f"figure_{i}"] = {
                    "id": f"figure_{i}",
                    "label": figure_name[:8],
                    "type": "人物",
                    "name": figure_name,
                    "introduction": figure.get('introduction', figure.get('description', ''))
                }
            
            # 注入点击事件处理 - 显示详情卡片
            import json
            nodes_json = json.dumps(nodes_data, ensure_ascii=False)
            
            click_handler = f"""
            <style>
            html, body {{
                margin: 0 !important;
                padding: 0 !important;
                overflow: hidden !important;
            }}
            #node-detail-panel {{
                position: fixed;
                top: 20px;
                right: 20px;
                width: 400px;
                max-height: 85vh;
                background: rgba(255,255,255,0.98);
                padding: 25px;
                z-index: 9999;
                overflow-y: auto;
                display: none;
                font-family: 'Microsoft YaHei', sans-serif;
                box-shadow: 0 4px 20px rgba(0,0,0,0.15);
                border-radius: 12px;
                border: 2px solid #4ECDC4;
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
                display: inline-block;
                min-width: 80px;
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
            
            function closeDetailPanel() {{
                document.getElementById('node-detail-panel').style.display = 'none';
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
                        
                        // 稳定后禁用物理引擎
                        networkObj.on('stabilized', function() {{
                            networkObj.setOptions({{physics: {{enabled: false}}}});
                        }});
                        
                        // 点击事件
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
                        "单元": "#FF6B6B",
                        "课程": "#4ECDC4",
                        "事件": "#45B7D1",
                        "人物": "#96CEB4"
                    }};
                    var bgColor = typeColors[node.type] || "#999";
                    
                    var html = '<span class="type-badge" style="background:' + bgColor + ';color:white;">' + node.type + '</span>';
                    html += '<h3>' + (node.label || node.id) + '</h3>';
                    
                    if (node.type === "单元") {{
                        if (node.title) html += '<div class="detail-row"><span class="detail-label">📚 单元名称：</span><span class="detail-value">' + node.title + '</span></div>';
                        if (node.book_name) html += '<div class="detail-row"><span class="detail-label">📖 所属教材：</span><span class="detail-value">' + node.book_name + '</span></div>';
                        if (node.description) html += '<div class="detail-row"><span class="detail-label">📝 描述：</span><span class="detail-value">' + node.description + '</span></div>';
                    }} else if (node.type === "课程") {{
                        if (node.title) html += '<div class="detail-row"><span class="detail-label">📚 课程名称：</span><span class="detail-value">' + node.title + '</span></div>';
                        if (node.book_name) html += '<div class="detail-row"><span class="detail-label">📖 所属教材：</span><span class="detail-value">' + node.book_name + '</span></div>';
                        if (node.content) html += '<div class="detail-row"><span class="detail-label">📝 内容简介：</span><span class="detail-value">' + node.content + '</span></div>';
                    }} else if (node.type === "事件") {{
                        if (node.event) html += '<div class="detail-row"><span class="detail-label">📅 事件名称：</span><span class="detail-value">' + node.event + '</span></div>';
                        if (node.year) html += '<div class="detail-row"><span class="detail-label">⏰ 时间：</span><span class="detail-value">' + node.year + '年</span></div>';
                        if (node.description) html += '<div class="detail-row"><span class="detail-label">💡 描述：</span><span class="detail-value">' + node.description + '</span></div>';
                    }} else if (node.type === "人物") {{
                        if (node.name) html += '<div class="detail-row"><span class="detail-label">👤 人物姓名：</span><span class="detail-value">' + node.name + '</span></div>';
                        if (node.introduction) html += '<div class="detail-row"><span class="detail-label">📝 简介：</span><span class="detail-value">' + node.introduction + '</span></div>';
                    }}
                    
                    content.innerHTML = html;
                    panel.style.display = 'block';
                }}
                
                setTimeout(tryBindEvents, 500);
            }};
            </script>
            """
            
            html_content = html_content.replace("</body>", click_handler + "</body>")
            
            # 添加交互说明
            instruction_html = """
            <div style='background:#f0f8ff;padding:15px;border-radius:8px;margin-bottom:10px;border-left:4px solid #4ECDC4;'>
                <p style='margin:0;color:#333;font-size:14px;'>
                    💡 <strong>使用提示：</strong>
                    • 鼠标拖动节点调整位置 
                    • 滚轮缩放视图 
                    • <strong>点击节点查看详细信息卡片</strong> 
                    • 拖动空白区域移动整体视图
                </p>
            </div>
            """
            st.markdown(instruction_html, unsafe_allow_html=True)
            
            # 嵌入HTML
            components.html(html_content, height=750, scrolling=False)
            
            # 清理临时文件
            try:
                os.unlink(graph_path)
            except:
                pass
                
        except Exception as e:
            st.error(f"⚠️ 图谱渲染失败：{str(e)}")
            st.info("💡 提示：可以查看下方的文本列表了解相关知识点")


def render_knowledge_graph_visual(related_knowledge, events, figures, lessons, units, core_concept=""):
    """
    渲染知识图谱可视化（供外部调用的便捷函数）
    
    Args:
        related_knowledge: 相关知识点数据
        events: 所有历史事件数据
        figures: 所有历史人物数据
        lessons: 所有课程数据
        units: 所有单元数据
        core_concept: 核心概念/知识点
    """
    visualizer = KnowledgeGraphVisualizer(events, figures, lessons, units)
    visualizer.render(related_knowledge, core_concept)

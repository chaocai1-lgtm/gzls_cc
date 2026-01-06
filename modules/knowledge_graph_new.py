"""
高分子物理知识图谱可视化模块（节点+关系形式）
采用 xjygraph 的交互设计，支持点击节点高亮关联内容
"""

import streamlit as st
from pyvis.network import Network
import streamlit.components.v1 as components
import json
import tempfile
import os
from data.knowledge_graph_graph_format import (
    get_graph_data, 
    get_node_by_id, 
    GFZ_CATEGORY_COLORS
)

def create_knowledge_graph_viz(selected_node_id=None):
    """
    创建交互式知识图谱（参考 xjygraph 设计）
    支持点击节点查看详情和高亮关联内容
    """
    try:
        graph_data = get_graph_data()
        nodes = graph_data.get("nodes", [])
        relationships = graph_data.get("relationships", [])
        
        if not nodes:
            return None, [], []
        
        # 创建网络对象
        net = Network(
            height="900px",
            width="100%",
            bgcolor="#ffffff",
            font_color="#333333",
            directed=True
        )
    except Exception as e:
        print(f"创建知识图谱网络对象失败: {e}")
        return None, [], []
    
    # 添加所有节点
    for node in nodes:
        color = GFZ_CATEGORY_COLORS.get(node["category"], "#888888")
        
        # 根据层级设置节点大小
        size_map = {1: 60, 2: 50, 3: 40}
        size = size_map.get(node["level"], 40)
        
        # 如果是选中的节点，增加边框宽度
        border_width = 5 if selected_node_id == node["id"] else 2
        
        net.add_node(
            node["id"],
            label=node["label"],
            color=color,
            size=size,
            title=f"{node['label']} ({node['category']})",
            borderWidth=border_width,
            borderWidthSelected=5,
            font={
                "size": 16,
                "color": "#222222",
                "face": "Microsoft YaHei, SimHei, sans-serif",
                "bold": True
            }
        )
    
    # 添加所有关系边
    for rel in relationships:
        net.add_edge(
            rel["source"],
            rel["target"],
            title=rel.get("type", "关联"),
            label=rel.get("type", ""),
            color="#999999",
            width=1.5,
            arrows={
                "to": {
                    "enabled": True,
                    "scaleFactor": 0.4
                }
            },
            font={
                "size": 13,
                "color": "#555"
            }
        )
    
    # 配置物理引擎
    net.set_options("""
    {
        "physics": {
            "enabled": true,
            "barnesHut": {
                "gravitationalConstant": -8000,
                "centralGravity": 0.1,
                "springLength": 300,
                "springConstant": 0.01,
                "avoidOverlap": 0.8,
                "damping": 0.5
            },
            "stabilization": {
                "enabled": true,
                "iterations": 300,
                "fit": true
            }
        },
        "interaction": {
            "hover": true,
            "navigationButtons": true,
            "keyboard": true,
            "dragNodes": true,
            "dragView": true,
            "zoomView": true
        },
        "edges": {
            "smooth": {
                "enabled": false
            }
        }
    }
    """)
    
    return net, nodes, relationships

def render_knowledge_graph_interactive():
    """
    渲染交互式知识图谱页面（xjygraph 风格）
    """
    st.title("🧬 高分子物理知识图谱")
    st.markdown("*基于《高分子物理（第五版）》教材构建 - 点击节点查看详情*")
    
    # 尝试加载数据
    try:
        graph_data = get_graph_data()
        if not graph_data or not graph_data.get("nodes"):
            st.error("❌ 知识图谱数据为空，请检查数据源")
            return
    except Exception as e:
        st.error(f"❌ 加载知识图谱数据失败: {str(e)}")
        return
    
    # 左侧侧边栏
    with st.sidebar:
        st.markdown("### 📋 知识节点导航")
        
        # 按类别显示节点
        graph_data = get_graph_data()
        nodes = graph_data.get("nodes", [])
        
        # 按类别分组
        nodes_by_category = {}
        for node in nodes:
            cat = node.get("category", "其他")
            if cat not in nodes_by_category:
                nodes_by_category[cat] = []
            nodes_by_category[cat].append(node)
        
        selected_node = None
        selected_node_id = None
        
        # 显示各分类的节点列表
        for category in ["模块", "章节", "重要概念", "知识点", "应用实践"]:
            if category in nodes_by_category:
                color = GFZ_CATEGORY_COLORS.get(category, "#888888")
                with st.expander(f"📂 {category} ({len(nodes_by_category[category])})", expanded=category in ["模块", "重要概念"]):
                    for node in nodes_by_category[category]:
                        if st.button(
                            f"🔹 {node['label']}", 
                            key=f"node_{node['id']}",
                            use_container_width=True
                        ):
                            selected_node = node
                            selected_node_id = node["id"]
                            st.session_state.selected_node = node
                            st.rerun()
        
        # 显示选中节点的详情
        st.markdown("---")
        if st.session_state.get("selected_node"):
            render_node_detail_panel(st.session_state.get("selected_node"))
    
    # 主区域
    st.markdown("##### 📊 知识分类")
    legend_html = "<div style='display:flex;gap:8px;flex-wrap:wrap;justify-content:flex-end;margin-bottom:20px;'>"
    for cat, color in GFZ_CATEGORY_COLORS.items():
        legend_html += f"<span style='background:{color}33;border:1px solid {color};border-radius:4px;padding:2px 8px;font-size:11px;color:{color};'>{cat}</span>"
    legend_html += "</div>"
    st.markdown(legend_html, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # 获取选中节点（如果有）
    selected_node_id = None
    if st.session_state.get("selected_node"):
        selected_node_id = st.session_state.selected_node["id"]
    
    # 创建图谱
    st.markdown("### 🗺️ 知识图谱（点击节点可在左侧查看详情）")
    
    net, nodes, relationships = create_knowledge_graph_viz(selected_node_id)
    
    if net is None:
        st.error("❌ 无法加载知识图谱数据，请刷新页面重试")
        return
    
    # 使用临时文件保存和读取 HTML
    try:
        with tempfile.NamedTemporaryFile(mode="w+", suffix=".html", delete=False, encoding="utf-8") as tmp_file:
            graph_file = tmp_file.name
        
        # 保存网络图谱
        net.show(graph_file)
        
        # 读取 HTML 内容
        with open(graph_file, "r", encoding="utf-8") as f:
            html_str = f.read()
        
        # 在 Streamlit 中显示
        st.components.v1.html(html_str, height=950)
        
        # 清理临时文件
        try:
            os.unlink(graph_file)
        except:
            pass
            
    except FileNotFoundError as e:
        st.error(f"❌ 无法生成知识图谱文件: {e}")
        return
    except AttributeError as e:
        st.error(f"❌ 知识图谱渲染出错: {e}")
        return
    except Exception as e:
        st.error(f"❌ 出错: {str(e)}")


def render_node_detail_panel(node):
    #node-info-panel {{
        position: fixed;
        top: 20px;
        right: 20px;
        width: 380px;
        max-height: 80vh;
        background: rgba(255,255,255,0.95);
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        z-index: 9999;
        overflow-y: auto;
        font-family: 'Microsoft YaHei', sans-serif;
        display: none;
    }}
    #node-info-panel h3 {{
        margin: 0 0 15px 0;
        color: #1f77b4;
        font-size: 20px;
        padding-bottom: 10px;
        border-bottom: 2px solid #1f77b4;
    }}
    #node-info-panel .info-item {{
        margin: 12px 0;
        font-size: 14px;
    }}
    #node-info-panel .info-label {{
        font-weight: bold;
        color: #333;
    }}
    #node-info-panel .info-value {{
        color: #666;
        margin-left: 8px;
    }}
    #node-info-panel .close-btn {{
        position: absolute;
        top: 15px;
        right: 20px;
        cursor: pointer;
        font-size: 24px;
        color: #999;
    }}
    #node-info-panel .relations {{
        margin-top: 20px;
        padding-top: 15px;
        border-top: 1px solid #ddd;
    }}
    #node-info-panel .relations h4 {{
        margin: 0 0 10px 0;
        color: #666;
        font-size: 14px;
    }}
    .relation-link {{
        display: inline-block;
        background: #f0f0f0;
        padding: 4px 8px;
        border-radius: 4px;
        margin: 4px 4px 4px 0;
        font-size: 12px;
        cursor: pointer;
    }}
    .relation-link:hover {{
        background: #e0e0e0;
    }}
    </style>
    
    <div id="node-info-panel">
        <span class="close-btn" onclick="closeNodeInfo()">✕</span>
        <h3 id="node-title"></h3>
        <div id="node-content"></div>
        <div id="node-relations"></div>
    </div>
    
    <script>
    var nodesData = {nodes_json};
    var relsData = {rels_json};
    var networkRef = null;
    var originalColors = {{nodes: {{}}, edges: {{}}}};
    
    function closeNodeInfo() {{
        document.getElementById('node-info-panel').style.display = 'none';
        restoreColors();
    }}
    
    function restoreColors() {{
        if (!networkRef) return;
        var nodeUpdates = [];
        var edgeUpdates = [];
        
        for (var nodeId in originalColors.nodes) {{
            nodeUpdates.push({{id: nodeId, color: originalColors.nodes[nodeId], font: {{color: '#222222'}}}});
        }}
        for (var edgeId in originalColors.edges) {{
            edgeUpdates.push({{id: edgeId, color: '#999999', font: {{color: '#555'}}}});
        }}
        
        if (nodeUpdates.length > 0 && networkRef.body.data.nodes) {{
            networkRef.body.data.nodes.update(nodeUpdates);
        }}
        if (edgeUpdates.length > 0 && networkRef.body.data.edges) {{
            networkRef.body.data.edges.update(edgeUpdates);
        }}
    }}
    
    function highlightRelated(nodeId) {{
        if (!networkRef) return;
        
        restoreColors();
        
        // 找出相关节点
        var relatedNodeIds = new Set([nodeId]);
        var relatedEdgeIds = new Set();
        
        if (networkRef.body.data.edges) {{
            var allEdges = networkRef.body.data.edges.get();
            allEdges.forEach(function(edge) {{
                if (edge.from === nodeId || edge.to === nodeId) {{
                    relatedNodeIds.add(edge.from);
                    relatedNodeIds.add(edge.to);
                    relatedEdgeIds.add(edge.id);
                }}
            }});
        }}
        
        // 更新颜色
        if (networkRef.body.data.nodes) {{
            var allNodes = networkRef.body.data.nodes.get();
            var nodeUpdates = [];
            
            originalColors.nodes = {{}};
            allNodes.forEach(function(node) {{
                originalColors.nodes[node.id] = node.color;
                if (relatedNodeIds.has(node.id)) {{
                    nodeUpdates.push({{id: node.id, font: {{color: '#222222'}}}});
                }} else {{
                    nodeUpdates.push({{id: node.id, color: '#dddddd', font: {{color: '#bbbbbb'}}}});
                }}
            }});
            networkRef.body.data.nodes.update(nodeUpdates);
        }}
        
        if (networkRef.body.data.edges) {{
            var allEdges = networkRef.body.data.edges.get();
            var edgeUpdates = [];
            
            originalColors.edges = {{}};
            allEdges.forEach(function(edge) {{
                originalColors.edges[edge.id] = edge.color;
                if (relatedEdgeIds.has(edge.id)) {{
                    edgeUpdates.push({{id: edge.id, color: '#1f77b4', font: {{color: '#1f77b4'}}}});
                }} else {{
                    edgeUpdates.push({{id: edge.id, color: '#eeeeee', font: {{color: '#cccccc'}}}});
                }}
            }});
            networkRef.body.data.edges.update(edgeUpdates);
        }}
    }}
    
    function showNodeInfo(nodeId) {{
        var node = nodesData[nodeId];
        if (!node) return;
        
        var panel = document.getElementById('node-info-panel');
        var title = document.getElementById('node-title');
        var content = document.getElementById('node-content');
        var relations = document.getElementById('node-relations');
        
        title.innerText = '📍 ' + node.label;
        
        var html = '';
        html += '<div class="info-item"><span class="info-label">类别:</span><span class="info-value">' + node.category + '</span></div>';
        html += '<div class="info-item"><span class="info-label">类型:</span><span class="info-value">' + node.type + '</span></div>';
        html += '<div class="info-item"><span class="info-label">层级:</span><span class="info-value">' + node.level + '</span></div>';
        
        if (node.properties) {{
            for (var key in node.properties) {{
                if (node.properties[key] && node.properties[key] !== '') {{
                    html += '<div class="info-item"><span class="info-label">' + key + ':</span><span class="info-value">' + node.properties[key] + '</span></div>';
                }}
            }}
        }}
        
        content.innerHTML = html;
        
        // 显示关联关系
        var relHtml = '<div class="relations"><h4>🔗 相关联系</h4>';
        var hasRels = false;
        
        relsData.forEach(function(rel) {{
            if (rel.source === nodeId) {{
                var target = nodesData[rel.target];
                if (target) {{
                    relHtml += '<div class="info-item">➡️ <strong>' + rel.type + '</strong><br/>→ ' + target.label + '</div>';
                    hasRels = true;
                }}
            }} else if (rel.target === nodeId) {{
                var source = nodesData[rel.source];
                if (source) {{
                    relHtml += '<div class="info-item">⬅️ ' + source.label + '<br/><strong>' + rel.type + '</strong></div>';
                    hasRels = true;
                }}
            }}
        }});
        
        relHtml += '</div>';
        relations.innerHTML = hasRels ? relHtml : '<div class="relations"><p style="color:#999;font-size:12px;">无关联内容</p></div>';
        
        panel.style.display = 'block';
        highlightRelated(nodeId);
    }}
    
    window.onload = function() {{
        var attempts = 0;
        function bindEvents() {{
            attempts++;
            var net = null;
            if (typeof network !== 'undefined') net = network;
            else if (typeof window.network !== 'undefined') net = window.network;
            
            if (net) {{
                networkRef = net;
                
                net.on('stabilized', function() {{
                    net.setOptions({{physics: {{enabled: false}}}});
                }});
                
                net.on('click', function(params) {{
                    if (params.nodes && params.nodes.length > 0) {{
                        showNodeInfo(params.nodes[0]);
                    }} else {{
                        closeNodeInfo();
                    }}
                }});
            }} else if (attempts < 20) {{
                setTimeout(bindEvents, 300);
            }}
        }}
        setTimeout(bindEvents, 500);
    }};
    </script>
    """
    
    # 注入脚本到HTML
    html_str = html_str.replace("</body>", interaction_script + "</body>")
    
    # 显示图谱
    components.html(html_str, height=1000, scrolling=False)

def render_node_detail_panel(node):
    """渲染节点详情面板"""
    color = GFZ_CATEGORY_COLORS.get(node["category"], "#888888")
    
    st.markdown(f"""
    <div style='
        background: #ffffff;
        border-left: 4px solid {color};
        border-radius: 8px;
        padding: 15px;
        margin: 10px 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    '>
        <h4 style='color: {color}; margin: 0 0 10px 0;'>📌 {node["label"]}</h4>
        <div style='display: flex; gap: 6px; flex-wrap: wrap; margin-bottom: 10px;'>
            <span style='background: {color}22; color: {color}; padding: 3px 8px; border-radius: 12px; font-size: 11px;'>
                {node["category"]}
            </span>
            <span style='background: #f0f0f0; color: #666; padding: 3px 8px; border-radius: 12px; font-size: 11px;'>
                {node["type"]}
            </span>
            <span style='background: #f0f0f0; color: #666; padding: 3px 8px; border-radius: 12px; font-size: 11px;'>
                L{node["level"]}
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # 属性详情
    st.markdown("**详细信息**")
    props = node.get("properties", {})
    if props:
        for key, value in props.items():
            st.markdown(f"- **{key}**: {value}")
    else:
        st.info("暂无详细属性")

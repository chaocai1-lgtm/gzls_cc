"""
历史知识图谱模块 - 交互式可视化
基于pyvis Network实现，参考范各庄矿知识图谱设计
"""

import streamlit as st
import streamlit.components.v1 as components
from pyvis.network import Network
import json
import os

# 知识节点分类颜色
CATEGORY_COLORS = {
    "古代史": "#FF6B6B",
    "近代史": "#4ECDC4",
    "现代史": "#45B7D1",
    "世界史": "#96CEB4",
    "专题史": "#FFEAA7"
}

def render_knowledge_graph():
    """渲染知识图谱页面"""
    st.title("🗺️ 历史知识图谱")
    
    st.markdown("""
    <div class="info-box">
        <h3>💡 交互式知识图谱</h3>
        <p>点击节点查看详细信息，拖动节点调整位置，滚轮缩放视图</p>
        <p>节点大小表示重要程度，颜色表示历史时期</p>
    </div>
    """, unsafe_allow_html=True)
    
    # 书籍和章节选择
    st.markdown("### 📚 选择内容范围")
    
    # 书籍定义
    books = {
        "中外历史纲要（上）": {
            "第一单元 从中华文明起源到秦汉统一": ["0.1百万年前的人类", "0.2新石器时代", "0.3夏商周时期"],
            "第二单元 三国两晋南北朝隔离与融合": ["1.1三国鼎立", "1.2东晋与南北朝"],
            "第三单元 隆唐的繁荣与开放": ["2.1隇唐统一", "2.2唐朝繁荣", "2.3安史之乱"]
        },
        "中外历史纲要（下）": {
            "第一单元 鸦片战争与洋务运动": ["3.1鸦片战争", "3.2洋务运动"],
            "第二单元 辛亥革命与五四运动": ["4.1戊戌变法", "4.2辛亥革命", "4.3五四运动"],
            "第三单元 中国共产党成立与新民主主义革命": ["5.1中国共产党成立", "5.2国共合作"]
        },
        "选择1 国家制度与社会治理": {
            "专题一 政治制度": ["6.1中央集权", "6.2地方制度"],
            "专题二 法律与社会": ["7.1古代法律", "7.2近代法制"]
        }
    }
    
    col1, col2 = st.columns(2)
    
    with col1:
        selected_book = st.selectbox(
            "📚 选择教材",
            list(books.keys()),
            key="graph_book_select"
        )
    
    with col2:
        chapters = list(books[selected_book].keys())
        selected_chapter = st.selectbox(
            "📝 选择单元/专题",
            chapters,
            key="graph_chapter_select"
        )
    
    # 显示当前选择
    st.info(f"🎯 当前显示：{selected_book} - {selected_chapter}")
    
    # 侧边栏 - 节点详情和设置
    with st.sidebar:
        st.markdown("### 🎯 图谱设置")
        
        # 选择展示范围
        scope = st.selectbox(
            "展示范围",
            ["全部", "中国古代史", "中国近代史", "中国现代史", "世界史"],
            index=0
        )
        
        # 显示层级
        show_levels = st.multiselect(
            "显示层级",
            ["一级（重大事件）", "二级（重要事件）", "三级（详细知识）"],
            default=["一级（重大事件）", "二级（重要事件）"]
        )
        
        # 显示关系类型
        show_relations = st.multiselect(
            "显示关系",
            ["因果关系", "时间顺序", "影响关系", "对比关系"],
            default=["因果关系", "时间顺序", "影响关系"]
        )
        
        st.markdown("---")
        st.markdown("### 📍 选中节点详情")
        
        if st.session_state.get('selected_node_detail'):
            detail = st.session_state.selected_node_detail
            st.markdown(f"**节点：** {detail.get('label', 'N/A')}")
            st.markdown(f"**类别：** {detail.get('category', 'N/A')}")
            st.markdown(f"**时期：** {detail.get('period', 'N/A')}")
            if 'description' in detail:
                st.markdown(f"**说明：** {detail['description']}")
        else:
            st.info("点击图谱中的节点查看详情")
    
    # 图例
    st.markdown("##### 📊 时期分类")
    legend_html = "<div style='display:flex;gap:10px;flex-wrap:wrap;'>"
    for cat, color in CATEGORY_COLORS.items():
        legend_html += f"<span style='background:{color};border-radius:4px;padding:4px 12px;color:white;font-size:13px;'>{cat}</span>"
    legend_html += "</div>"
    st.markdown(legend_html, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # 创建知识图谱数据（传入选择的书籍和章节）
    graph_data = create_history_knowledge_graph(selected_book, selected_chapter)
    
    # 创建并显示图谱
    net = create_interactive_graph(graph_data)
    
    # 保存并显示
    current_dir = os.path.dirname(os.path.abspath(__file__))
    graph_path = os.path.join(current_dir, "..", "temp_history_graph.html")
    net.save_graph(graph_path)
    
    # 读取并注入交互脚本
    with open(graph_path, "r", encoding="utf-8") as f:
        html_content = f.read()
    
    # 添加点击事件处理
    nodes_json = json.dumps(graph_data['nodes'], ensure_ascii=False)
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
        width: 350px;
        max-height: 80vh;
        background: rgba(255,255,255,0.95);
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        display: none;
        z-index: 9999;
        overflow-y: auto;
    }}
    #node-detail-panel h3 {{
        margin: 0 0 15px 0;
        color: #1976d2;
        border-bottom: 2px solid #1976d2;
        padding-bottom: 8px;
    }}
    #node-detail-panel .close-btn {{
        position: absolute;
        top: 15px;
        right: 15px;
        cursor: pointer;
        font-size: 20px;
        color: #999;
    }}
    #node-detail-panel .detail-item {{
        margin: 10px 0;
        font-size: 14px;
        line-height: 1.6;
    }}
    #node-detail-panel .detail-label {{
        font-weight: bold;
        color: #666;
    }}
    </style>
    
    <div id="node-detail-panel">
        <span class="close-btn" onclick="closePanel()">✕</span>
        <h3 id="detail-title">节点详情</h3>
        <div id="detail-content"></div>
    </div>
    
    <script>
    var nodesData = {nodes_json};
    var nodesMap = {{}};
    nodesData.forEach(function(node) {{
        nodesMap[node.id] = node;
    }});
    
    function closePanel() {{
        document.getElementById('node-detail-panel').style.display = 'none';
    }}
    
    function showNodeDetail(nodeId) {{
        var node = nodesMap[nodeId];
        if (!node) return;
        
        var panel = document.getElementById('node-detail-panel');
        var title = document.getElementById('detail-title');
        var content = document.getElementById('detail-content');
        
        title.innerText = '📍 ' + node.label;
        
        var html = '';
        html += '<div class="detail-item"><span class="detail-label">类别：</span>' + (node.category || 'N/A') + '</div>';
        html += '<div class="detail-item"><span class="detail-label">时期：</span>' + (node.period || 'N/A') + '</div>';
        if (node.time) {{
            html += '<div class="detail-item"><span class="detail-label">时间：</span>' + node.time + '</div>';
        }}
        if (node.description) {{
            html += '<div class="detail-item"><span class="detail-label">说明：</span>' + node.description + '</div>';
        }}
        
        content.innerHTML = html;
        panel.style.display = 'block';
    }}
    
    window.onload = function() {{
        var attempts = 0;
        function tryBind() {{
            attempts++;
            var networkObj = typeof network !== 'undefined' ? network : window.network;
            
            if (networkObj) {{
                // 稳定后禁用物理引擎
                networkObj.on('stabilized', function() {{
                    networkObj.setOptions({{physics: {{enabled: false}}}});
                }});
                
                // 点击事件
                networkObj.on('click', function(params) {{
                    if (params.nodes && params.nodes.length > 0) {{
                        showNodeDetail(params.nodes[0]);
                    }} else {{
                        closePanel();
                    }}
                }});
            }} else if (attempts < 20) {{
                setTimeout(tryBind, 300);
            }}
        }}
        setTimeout(tryBind, 500);
    }};
    </script>
    """
    
    html_content = html_content.replace("</body>", click_handler + "</body>")
    
    # 显示图谱
    components.html(html_content, height=900, scrolling=False)


def create_history_knowledge_graph(book_name, chapter_name):
    """根据书籍和章节创建历史知识图谱数据"""
    
    # 根据不同的书籍和章节返回不同的节点和关系
    nodes = []
    relationships = []
    
    # 根据章节名称决定显示哪些知识点
    if "洋务运动" in chapter_name or "鸦片战争" in chapter_name or "近代史" in chapter_name:
        # 近代史 - 完整脉络
        nodes.extend([
            # 第一层：鸦片战争
            {
                "id": "opium_war",
                "label": "鸦片战争",
                "category": "近代史",
                "period": "1840-1842",
                "level": 1,
                "time": "1840-1842年",
                "description": "英国对华第一次战争，中国被迫开放市场"
            },
            # 第二层：影响和后续
            {
                "id": "yangwu",
                "label": "洋务运动",
                "category": "近代史",
                "period": "1861-1894",
                "level": 2,
                "time": "1861-1894年",
                "description": "学习西方先进技术的运动"
            },
            {
                "id": "wuxu",
                "label": "戊戌变法",
                "category": "近代史",
                "period": "1898",
                "level": 2,
                "time": "1898年6-9月",
                "description": "资产阶级维新派的政治改革运动"
            },
            {
                "id": "self_strengthening",
                "label": "自强求富",
                "category": "近代史",
                "period": "1861-1894",
                "level": 3,
                "description": "洋务运动的核心目标"
            },
            {
                "id": "yangwu_failure",
                "label": "甲午战争",
                "category": "近代史",
                "period": "1894-1895",
                "level": 2,
                "time": "1894-1895年",
                "description": "洋务运动破产的标志"
            },
            # 第三层：新阶段
            {
                "id": "xinhai",
                "label": "辛亥革命",
                "category": "近代史",
                "period": "1911",
                "level": 1,
                "time": "1911年",
                "description": "推翻清朝统治，建立共和"
            },
            {
                "id": "republic",
                "label": "中华民国",
                "category": "近代史",
                "period": "1912",
                "level": 2,
                "time": "1912年1月1日",
                "description": "孙中山就任临时大总统"
            },
            {
                "id": "new_culture",
                "label": "新文化运动",
                "category": "近代史",
                "period": "1915",
                "level": 2,
                "time": "1915年",
                "description": "提倡民主与科学，反对封建"
            },
            {
                "id": "enlightenment",
                "label": "思想启蒙",
                "category": "近代史",
                "period": "1915-1921",
                "level": 3,
                "description": "传播西方民主科学思想"
            },
            # 第四层：反帝反封建
            {
                "id": "may_fourth",
                "label": "五四运动",
                "category": "近代史",
                "period": "1919",
                "level": 1,
                "time": "1919年5月4日",
                "description": "爱国运动，新民主主义开端"
            },
            {
                "id": "student_movement",
                "label": "学生运动",
                "category": "近代史",
                "period": "1919",
                "level": 3,
                "description": "学生主力军，提出反帝反封建"
            },
            {
                "id": "marxism",
                "label": "马克思主义传播",
                "category": "近代史",
                "period": "1919-1921",
                "level": 3,
                "description": "五四运动后加速传播"
            },
            # 第五层：中共成立
            {
                "id": "cpc_found",
                "label": "中国共产党成立",
                "category": "近代史",
                "period": "1921",
                "level": 1,
                "time": "1921年7月",
                "description": "中国历史的新纪元"
            },
            {
                "id": "proletarian",
                "label": "无产阶级领导",
                "category": "近代史",
                "period": "1921",
                "level": 3,
                "description": "以工人阶级为领导核心"
            }
        ])
        
        # 建立关系链
        relationships.extend([
            # 第一阶段：鸦片战争及其影响
            {"from": "opium_war", "to": "yangwu", "type": "导致"},
            {"from": "yangwu", "to": "self_strengthening", "type": "目标"},
            {"from": "yangwu", "to": "yangwu_failure", "type": "失败"},
            
            # 第二阶段：政治改革尝试
            {"from": "yangwu_failure", "to": "wuxu", "type": "推动"},
            {"from": "wuxu", "to": "xinhai", "type": "失败导致"},
            
            # 第三阶段：推翻帝制
            {"from": "xinhai", "to": "republic", "type": "建立"},
            {"from": "xinhai", "to": "new_culture", "type": "促进"},
            
            # 第四阶段：思想启蒙
            {"from": "new_culture", "to": "enlightenment", "type": "体现"},
            {"from": "enlightenment", "to": "may_fourth", "type": "推动"},
            
            # 第五阶段：新民主主义
            {"from": "may_fourth", "to": "student_movement", "type": "组织"},
            {"from": "may_fourth", "to": "marxism", "type": "传播"},
            {"from": "marxism", "to": "cpc_found", "type": "指导"},
            
            # 纵向时间关系
            {"from": "opium_war", "to": "yangwu", "type": "之后"},
            {"from": "yangwu", "to": "xinhai", "type": "之后"},
            {"from": "xinhai", "to": "may_fourth", "type": "之后"},
            {"from": "may_fourth", "to": "cpc_found", "type": "之后"},
            
            # 交叉关系
            {"from": "cpc_found", "to": "proletarian", "type": "体现"},
            {"from": "new_culture", "to": "marxism", "type": "传播"}
        ])
    
    if "中华文明起源" in chapter_name or "古代史" in chapter_name:
        # 古代史
        nodes.extend([
            {
                "id": "origin",
                "label": "中华文明起源",
                "category": "古代史",
                "period": "远古",
                "level": 1,
                "description": "从北京人到新石器时代"
            },
            {
                "id": "xia",
                "label": "夏朝",
                "category": "古代史",
                "period": "约公元前2070年",
                "level": 1,
                "description": "中国第一个王朝"
            },
            {
                "id": "shang",
                "label": "商朝",
                "category": "古代史",
                "period": "约公元前1600年",
                "level": 1,
                "description": "青铜文明鼎盛时期"
            }
        ])
        
        relationships.extend([
            {"from": "origin", "to": "xia", "type": "发展"},
            {"from": "xia", "to": "shang", "type": "更替"}
        ])
    
    # 如果没有选择特定章节，显示默认的完整图谱
    if not nodes:
        nodes = [
            {
                "id": "opium_war",
                "label": "鸦片战争",
                "category": "近代史",
                "period": "1840-1842",
                "level": 1,
                "time": "1840-1842年",
                "description": "中国近代史开端"
            },
            {
                "id": "yangwu",
                "label": "洋务运动",
                "category": "近代史",
                "period": "1861-1894",
                "level": 2,
                "time": "1861-1894年",
                "description": "学习西方技术"
            },
            {
                "id": "xinhai",
                "label": "辛亥革命",
                "category": "近代史",
                "period": "1911",
                "level": 1,
                "time": "1911年",
                "description": "推翻清朝统治"
            },
            {
                "id": "may_fourth",
                "label": "五四运动",
                "category": "近代史",
                "period": "1919",
                "level": 1,
                "time": "1919年5月4日",
                "description": "新民主主义开端"
            },
            {
                "id": "cpc_found",
                "label": "中国共产党成立",
                "category": "近代史",
                "period": "1921",
                "level": 1,
                "time": "1921年7月",
                "description": "开天辟地的大事"
            }
        ]
        
        relationships = [
            {"from": "opium_war", "to": "yangwu", "type": "导致"},
            {"from": "yangwu", "to": "xinhai", "type": "推动"},
            {"from": "xinhai", "to": "may_fourth", "type": "促进"},
            {"from": "may_fourth", "to": "cpc_found", "type": "催生"}
        ]
    
    return {"nodes": nodes, "relationships": relationships}


def create_interactive_graph(graph_data):
    """创建交互式图谱"""
    net = Network(height="850px", width="100%", bgcolor="#ffffff", font_color="#333333")
    
    # 配置物理引擎（使用简化参数）
    net.barnes_hut(
        gravity=-80000,
        central_gravity=0.3,
        spring_length=250,
        damping=0.09
    )
    
    # 添加节点
    for node in graph_data['nodes']:
        color = CATEGORY_COLORS.get(node['category'], "#888888")
        size = (50 - (node['level'] - 1) * 10) * 1.5
        
        net.add_node(
            node['id'],
            label=node['label'],
            color=color,
            size=size,
            title=f"{node['label']}\n{node.get('time', '')}",
            borderWidth=3,
            font={"size": 18, "color": "#222", "face": "Microsoft YaHei", "bold": True}
        )
    
    # 添加关系
    for rel in graph_data['relationships']:
        net.add_edge(
            rel['from'],
            rel['to'],
            title=rel.get('type', ''),
            label=rel.get('type', ''),
            color="#999999",
            width=2,
            arrows={"to": {"enabled": True, "scaleFactor": 0.5}},
            font={"size": 14, "color": "#555"},
            smooth=False  # 直线连接
        )
    
    # 配置交互选项
    net.set_options("""
    {
        "nodes": {
            "font": {
                "size": 18,
                "face": "Microsoft YaHei"
            },
            "scaling": {
                "min": 20,
                "max": 80
            }
        },
        "edges": {
            "smooth": false,
            "width": 2
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
                "springLength": 250
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

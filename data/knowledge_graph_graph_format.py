"""
高分子物理知识图谱 - 节点+关系形式
将树形结构转换为节点和关系的数据格式（参考 xjygraph.py 的形式）
"""

from data.knowledge_graph_gfz import GFZ_KNOWLEDGE_GRAPH

# ==================== 颜色配置 ====================
GFZ_CATEGORY_COLORS = {
    "模块": "#FF6B6B",           # 红色 - 一级章节
    "章节": "#4ECDC4",           # 青色 - 二级章节
    "知识点": "#45B7D1",         # 蓝色 - 知识点
    "重要概念": "#96CEB4",       # 绿色 - 重点
    "应用实践": "#FFEAA7"        # 黄色 - 应用
}

def convert_tree_to_graph():
    """
    将树形结构的知识图谱转换为节点+关系形式
    Returns: {"nodes": [...], "relationships": [...]}
    """
    nodes = []
    relationships = []
    
    # 1. 创建模块节点并收集关系
    for module in GFZ_KNOWLEDGE_GRAPH.get("modules", []):
        module_node = {
            "id": module["id"],
            "label": module["name"],
            "category": "模块",
            "level": 1,
            "type": "高分子教学模块",
            "properties": {
                "description": module.get("description", ""),
                "module_order": module["id"].split("_")[-1]
            }
        }
        nodes.append(module_node)
        
        # 2. 创建章节节点
        for chapter in module.get("chapters", []):
            chapter_node = {
                "id": chapter["id"],
                "label": chapter["name"],
                "category": "章节",
                "level": 2,
                "type": "教学章节",
                "properties": {
                    "parent_module": module["id"],
                    "chapter_order": chapter["id"].split("_")[-1]
                }
            }
            nodes.append(chapter_node)
            
            # 模块 -> 章节 的关系
            relationships.append({
                "source": module["id"],
                "target": chapter["id"],
                "type": "包含",
                "properties": {
                    "strength": "强"
                }
            })
            
            # 3. 创建知识点节点
            for kp in chapter.get("knowledge_points", []):
                importance = kp.get("importance", 3)
                
                # 根据重要程度分类
                if importance >= 5:
                    category = "重要概念"
                elif importance <= 3:
                    category = "应用实践"
                else:
                    category = "知识点"
                
                kp_node = {
                    "id": kp["id"],
                    "label": kp["name"],
                    "category": category,
                    "level": 3,
                    "type": "知识点",
                    "properties": {
                        "importance": importance,  # 1-5，5最重要
                        "parent_chapter": chapter["id"],
                        "difficulty": "中等" if importance >= 4 else "简单" if importance <= 2 else "中等",
                    }
                }
                nodes.append(kp_node)
                
                # 章节 -> 知识点 的关系
                relationships.append({
                    "source": chapter["id"],
                    "target": kp["id"],
                    "type": "教学",
                    "properties": {
                        "importance": importance
                    }
                })
    
    # 4. 添加同一章节内知识点的关联关系（相邻知识点）
    chapters_kps = {}
    for relationship in relationships:
        if relationship["type"] == "教学":
            chapter_id = relationship["source"]
            kp_id = relationship["target"]
            if chapter_id not in chapters_kps:
                chapters_kps[chapter_id] = []
            chapters_kps[chapter_id].append(kp_id)
    
    # 为同一章节的相邻知识点添加"相关"关系
    for chapter_id, kp_ids in chapters_kps.items():
        for i in range(len(kp_ids) - 1):
            relationships.append({
                "source": kp_ids[i],
                "target": kp_ids[i + 1],
                "type": "相关",
                "properties": {
                    "order": f"{i} -> {i+1}"
                }
            })
    
    return {
        "metadata": {
            "title": "高分子物理知识图谱",
            "description": "基于《高分子物理（第五版）》教材构建的完整知识图谱",
            "version": "1.0",
            "created_time": "2026-01-06"
        },
        "nodes": nodes,
        "relationships": relationships
    }

# 生成图谱数据
GFZ_KNOWLEDGE_GRAPH_NODES = convert_tree_to_graph()

def get_graph_data():
    """获取图谱数据"""
    return GFZ_KNOWLEDGE_GRAPH_NODES

def get_nodes():
    """获取所有节点"""
    return GFZ_KNOWLEDGE_GRAPH_NODES.get("nodes", [])

def get_relationships():
    """获取所有关系"""
    return GFZ_KNOWLEDGE_GRAPH_NODES.get("relationships", [])

def get_node_by_id(node_id):
    """根据ID获取节点"""
    for node in GFZ_KNOWLEDGE_GRAPH_NODES.get("nodes", []):
        if node["id"] == node_id:
            return node
    return None

def get_related_nodes(node_id):
    """获取与某个节点相关的所有节点"""
    related = {"outgoing": [], "incoming": []}
    
    for rel in GFZ_KNOWLEDGE_GRAPH_NODES.get("relationships", []):
        if rel["source"] == node_id:
            target_node = get_node_by_id(rel["target"])
            if target_node:
                related["outgoing"].append({
                    "node": target_node,
                    "relationship": rel
                })
        elif rel["target"] == node_id:
            source_node = get_node_by_id(rel["source"])
            if source_node:
                related["incoming"].append({
                    "node": source_node,
                    "relationship": rel
                })
    
    return related

def get_nodes_by_category(category):
    """根据分类获取节点"""
    return [node for node in GFZ_KNOWLEDGE_GRAPH_NODES.get("nodes", []) 
            if node["category"] == category]

def get_module_subgraph(module_id):
    """获取特定模块的子图（只包含该模块及其内容）"""
    module_nodes = [n for n in GFZ_KNOWLEDGE_GRAPH_NODES.get("nodes", []) 
                    if n["id"] == module_id or n.get("properties", {}).get("parent_module") == module_id]
    
    module_node_ids = set(n["id"] for n in module_nodes)
    
    module_rels = [r for r in GFZ_KNOWLEDGE_GRAPH_NODES.get("relationships", [])
                   if r["source"] in module_node_ids and r["target"] in module_node_ids]
    
    return {
        "nodes": module_nodes,
        "relationships": module_rels
    }

# 测试用：打印图谱统计
if __name__ == "__main__":
    graph = GFZ_KNOWLEDGE_GRAPH_NODES
    print(f"📊 高分子物理知识图谱统计:")
    print(f"  - 总节点数: {len(graph['nodes'])}")
    print(f"  - 总关系数: {len(graph['relationships'])}")
    
    # 按类别统计
    from collections import Counter
    categories = Counter(n["category"] for n in graph["nodes"])
    print(f"  - 节点分类:")
    for cat, count in categories.items():
        print(f"    • {cat}: {count}")

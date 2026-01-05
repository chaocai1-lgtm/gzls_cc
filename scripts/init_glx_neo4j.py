"""
Neo4j数据库初始化脚本（管理学）
将管理学知识图谱数据导入Neo4j，使用 glx_ 前缀
"""

from neo4j import GraphDatabase
import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.settings import NEO4J_URI, NEO4J_USERNAME, NEO4J_PASSWORD
from data.knowledge_graph import get_knowledge_graph

def init_glx_neo4j():
    """初始化管理学知识图谱到Neo4j"""
    
    driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USERNAME, NEO4J_PASSWORD))
    
    print("🚀 开始初始化Neo4j数据库（管理学 glx_前缀）...")
    
    try:
        with driver.session() as session:
            # 1. 清空旧的glx标签数据
            print("📌 清空旧的glx_数据...")
            session.run("""
                MATCH (n)
                WHERE any(label IN labels(n) WHERE label STARTS WITH 'glx_')
                DETACH DELETE n
            """)
            print("  ✓ 旧数据已清空")
            
            # 2. 获取知识图谱数据
            kg = get_knowledge_graph()
            
            # 3. 创建模块、章节、知识点节点
            print("📌 创建管理学知识图谱...")
            
            module_count = 0
            chapter_count = 0
            knowledge_count = 0
            
            # 遍历各篇（模块）
            for m_idx, module in enumerate(kg.get('children', []), 1):
                module_id = f"M{m_idx}"
                module_name = module.get('name', f'模块{m_idx}')
                
                # 创建模块节点
                session.run("""
                    CREATE (m:glx_Module {
                        id: $id,
                        name: $name
                    })
                """, id=module_id, name=module_name)
                module_count += 1
                
                # 遍历各章
                for c_idx, chapter in enumerate(module.get('children', []), 1):
                    chapter_id = f"C{m_idx}_{c_idx}"
                    chapter_name = chapter.get('name', f'章节{c_idx}')
                    
                    # 创建章节节点并关联到模块
                    session.run("""
                        MATCH (m:glx_Module {id: $module_id})
                        CREATE (c:glx_Chapter {
                            id: $id,
                            name: $name,
                            module_id: $module_id
                        })
                        CREATE (m)-[:CONTAINS]->(c)
                    """, id=chapter_id, name=chapter_name, module_id=module_id)
                    chapter_count += 1
                    
                    # 遍历各知识点
                    for k_idx, knowledge in enumerate(chapter.get('children', []), 1):
                        knowledge_id = f"KP_{m_idx}_{c_idx}_{k_idx}"
                        knowledge_name = knowledge.get('name', f'知识点{k_idx}')
                        importance = knowledge.get('value', 80)
                        
                        # 创建知识点节点并关联到章节
                        session.run("""
                            MATCH (c:glx_Chapter {id: $chapter_id})
                            CREATE (k:glx_Knowledge {
                                id: $id,
                                name: $name,
                                chapter_id: $chapter_id,
                                importance: $importance
                            })
                            CREATE (c)-[:CONTAINS]->(k)
                        """, id=knowledge_id, name=knowledge_name, 
                            chapter_id=chapter_id, importance=importance)
                        knowledge_count += 1
            
            print(f"  ✓ 创建了 {module_count} 个模块")
            print(f"  ✓ 创建了 {chapter_count} 个章节")
            print(f"  ✓ 创建了 {knowledge_count} 个知识点")
            
            # 4. 验证数据
            print("\n📊 数据统计:")
            
            labels_to_check = [
                ('glx_Module', '模块'),
                ('glx_Chapter', '章节'),
                ('glx_Knowledge', '知识点'),
            ]
            
            for label, name in labels_to_check:
                result = session.run(f"MATCH (n:{label}) RETURN count(n) as count")
                count = result.single()['count']
                print(f"  {name}数: {count}")
            
            result = session.run("""
                MATCH ()-[r:CONTAINS]->() 
                RETURN count(r) as count
            """)
            print(f"  CONTAINS关系数: {result.single()['count']}")
            
        print("\n✅ 管理学知识图谱初始化完成！")
        
    except Exception as e:
        print(f"\n❌ 初始化失败: {str(e)}")
        raise
    finally:
        driver.close()

if __name__ == "__main__":
    init_glx_neo4j()

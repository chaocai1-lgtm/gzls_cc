"""
将解析后的历史数据导入Neo4j知识图谱
"""
import json
from pathlib import Path
import sys
from neo4j import GraphDatabase

sys.path.append(str(Path(__file__).parent.parent))

from config.history_config import NEO4J_URI, NEO4J_USERNAME, NEO4J_PASSWORD


class Neo4jImporter:
    """Neo4j数据导入器"""
    
    def __init__(self):
        self.driver = GraphDatabase.driver(
            NEO4J_URI,
            auth=(NEO4J_USERNAME, NEO4J_PASSWORD)
        )
        self.data_dir = Path(__file__).parent.parent / "data" / "parsed"
    
    def close(self):
        self.driver.close()
    
    def clear_database(self):
        """清空数据库"""
        with self.driver.session() as session:
            print("清空现有数据...")
            session.run("MATCH (n) DETACH DELETE n")
            print("数据库已清空")
    
    def create_indexes(self):
        """创建索引以提升查询性能"""
        with self.driver.session() as session:
            print("创建索引...")
            
            indexes = [
                "CREATE INDEX textbook_id IF NOT EXISTS FOR (b:Textbook) ON (b.id)",
                "CREATE INDEX unit_id IF NOT EXISTS FOR (u:Unit) ON (u.id)",
                "CREATE INDEX lesson_id IF NOT EXISTS FOR (l:Lesson) ON (l.id)",
                "CREATE INDEX event_id IF NOT EXISTS FOR (e:HistoricalEvent) ON (e.id)",
                "CREATE INDEX figure_id IF NOT EXISTS FOR (f:HistoricalFigure) ON (f.id)",
                "CREATE INDEX concept_id IF NOT EXISTS FOR (c:Concept) ON (c.id)",
            ]
            
            for index in indexes:
                try:
                    session.run(index)
                except Exception as e:
                    print(f"索引创建警告: {e}")
            
            print("索引创建完成")
    
    def import_all_data(self):
        """导入所有数据"""
        print("="*50)
        print("开始导入数据到Neo4j...")
        print("="*50)
        
        # 1. 导入教科书节点
        self._import_textbooks()
        
        # 2. 导入单元
        self._import_units()
        
        # 3. 导入课文
        self._import_lessons()
        
        # 4. 导入历史事件
        self._import_events()
        
        # 5. 导入历史人物
        self._import_figures()
        
        # 6. 导入概念
        self._import_concepts()
        
        # 7. 创建时间线关系
        self._create_timeline_relationships()
        
        print("\n" + "="*50)
        print("数据导入完成！")
        print("="*50)
        
        # 显示统计信息
        self._show_statistics()
    
    def _import_textbooks(self):
        """导入教科书节点"""
        from config.history_config import TEXTBOOKS
        
        print("\n[1/7] 导入教科书...")
        
        with self.driver.session() as session:
            for book_id, book_info in TEXTBOOKS.items():
                session.run("""
                    CREATE (b:Textbook {
                        id: $id,
                        name: $name,
                        type: $type,
                        description: $description
                    })
                """, id=book_id, **book_info)
        
        print(f"  导入了 {len(TEXTBOOKS)} 本教科书")
    
    def _import_units(self):
        """导入单元"""
        print("\n[2/7] 导入单元...")
        
        units_file = self.data_dir / "units.json"
        if not units_file.exists():
            print("  警告: units.json 不存在")
            return
        
        with open(units_file, 'r', encoding='utf-8') as f:
            units = json.load(f)
        
        with self.driver.session() as session:
            for unit in units:
                # 创建单元节点
                session.run("""
                    CREATE (u:Unit {
                        id: $id,
                        book_id: $book_id,
                        book_name: $book_name,
                        unit_number: $unit_number,
                        title: $title
                    })
                """, **unit)
                
                # 创建教科书与单元的关系
                session.run("""
                    MATCH (b:Textbook {id: $book_id})
                    MATCH (u:Unit {id: $unit_id})
                    CREATE (b)-[:HAS_UNIT]->(u)
                """, book_id=unit['book_id'], unit_id=unit['id'])
        
        print(f"  导入了 {len(units)} 个单元")
    
    def _import_lessons(self):
        """导入课文"""
        print("\n[3/7] 导入课文...")
        
        lessons_file = self.data_dir / "lessons.json"
        if not lessons_file.exists():
            print("  警告: lessons.json 不存在")
            return
        
        with open(lessons_file, 'r', encoding='utf-8') as f:
            lessons = json.load(f)
        
        with self.driver.session() as session:
            for lesson in lessons:
                # 创建课文节点（不包含完整内容，太大）
                session.run("""
                    CREATE (l:Lesson {
                        id: $id,
                        book_id: $book_id,
                        book_name: $book_name,
                        unit_id: $unit_id,
                        lesson_number: $lesson_number,
                        title: $title,
                        content_preview: $content_preview
                    })
                """, 
                    id=lesson['id'],
                    book_id=lesson['book_id'],
                    book_name=lesson['book_name'],
                    unit_id=lesson.get('unit_id'),
                    lesson_number=lesson['lesson_number'],
                    title=lesson['title'],
                    content_preview=lesson['content'][:200] if lesson.get('content') else ""
                )
                
                # 创建单元与课文的关系
                if lesson.get('unit_id'):
                    session.run("""
                        MATCH (u:Unit {id: $unit_id})
                        MATCH (l:Lesson {id: $lesson_id})
                        CREATE (u)-[:HAS_LESSON]->(l)
                    """, unit_id=lesson['unit_id'], lesson_id=lesson['id'])
        
        print(f"  导入了 {len(lessons)} 课")
    
    def _import_events(self):
        """导入历史事件"""
        print("\n[4/7] 导入历史事件...")
        
        events_file = self.data_dir / "historical_events.json"
        if not events_file.exists():
            print("  警告: historical_events.json 不存在")
            return
        
        with open(events_file, 'r', encoding='utf-8') as f:
            events = json.load(f)
        
        with self.driver.session() as session:
            for event in events:
                # 创建事件节点
                session.run("""
                    CREATE (e:HistoricalEvent {
                        id: $id,
                        year: $year,
                        description: $description,
                        lesson_id: $lesson_id,
                        book_id: $book_id
                    })
                """, **event)
                
                # 创建课文与事件的关系
                session.run("""
                    MATCH (l:Lesson {id: $lesson_id})
                    MATCH (e:HistoricalEvent {id: $event_id})
                    CREATE (l)-[:MENTIONS_EVENT]->(e)
                """, lesson_id=event['lesson_id'], event_id=event['id'])
        
        print(f"  导入了 {len(events)} 个历史事件")
    
    def _import_figures(self):
        """导入历史人物"""
        print("\n[5/7] 导入历史人物...")
        
        figures_file = self.data_dir / "historical_figures.json"
        if not figures_file.exists():
            print("  警告: historical_figures.json 不存在")
            return
        
        with open(figures_file, 'r', encoding='utf-8') as f:
            figures = json.load(f)
        
        with self.driver.session() as session:
            for figure in figures:
                # 创建人物节点
                session.run("""
                    MERGE (f:HistoricalFigure {id: $id})
                    SET f.name = $name,
                        f.description = $description,
                        f.lesson_id = $lesson_id,
                        f.book_id = $book_id
                """, **figure)
                
                # 创建课文与人物的关系
                session.run("""
                    MATCH (l:Lesson {id: $lesson_id})
                    MATCH (f:HistoricalFigure {id: $figure_id})
                    MERGE (l)-[:MENTIONS_FIGURE]->(f)
                """, lesson_id=figure['lesson_id'], figure_id=figure['id'])
        
        print(f"  导入了 {len(figures)} 个历史人物")
    
    def _import_concepts(self):
        """导入概念"""
        print("\n[6/7] 导入概念...")
        
        concepts_file = self.data_dir / "concepts.json"
        if not concepts_file.exists():
            print("  警告: concepts.json 不存在")
            return
        
        with open(concepts_file, 'r', encoding='utf-8') as f:
            concepts = json.load(f)
        
        with self.driver.session() as session:
            for concept in concepts:
                # 创建概念节点
                session.run("""
                    CREATE (c:Concept {
                        id: $id,
                        term: $term,
                        lesson_id: $lesson_id,
                        book_id: $book_id
                    })
                """, **concept)
                
                # 创建课文与概念的关系
                session.run("""
                    MATCH (l:Lesson {id: $lesson_id})
                    MATCH (c:Concept {id: $concept_id})
                    CREATE (l)-[:DEFINES_CONCEPT]->(c)
                """, lesson_id=concept['lesson_id'], concept_id=concept['id'])
        
        print(f"  导入了 {len(concepts)} 个概念")
    
    def _create_timeline_relationships(self):
        """创建时间线关系（事件之间的先后顺序）"""
        print("\n[7/7] 创建时间线关系...")
        
        with self.driver.session() as session:
            # 根据年份排序，创建NEXT关系
            result = session.run("""
                MATCH (e:HistoricalEvent)
                WHERE e.year IS NOT NULL
                WITH e ORDER BY toInteger(e.year)
                WITH collect(e) as events
                UNWIND range(0, size(events)-2) as i
                WITH events[i] as e1, events[i+1] as e2
                MERGE (e1)-[:NEXT]->(e2)
                RETURN count(*) as count
            """)
            
            record = result.single()
            count = record['count'] if record else 0
            print(f"  创建了 {count} 个时间线关系")
    
    def _show_statistics(self):
        """显示数据库统计信息"""
        print("\n数据库统计:")
        print("-"*50)
        
        with self.driver.session() as session:
            # 统计各类节点数量
            stats_queries = {
                "教科书": "MATCH (n:Textbook) RETURN count(n) as count",
                "单元": "MATCH (n:Unit) RETURN count(n) as count",
                "课文": "MATCH (n:Lesson) RETURN count(n) as count",
                "历史事件": "MATCH (n:HistoricalEvent) RETURN count(n) as count",
                "历史人物": "MATCH (n:HistoricalFigure) RETURN count(n) as count",
                "概念": "MATCH (n:Concept) RETURN count(n) as count",
            }
            
            for name, query in stats_queries.items():
                result = session.run(query)
                record = result.single()
                count = record['count'] if record else 0
                print(f"{name}: {count}")


def main():
    importer = Neo4jImporter()
    
    try:
        # 清空数据库
        response = input("是否清空现有数据库？(yes/no): ")
        if response.lower() == 'yes':
            importer.clear_database()
        
        # 创建索引
        importer.create_indexes()
        
        # 导入所有数据
        importer.import_all_data()
        
    finally:
        importer.close()


if __name__ == "__main__":
    main()

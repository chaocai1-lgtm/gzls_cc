"""
将解析后的历史数据导入Elasticsearch
"""
import json
from pathlib import Path
import sys
from elasticsearch import Elasticsearch

sys.path.append(str(Path(__file__).parent.parent))

from config.history_config import (
    ES_CLOUD_ID, ES_USERNAME, ES_PASSWORD,
    ES_INDEX_KNOWLEDGE, ES_INDEX_LESSONS, ES_INDEX_QUESTIONS, ES_INDEX_EVENTS
)


class ElasticsearchImporter:
    """Elasticsearch数据导入器"""
    
    def __init__(self):
        self.es = Elasticsearch(
            cloud_id=ES_CLOUD_ID,
            basic_auth=(ES_USERNAME, ES_PASSWORD)
        )
        self.data_dir = Path(__file__).parent.parent / "data" / "parsed"
        
        # 检查连接
        if not self.es.ping():
            raise Exception("无法连接到Elasticsearch")
        
        print("成功连接到Elasticsearch")
    
    def create_indexes(self):
        """创建索引及映射"""
        print("\n创建索引...")
        
        # 1. 知识点索引
        if not self.es.indices.exists(index=ES_INDEX_KNOWLEDGE):
            self.es.indices.create(
                index=ES_INDEX_KNOWLEDGE,
                body={
                    "mappings": {
                        "properties": {
                            "id": {"type": "keyword"},
                            "term": {"type": "text", "analyzer": "ik_max_word"},
                            "description": {"type": "text", "analyzer": "ik_max_word"},
                            "category": {"type": "keyword"},
                            "lesson_id": {"type": "keyword"},
                            "book_id": {"type": "keyword"}
                        }
                    }
                }
            )
            print(f"  创建索引: {ES_INDEX_KNOWLEDGE}")
        
        # 2. 课文内容索引
        if not self.es.indices.exists(index=ES_INDEX_LESSONS):
            self.es.indices.create(
                index=ES_INDEX_LESSONS,
                body={
                    "mappings": {
                        "properties": {
                            "id": {"type": "keyword"},
                            "title": {"type": "text", "analyzer": "ik_max_word"},
                            "content": {"type": "text", "analyzer": "ik_max_word"},
                            "book_id": {"type": "keyword"},
                            "book_name": {"type": "text"},
                            "unit_id": {"type": "keyword"},
                            "lesson_number": {"type": "integer"}
                        }
                    }
                }
            )
            print(f"  创建索引: {ES_INDEX_LESSONS}")
        
        # 3. 历史事件索引
        if not self.es.indices.exists(index=ES_INDEX_EVENTS):
            self.es.indices.create(
                index=ES_INDEX_EVENTS,
                body={
                    "mappings": {
                        "properties": {
                            "id": {"type": "keyword"},
                            "year": {"type": "keyword"},
                            "description": {"type": "text", "analyzer": "ik_max_word"},
                            "lesson_id": {"type": "keyword"},
                            "book_id": {"type": "keyword"},
                            "figures": {"type": "text"},  # 相关人物
                            "concepts": {"type": "text"}  # 相关概念
                        }
                    }
                }
            )
            print(f"  创建索引: {ES_INDEX_EVENTS}")
    
    def import_all_data(self):
        """导入所有数据"""
        print("="*50)
        print("开始导入数据到Elasticsearch...")
        print("="*50)
        
        # 1. 导入课文内容
        self._import_lessons()
        
        # 2. 导入历史事件
        self._import_events()
        
        # 3. 导入概念（作为知识点）
        self._import_concepts()
        
        # 4. 导入历史人物（作为知识点）
        self._import_figures()
        
        print("\n" + "="*50)
        print("数据导入完成！")
        print("="*50)
        
        # 显示统计信息
        self._show_statistics()
    
    def _import_lessons(self):
        """导入课文内容"""
        print("\n[1/4] 导入课文内容...")
        
        lessons_file = self.data_dir / "lessons.json"
        if not lessons_file.exists():
            print("  警告: lessons.json 不存在")
            return
        
        with open(lessons_file, 'r', encoding='utf-8') as f:
            lessons = json.load(f)
        
        count = 0
        for lesson in lessons:
            doc = {
                "id": lesson['id'],
                "title": lesson['title'],
                "content": lesson.get('content', ''),
                "book_id": lesson['book_id'],
                "book_name": lesson['book_name'],
                "unit_id": lesson.get('unit_id'),
                "lesson_number": lesson['lesson_number']
            }
            
            self.es.index(
                index=ES_INDEX_LESSONS,
                id=lesson['id'],
                document=doc
            )
            count += 1
        
        print(f"  导入了 {count} 课内容")
    
    def _import_events(self):
        """导入历史事件"""
        print("\n[2/4] 导入历史事件...")
        
        events_file = self.data_dir / "historical_events.json"
        if not events_file.exists():
            print("  警告: historical_events.json 不存在")
            return
        
        with open(events_file, 'r', encoding='utf-8') as f:
            events = json.load(f)
        
        count = 0
        for event in events:
            doc = {
                "id": event['id'],
                "year": event['year'],
                "description": event['description'],
                "lesson_id": event['lesson_id'],
                "book_id": event['book_id']
            }
            
            self.es.index(
                index=ES_INDEX_EVENTS,
                id=event['id'],
                document=doc
            )
            count += 1
        
        print(f"  导入了 {count} 个历史事件")
    
    def _import_concepts(self):
        """导入概念"""
        print("\n[3/4] 导入概念...")
        
        concepts_file = self.data_dir / "concepts.json"
        if not concepts_file.exists():
            print("  警告: concepts.json 不存在")
            return
        
        with open(concepts_file, 'r', encoding='utf-8') as f:
            concepts = json.load(f)
        
        count = 0
        for concept in concepts:
            doc = {
                "id": concept['id'],
                "term": concept['term'],
                "description": "",
                "category": "概念",
                "lesson_id": concept['lesson_id'],
                "book_id": concept['book_id']
            }
            
            self.es.index(
                index=ES_INDEX_KNOWLEDGE,
                id=concept['id'],
                document=doc
            )
            count += 1
        
        print(f"  导入了 {count} 个概念")
    
    def _import_figures(self):
        """导入历史人物"""
        print("\n[4/4] 导入历史人物...")
        
        figures_file = self.data_dir / "historical_figures.json"
        if not figures_file.exists():
            print("  警告: historical_figures.json 不存在")
            return
        
        with open(figures_file, 'r', encoding='utf-8') as f:
            figures = json.load(f)
        
        count = 0
        for figure in figures:
            doc = {
                "id": figure['id'],
                "term": figure['name'],
                "description": figure['description'],
                "category": "历史人物",
                "lesson_id": figure['lesson_id'],
                "book_id": figure['book_id']
            }
            
            self.es.index(
                index=ES_INDEX_KNOWLEDGE,
                id=figure['id'],
                document=doc
            )
            count += 1
        
        print(f"  导入了 {count} 个历史人物")
    
    def _show_statistics(self):
        """显示索引统计信息"""
        print("\nElasticsearch索引统计:")
        print("-"*50)
        
        indexes = [
            ES_INDEX_KNOWLEDGE,
            ES_INDEX_LESSONS,
            ES_INDEX_EVENTS
        ]
        
        for index in indexes:
            try:
                count = self.es.count(index=index)['count']
                print(f"{index}: {count} 条文档")
            except Exception as e:
                print(f"{index}: 错误 - {e}")
    
    def test_search(self):
        """测试搜索功能"""
        print("\n" + "="*50)
        print("测试搜索功能")
        print("="*50)
        
        # 测试1: 搜索课文内容
        print("\n[测试1] 搜索课文: '秦始皇'")
        result = self.es.search(
            index=ES_INDEX_LESSONS,
            body={
                "query": {
                    "match": {
                        "content": "秦始皇"
                    }
                },
                "size": 3
            }
        )
        
        print(f"找到 {result['hits']['total']['value']} 条结果")
        for hit in result['hits']['hits']:
            print(f"  - {hit['_source']['title']}")
        
        # 测试2: 搜索历史事件
        print("\n[测试2] 搜索历史事件: '221'")
        result = self.es.search(
            index=ES_INDEX_EVENTS,
            body={
                "query": {
                    "match": {
                        "year": "221"
                    }
                },
                "size": 5
            }
        )
        
        print(f"找到 {result['hits']['total']['value']} 条结果")
        for hit in result['hits']['hits']:
            print(f"  - {hit['_source']['year']}: {hit['_source']['description']}")


def main():
    importer = ElasticsearchImporter()
    
    # 创建索引
    importer.create_indexes()
    
    # 导入所有数据
    importer.import_all_data()
    
    # 测试搜索
    importer.test_search()


if __name__ == "__main__":
    main()

"""
解析高中历史教科书，提取结构化数据
"""
import re
import json
from pathlib import Path
import sys

# 添加父目录到路径
sys.path.append(str(Path(__file__).parent.parent))

from config.history_config import TEXTBOOKS, KNOWLEDGE_CATEGORIES, TIME_PERIODS


class TextbookParser:
    """教科书解析器"""
    
    def __init__(self, textbook_root):
        self.textbook_root = Path(textbook_root)
        self.parsed_data = {
            "units": [],
            "lessons": [],
            "knowledge_points": [],
            "historical_events": [],
            "historical_figures": [],
            "concepts": []
        }
    
    def parse_all_textbooks(self):
        """解析所有教科书"""
        print("开始解析教科书...")
        
        for book_id, book_info in TEXTBOOKS.items():
            print(f"\n正在解析: {book_info['name']}")
            file_path = self.textbook_root / book_info['file']
            
            if not file_path.exists():
                print(f"警告: 文件不存在 {file_path}")
                continue
            
            # 读取文件内容
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 解析内容
            self._parse_textbook(content, book_id, book_info)
        
        # 保存解析结果
        self._save_parsed_data()
        
        return self.parsed_data
    
    def _parse_textbook(self, content, book_id, book_info):
        """解析单个教科书"""
        # 按页分割
        pages = re.split(r'--- 第 \d+ 页 ---', content)
        
        current_unit = None
        current_lesson = None
        lesson_content = []
        
        for page in pages:
            page = page.strip()
            if not page:
                continue
            
            # 检测单元标题
            unit_match = re.search(r'第([一二三四五六七八九十]+)单元\s+(.+)', page)
            if unit_match:
                # 保存上一课的内容
                if current_lesson and lesson_content:
                    self._extract_knowledge_from_lesson(
                        current_lesson, '\n'.join(lesson_content), book_id
                    )
                    lesson_content = []
                
                unit_number = self._chinese_to_number(unit_match.group(1))
                unit_title = unit_match.group(2).strip()
                
                current_unit = {
                    "id": f"{book_id}_unit_{unit_number}",
                    "book_id": book_id,
                    "book_name": book_info['name'],
                    "unit_number": unit_number,
                    "title": unit_title,
                    "lessons": []
                }
                self.parsed_data["units"].append(current_unit)
                print(f"  发现单元: 第{unit_number}单元 {unit_title}")
                continue
            
            # 检测课标题
            lesson_match = re.search(r'第(\d+)课\s+(.+)', page)
            if lesson_match:
                # 保存上一课的内容
                if current_lesson and lesson_content:
                    self._extract_knowledge_from_lesson(
                        current_lesson, '\n'.join(lesson_content), book_id
                    )
                    lesson_content = []
                
                lesson_number = int(lesson_match.group(1))
                lesson_title = lesson_match.group(2).strip()
                
                current_lesson = {
                    "id": f"{book_id}_lesson_{lesson_number}",
                    "book_id": book_id,
                    "book_name": book_info['name'],
                    "unit_id": current_unit['id'] if current_unit else None,
                    "lesson_number": lesson_number,
                    "title": lesson_title,
                    "content": "",
                    "knowledge_points": []
                }
                
                if current_unit:
                    current_unit['lessons'].append(current_lesson['id'])
                
                self.parsed_data["lessons"].append(current_lesson)
                print(f"    发现课文: 第{lesson_number}课 {lesson_title}")
            
            # 累积课文内容
            if current_lesson:
                lesson_content.append(page)
        
        # 保存最后一课的内容
        if current_lesson and lesson_content:
            self._extract_knowledge_from_lesson(
                current_lesson, '\n'.join(lesson_content), book_id
            )
    
    def _extract_knowledge_from_lesson(self, lesson, content, book_id):
        """从课文中提取知识点"""
        lesson['content'] = content
        
        # 提取历史事件（简单规则）
        # 匹配年份 + 事件描述
        event_patterns = [
            r'(\d{4})年\s*([^。，；！？\n]{4,30})',
            r'公元前?(\d+)年\s*([^。，；！？\n]{4,30})',
        ]
        
        for pattern in event_patterns:
            matches = re.findall(pattern, content)
            for match in matches:
                year = match[0]
                description = match[1].strip()
                
                # 过滤掉目录等
                if len(description) < 4 or '第' in description[:2]:
                    continue
                
                event = {
                    "id": f"event_{book_id}_{len(self.parsed_data['historical_events'])}",
                    "lesson_id": lesson['id'],
                    "year": year,
                    "description": description,
                    "book_id": book_id
                }
                self.parsed_data['historical_events'].append(event)
                lesson['knowledge_points'].append(event['id'])
        
        # 提取历史人物（简单规则 - 查找常见历史人物名）
        # 这里需要一个历史人物名单，暂时用简单匹配
        figure_keywords = [
            '秦始皇', '汉武帝', '唐太宗', '康熙', '乾隆', '慈禧',
            '孙中山', '毛泽东', '邓小平', '马克思', '恩格斯', '列宁',
            '华盛顿', '拿破仑', '林肯', '罗斯福', '丘吉尔', '斯大林'
        ]
        
        for keyword in figure_keywords:
            if keyword in content:
                # 提取相关句子
                sentences = re.findall(f'[^。；！？]*{keyword}[^。；！？]*[。；！？]', content)
                if sentences:
                    figure = {
                        "id": f"figure_{book_id}_{keyword}",
                        "name": keyword,
                        "lesson_id": lesson['id'],
                        "description": sentences[0][:100],
                        "book_id": book_id
                    }
                    
                    # 避免重复
                    if not any(f['id'] == figure['id'] for f in self.parsed_data['historical_figures']):
                        self.parsed_data['historical_figures'].append(figure)
                        lesson['knowledge_points'].append(figure['id'])
        
        # 提取概念（匹配特殊标记或关键词）
        concept_patterns = [
            r'【([^】]{2,10})】',  # 方括号标记
            r'"([^"]{3,15})"',  # 双引号标记
        ]
        
        for pattern in concept_patterns:
            matches = re.findall(pattern, content)
            for match in matches[:5]:  # 限制每课提取数量
                concept = {
                    "id": f"concept_{book_id}_{len(self.parsed_data['concepts'])}",
                    "term": match.strip(),
                    "lesson_id": lesson['id'],
                    "book_id": book_id
                }
                self.parsed_data['concepts'].append(concept)
    
    def _chinese_to_number(self, chinese_num):
        """将中文数字转换为阿拉伯数字"""
        chinese_dict = {
            '一': 1, '二': 2, '三': 3, '四': 4, '五': 5,
            '六': 6, '七': 7, '八': 8, '九': 9, '十': 10,
            '十一': 11
        }
        return chinese_dict.get(chinese_num, 0)
    
    def _save_parsed_data(self):
        """保存解析后的数据"""
        output_dir = self.textbook_root / "初中历史自适应学习系统" / "data" / "parsed"
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # 保存各类数据
        for key, data in self.parsed_data.items():
            output_file = output_dir / f"{key}.json"
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"\n已保存: {output_file} ({len(data)} 条)")
        
        # 保存统计信息
        stats = {
            "total_units": len(self.parsed_data['units']),
            "total_lessons": len(self.parsed_data['lessons']),
            "total_knowledge_points": len(self.parsed_data['knowledge_points']),
            "total_events": len(self.parsed_data['historical_events']),
            "total_figures": len(self.parsed_data['historical_figures']),
            "total_concepts": len(self.parsed_data['concepts'])
        }
        
        stats_file = output_dir / "stats.json"
        with open(stats_file, 'w', encoding='utf-8') as f:
            json.dump(stats, f, ensure_ascii=False, indent=2)
        
        print("\n" + "="*50)
        print("解析完成！统计信息:")
        print("="*50)
        for key, value in stats.items():
            print(f"{key}: {value}")


def main():
    # 设置教科书根目录
    textbook_root = Path(__file__).parent.parent.parent
    
    parser = TextbookParser(textbook_root)
    parser.parse_all_textbooks()


if __name__ == "__main__":
    main()

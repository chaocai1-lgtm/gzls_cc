"""
高中历史学习系统 - 数据导入主脚本
自动执行：解析教科书 -> 导入Neo4j -> 导入Elasticsearch
"""
import sys
from pathlib import Path

# 添加父目录到路径
sys.path.append(str(Path(__file__).parent.parent))

def main():
    print("="*70)
    print(" "*15 + "高中历史学习系统 - 数据导入工具")
    print("="*70)
    print()
    
    # 步骤1: 解析教科书
    print("【步骤 1/3】 解析教科书内容...")
    print("-"*70)
    try:
        from parse_textbooks import TextbookParser
        
        textbook_root = Path(__file__).parent.parent.parent
        parser = TextbookParser(textbook_root)
        parsed_data = parser.parse_all_textbooks()
        
        print("\n✓ 教科书解析完成")
    except Exception as e:
        print(f"\n✗ 教科书解析失败: {e}")
        print("\n请确保教科书文件存在于正确的路径")
        return
    
    print("\n" + "="*70)
    
    # 步骤2: 导入Neo4j
    print("\n【步骤 2/3】 导入数据到 Neo4j 知识图谱...")
    print("-"*70)
    try:
        from import_to_neo4j import Neo4jImporter
        
        neo4j_importer = Neo4jImporter()
        
        # 询问是否清空数据库
        response = input("\n是否清空现有Neo4j数据？(yes/no，默认no): ").strip().lower()
        if response == 'yes':
            neo4j_importer.clear_database()
        
        neo4j_importer.create_indexes()
        neo4j_importer.import_all_data()
        neo4j_importer.close()
        
        print("\n✓ Neo4j 数据导入完成")
    except Exception as e:
        print(f"\n✗ Neo4j 导入失败: {e}")
        print("\n请检查:")
        print("  1. Neo4j 服务是否运行")
        print("  2. config/history_config.py 中的连接配置是否正确")
        print("  3. 是否安装了 neo4j 驱动: pip install neo4j")
    
    print("\n" + "="*70)
    
    # 步骤3: 导入Elasticsearch
    print("\n【步骤 3/3】 导入数据到 Elasticsearch 搜索引擎...")
    print("-"*70)
    try:
        from import_to_elasticsearch import ElasticsearchImporter
        
        es_importer = ElasticsearchImporter()
        es_importer.create_indexes()
        es_importer.import_all_data()
        
        print("\n✓ Elasticsearch 数据导入完成")
        
        # 测试搜索
        print("\n正在测试搜索功能...")
        es_importer.test_search()
        
    except Exception as e:
        print(f"\n✗ Elasticsearch 导入失败: {e}")
        print("\n请检查:")
        print("  1. Elasticsearch 云服务是否可访问")
        print("  2. config/history_config.py 中的连接配置是否正确")
        print("  3. 是否安装了 elasticsearch 库: pip install elasticsearch")
    
    print("\n" + "="*70)
    print(" "*20 + "数据导入流程完成！")
    print("="*70)
    print()
    print("接下来:")
    print("  1. 运行 streamlit run app.py 启动系统")
    print("  2. 在浏览器中访问学习系统")
    print()


if __name__ == "__main__":
    main()

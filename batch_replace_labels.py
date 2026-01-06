"""
批量替换数据库标签为GFZ前缀的脚本
将所有 mfx_ 和 glx_ 标签替换为 gfz_ 标签
"""

import os
import re
from pathlib import Path

# 需要替换的标签映射
LABEL_MAPPINGS = {
    # mfx标签 -> gfz标签
    'mfx_Student': 'gfz_Student',
    'mfx_Activity': 'gfz_Activity',
    'mfx_Question': 'gfz_Question',
    'mfx_Ability': 'gfz_Ability',
    'mfx_Knowledge': 'gfz_KnowledgePoint',
    'mfx_Case': 'gfz_Case',
    
    # glx标签 -> gfz标签
    'glx_Module': 'gfz_Module',
    'glx_Chapter': 'gfz_Chapter',
    'glx_Section': 'gfz_Section',
    'glx_Knowledge': 'gfz_KnowledgePoint',
}

def replace_labels_in_file(file_path):
    """在单个文件中替换标签"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        modified = False
        
        # 替换每个标签
        for old_label, new_label in LABEL_MAPPINGS.items():
            # 替换格式：:label 和 (label)
            # 例如: :mfx_Student -> :gfz_Student
            #      (mfx_Student -> (gfz_Student
            if old_label in content:
                content = content.replace(f':{old_label}', f':{new_label}')
                content = content.replace(f'({old_label}', f'({new_label}')
                content = content.replace(f'`{old_label}`', f'`{new_label}`')
                modified = True
        
        # 如果有修改，写回文件
        if modified and content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f'✓ 已更新: {file_path}')
            return True
        return False
            
    except Exception as e:
        print(f'✗ 处理失败 {file_path}: {e}')
        return False

def process_directory(directory):
    """处理目录下的所有Python文件"""
    directory = Path(directory)
    updated_files = []
    
    for py_file in directory.rglob('*.py'):
        # 跳过 __pycache__ 目录
        if '__pycache__' in str(py_file):
            continue
            
        if replace_labels_in_file(py_file):
            updated_files.append(str(py_file))
    
    return updated_files

if __name__ == '__main__':
    # 获取脚本所在目录的父目录（项目根目录）
    project_root = Path(__file__).parent
    
    print('=' * 60)
    print('开始批量替换数据库标签为 GFZ 前缀')
    print('=' * 60)
    print()
    
    # 处理 modules 目录
    print('📁 处理 modules/ 目录...')
    modules_dir = project_root / 'modules'
    if modules_dir.exists():
        updated = process_directory(modules_dir)
        print(f'   更新了 {len(updated)} 个文件')
    else:
        print('   ⚠️  目录不存在')
    
    print()
    
    # 处理 data 目录
    print('📁 处理 data/ 目录...')
    data_dir = project_root / 'data'
    if data_dir.exists():
        updated = process_directory(data_dir)
        print(f'   更新了 {len(updated)} 个文件')
    else:
        print('   ⚠️  目录不存在')
    
    print()
    
    # 处理 scripts 目录
    print('📁 处理 scripts/ 目录...')
    scripts_dir = project_root / 'scripts'
    if scripts_dir.exists():
        updated = process_directory(scripts_dir)
        print(f'   更新了 {len(updated)} 个文件')
    else:
        print('   ⚠️  目录不存在')
    
    print()
    print('=' * 60)
    print('✓ 批量替换完成！')
    print('=' * 60)
    print()
    print('⚠️  重要提醒：')
    print('1. 请检查修改后的代码是否正确')
    print('2. 确保Neo4j数据库中使用的是 gfz_ 前缀的标签')
    print('3. 运行测试确保系统正常工作')
    print()
    print('下一步：')
    print('1. 检查 config/settings.py 中的配置是否正确')
    print('2. 更新 Neo4j 数据库中的标签（如果需要）')
    print('3. 运行 app.py 测试系统')

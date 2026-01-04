"""
民法学系统配置检查脚本
运行此脚本验证系统配置是否正确
"""

import os
import sys

def check_files():
    """检查必需文件是否存在"""
    print("=" * 50)
    print("📁 检查文件结构...")
    print("=" * 50)
    
    required_files = [
        "app.py",
        "requirements.txt",
        "README.md",
        "modules/auth.py",
        "modules/case_library.py",
        "modules/knowledge_graph.py",
        "modules/ability_recommender.py",
        "modules/classroom_interaction.py",
        "data/cases.py",
        "data/knowledge_graph.py",
        "data/abilities.py",
        "config/settings.py"
    ]
    
    all_exist = True
    for file in required_files:
        if os.path.exists(file):
            print(f"✅ {file}")
        else:
            print(f"❌ {file} - 缺失！")
            all_exist = False
    
    return all_exist

def check_labels():
    """检查数据库标签是否正确替换"""
    print("\n" + "=" * 50)
    print("🏷️  检查数据库标签...")
    print("=" * 50)
    
    files_to_check = [
        "modules/auth.py",
        "modules/case_library.py",
        "modules/knowledge_graph.py",
        "modules/ability_recommender.py",
        "modules/classroom_interaction.py"
    ]
    
    all_correct = True
    for file in files_to_check:
        try:
            with open(file, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # 检查是否还有旧标签
            if 'glx_Student' in content or 'glx_Activity' in content:
                print(f"❌ {file} - 仍包含旧标签 glx_")
                all_correct = False
            # 检查是否有新标签
            elif 'mfx_Student' in content or 'mfx_Activity' in content:
                print(f"✅ {file} - 标签已更新为 mfx_")
            else:
                print(f"⚠️  {file} - 未找到数据库标签")
        except Exception as e:
            print(f"❌ {file} - 读取错误: {e}")
            all_correct = False
    
    return all_correct

def check_content():
    """检查内容是否正确替换"""
    print("\n" + "=" * 50)
    print("📝 检查课程内容...")
    print("=" * 50)
    
    checks = [
        ("data/cases.py", ["民间借贷", "高空抛物", "离婚财产"], ["管理炎", "牙龈"]),
        ("data/knowledge_graph.py", ["民法典", "物权", "合同"], ["管理病", "牙龈炎"]),
        ("data/abilities.py", ["民法总则", "物权法律", "合同法律"], ["管理诊断", "治疗方案"])
    ]
    
    all_correct = True
    for file, should_have, should_not_have in checks:
        try:
            with open(file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            has_correct = any(keyword in content for keyword in should_have)
            has_wrong = any(keyword in content for keyword in should_not_have)
            
            if has_correct and not has_wrong:
                print(f"✅ {file} - 内容正确")
            elif has_wrong:
                print(f"❌ {file} - 仍包含旧内容（医学相关）")
                all_correct = False
            else:
                print(f"⚠️  {file} - 内容可能不完整")
        except Exception as e:
            print(f"❌ {file} - 读取错误: {e}")
            all_correct = False
    
    return all_correct

def check_git():
    """检查Git状态"""
    print("\n" + "=" * 50)
    print("🔧 检查Git仓库...")
    print("=" * 50)
    
    if os.path.exists(".git"):
        print("✅ Git仓库已初始化")
        
        # 检查远程仓库
        import subprocess
        try:
            result = subprocess.run(
                ["git", "remote", "-v"],
                capture_output=True,
                text=True,
                check=True
            )
            if result.stdout.strip():
                print("✅ 已配置远程仓库:")
                print(result.stdout)
            else:
                print("⚠️  尚未配置远程仓库")
                print("   运行: git remote add origin <repo-url>")
        except:
            print("⚠️  无法检查远程仓库状态")
        
        return True
    else:
        print("❌ Git仓库未初始化")
        print("   运行: git init")
        return False

def main():
    """主检查函数"""
    print("\n🎯 民法学系统配置检查")
    print("=" * 50)
    
    results = []
    
    # 执行各项检查
    results.append(("文件结构", check_files()))
    results.append(("数据库标签", check_labels()))
    results.append(("课程内容", check_content()))
    results.append(("Git仓库", check_git()))
    
    # 总结
    print("\n" + "=" * 50)
    print("📊 检查结果汇总")
    print("=" * 50)
    
    all_passed = all(result[1] for result in results)
    
    for name, passed in results:
        status = "✅ 通过" if passed else "❌ 未通过"
        print(f"{status} - {name}")
    
    print("\n" + "=" * 50)
    if all_passed:
        print("🎉 所有检查通过！系统已准备就绪。")
        print("\n📋 下一步:")
        print("1. 在GitHub创建新仓库 mfx_system")
        print("2. git remote add origin <repo-url>")
        print("3. git push -u origin main")
        print("4. 在Streamlit Cloud部署")
    else:
        print("⚠️  部分检查未通过，请根据上述提示修复。")
    print("=" * 50)

if __name__ == "__main__":
    main()

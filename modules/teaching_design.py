"""
教学方案设计模块
根据知识图谱章节和教学方法，使用 DeepSeek AI 生成教学设计方案
"""

import streamlit as st
from datetime import datetime
from openai import OpenAI
from config.settings import *

# 教学方法列表及其描述
TEACHING_METHODS = {
    "PBL（问题导向学习）": {
        "name": "PBL（Problem-Based Learning）",
        "description": "以问题为导向的学习方法，通过真实情境问题激发学生主动学习",
        "key_elements": ["问题情境设计", "小组协作", "自主探究", "成果展示", "反思评价"]
    },
    "BOPPPS": {
        "name": "BOPPPS教学模型",
        "description": "包含导入、目标、前测、参与式学习、后测、总结六个环节的教学模型",
        "key_elements": ["Bridge-in导入", "Objective目标", "Pre-assessment前测", "Participatory Learning参与式学习", "Post-assessment后测", "Summary总结"]
    },
    "OBE（成果导向教育）": {
        "name": "OBE（Outcome-Based Education）",
        "description": "以学习成果为导向的教育模式，强调能力目标的达成",
        "key_elements": ["明确学习成果", "反向课程设计", "能力达成评价", "持续改进"]
    },
    "5E教学法": {
        "name": "5E教学模型",
        "description": "包含参与、探索、解释、精致化、评价五个阶段的探究式教学",
        "key_elements": ["Engage参与", "Explore探索", "Explain解释", "Elaborate精致化", "Evaluate评价"]
    },
    "ADDIE": {
        "name": "ADDIE教学设计模型",
        "description": "系统化教学设计模型，包含分析、设计、开发、实施、评估五个阶段",
        "key_elements": ["Analysis分析", "Design设计", "Development开发", "Implementation实施", "Evaluation评估"]
    },
    "翻转课堂": {
        "name": "翻转课堂（Flipped Classroom）",
        "description": "课前自主学习，课堂深度互动的教学模式",
        "key_elements": ["课前视频/资料", "课前自测", "课堂讨论互动", "深度应用练习", "总结反馈"]
    }
}

def check_neo4j_available():
    """检查Neo4j是否可用"""
    from modules.auth import check_neo4j_available as auth_check
    return auth_check()

def get_neo4j_driver():
    """获取Neo4j连接"""
    from modules.auth import get_neo4j_driver as auth_get_driver
    return auth_get_driver()

def get_all_chapters():
    """获取所有章节及其所属模块"""
    if not check_neo4j_available():
        return []
    
    try:
        driver = get_neo4j_driver()
        with driver.session() as session:
            result = session.run("""
                MATCH (m:glx_Module)-[:CONTAINS]->(c:glx_Chapter)
                RETURN m.name as module_name, c.id as chapter_id, c.name as chapter_name
                ORDER BY m.id, c.id
            """)
            chapters = [dict(record) for record in result]
        return chapters
    except Exception as e:
        st.error(f"获取章节列表失败: {e}")
        return []

def get_chapter_knowledge_points(chapter_id):
    """获取章节下的所有知识点"""
    if not check_neo4j_available():
        return []
    
    try:
        driver = get_neo4j_driver()
        with driver.session() as session:
            result = session.run("""
                MATCH (c:glx_Chapter {id: $chapter_id})-[:CONTAINS]->(k:glx_Knowledge)
                RETURN k.name as name, k.importance as importance
                ORDER BY k.importance DESC
            """, chapter_id=chapter_id)
            knowledge_points = [dict(record) for record in result]
        return knowledge_points
    except Exception as e:
        st.error(f"获取知识点失败: {e}")
        return []

def generate_teaching_design(chapter_name, knowledge_points, method_key):
    """使用 DeepSeek AI 生成教学设计方案"""
    method_info = TEACHING_METHODS.get(method_key, {})
    
    try:
        client = OpenAI(
            api_key=DEEPSEEK_API_KEY,
            base_url=DEEPSEEK_BASE_URL
        )
        
        # 构建知识点列表
        kp_text = "\n".join([f"- {kp['name']}（重要性：{kp.get('importance', 80)}）" for kp in knowledge_points])
        
        # 构建提示词
        prompt = f"""
请作为一名资深的管理学教育专家，为以下教学内容设计一份详细的教学方案。

# 教学内容
- 章节名称：{chapter_name}
- 包含知识点：
{kp_text}

# 教学方法
- 方法名称：{method_info.get('name', method_key)}
- 方法描述：{method_info.get('description', '')}
- 核心要素：{', '.join(method_info.get('key_elements', []))}

# 教学设计要求

请按照 **{method_key}** 的教学模式，设计一份完整的教学方案，包括：

## 1. 教学目标设计
- 知识目标（2-3条）
- 能力目标（2-3条）
- 素质目标（1-2条）

## 2. 学情分析
- 学生基础分析
- 学习难点预判

## 3. 教学内容分析
- 重点内容
- 难点内容
- 知识点之间的逻辑关系

## 4. 教学过程设计
请严格按照 **{method_key}** 的各个环节进行详细设计：
{chr(10).join([f"- {elem}" for elem in method_info.get('key_elements', [])])}

每个环节需要包括：
- 环节时长（建议）
- 教师活动
- 学生活动
- 设计意图

## 5. 教学资源与工具
- 多媒体资源
- 案例材料
- 互动工具

## 6. 教学评价设计
- 过程性评价方案
- 终结性评价方案
- 评价标准/量规

## 7. 课后延伸
- 作业设计
- 拓展阅读
- 实践任务

# 输出要求
- 方案要具体、可操作
- 体现{method_key}的教学理念和特色
- 适合管理学专业本科生
- 按照上述结构用 Markdown 格式输出
- 总字数2000-3000字
"""
        
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": f"你是一位精通{method_key}教学法的管理学教育专家，擅长设计创新、有效的教学方案。"},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=4000
        )
        
        design = response.choices[0].message.content
        return design
        
    except Exception as e:
        return f"生成教学方案失败：{str(e)}"

def render_teaching_design():
    """渲染教学方案设计页面"""
    st.markdown("## 📐 教学方案设计")
    st.markdown("根据章节内容和教学方法，AI辅助生成教学设计方案")
    st.markdown("---")
    
    if not check_neo4j_available():
        st.error("❌ Neo4j数据库连接失败，无法获取章节信息")
        return
    
    # 获取所有章节
    chapters = get_all_chapters()
    if not chapters:
        st.warning("暂无章节数据，请先初始化知识图谱")
        return
    
    # 布局
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📚 选择教学内容")
        
        # 按模块分组章节
        module_chapters = {}
        for ch in chapters:
            module = ch['module_name']
            if module not in module_chapters:
                module_chapters[module] = []
            module_chapters[module].append(ch)
        
        # 先选择模块
        module_names = list(module_chapters.keys())
        selected_module = st.selectbox("选择篇章模块", module_names)
        
        # 再选择章节
        if selected_module:
            chapter_list = module_chapters[selected_module]
            chapter_options = [ch['chapter_name'] for ch in chapter_list]
            selected_chapter_name = st.selectbox("选择具体章节", chapter_options)
            
            # 获取章节ID
            selected_chapter = next((ch for ch in chapter_list if ch['chapter_name'] == selected_chapter_name), None)
            
            if selected_chapter:
                # 显示该章节的知识点
                knowledge_points = get_chapter_knowledge_points(selected_chapter['chapter_id'])
                if knowledge_points:
                    st.markdown("**包含知识点：**")
                    for kp in knowledge_points:
                        importance = kp.get('importance', 80)
                        if importance >= 100:
                            st.markdown(f"- 🔴 {kp['name']}（核心）")
                        elif importance >= 90:
                            st.markdown(f"- 🟠 {kp['name']}（重要）")
                        else:
                            st.markdown(f"- 🟢 {kp['name']}")
    
    with col2:
        st.markdown("### 🎯 选择教学方法")
        
        # 教学方法选择
        method_options = list(TEACHING_METHODS.keys())
        selected_method = st.selectbox("选择教学方法", method_options)
        
        # 显示方法说明
        if selected_method:
            method_info = TEACHING_METHODS[selected_method]
            st.info(f"""
            **{method_info['name']}**
            
            {method_info['description']}
            
            **核心环节：**
            {', '.join(method_info['key_elements'])}
            """)
    
    st.markdown("---")
    
    # 生成按钮
    if st.button("🤖 生成教学方案", type="primary", use_container_width=True):
        if not selected_chapter:
            st.error("请选择章节")
            return
        
        knowledge_points = get_chapter_knowledge_points(selected_chapter['chapter_id'])
        
        with st.spinner(f"正在使用 {selected_method} 设计教学方案..."):
            design = generate_teaching_design(
                selected_chapter_name,
                knowledge_points,
                selected_method
            )
            
            # 保存到 session state
            st.session_state['teaching_design'] = design
            st.session_state['teaching_design_info'] = {
                'chapter': selected_chapter_name,
                'method': selected_method,
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
    
    # 显示生成的方案
    if 'teaching_design' in st.session_state and st.session_state['teaching_design']:
        st.markdown("---")
        design_info = st.session_state.get('teaching_design_info', {})
        st.markdown(f"### 📄 教学方案 - {design_info.get('chapter', '')} ({design_info.get('method', '')})")
        st.markdown(f"*生成时间：{design_info.get('timestamp', '')}*")
        
        # 显示方案内容
        st.markdown(st.session_state['teaching_design'])
        
        # 下载按钮
        st.markdown("---")
        col_dl1, col_dl2, col_dl3 = st.columns([1, 1, 1])
        
        with col_dl2:
            # 生成文件名
            filename = f"教学方案_{design_info.get('chapter', '章节')}_{design_info.get('method', '方法')}_{datetime.now().strftime('%Y%m%d')}.md"
            
            st.download_button(
                label="📥 下载教学方案",
                data=st.session_state['teaching_design'],
                file_name=filename,
                mime="text/markdown",
                use_container_width=True
            )

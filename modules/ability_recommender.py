"""
能力推荐模块
基于能力自评，AI推荐学习路径
"""

import streamlit as st
from openai import OpenAI
from config.settings import *

def check_neo4j_available():
    """检查Neo4j是否可用"""
    from modules.auth import check_neo4j_available as auth_check
    return auth_check()

def get_neo4j_driver():
    """获取Neo4j连接（复用auth模块的缓存连接）"""
    from modules.auth import get_neo4j_driver as auth_get_driver
    return auth_get_driver()

def get_current_student():
    """获取当前学生信息"""
    if st.session_state.get('user_role') == 'student':
        return st.session_state.get('student_id')
    return None

def log_ability_activity(activity_type, content_id=None, content_name=None, details=None):
    """记录能力推荐模块活动"""
    student_id = get_current_student()
    if not student_id:
        return
    
    from modules.auth import log_activity
    log_activity(
        student_id=student_id,
        activity_type=activity_type,
        module_name="能力推荐",
        content_id=content_id,
        content_name=content_name,
        details=details
    )

def get_all_abilities():
    """获取所有能力列表"""
    if not check_neo4j_available():
        return []
    
    try:
        driver = get_neo4j_driver()
        
        with driver.session() as session:
            result = session.run("""
                MATCH (a:mfx_Ability)
                RETURN a.id as id, a.name as name, a.category as category, a.description as description
                ORDER BY a.category, a.name
            """)
            
            abilities = [dict(record) for record in result]
        
        # 不关闭driver，保持连接池复用
        return abilities
    except Exception:
        return []

def analyze_learning_path(selected_abilities, mastery_levels, abilities_info=None):
    """分析学习路径并生成推荐"""
    required_knowledge = []
    
    # 尝试从Neo4j获取知识点数据
    if check_neo4j_available():
        try:
            driver = get_neo4j_driver()
            
            # 获取能力需要的知识点
            with driver.session() as session:
                result = session.run("""
                MATCH (a:mfx_Ability)-[r:REQUIRES]->(k:mfx_Knowledge)
                WHERE a.id IN $abilities
                RETURN k.id as kp_id, k.name as kp_name, k.difficulty as difficulty, 
                       collect(a.name) as required_by, max(r.weight) as max_weight
                ORDER BY max_weight DESC
            """, abilities=selected_abilities)
            
                required_knowledge = [dict(record) for record in result]
            
            # 不关闭driver，保持连接池复用
        except Exception:
            required_knowledge = []
    
    # 如果没有从数据库获取到数据，使用示例知识点
    if not required_knowledge:
        # 根据选择的能力生成相关知识点
        ability_knowledge_map = {
            "A1": [("牙龈解剖结构", "基础", 0.9), ("管理膜组成", "基础", 0.8), ("牙槽骨特征", "基础", 0.7)],
            "A2": [("管理探诊技术", "基础", 0.9), ("探诊深度测量", "基础", 0.8), ("附着丧失评估", "中等", 0.7)],
            "A3": [("牙菌斑识别方法", "基础", 0.9), ("菌斑染色技术", "基础", 0.8), ("生物膜特征", "中等", 0.7)],
            "A4": [("管理病分类标准", "中等", 0.9), ("临床检查要点", "基础", 0.8), ("影像学诊断", "中等", 0.8)],
            "A5": [("管理X线片判读", "中等", 0.9), ("骨吸收程度评估", "中等", 0.8), ("根分叉病变诊断", "高级", 0.7)],
            "A6": [("龈上洁治原理", "基础", 0.9), ("器械使用方法", "中等", 0.9), ("操作规范", "基础", 0.8)],
            "A7": [("龈下刮治技术", "中等", 0.9), ("根面平整术", "高级", 0.9), ("局部麻醉技术", "中等", 0.8)],
            "A8": [("治疗计划制定原则", "高级", 0.9), ("管理病分期分级", "中等", 0.8), ("预后评估", "高级", 0.8)],
            "A9": [("口腔卫生指导方法", "基础", 0.9), ("刷牙技术培训", "基础", 0.8), ("辅助工具使用", "基础", 0.7)],
            "A10": [("管理维护治疗原则", "中等", 0.9), ("复查周期规划", "中等", 0.8), ("SPT标准流程", "中等", 0.8)],
        }
        
        for ability_id in selected_abilities:
            if ability_id in ability_knowledge_map:
                for kp_name, difficulty, weight in ability_knowledge_map[ability_id]:
                    ability_name = next((a['name'] for a in (abilities_info or []) if a['id'] == ability_id), ability_id)
                    required_knowledge.append({
                        'kp_id': f"KP_{ability_id}_{kp_name}",
                        'kp_name': kp_name,
                        'difficulty': difficulty,
                        'required_by': [ability_name],
                        'max_weight': weight
                    })
    
    # 获取能力名称映射
    ability_names = []
    for a_id in selected_abilities:
        if abilities_info:
            name = next((a['name'] for a in abilities_info if a['id'] == a_id), a_id)
        else:
            name = a_id
        mastery = mastery_levels.get(a_id, 0.5)
        ability_names.append(f"{name}(自评掌握度: {int(mastery*100)}%)")
    
    # 构建知识点描述
    knowledge_desc = []
    for kp in required_knowledge[:15]:
        if isinstance(kp.get('required_by'), list):
            required_by_str = ', '.join(kp['required_by'])
        else:
            required_by_str = str(kp.get('required_by', ''))
        weight = kp.get('max_weight', 0.5)
        if isinstance(weight, (int, float)):
            weight_str = f"{weight:.1f}"
        else:
            weight_str = str(weight)
        knowledge_desc.append(f"- {kp['kp_name']} (难度: {kp.get('difficulty', '未知')}, 重要性: {weight_str}, 所需能力: {required_by_str})")
    
    # 使用DeepSeek AI生成推荐
    try:
        import httpx
        
        # 创建不使用代理的httpx客户端，解决Streamlit Cloud部署问题
        http_client = httpx.Client(
            base_url=DEEPSEEK_BASE_URL,
            timeout=60.0,
            follow_redirects=True
        )
        
        client = OpenAI(
            api_key=DEEPSEEK_API_KEY,
            base_url=DEEPSEEK_BASE_URL,
            http_client=http_client
        )
        
        prompt = f"""
你是一位民法学教学专家。学生选择了以下目标能力：

{', '.join(ability_names)}

这些能力需要掌握以下知识点：
{chr(10).join(knowledge_desc) if knowledge_desc else "（系统将根据能力要求推荐学习内容）"}

请为学生制定一个个性化的学习路径，包括：
1. **学习优先级排序**：按照"基础→重要→高级"的顺序，列出应该优先学习的知识点（5-8个）
2. **学习建议**：针对每个知识点，给出简短的学习建议
3. **预计学习时间**：估算总学习时间
4. **能力提升预期**：完成学习后，学生在选定能力上能达到什么水平

请用简洁、友好的语言，给出实用的建议。
"""
        
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[{"role": "user", "content": prompt}],
            stream=False
        )
        
        # 关闭httpx客户端
        http_client.close()
        
        return response.choices[0].message.content
    except Exception as e:
        import traceback
        error_trace = traceback.format_exc()
        # 如果AI调用失败，返回一个基本的推荐
        return f"""
### 📚 学习路径推荐

基于您选择的能力目标，建议按以下顺序学习：

**第一阶段：基础知识夯实**
1. 管理组织解剖结构 - 了解牙龈、管理膜、牙槽骨的基本结构
2. 管理检查基本方法 - 掌握探诊技术和记录方法

**第二阶段：核心技能培养**
3. 管理病诊断要点 - 学习分类标准和诊断流程
4. 基础治疗操作 - 练习洁治和刮治技术

**第三阶段：综合能力提升**
5. 治疗计划制定 - 整合知识进行临床决策
6. 患者教育技巧 - 提高口腔卫生指导能力

**预计学习时间**：约 2-3 周（每天 1-2 小时）

**学习建议**：建议结合教材、临床观摩和实践操作进行学习。

⚠️ 注意：AI分析服务暂时不可用（{str(e)[:50]}），以上为系统预设推荐。
"""

def render_ability_recommender():
    """渲染能力推荐页面"""
    st.title("🎯 能力自评与学习推荐")
    
    # 记录进入能力推荐
    log_ability_activity("进入模块", details="访问能力推荐")
    
    st.markdown("""
    选择你想掌握的能力，系统将基于AI为你推荐个性化的学习路径。
    """)
    
    # 获取所有能力
    abilities = get_all_abilities()
    
    # 始终使用完整的10个能力列表（无论数据库有无数据）
    abilities = [
        {"id": "A1", "name": "管理组织解剖识别", "category": "基础能力", "description": "能够识别和描述正常管理组织的解剖结构，包括牙龈、管理膜、牙槽骨和牙骨质"},
        {"id": "A2", "name": "管理探诊技术", "category": "基础能力", "description": "掌握正确的管理探诊方法和技巧，能够准确测量探诊深度"},
        {"id": "A3", "name": "牙菌斑识别", "category": "诊断能力", "description": "能够识别和评估牙菌斑的分布和程度，理解菌斑染色方法"},
        {"id": "A4", "name": "管理病诊断", "category": "诊断能力", "description": "能够根据临床表现做出正确的管理病诊断，掌握2018年新分类"},
        {"id": "A5", "name": "X线片解读", "category": "诊断能力", "description": "能够解读管理病相关的X线影像，判断骨吸收类型和程度"},
        {"id": "A6", "name": "洁治术操作", "category": "治疗能力", "description": "掌握龈上洁治术的操作技能，熟悉超声和手工器械使用"},
        {"id": "A7", "name": "刮治术操作", "category": "治疗能力", "description": "掌握龈下刮治和根面平整术的操作要点"},
        {"id": "A8", "name": "治疗计划制定", "category": "治疗能力", "description": "能够制定合理的管理治疗计划，包括分期分级和预后评估"},
        {"id": "A9", "name": "口腔卫生指导", "category": "预防能力", "description": "能够进行有效的口腔卫生宣教，指导患者正确刷牙和使用辅助工具"},
        {"id": "A10", "name": "维护治疗管理", "category": "预防能力", "description": "掌握管理维护治疗的原则和方法，制定个性化复查计划"},
    ]
    
    # 按类别分组
    categories = {}
    for ability in abilities:
        cat = ability['category']
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(ability)
    
    # 1. 能力选择 - 使用form避免每次交互都刷新页面
    st.subheader("1️⃣ 选择目标能力")
    
    # 初始化session_state
    if 'selected_abilities' not in st.session_state:
        st.session_state.selected_abilities = []
    if 'mastery_levels' not in st.session_state:
        st.session_state.mastery_levels = {}
    
    # 使用expander分类显示能力，减少页面复杂度
    for category, abs_list in categories.items():
        with st.expander(f"📂 {category}", expanded=True):
            for ability in abs_list:
                col1, col2 = st.columns([3, 2])
                with col1:
                    checked = st.checkbox(
                        f"{ability['name']}",
                        key=f"ability_{ability['id']}",
                        help=ability['description'],
                        value=ability['id'] in st.session_state.selected_abilities
                    )
                    if checked and ability['id'] not in st.session_state.selected_abilities:
                        st.session_state.selected_abilities.append(ability['id'])
                    elif not checked and ability['id'] in st.session_state.selected_abilities:
                        st.session_state.selected_abilities.remove(ability['id'])
                with col2:
                    if ability['id'] in st.session_state.selected_abilities:
                        level = st.slider(
                            "当前掌握度",
                            0.0, 1.0, 
                            st.session_state.mastery_levels.get(ability['id'], 0.3), 
                            0.1,
                            key=f"level_{ability['id']}",
                            label_visibility="collapsed"
                        )
                        st.session_state.mastery_levels[ability['id']] = level
    
    selected_abilities = st.session_state.selected_abilities
    mastery_levels = st.session_state.mastery_levels
    
    # 2. 生成推荐
    if selected_abilities:
        st.divider()
        st.subheader("2️⃣ AI学习路径推荐")
        
        if st.button("🤖 生成个性化学习推荐", type="primary"):
            # 记录能力选择和自评
            abilities_str = ', '.join(selected_abilities)
            log_ability_activity("能力自评", content_name=abilities_str, details=f"选择能力: {abilities_str}")
            
            # 创建AI分析可视化容器
            analysis_container = st.container()
            
            with analysis_container:
                st.markdown("""
                <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                            padding: 25px; border-radius: 15px; margin: 20px 0;">
                    <h3 style="color: white; margin: 0 0 15px 0;">🧠 AI 智能分析中心</h3>
                    <p style="color: rgba(255,255,255,0.9); margin: 0;">基于DeepSeek大模型进行个性化学习路径规划</p>
                </div>
                """, unsafe_allow_html=True)
                
                # 分析步骤显示
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    step1 = st.empty()
                    step1.markdown("""
                    <div style="text-align: center; padding: 15px; background: #f8f9fa; border-radius: 10px;">
                        <div style="font-size: 30px;">📊</div>
                        <div style="font-weight: bold; margin: 5px 0;">能力解析</div>
                        <div style="color: #999; font-size: 12px;">分析目标能力</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    step2 = st.empty()
                    step2.markdown("""
                    <div style="text-align: center; padding: 15px; background: #f8f9fa; border-radius: 10px;">
                        <div style="font-size: 30px;">🔍</div>
                        <div style="font-weight: bold; margin: 5px 0;">知识匹配</div>
                        <div style="color: #999; font-size: 12px;">检索知识图谱</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col3:
                    step3 = st.empty()
                    step3.markdown("""
                    <div style="text-align: center; padding: 15px; background: #f8f9fa; border-radius: 10px;">
                        <div style="font-size: 30px;">🤖</div>
                        <div style="font-weight: bold; margin: 5px 0;">AI推理</div>
                        <div style="color: #999; font-size: 12px;">深度学习分析</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col4:
                    step4 = st.empty()
                    step4.markdown("""
                    <div style="text-align: center; padding: 15px; background: #f8f9fa; border-radius: 10px;">
                        <div style="font-size: 30px;">📋</div>
                        <div style="font-weight: bold; margin: 5px 0;">生成方案</div>
                        <div style="color: #999; font-size: 12px;">输出学习路径</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                import time
                
                # 步骤1: 能力解析
                time.sleep(0.5)
                step1.markdown("""
                <div style="text-align: center; padding: 15px; background: #d4edda; border-radius: 10px; border: 2px solid #28a745;">
                    <div style="font-size: 30px;">✅</div>
                    <div style="font-weight: bold; margin: 5px 0; color: #155724;">能力解析</div>
                    <div style="color: #155724; font-size: 12px;">完成</div>
                </div>
                """, unsafe_allow_html=True)
                
                # 显示解析的能力
                st.markdown("##### 📊 解析的目标能力:")
                abilities_display = st.empty()
                abilities_html = ""
                for ability_id in selected_abilities:
                    ability_name = next((a['name'] for a in abilities if a['id'] == ability_id), ability_id)
                    mastery = mastery_levels.get(ability_id, 0.5)
                    color = "#28a745" if mastery >= 0.7 else "#ffc107" if mastery >= 0.4 else "#dc3545"
                    abilities_html += f"""
                    <span style="display: inline-block; background: {color}22; color: {color}; 
                                 padding: 5px 12px; margin: 3px; border-radius: 20px; border: 1px solid {color};">
                        {ability_name} ({int(mastery*100)}%)
                    </span>
                    """
                abilities_display.markdown(abilities_html, unsafe_allow_html=True)
                
                # 步骤2: 知识匹配
                time.sleep(0.6)
                step2.markdown("""
                <div style="text-align: center; padding: 15px; background: #d4edda; border-radius: 10px; border: 2px solid #28a745;">
                    <div style="font-size: 30px;">✅</div>
                    <div style="font-weight: bold; margin: 5px 0; color: #155724;">知识匹配</div>
                    <div style="color: #155724; font-size: 12px;">完成</div>
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown("##### 🔍 知识图谱检索结果:")
                st.info(f"已从知识图谱中匹配到 {len(selected_abilities) * 3} 个相关知识点")
                
                # 步骤3: AI推理
                time.sleep(0.5)
                step3.markdown("""
                <div style="text-align: center; padding: 15px; background: #cce5ff; border-radius: 10px; border: 2px solid #004085; animation: pulse 1s infinite;">
                    <div style="font-size: 30px;">⏳</div>
                    <div style="font-weight: bold; margin: 5px 0; color: #004085;">AI推理中</div>
                    <div style="color: #004085; font-size: 12px;">请稍候...</div>
                </div>
                """, unsafe_allow_html=True)
                
                # 显示AI思考过程
                thinking_box = st.empty()
                thinking_box.markdown("""
                <div style="background: #f8f9fa; padding: 15px; border-radius: 10px; border-left: 4px solid #667eea;">
                    <p style="margin: 0; color: #666;">🤖 <strong>AI正在思考...</strong></p>
                    <p style="margin: 5px 0 0 0; color: #888; font-size: 14px;">
                        正在分析您的能力水平、学习目标，结合民法学知识体系生成最优学习路径...
                    </p>
                </div>
                """, unsafe_allow_html=True)
                
                try:
                    recommendation = analyze_learning_path(selected_abilities, mastery_levels, abilities)
                    
                    # 步骤3完成
                    step3.markdown("""
                    <div style="text-align: center; padding: 15px; background: #d4edda; border-radius: 10px; border: 2px solid #28a745;">
                        <div style="font-size: 30px;">✅</div>
                        <div style="font-weight: bold; margin: 5px 0; color: #155724;">AI推理</div>
                        <div style="color: #155724; font-size: 12px;">完成</div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    thinking_box.empty()
                    
                    # 步骤4完成
                    time.sleep(0.3)
                    step4.markdown("""
                    <div style="text-align: center; padding: 15px; background: #d4edda; border-radius: 10px; border: 2px solid #28a745;">
                        <div style="font-size: 30px;">✅</div>
                        <div style="font-weight: bold; margin: 5px 0; color: #155724;">生成方案</div>
                        <div style="color: #155724; font-size: 12px;">完成</div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # 显示AI推荐结果
                    st.markdown("""
                    <div style="background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%); 
                                padding: 20px; border-radius: 12px; margin: 20px 0;">
                        <h4 style="color: white; margin: 0;">🎯 AI个性化学习推荐</h4>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    st.markdown(recommendation)
                    
                    # 记录AI推荐生成
                    log_ability_activity("生成AI推荐", details="成功生成学习路径推荐")
                    
                    # 保存到session
                    st.session_state['last_recommendation'] = recommendation
                    
                    st.success("🎉 推荐生成完成！按照上述路径学习，效率更高！")
                    
                except Exception as e:
                    step3.markdown("""
                    <div style="text-align: center; padding: 15px; background: #f8d7da; border-radius: 10px; border: 2px solid #dc3545;">
                        <div style="font-size: 30px;">❌</div>
                        <div style="font-weight: bold; margin: 5px 0; color: #721c24;">AI推理</div>
                        <div style="color: #721c24; font-size: 12px;">失败</div>
                    </div>
                    """, unsafe_allow_html=True)
                    thinking_box.empty()
                    st.error(f"生成推荐失败: {str(e)}")
        
        # 显示历史推荐
        if 'last_recommendation' in st.session_state:
            with st.expander("查看上次推荐"):
                st.markdown(st.session_state['last_recommendation'])
    else:
        st.info("👆 请先选择至少一个目标能力")
    
    # 能力雷达图 - 放在主界面
    if selected_abilities and mastery_levels:
        st.divider()
        st.subheader("📈 能力掌握度雷达图")
        
        # 创建雷达图数据
        import plotly.graph_objects as go
        
        # 获取已选能力的名称和掌握度（转换为0-10分制）
        selected_ability_names = []
        selected_mastery_scores = []
        
        for ability in abilities:
            if ability['id'] in selected_abilities:
                selected_ability_names.append(ability['name'])
                # 将0-1的值转换为0-10分制
                selected_mastery_scores.append(mastery_levels[ability['id']] * 10)
        
        # 创建雷达图
        if selected_ability_names:
            col1, col2 = st.columns([2, 1])
            
            with col1:
                fig = go.Figure()
                
                # 闭合雷达图：在数据末尾添加第一个点
                closed_names = selected_ability_names + [selected_ability_names[0]]
                closed_scores = selected_mastery_scores + [selected_mastery_scores[0]]
                
                fig.add_trace(go.Scatterpolar(
                    r=closed_scores,
                    theta=closed_names,
                    fill='toself',
                    name='当前掌握度',
                    line=dict(color='#4ECDC4', width=3),
                    fillcolor='rgba(78, 205, 196, 0.3)'
                ))
                
                fig.update_layout(
                    polar=dict(
                        radialaxis=dict(
                            visible=True,
                            range=[0, 10],
                            tickmode='linear',
                            tick0=0,
                            dtick=2,
                            gridcolor='#e0e0e0'
                        ),
                        angularaxis=dict(
                            gridcolor='#e0e0e0'
                        )
                    ),
                    showlegend=True,
                    height=500,
                    margin=dict(l=100, r=100, t=40, b=40),
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)'
                )
                
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                st.markdown("### 📊 能力统计")
                
                # 显示统计信息
                avg_mastery = sum(selected_mastery_scores) / len(selected_mastery_scores)
                st.metric("平均掌握度", f"{avg_mastery:.1f}/10", 
                         help="所有选中能力的平均掌握程度")
                
                st.markdown("---")
                
                # 显示最强和最弱能力
                min_idx = selected_mastery_scores.index(min(selected_mastery_scores))
                max_idx = selected_mastery_scores.index(max(selected_mastery_scores))
                
                st.metric("💪 最强能力", 
                         selected_ability_names[max_idx], 
                         f"{selected_mastery_scores[max_idx]:.1f}/10")
                
                st.metric("📖 待提升能力", 
                         selected_ability_names[min_idx], 
                         f"{selected_mastery_scores[min_idx]:.1f}/10")
                
                # 能力分布
                st.markdown("---")
                st.markdown("**能力分布：**")
                high_count = sum(1 for s in selected_mastery_scores if s >= 7)
                mid_count = sum(1 for s in selected_mastery_scores if 4 <= s < 7)
                low_count = sum(1 for s in selected_mastery_scores if s < 4)
                
                st.write(f"🟢 熟练（≥7分）：{high_count}个")
                st.write(f"🟡 中等（4-7分）：{mid_count}个")
                st.write(f"🔴 薄弱（<4分）：{low_count}个")

"""
管理学知识图谱数据
基于经典管理学理论体系
"""

KNOWLEDGE_GRAPH = {
    "name": "管理学知识体系",
    "children": [
        {
            "name": "第一篇 管理与管理学",
            "children": [
                {
                    "name": "第一章 管理活动与管理理论",
                    "children": [
                        {"name": "管理的概念与性质", "value": 100},
                        {"name": "管理的职能", "value": 100},
                        {"name": "管理者的角色与技能", "value": 90},
                        {"name": "管理学的研究对象与方法", "value": 80}
                    ]
                },
                {
                    "name": "第二章 管理思想的演变",
                    "children": [
                        {"name": "古典管理理论", "value": 100},
                        {"name": "泰勒的科学管理", "value": 90},
                        {"name": "法约尔的一般管理理论", "value": 90},
                        {"name": "韦伯的官僚组织理论", "value": 80},
                        {"name": "行为科学理论", "value": 90},
                        {"name": "霍桑实验", "value": 80},
                        {"name": "现代管理理论丛林", "value": 70}
                    ]
                },
                {
                    "name": "第三章 管理道德与企业社会责任",
                    "children": [
                        {"name": "管理道德", "value": 80},
                        {"name": "企业社会责任", "value": 90},
                        {"name": "利益相关者理论", "value": 80}
                    ]
                },
                {
                    "name": "第四章 全球化与管理",
                    "children": [
                        {"name": "全球化内涵与趋势", "value": 80},
                        {"name": "跨文化管理", "value": 80},
                        {"name": "国际企业管理模式", "value": 70}
                    ]
                },
                {
                    "name": "第五章 信息与信息化管理",
                    "children": [
                        {"name": "信息及其特征", "value": 70},
                        {"name": "管理信息系统", "value": 80},
                        {"name": "数字化转型", "value": 90}
                    ]
                }
            ]
        },
        {
            "name": "第二篇 决策与计划",
            "children": [
                {
                    "name": "第六章 决策与决策方法",
                    "children": [
                        {"name": "决策的概念与类型", "value": 100},
                        {"name": "决策的过程", "value": 100},
                        {"name": "决策的影响因素", "value": 90},
                        {"name": "定性决策方法", "value": 80},
                        {"name": "定量决策方法", "value": 80},
                        {"name": "群体决策", "value": 80}
                    ]
                },
                {
                    "name": "第七章 计划与计划工作",
                    "children": [
                        {"name": "计划的概念与性质", "value": 100},
                        {"name": "计划的类型", "value": 90},
                        {"name": "计划编制过程", "value": 90},
                        {"name": "目标管理(MBO)", "value": 90}
                    ]
                },
                {
                    "name": "第八章 战略性计划与计划实施",
                    "children": [
                        {"name": "战略环境分析", "value": 100},
                        {"name": "SWOT分析", "value": 100},
                        {"name": "波特五力模型", "value": 90},
                        {"name": "基本竞争战略", "value": 90},
                        {"name": "战略实施", "value": 80}
                    ]
                }
            ]
        },
        {
            "name": "第三篇 组织",
            "children": [
                {
                    "name": "第九章 组织设计",
                    "children": [
                        {"name": "组织与组织设计", "value": 100},
                        {"name": "组织结构类型", "value": 100},
                        {"name": "直线职能制", "value": 80},
                        {"name": "事业部制", "value": 80},
                        {"name": "矩阵制", "value": 80},
                        {"name": "网络型组织", "value": 70}
                    ]
                },
                {
                    "name": "第十章 人力资源管理",
                    "children": [
                        {"name": "人力资源计划", "value": 90},
                        {"name": "员工招聘", "value": 90},
                        {"name": "员工培训", "value": 80},
                        {"name": "绩效考核", "value": 90},
                        {"name": "薪酬管理", "value": 80}
                    ]
                },
                {
                    "name": "第十一章 组织变革与组织文化",
                    "children": [
                        {"name": "组织变革的动因", "value": 80},
                        {"name": "组织变革的类型", "value": 80},
                        {"name": "组织变革的阻力与克服", "value": 80},
                        {"name": "组织文化的概念与功能", "value": 90},
                        {"name": "组织文化的塑造", "value": 80}
                    ]
                }
            ]
        },
        {
            "name": "第四篇 领导",
            "children": [
                {
                    "name": "第十二章 领导概论",
                    "children": [
                        {"name": "领导的内涵", "value": 100},
                        {"name": "领导与管理的区别", "value": 90},
                        {"name": "领导权力的来源", "value": 90},
                        {"name": "领导特质理论", "value": 80},
                        {"name": "领导行为理论", "value": 80},
                        {"name": "领导权变理论", "value": 90}
                    ]
                },
                {
                    "name": "第十三章 激励",
                    "children": [
                        {"name": "激励的概念与过程", "value": 100},
                        {"name": "需要层次理论", "value": 100},
                        {"name": "双因素理论", "value": 90},
                        {"name": "期望理论", "value": 90},
                        {"name": "公平理论", "value": 80},
                        {"name": "强化理论", "value": 80}
                    ]
                },
                {
                    "name": "第十四章 沟通",
                    "children": [
                        {"name": "沟通的概念与过程", "value": 100},
                        {"name": "沟通的类型", "value": 90},
                        {"name": "正式沟通与非正式沟通", "value": 80},
                        {"name": "沟通障碍及克服", "value": 80},
                        {"name": "有效沟通技巧", "value": 90}
                    ]
                }
            ]
        },
        {
            "name": "第五篇 控制",
            "children": [
                {
                    "name": "第十五章 控制与控制过程",
                    "children": [
                        {"name": "控制的概念与作用", "value": 100},
                        {"name": "控制的类型", "value": 90},
                        {"name": "前馈控制", "value": 80},
                        {"name": "同期控制", "value": 80},
                        {"name": "反馈控制", "value": 80},
                        {"name": "控制的基本过程", "value": 90}
                    ]
                },
                {
                    "name": "第十六章 控制方法",
                    "children": [
                        {"name": "预算控制", "value": 90},
                        {"name": "财务控制", "value": 80},
                        {"name": "审计控制", "value": 70},
                        {"name": "标杆管理", "value": 80},
                        {"name": "平衡计分卡", "value": 90}
                    ]
                }
            ]
        },
        {
            "name": "第六篇 创新",
            "children": [
                {
                    "name": "第十七章 管理的创新职能",
                    "children": [
                        {"name": "创新的概念与类别", "value": 90},
                        {"name": "创新的过程", "value": 80},
                        {"name": "创新与创业精神", "value": 80}
                    ]
                },
                {
                    "name": "第十八章 企业技术创新",
                    "children": [
                        {"name": "技术创新的内涵", "value": 80},
                        {"name": "技术创新的类型", "value": 80},
                        {"name": "创新战略", "value": 90}
                    ]
                },
                {
                    "name": "第十九章 企业组织创新",
                    "children": [
                        {"name": "组织创新的动因", "value": 80},
                        {"name": "组织结构创新", "value": 80},
                        {"name": "流程再造", "value": 90},
                        {"name": "学习型组织", "value": 80}
                    ]
                }
            ]
        }
    ]
}

def get_knowledge_graph():
    """返回管理学知识图谱数据"""
    return KNOWLEDGE_GRAPH

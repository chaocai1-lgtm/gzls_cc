"""
管理学核心能力定义
基于管理者胜任力模型设计
"""

ABILITIES = [
    {
        "id": "glx_ability_01",
        "name": "战略思维能力",
        "description": "能够分析企业内外部环境，识别机会与威胁，制定和评估战略方案",
        "related_modules": ["决策与计划"],
        "level_descriptions": {
            1: "了解SWOT等基本分析工具",
            2: "能够进行简单的环境分析",
            3: "能够应用战略分析框架",
            4: "能够独立制定战略方案",
            5: "能够系统评估战略可行性"
        }
    },
    {
        "id": "glx_ability_02",
        "name": "决策分析能力",
        "description": "能够识别问题、收集信息、分析方案，做出科学合理的管理决策",
        "related_modules": ["决策与计划"],
        "level_descriptions": {
            1: "了解决策的基本概念和过程",
            2: "能够区分不同类型的决策",
            3: "能够运用决策树等分析工具",
            4: "能够在复杂情境中做出决策",
            5: "能够在不确定条件下科学决策"
        }
    },
    {
        "id": "glx_ability_03",
        "name": "计划组织能力",
        "description": "能够制定工作计划，合理配置资源，确保目标的有效达成",
        "related_modules": ["决策与计划"],
        "level_descriptions": {
            1: "了解计划的类型和作用",
            2: "能够制定简单的工作计划",
            3: "能够制定较完整的行动计划",
            4: "能够制定战略规划和年度计划",
            5: "能够进行动态计划调整和优化"
        }
    },
    {
        "id": "glx_ability_04",
        "name": "组织设计能力",
        "description": "能够根据组织目标设计合理的组织结构，明确职责权限",
        "related_modules": ["组织"],
        "level_descriptions": {
            1: "了解常见组织结构类型",
            2: "能够分析组织结构的优缺点",
            3: "能够设计部门和岗位",
            4: "能够设计完整的组织架构",
            5: "能够进行组织结构优化重组"
        }
    },
    {
        "id": "glx_ability_05",
        "name": "人力资源管理能力",
        "description": "能够进行人员的选拔、培养、评价和激励，打造高效团队",
        "related_modules": ["组织", "领导"],
        "level_descriptions": {
            1: "了解人力资源管理的基本职能",
            2: "能够进行基本的员工评价",
            3: "能够设计培训和考核方案",
            4: "能够进行系统的人才管理",
            5: "能够构建战略性人力资源体系"
        }
    },
    {
        "id": "glx_ability_06",
        "name": "领导影响能力",
        "description": "能够根据情境运用恰当的领导方式，激发团队动力",
        "related_modules": ["领导"],
        "level_descriptions": {
            1: "了解领导的基本概念",
            2: "了解不同的领导风格",
            3: "能够根据情境选择领导方式",
            4: "能够有效影响他人行为",
            5: "能够塑造组织文化和价值观"
        }
    },
    {
        "id": "glx_ability_07",
        "name": "激励赋能能力",
        "description": "能够识别员工需求，设计激励机制，激发员工潜能",
        "related_modules": ["领导"],
        "level_descriptions": {
            1: "了解基本的激励理论",
            2: "能够识别员工的需求层次",
            3: "能够运用多种激励方法",
            4: "能够设计系统的激励机制",
            5: "能够构建全面激励体系"
        }
    },
    {
        "id": "glx_ability_08",
        "name": "沟通协调能力",
        "description": "能够进行有效的信息传递，协调各方关系，促进团队协作",
        "related_modules": ["领导"],
        "level_descriptions": {
            1: "了解沟通的基本过程",
            2: "能够进行清晰的表达",
            3: "能够处理沟通障碍",
            4: "能够协调复杂的利益关系",
            5: "能够构建高效沟通机制"
        }
    },
    {
        "id": "glx_ability_09",
        "name": "控制评估能力",
        "description": "能够建立控制标准，监测执行过程，及时纠正偏差",
        "related_modules": ["控制"],
        "level_descriptions": {
            1: "了解控制的基本概念",
            2: "能够设定控制标准",
            3: "能够进行过程监控",
            4: "能够设计控制系统",
            5: "能够进行战略控制"
        }
    },
    {
        "id": "glx_ability_10",
        "name": "创新变革能力",
        "description": "能够识别创新机会，推动组织变革，引领持续改进",
        "related_modules": ["创新"],
        "level_descriptions": {
            1: "了解创新的基本概念",
            2: "能够识别创新机会",
            3: "能够推动小范围改进",
            4: "能够领导组织变革项目",
            5: "能够构建创新型组织"
        }
    }
]

def get_abilities():
    """返回所有能力"""
    return ABILITIES

def get_ability_by_id(ability_id):
    """根据ID获取能力"""
    for ability in ABILITIES:
        if ability['id'] == ability_id:
            return ability
    return None

def get_abilities_by_module(module):
    """根据模块获取相关能力"""
    return [ability for ability in ABILITIES if module in ability['related_modules']]

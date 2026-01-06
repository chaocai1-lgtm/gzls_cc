"""
高分子物理专业能力定义
基于高分子材料专业人才培养要求设计
"""

ABILITIES_GFZ = [
    {
        "id": "gfz_ability_01",
        "name": "高分子结构分析能力",
        "description": "能够分析高分子链的化学组成、构型、构造和构象，理解结构与性能的关系",
        "related_chapters": ["第1章", "第2章"],
        "related_kps": ["kp_1_1_2", "kp_1_2_1", "kp_2_1_2"],
        "level_descriptions": {
            1: "了解高分子结构的基本概念（单体、聚合度、构型等）",
            2: "能够识别全同、间同、无规立构",
            3: "能够分析高分子链的构象和柔性",
            4: "能够通过谱学方法（NMR、IR）表征高分子结构",
            5: "能够建立结构-性能关系，预测材料性能"
        }
    },
    {
        "id": "gfz_ability_02",
        "name": "聚合物结晶分析能力",
        "description": "能够分析聚合物的结晶行为、结晶形态和结晶度，掌握结晶对性能的影响",
        "related_chapters": ["第2章", "第5章"],
        "related_kps": ["kp_2_1_3", "kp_5_4_1", "kp_5_4_2"],
        "level_descriptions": {
            1: "了解聚合物结晶的基本概念和类型",
            2: "能够识别球晶、片晶等结晶形态",
            3: "能够测定结晶度和分析结晶动力学",
            4: "能够通过XRD、DSC等手段表征结晶行为",
            5: "能够控制结晶过程优化材料性能"
        }
    },
    {
        "id": "gfz_ability_03",
        "name": "溶液性质分析能力",
        "description": "能够分析高分子溶液的热力学和动力学性质，掌握溶解和相分离行为",
        "related_chapters": ["第3章"],
        "related_kps": ["kp_3_2_1", "kp_3_3_1", "kp_3_3_2"],
        "level_descriptions": {
            1: "了解聚合物的溶解过程和溶剂选择",
            2: "能够应用Flory-Huggins理论分析溶液性质",
            3: "能够测定和计算渗透压、黏度等性质",
            4: "能够分析相分离行为和相图",
            5: "能够设计溶液制备和加工工艺"
        }
    },
    {
        "id": "gfz_ability_04",
        "name": "分子量测定能力",
        "description": "能够选择合适的方法测定聚合物的分子量和分子量分布",
        "related_chapters": ["第4章"],
        "related_kps": ["kp_4_2_4", "kp_4_2_5", "kp_4_2_7", "kp_4_3_2"],
        "level_descriptions": {
            1: "了解分子量的统计意义和类型",
            2: "能够区分数均、重均、黏均分子量",
            3: "能够使用渗透压法、光散射法测分子量",
            4: "能够使用GPC/SEC测定分子量分布",
            5: "能够建立分子量与性能的关系"
        }
    },
    {
        "id": "gfz_ability_05",
        "name": "热转变分析能力",
        "description": "能够测定和分析玻璃化转变、熔融等热转变行为，掌握影响因素",
        "related_chapters": ["第5章"],
        "related_kps": ["kp_5_3_1", "kp_5_3_2", "kp_5_3_3", "kp_5_5_1"],
        "level_descriptions": {
            1: "了解Tg和Tm的基本概念",
            2: "能够通过DSC、DMA测定Tg和Tm",
            3: "能够分析结构因素对Tg的影响",
            4: "能够应用自由体积理论和WLF方程",
            5: "能够通过热转变行为优化材料设计"
        }
    },
    {
        "id": "gfz_ability_06",
        "name": "橡胶弹性理论应用能力",
        "description": "能够应用橡胶弹性的统计理论和唯象理论分析弹性行为",
        "related_chapters": ["第6章"],
        "related_kps": ["kp_6_2_1", "kp_6_3_1", "kp_6_5_1"],
        "level_descriptions": {
            1: "了解橡胶弹性的基本概念和特征",
            2: "能够区分熵弹性和能弹性",
            3: "能够应用统计理论计算弹性模量",
            4: "能够测定交联密度和分析溶胀行为",
            5: "能够设计橡胶配方和优化交联体系"
        }
    },
    {
        "id": "gfz_ability_07",
        "name": "黏弹性分析能力",
        "description": "能够分析聚合物的黏弹性行为，掌握蠕变、应力松弛和动态力学性能",
        "related_chapters": ["第7章"],
        "related_kps": ["kp_7_1_1", "kp_7_1_2", "kp_7_2_1", "kp_7_3_1"],
        "level_descriptions": {
            1: "了解黏弹性的基本概念和表现",
            2: "能够测定蠕变和应力松弛曲线",
            3: "能够应用力学模型描述黏弹性行为",
            4: "能够进行动态力学分析（DMA）",
            5: "能够应用时温等效原理预测长期性能"
        }
    },
    {
        "id": "gfz_ability_08",
        "name": "力学性能评价能力",
        "description": "能够评价聚合物的拉伸、冲击、疲劳等力学性能，分析屈服和断裂行为",
        "related_chapters": ["第8章"],
        "related_kps": ["kp_8_1_1", "kp_8_1_5", "kp_8_2_1", "kp_8_2_3"],
        "level_descriptions": {
            1: "了解应力-应变曲线和基本力学参数",
            2: "能够测定拉伸、弯曲、冲击性能",
            3: "能够分析屈服、银纹、剪切带现象",
            4: "能够应用断裂力学理论分析断裂行为",
            5: "能够通过增韧改性提高力学性能"
        }
    },
    {
        "id": "gfz_ability_09",
        "name": "流变性能测试能力",
        "description": "能够测定和分析聚合物熔体和溶液的流变性能，指导加工工艺",
        "related_chapters": ["第9章"],
        "related_kps": ["kp_9_1_2", "kp_9_2_1", "kp_9_4_3"],
        "level_descriptions": {
            1: "了解牛顿流体和非牛顿流体的区别",
            2: "能够测定黏度和流动曲线",
            3: "能够分析剪切变稀和弹性效应",
            4: "能够使用毛细管、旋转流变仪测试",
            5: "能够根据流变性能优化加工条件"
        }
    },
    {
        "id": "gfz_ability_10",
        "name": "电学性能测试能力",
        "description": "能够测定和分析聚合物的介电性能和导电性能",
        "related_chapters": ["第10章"],
        "related_kps": ["kp_10_1_1", "kp_10_1_2", "kp_10_2_1", "kp_10_2_2"],
        "level_descriptions": {
            1: "了解介电常数、介电损耗等基本概念",
            2: "能够测定介电常数和电导率",
            3: "能够分析介电松弛和极化机理",
            4: "能够表征导电聚合物的电学性能",
            5: "能够设计功能性电学材料"
        }
    },
    {
        "id": "gfz_ability_11",
        "name": "热学性能评价能力",
        "description": "能够评价聚合物的耐热性、热稳定性、导热性等热学性能",
        "related_chapters": ["第10章"],
        "related_kps": ["kp_10_3_1", "kp_10_3_2", "kp_10_3_3"],
        "level_descriptions": {
            1: "了解耐热性、热稳定性的概念",
            2: "能够测定热变形温度、维卡软化点",
            3: "能够进行TGA热重分析",
            4: "能够测定导热系数和热膨胀系数",
            5: "能够设计耐高温聚合物材料"
        }
    },
    {
        "id": "gfz_ability_12",
        "name": "表面与界面分析能力",
        "description": "能够表征和改性聚合物表面与界面，分析表界面性质",
        "related_chapters": ["第11章"],
        "related_kps": ["kp_11_2_1", "kp_11_4_1", "kp_11_6_1"],
        "level_descriptions": {
            1: "了解表面张力、润湿等基本概念",
            2: "能够测定接触角和表面能",
            3: "能够进行表面改性（等离子体、化学接枝）",
            4: "能够使用XPS、AFM等表征表面",
            5: "能够设计功能性表面和界面"
        }
    },
    {
        "id": "gfz_ability_13",
        "name": "共混与复合设计能力",
        "description": "能够设计聚合物共混物和复合材料，控制相容性和形态",
        "related_chapters": ["第2章", "第3章", "第7章"],
        "related_kps": ["kp_2_5_2", "kp_3_4_1", "kp_7_5_3", "kp_7_5_4"],
        "level_descriptions": {
            1: "了解共混和复合的基本概念",
            2: "能够判断共混物的相容性",
            3: "能够选择增容剂和界面改性方法",
            4: "能够表征共混物和复合材料的形态",
            5: "能够设计高性能共混和复合材料"
        }
    },
    {
        "id": "gfz_ability_14",
        "name": "材料改性设计能力",
        "description": "能够通过增韧、增强、功能化等手段改性聚合物材料",
        "related_chapters": ["第6章", "第8章", "第10章", "第11章"],
        "related_kps": ["kp_6_6_1", "kp_8_2_4", "kp_8_2_6", "kp_10_2_2"],
        "level_descriptions": {
            1: "了解材料改性的基本方法和目的",
            2: "能够选择合适的改性方法",
            3: "能够设计改性配方和工艺",
            4: "能够表征改性效果和优化参数",
            5: "能够开发新型功能材料"
        }
    },
    {
        "id": "gfz_ability_15",
        "name": "加工工艺设计能力",
        "description": "能够根据聚合物的性能设计合理的加工工艺参数",
        "related_chapters": ["第5章", "第9章"],
        "related_kps": ["kp_5_4_1", "kp_9_2_2", "kp_9_4_4"],
        "level_descriptions": {
            1: "了解聚合物的基本加工方法",
            2: "能够根据性能选择加工方法",
            3: "能够设计基本的加工工艺参数",
            4: "能够优化加工条件提高产品质量",
            5: "能够解决复杂的加工问题"
        }
    },
    {
        "id": "gfz_ability_16",
        "name": "综合分析与问题解决能力",
        "description": "能够综合运用高分子物理知识分析实际问题，提出解决方案",
        "related_chapters": ["全部"],
        "related_kps": [],  # 涉及多个知识点
        "level_descriptions": {
            1: "能够识别简单的材料问题",
            2: "能够分析问题的可能原因",
            3: "能够提出初步的解决方案",
            4: "能够设计实验验证解决方案",
            5: "能够创新性地解决复杂工程问题"
        }
    }
]

# 能力ID到名称的映射（向后兼容）
ABILITY_ID_TO_NAME = {
    ability["id"]: ability["name"] 
    for ability in ABILITIES_GFZ
}

# 能力分类
ABILITY_CATEGORIES = {
    "基础理论能力": ["gfz_ability_01", "gfz_ability_02", "gfz_ability_03", "gfz_ability_04"],
    "性能分析能力": ["gfz_ability_05", "gfz_ability_06", "gfz_ability_07", "gfz_ability_08", "gfz_ability_09"],
    "功能性能力": ["gfz_ability_10", "gfz_ability_11", "gfz_ability_12"],
    "设计开发能力": ["gfz_ability_13", "gfz_ability_14", "gfz_ability_15"],
    "综合应用能力": ["gfz_ability_16"]
}

def get_ability_by_id(ability_id):
    """根据ID获取能力"""
    for ability in ABILITIES_GFZ:
        if ability["id"] == ability_id:
            return ability
    return None

def get_abilities_by_chapter(chapter_name):
    """根据章节获取相关能力"""
    return [
        ability for ability in ABILITIES_GFZ 
        if chapter_name in ability.get("related_chapters", [])
    ]

def get_abilities_by_category(category):
    """根据分类获取能力"""
    ability_ids = ABILITY_CATEGORIES.get(category, [])
    return [get_ability_by_id(aid) for aid in ability_ids if get_ability_by_id(aid)]

def evaluate_ability_level(ability_id, knowledge_points_mastered):
    """
    评估能力等级
    knowledge_points_mastered: 已掌握的知识点ID列表
    """
    ability = get_ability_by_id(ability_id)
    if not ability:
        return 0
    
    related_kps = ability.get("related_kps", [])
    if not related_kps:
        return 0
    
    # 计算掌握比例
    mastered_count = sum(1 for kp in related_kps if kp in knowledge_points_mastered)
    mastery_ratio = mastered_count / len(related_kps)
    
    # 根据掌握比例确定等级
    if mastery_ratio >= 0.9:
        return 5
    elif mastery_ratio >= 0.7:
        return 4
    elif mastery_ratio >= 0.5:
        return 3
    elif mastery_ratio >= 0.3:
        return 2
    elif mastery_ratio > 0:
        return 1
    else:
        return 0

"""
高分子物理知识图谱数据
基于《高分子物理（第五版）》教材目录构建
"""

# 高分子物理课程知识图谱结构
# 模块(Module) -> 章节(Chapter/Section) -> 知识点(KnowledgePoint)

GFZ_KNOWLEDGE_GRAPH = {
    "modules": [
        {
            "id": "gfz_module_1",
            "name": "第1章 高分子链的结构",
            "description": "研究高分子链的化学组成、构型、构造和构象",
            "chapters": [
                {
                    "id": "gfz_chapter_1_1",
                    "name": "1.1 化学组成、构型、构造和共聚物的序列结构",
                    "knowledge_points": [
                        {"id": "kp_1_1_1", "name": "结构单元的化学组成", "importance": 5},
                        {"id": "kp_1_1_2", "name": "高分子链的构型", "importance": 5},
                        {"id": "kp_1_1_3", "name": "分子构造", "importance": 4},
                        {"id": "kp_1_1_4", "name": "共聚物的序列结构", "importance": 4},
                        {"id": "kp_1_1_5", "name": "研究高分子链结构的主要方法", "importance": 3}
                    ]
                },
                {
                    "id": "gfz_chapter_1_2",
                    "name": "1.2 构象",
                    "knowledge_points": [
                        {"id": "kp_1_2_1", "name": "微构象和宏构象", "importance": 5},
                        {"id": "kp_1_2_2", "name": "高分子链的柔性", "importance": 5},
                        {"id": "kp_1_2_3", "name": "高分子链的构象统计", "importance": 4},
                        {"id": "kp_1_2_4", "name": "蠕虫状链", "importance": 3},
                        {"id": "kp_1_2_5", "name": "晶体、熔体和溶液中的分子构象", "importance": 4}
                    ]
                }
            ]
        },
        {
            "id": "gfz_module_2",
            "name": "第2章 高分子的凝聚态结构",
            "description": "研究聚合物在固态和液态下的结构特征",
            "chapters": [
                {
                    "id": "gfz_chapter_2_1",
                    "name": "2.1 晶态聚合物结构",
                    "knowledge_points": [
                        {"id": "kp_2_1_1", "name": "基本概念", "importance": 4},
                        {"id": "kp_2_1_2", "name": "聚合物的晶体结构和研究方法", "importance": 5},
                        {"id": "kp_2_1_3", "name": "聚合物的结晶形态和研究方法", "importance": 5},
                        {"id": "kp_2_1_4", "name": "晶态聚合物的结构模型", "importance": 4},
                        {"id": "kp_2_1_5", "name": "结晶度和晶粒尺寸、片晶厚度", "importance": 4}
                    ]
                },
                {
                    "id": "gfz_chapter_2_2",
                    "name": "2.2 非晶态聚合物结构",
                    "knowledge_points": [
                        {"id": "kp_2_2_1", "name": "概述", "importance": 3},
                        {"id": "kp_2_2_2", "name": "无规线团模型及实验证据", "importance": 5},
                        {"id": "kp_2_2_3", "name": "局部有序模型及实验证据", "importance": 4},
                        {"id": "kp_2_2_4", "name": "高分子链的缠结", "importance": 5}
                    ]
                },
                {
                    "id": "gfz_chapter_2_3",
                    "name": "2.3 高分子液晶",
                    "knowledge_points": [
                        {"id": "kp_2_3_1", "name": "引言", "importance": 3},
                        {"id": "kp_2_3_2", "name": "小分子中介相及聚合物液晶的类型", "importance": 4},
                        {"id": "kp_2_3_3", "name": "液晶的光学织构和液晶相分类", "importance": 4},
                        {"id": "kp_2_3_4", "name": "高分子结构对液晶行为的影响", "importance": 4},
                        {"id": "kp_2_3_5", "name": "液晶态的表征", "importance": 3},
                        {"id": "kp_2_3_6", "name": "聚合物液晶理论", "importance": 4},
                        {"id": "kp_2_3_7", "name": "聚合物液晶的性质和应用", "importance": 3}
                    ]
                },
                {
                    "id": "gfz_chapter_2_4",
                    "name": "2.4 聚合物的取向结构",
                    "knowledge_points": [
                        {"id": "kp_2_4_1", "name": "取向现象和取向机理", "importance": 4},
                        {"id": "kp_2_4_2", "name": "取向度及其测定方法", "importance": 4},
                        {"id": "kp_2_4_3", "name": "取向研究的应用", "importance": 3}
                    ]
                },
                {
                    "id": "gfz_chapter_2_5",
                    "name": "2.5 多组分聚合物",
                    "knowledge_points": [
                        {"id": "kp_2_5_1", "name": "概述", "importance": 3},
                        {"id": "kp_2_5_2", "name": "相容性及其判别方法", "importance": 4},
                        {"id": "kp_2_5_3", "name": "形态", "importance": 4}
                    ]
                }
            ]
        },
        {
            "id": "gfz_module_3",
            "name": "第3章 高分子溶液",
            "description": "研究聚合物在溶液中的行为和性质",
            "chapters": [
                {
                    "id": "gfz_chapter_3_1",
                    "name": "3.1 聚合物的溶解",
                    "knowledge_points": [
                        {"id": "kp_3_1_1", "name": "溶解过程的特点", "importance": 4},
                        {"id": "kp_3_1_2", "name": "溶解过程的热力学分析", "importance": 5},
                        {"id": "kp_3_1_3", "name": "溶剂对聚合物溶解能力的判定", "importance": 4}
                    ]
                },
                {
                    "id": "gfz_chapter_3_2",
                    "name": "3.2 柔性链高分子溶液的热力学性质",
                    "knowledge_points": [
                        {"id": "kp_3_2_1", "name": "Flory-Huggins格子模型理论（平均场理论）", "importance": 5},
                        {"id": "kp_3_2_2", "name": "Flory-Krigbaum理论（稀溶液理论）", "importance": 5},
                        {"id": "kp_3_2_3", "name": "其他理论", "importance": 3}
                    ]
                },
                {
                    "id": "gfz_chapter_3_3",
                    "name": "3.3 高分子溶液的相平衡",
                    "knowledge_points": [
                        {"id": "kp_3_3_1", "name": "渗透压", "importance": 5},
                        {"id": "kp_3_3_2", "name": "相分离", "importance": 4}
                    ]
                },
                {
                    "id": "gfz_chapter_3_4",
                    "name": "3.4 共混聚合物相容性的热力学",
                    "knowledge_points": [
                        {"id": "kp_3_4_1", "name": "相分离的热力学", "importance": 4},
                        {"id": "kp_3_4_2", "name": "相分离的动力学", "importance": 4}
                    ]
                },
                {
                    "id": "gfz_chapter_3_5",
                    "name": "3.5 聚电解质溶液",
                    "knowledge_points": [
                        {"id": "kp_3_5_1", "name": "聚电解质溶液概念", "importance": 4},
                        {"id": "kp_3_5_2", "name": "聚电解质溶液的黏度", "importance": 4},
                        {"id": "kp_3_5_3", "name": "聚电解质溶液的渗透压", "importance": 3}
                    ]
                },
                {
                    "id": "gfz_chapter_3_6",
                    "name": "3.6 聚合物的浓溶液",
                    "knowledge_points": [
                        {"id": "kp_3_6_1", "name": "聚合物的增塑", "importance": 4},
                        {"id": "kp_3_6_2", "name": "聚合物溶液纺丝", "importance": 4},
                        {"id": "kp_3_6_3", "name": "凝胶和冻胶", "importance": 3}
                    ]
                }
            ]
        },
        {
            "id": "gfz_module_4",
            "name": "第4章 聚合物的分子量和分子量分布",
            "description": "研究聚合物分子量的统计特征和测定方法",
            "chapters": [
                {
                    "id": "gfz_chapter_4_1",
                    "name": "4.1 聚合物分子量的统计意义",
                    "knowledge_points": [
                        {"id": "kp_4_1_1", "name": "聚合物分子量的多分散性", "importance": 5},
                        {"id": "kp_4_1_2", "name": "统计平均分子量", "importance": 5},
                        {"id": "kp_4_1_3", "name": "分子量分布宽度", "importance": 4},
                        {"id": "kp_4_1_4", "name": "聚合物的分子量分布函数", "importance": 4}
                    ]
                },
                {
                    "id": "gfz_chapter_4_2",
                    "name": "4.2 聚合物分子量的测定方法",
                    "knowledge_points": [
                        {"id": "kp_4_2_1", "name": "端基分析", "importance": 3},
                        {"id": "kp_4_2_2", "name": "沸点升高和冰点降低", "importance": 3},
                        {"id": "kp_4_2_3", "name": "气相渗透法(VPO)", "importance": 4},
                        {"id": "kp_4_2_4", "name": "渗透压法(或膜渗透法)", "importance": 5},
                        {"id": "kp_4_2_5", "name": "光散射法", "importance": 5},
                        {"id": "kp_4_2_6", "name": "质谱法", "importance": 3},
                        {"id": "kp_4_2_7", "name": "黏度法", "importance": 5}
                    ]
                },
                {
                    "id": "gfz_chapter_4_3",
                    "name": "4.3 聚合物分子量分布的测定方法",
                    "knowledge_points": [
                        {"id": "kp_4_3_1", "name": "沉淀与溶解分级", "importance": 3},
                        {"id": "kp_4_3_2", "name": "体积排除色谱(SEC)", "importance": 5}
                    ]
                }
            ]
        },
        {
            "id": "gfz_module_5",
            "name": "第5章 聚合物的分子运动和转变",
            "description": "研究聚合物分子的运动特点和相转变行为",
            "chapters": [
                {
                    "id": "gfz_chapter_5_1",
                    "name": "5.1 聚合物分子运动的特点",
                    "knowledge_points": [
                        {"id": "kp_5_1_1", "name": "运动单元的多重性", "importance": 5},
                        {"id": "kp_5_1_2", "name": "分子运动的时间依赖性", "importance": 5},
                        {"id": "kp_5_1_3", "name": "分子运动的温度依赖性", "importance": 5}
                    ]
                },
                {
                    "id": "gfz_chapter_5_2",
                    "name": "5.2 黏弹行为的五个区域",
                    "knowledge_points": [
                        {"id": "kp_5_2_1", "name": "玻璃态(区)", "importance": 4},
                        {"id": "kp_5_2_2", "name": "玻璃-橡胶转变区", "importance": 5},
                        {"id": "kp_5_2_3", "name": "橡胶-弹性平台区", "importance": 4},
                        {"id": "kp_5_2_4", "name": "橡胶流动区", "importance": 4},
                        {"id": "kp_5_2_5", "name": "液体流动区", "importance": 4}
                    ]
                },
                {
                    "id": "gfz_chapter_5_3",
                    "name": "5.3 玻璃-橡胶转变行为",
                    "knowledge_points": [
                        {"id": "kp_5_3_1", "name": "玻璃化转变温度测定", "importance": 5},
                        {"id": "kp_5_3_2", "name": "玻璃化转变理论", "importance": 5},
                        {"id": "kp_5_3_3", "name": "影响玻璃化转变温度的因素", "importance": 5},
                        {"id": "kp_5_3_4", "name": "玻璃化转变温度以下的松弛——次级转变", "importance": 4}
                    ]
                },
                {
                    "id": "gfz_chapter_5_4",
                    "name": "5.4 结晶行为和结晶动力学",
                    "knowledge_points": [
                        {"id": "kp_5_4_1", "name": "分子结构与结晶能力、结晶速率", "importance": 5},
                        {"id": "kp_5_4_2", "name": "结晶动力学", "importance": 5}
                    ]
                },
                {
                    "id": "gfz_chapter_5_5",
                    "name": "5.5 熔融热力学",
                    "knowledge_points": [
                        {"id": "kp_5_5_1", "name": "熔融过程和熔点", "importance": 5},
                        {"id": "kp_5_5_2", "name": "影响Tm的因素", "importance": 5}
                    ]
                }
            ]
        },
        {
            "id": "gfz_module_6",
            "name": "第6章 橡胶弹性",
            "description": "研究橡胶材料的弹性行为和理论",
            "chapters": [
                {
                    "id": "gfz_chapter_6_1",
                    "name": "6.1 形变类型及描述力学行为的基本物理量",
                    "knowledge_points": [
                        {"id": "kp_6_1_1", "name": "形变类型", "importance": 4},
                        {"id": "kp_6_1_2", "name": "基本物理量", "importance": 4}
                    ]
                },
                {
                    "id": "gfz_chapter_6_2",
                    "name": "6.2 橡胶弹性的热力学分析",
                    "knowledge_points": [
                        {"id": "kp_6_2_1", "name": "橡胶弹性的热力学特征", "importance": 5}
                    ]
                },
                {
                    "id": "gfz_chapter_6_3",
                    "name": "6.3 橡胶弹性的统计理论",
                    "knowledge_points": [
                        {"id": "kp_6_3_1", "name": "状态方程", "importance": 5},
                        {"id": "kp_6_3_2", "name": "一般修正", "importance": 4},
                        {"id": "kp_6_3_3", "name": "幻象网络理论", "importance": 4}
                    ]
                },
                {
                    "id": "gfz_chapter_6_4",
                    "name": "6.4 橡胶弹性的唯象理论",
                    "knowledge_points": [
                        {"id": "kp_6_4_1", "name": "唯象理论基础", "importance": 4}
                    ]
                },
                {
                    "id": "gfz_chapter_6_5",
                    "name": "6.5 橡胶弹性的影响因素",
                    "knowledge_points": [
                        {"id": "kp_6_5_1", "name": "交联与缠结效应", "importance": 5},
                        {"id": "kp_6_5_2", "name": "溶胀效应", "importance": 4},
                        {"id": "kp_6_5_3", "name": "其他影响因素", "importance": 3}
                    ]
                },
                {
                    "id": "gfz_chapter_6_6",
                    "name": "6.6 热塑性弹性体",
                    "knowledge_points": [
                        {"id": "kp_6_6_1", "name": "嵌段共聚型热塑性弹性体", "importance": 4},
                        {"id": "kp_6_6_2", "name": "共混型热塑性弹性体", "importance": 4}
                    ]
                }
            ]
        },
        {
            "id": "gfz_module_7",
            "name": "第7章 聚合物的黏弹性",
            "description": "研究聚合物的黏弹性行为和力学松弛现象",
            "chapters": [
                {
                    "id": "gfz_chapter_7_1",
                    "name": "7.1 聚合物的力学松弛现象",
                    "knowledge_points": [
                        {"id": "kp_7_1_1", "name": "蠕变", "importance": 5},
                        {"id": "kp_7_1_2", "name": "应力松弛", "importance": 5},
                        {"id": "kp_7_1_3", "name": "滞后与内耗", "importance": 4}
                    ]
                },
                {
                    "id": "gfz_chapter_7_2",
                    "name": "7.2 黏弹性的数学描述",
                    "knowledge_points": [
                        {"id": "kp_7_2_1", "name": "力学模型", "importance": 5},
                        {"id": "kp_7_2_2", "name": "Boltzmann叠加原理", "importance": 5},
                        {"id": "kp_7_2_3", "name": "分子理论", "importance": 4}
                    ]
                },
                {
                    "id": "gfz_chapter_7_3",
                    "name": "7.3 时温等效和叠加",
                    "knowledge_points": [
                        {"id": "kp_7_3_1", "name": "时温等效原理", "importance": 5},
                        {"id": "kp_7_3_2", "name": "WLF方程", "importance": 5}
                    ]
                },
                {
                    "id": "gfz_chapter_7_4",
                    "name": "7.4 研究黏弹行为的实验方法",
                    "knowledge_points": [
                        {"id": "kp_7_4_1", "name": "瞬态测量", "importance": 4},
                        {"id": "kp_7_4_2", "name": "动态测量", "importance": 5}
                    ]
                },
                {
                    "id": "gfz_chapter_7_5",
                    "name": "7.5 聚合物、共混物及复合材料的结构与动态力学性能关系",
                    "knowledge_points": [
                        {"id": "kp_7_5_1", "name": "非晶态聚合物的玻璃化转变和次级转变", "importance": 4},
                        {"id": "kp_7_5_2", "name": "晶态、液晶态聚合物的松弛转变和相转变", "importance": 4},
                        {"id": "kp_7_5_3", "name": "共聚物、共混物的动态力学性能", "importance": 4},
                        {"id": "kp_7_5_4", "name": "复合材料的动态力学性能", "importance": 3}
                    ]
                }
            ]
        },
        {
            "id": "gfz_module_8",
            "name": "第8章 聚合物的屈服和断裂",
            "description": "研究聚合物材料的力学性能和破坏行为",
            "chapters": [
                {
                    "id": "gfz_chapter_8_1",
                    "name": "8.1 聚合物的塑性和屈服",
                    "knowledge_points": [
                        {"id": "kp_8_1_1", "name": "聚合物的应力-应变行为", "importance": 5},
                        {"id": "kp_8_1_2", "name": "屈服-冷拉机理和Considère作图法", "importance": 5},
                        {"id": "kp_8_1_3", "name": "屈服判据", "importance": 4},
                        {"id": "kp_8_1_4", "name": "剪切带的结构形态和应力分析", "importance": 4},
                        {"id": "kp_8_1_5", "name": "银纹现象", "importance": 5}
                    ]
                },
                {
                    "id": "gfz_chapter_8_2",
                    "name": "8.2 聚合物的断裂与强度",
                    "knowledge_points": [
                        {"id": "kp_8_2_1", "name": "脆性断裂和韧性断裂", "importance": 5},
                        {"id": "kp_8_2_2", "name": "聚合物的强度", "importance": 5},
                        {"id": "kp_8_2_3", "name": "断裂理论", "importance": 5},
                        {"id": "kp_8_2_4", "name": "聚合物的增强", "importance": 4},
                        {"id": "kp_8_2_5", "name": "聚合物的耐冲击性", "importance": 4},
                        {"id": "kp_8_2_6", "name": "塑料增韧", "importance": 5},
                        {"id": "kp_8_2_7", "name": "疲劳", "importance": 4}
                    ]
                }
            ]
        },
        {
            "id": "gfz_module_9",
            "name": "第9章 聚合物的流变性能",
            "description": "研究聚合物熔体和溶液的流动行为",
            "chapters": [
                {
                    "id": "gfz_chapter_9_1",
                    "name": "9.1 牛顿流体和非牛顿流体",
                    "knowledge_points": [
                        {"id": "kp_9_1_1", "name": "牛顿流体", "importance": 4},
                        {"id": "kp_9_1_2", "name": "非牛顿流体", "importance": 5},
                        {"id": "kp_9_1_3", "name": "流动曲线", "importance": 4}
                    ]
                },
                {
                    "id": "gfz_chapter_9_2",
                    "name": "9.2 聚合物熔体的切黏度",
                    "knowledge_points": [
                        {"id": "kp_9_2_1", "name": "测定方法", "importance": 4},
                        {"id": "kp_9_2_2", "name": "影响因素", "importance": 5}
                    ]
                },
                {
                    "id": "gfz_chapter_9_3",
                    "name": "9.3 多组分聚合物的流变行为",
                    "knowledge_points": [
                        {"id": "kp_9_3_1", "name": "黏度与组成的关系", "importance": 4},
                        {"id": "kp_9_3_2", "name": "流变性能与形态", "importance": 4}
                    ]
                },
                {
                    "id": "gfz_chapter_9_4",
                    "name": "9.4 聚合物熔体的弹性效应",
                    "knowledge_points": [
                        {"id": "kp_9_4_1", "name": "可回复的切形变", "importance": 4},
                        {"id": "kp_9_4_2", "name": "动态黏度", "importance": 4},
                        {"id": "kp_9_4_3", "name": "法向应力效应", "importance": 5},
                        {"id": "kp_9_4_4", "name": "挤出物膨胀", "importance": 4},
                        {"id": "kp_9_4_5", "name": "不稳定流动", "importance": 3}
                    ]
                },
                {
                    "id": "gfz_chapter_9_5",
                    "name": "9.5 拉伸黏度",
                    "knowledge_points": [
                        {"id": "kp_9_5_1", "name": "拉伸黏度的测定和应用", "importance": 4}
                    ]
                }
            ]
        },
        {
            "id": "gfz_module_10",
            "name": "第10章 聚合物的电学性能、热学性能和光学性能",
            "description": "研究聚合物的功能性物理性能",
            "chapters": [
                {
                    "id": "gfz_chapter_10_1",
                    "name": "10.1 聚合物的介电性能",
                    "knowledge_points": [
                        {"id": "kp_10_1_1", "name": "介电极化和介电常数", "importance": 5},
                        {"id": "kp_10_1_2", "name": "介电松弛", "importance": 5},
                        {"id": "kp_10_1_3", "name": "聚合物驻极体及热释电", "importance": 4},
                        {"id": "kp_10_1_4", "name": "聚合物的电击穿", "importance": 4},
                        {"id": "kp_10_1_5", "name": "聚合物的静电现象", "importance": 3}
                    ]
                },
                {
                    "id": "gfz_chapter_10_2",
                    "name": "10.2 聚合物的导电性能",
                    "knowledge_points": [
                        {"id": "kp_10_2_1", "name": "聚合物的电导率", "importance": 4},
                        {"id": "kp_10_2_2", "name": "导电聚合物的结构与导电性", "importance": 5},
                        {"id": "kp_10_2_3", "name": "离子电导", "importance": 4},
                        {"id": "kp_10_2_4", "name": "电致发光共轭聚合物、共轭聚合物光伏材料和太阳能电池", "importance": 4}
                    ]
                },
                {
                    "id": "gfz_chapter_10_3",
                    "name": "10.3 聚合物的热学性能",
                    "knowledge_points": [
                        {"id": "kp_10_3_1", "name": "耐热性", "importance": 5},
                        {"id": "kp_10_3_2", "name": "热稳定性", "importance": 5},
                        {"id": "kp_10_3_3", "name": "导热性", "importance": 4},
                        {"id": "kp_10_3_4", "name": "热膨胀", "importance": 4}
                    ]
                },
                {
                    "id": "gfz_chapter_10_4",
                    "name": "10.4 聚合物的光学性能",
                    "knowledge_points": [
                        {"id": "kp_10_4_1", "name": "光的折射和非线性光学性质", "importance": 4},
                        {"id": "kp_10_4_2", "name": "光的反射", "importance": 3},
                        {"id": "kp_10_4_3", "name": "光的吸收", "importance": 4}
                    ]
                }
            ]
        },
        {
            "id": "gfz_module_11",
            "name": "第11章 聚合物的表面与界面",
            "description": "研究聚合物表面与界面的性质和应用",
            "chapters": [
                {
                    "id": "gfz_chapter_11_1",
                    "name": "11.1 聚合物表面与界面",
                    "knowledge_points": [
                        {"id": "kp_11_1_1", "name": "表面与界面的基本概念", "importance": 4}
                    ]
                },
                {
                    "id": "gfz_chapter_11_2",
                    "name": "11.2 聚合物表面与界面热力学",
                    "knowledge_points": [
                        {"id": "kp_11_2_1", "name": "表面张力与润湿", "importance": 5},
                        {"id": "kp_11_2_2", "name": "界面张力的计算", "importance": 4}
                    ]
                },
                {
                    "id": "gfz_chapter_11_3",
                    "name": "11.3 聚合物表面与界面动力学",
                    "knowledge_points": [
                        {"id": "kp_11_3_1", "name": "表面与界面的动力学过程", "importance": 4}
                    ]
                },
                {
                    "id": "gfz_chapter_11_4",
                    "name": "11.4 聚合物表面与界面的测量、表征技术",
                    "knowledge_points": [
                        {"id": "kp_11_4_1", "name": "接触角测量", "importance": 4},
                        {"id": "kp_11_4_2", "name": "X射线光电子能谱法", "importance": 4},
                        {"id": "kp_11_4_3", "name": "离子散射谱", "importance": 3},
                        {"id": "kp_11_4_4", "name": "二次离子质谱", "importance": 3},
                        {"id": "kp_11_4_5", "name": "原子力显微技术", "importance": 4},
                        {"id": "kp_11_4_6", "name": "界面面积测量", "importance": 3}
                    ]
                },
                {
                    "id": "gfz_chapter_11_5",
                    "name": "11.5 聚合物共混物界面",
                    "knowledge_points": [
                        {"id": "kp_11_5_1", "name": "共混物界面特性", "importance": 4}
                    ]
                },
                {
                    "id": "gfz_chapter_11_6",
                    "name": "11.6 聚合物表面改性技术",
                    "knowledge_points": [
                        {"id": "kp_11_6_1", "name": "表面接枝", "importance": 4},
                        {"id": "kp_11_6_2", "name": "火焰处理", "importance": 3},
                        {"id": "kp_11_6_3", "name": "等离子体处理", "importance": 4},
                        {"id": "kp_11_6_4", "name": "表面电晕处理", "importance": 3},
                        {"id": "kp_11_6_5", "name": "表面金属化", "importance": 3}
                    ]
                },
                {
                    "id": "gfz_chapter_11_7",
                    "name": "11.7 生物医用高分子材料的表面改性及其应用",
                    "knowledge_points": [
                        {"id": "kp_11_7_1", "name": "抗细菌黏附策略", "importance": 4},
                        {"id": "kp_11_7_2", "name": "杀菌策略", "importance": 4},
                        {"id": "kp_11_7_3", "name": "抗细菌黏附-杀菌(抗-杀)结合策略", "importance": 4},
                        {"id": "kp_11_7_4", "name": "抗细菌黏附-杀菌转化表面构建策略", "importance": 3}
                    ]
                },
                {
                    "id": "gfz_chapter_11_8",
                    "name": "11.8 黏结",
                    "knowledge_points": [
                        {"id": "kp_11_8_1", "name": "黏结理论与机理", "importance": 4},
                        {"id": "kp_11_8_2", "name": "黏结薄弱层及内应力", "importance": 4},
                        {"id": "kp_11_8_3", "name": "结构胶黏剂", "importance": 3},
                        {"id": "kp_11_8_4", "name": "弹性体胶黏剂", "importance": 3}
                    ]
                }
            ]
        }
    ],
    
    # 知识点之间的前置关系（示例）
    "prerequisites": [
        # 第1章内部关系
        {"from": "kp_1_1_1", "to": "kp_1_1_2"},
        {"from": "kp_1_1_2", "to": "kp_1_2_1"},
        {"from": "kp_1_2_1", "to": "kp_1_2_2"},
        
        # 跨章节关系
        {"from": "kp_1_2_2", "to": "kp_5_1_1"},  # 链柔性 -> 分子运动
        {"from": "kp_2_1_2", "to": "kp_5_4_1"},  # 晶体结构 -> 结晶行为
        {"from": "kp_3_2_1", "to": "kp_3_3_1"},  # Flory-Huggins理论 -> 渗透压
        {"from": "kp_5_3_1", "to": "kp_7_1_1"},  # 玻璃化转变 -> 蠕变
        {"from": "kp_6_3_1", "to": "kp_7_2_1"},  # 橡胶弹性状态方程 -> 力学模型
    ]
}

# 导出函数
def get_gfz_modules():
    """获取所有模块"""
    return GFZ_KNOWLEDGE_GRAPH["modules"]

def get_gfz_module_by_id(module_id):
    """根据ID获取模块"""
    for module in GFZ_KNOWLEDGE_GRAPH["modules"]:
        if module["id"] == module_id:
            return module
    return None

def get_gfz_chapter_by_id(chapter_id):
    """根据ID获取章节"""
    for module in GFZ_KNOWLEDGE_GRAPH["modules"]:
        for chapter in module["chapters"]:
            if chapter["id"] == chapter_id:
                return chapter
    return None

def get_all_gfz_knowledge_points():
    """获取所有知识点"""
    kps = []
    for module in GFZ_KNOWLEDGE_GRAPH["modules"]:
        for chapter in module["chapters"]:
            kps.extend(chapter["knowledge_points"])
    return kps

def get_gfz_prerequisites():
    """获取知识点前置关系"""
    return GFZ_KNOWLEDGE_GRAPH["prerequisites"]

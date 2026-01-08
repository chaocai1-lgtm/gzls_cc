"""
高中历史题库数据
包含选择题、材料题、论述题等
"""

HISTORY_QUESTIONS = [
    # ===== 中国古代史 - 先秦时期 =====
    {
        "id": "q_ancient_001",
        "type": "choice",
        "chapter_id": "chapter_origin",
        "difficulty": "easy",
        "question": "夏朝是中国历史上第一个王朝，其建立者是？",
        "options": ["A. 黄帝", "B. 禹", "C. 汤", "D. 武王"],
        "answer": "B",
        "explanation": "禹是夏朝的开国君主，他因治水有功，被舜选为继承人，建立了中国第一个世袭制王朝。",
        "keywords": ["夏朝", "禹", "世袭制"],
        "ability": "ability_chronology"
    },
    {
        "id": "q_ancient_002",
        "type": "choice",
        "chapter_id": "chapter_origin",
        "difficulty": "medium",
        "question": "西周实行的分封制，其主要目的是？",
        "options": [
            "A. 削弱诸侯权力",
            "B. 巩固周王朝统治",
            "C. 发展商品经济",
            "D. 废除奴隶制度"
        ],
        "answer": "B",
        "explanation": "西周分封制是周王将土地和人民分封给诸侯，目的是通过血缘关系和政治联盟巩固周王朝的统治。",
        "keywords": ["西周", "分封制", "宗法制"],
        "ability": "ability_historical_interpretation"
    },
    {
        "id": "q_ancient_003",
        "type": "choice",
        "chapter_id": "chapter_warring_states",
        "difficulty": "medium",
        "question": "商鞅变法中，最能体现中央集权思想的措施是？",
        "options": [
            "A. 废除井田制，允许土地买卖",
            "B. 推行县制，由国君直接管理",
            "C. 奖励耕战，按军功授爵",
            "D. 统一度量衡"
        ],
        "answer": "B",
        "explanation": "推行县制，由国君直接派官员管理，削弱了地方贵族的权力，加强了中央集权。",
        "keywords": ["商鞅变法", "县制", "中央集权"],
        "ability": "ability_historical_interpretation"
    },
    {
        "id": "q_ancient_004",
        "type": "material",
        "chapter_id": "chapter_qin_unification",
        "difficulty": "hard",
        "question": """阅读材料，回答问题：
        
材料一："秦王扫六合，虎视何雄哉！挥剑决浮云，诸侯尽西来。"——李白
        
材料二："天下之事，无大小，皆决于上。上至以衡石量书，日夜有呈，不中呈不得休息。"——《史记·秦始皇本纪》

材料三："焚书令"规定："有敢偶语诗书者弃市，以古非今者族。"

请回答：
（1）材料一反映了秦始皇的什么历史功绩？（4分）
（2）材料二体现了秦朝什么样的政治特点？（4分）
（3）结合所学知识，分析材料三中"焚书坑儒"的历史影响。（6分）""",
        "answer": """（1）秦始皇统一六国，结束了春秋战国以来长期分裂割据的局面，建立了中国历史上第一个统一的多民族的中央集权国家。（4分）

（2）体现了秦朝高度中央集权的特点。皇帝独揽大权，所有政事都由皇帝一人决定，大臣只是执行者。这种制度使皇权得到极大加强。（4分）

（3）消极影响：焚书坑儒禁锢了思想，摧残了文化，造成了中国古代文化的巨大损失。（3分）
积极影响（或有限作用）：在一定程度上维护了统一，打击了反对统一的复辟势力。（3分）
【注：此题可从消极影响为主的角度作答】""",
        "scoring_points": [
            "统一六国",
            "中央集权",
            "思想文化摧残",
            "维护统一"
        ],
        "keywords": ["秦始皇", "统一", "中央集权", "焚书坑儒"],
        "ability": "ability_material_analysis"
    },
    
    # ===== 中国近代史 - 鸦片战争 =====
    {
        "id": "q_modern_001",
        "type": "choice",
        "chapter_id": "chapter_opium_wars",
        "difficulty": "easy",
        "question": "中国近代史开端的标志性事件是？",
        "options": [
            "A. 洋务运动",
            "B. 鸦片战争",
            "C. 甲午战争",
            "D. 辛亥革命"
        ],
        "answer": "B",
        "explanation": "1840年鸦片战争的爆发，标志着中国近代史的开端。战争失败后签订的《南京条约》，使中国开始沦为半殖民地半封建社会。",
        "keywords": ["鸦片战争", "近代史", "南京条约"],
        "ability": "ability_chronology"
    },
    {
        "id": "q_modern_002",
        "type": "choice",
        "chapter_id": "chapter_opium_wars",
        "difficulty": "medium",
        "question": "《南京条约》中，对中国主权危害最大的是？",
        "options": [
            "A. 割让香港岛",
            "B. 赔款2100万银元",
            "C. 开放五口通商",
            "D. 协定关税"
        ],
        "answer": "D",
        "explanation": "协定关税使中国丧失了关税自主权，这是主权受损最严重的体现，严重破坏了中国的经济主权。",
        "keywords": ["南京条约", "协定关税", "主权"],
        "ability": "ability_historical_interpretation"
    },
    {
        "id": "q_modern_003",
        "type": "material",
        "chapter_id": "chapter_reform_movement",
        "difficulty": "hard",
        "question": """阅读材料，回答问题：

材料一："师夷长技以制夷"——魏源《海国图志》

材料二：洋务派创办了江南制造总局、福州船政局等近代军事工业，后来又创办了轮船招商局、开平矿务局等民用工业。

材料三：1894年，在甲午战争中，北洋水师全军覆没。

请回答：
（1）材料一中"师夷长技"的含义是什么？这反映了当时中国人怎样的思想认识？（4分）
（2）根据材料二，概括洋务运动的主要内容。（4分）
（3）结合材料三和所学知识，分析洋务运动失败的根本原因。（6分）""",
        "answer": """（1）"师夷长技"指学习西方的先进技术。（2分）反映了当时中国先进知识分子开始认识到西方技术的先进性，主张学习西方以抵抗外来侵略。（2分）

（2）主要内容：创办近代军事工业（或"自强"）；创办近代民用工业（或"求富"）；创办新式学堂，培养人才；筹建海军。（答出2点得4分）

（3）根本原因：洋务运动只学习西方的技术，没有改变封建制度（2分）；指导思想是"中体西用"，维护封建统治（2分）；没有触动封建生产关系，无法真正实现国家富强（2分）。
【或答：不改变封建制度，只引进西方技术，不可能使国家真正富强。】""",
        "scoring_points": [
            "学习西方技术",
            "创办军事工业",
            "创办民用工业",
            "封建制度未变",
            "中体西用局限"
        ],
        "keywords": ["洋务运动", "师夷长技", "甲午战争", "中体西用"],
        "ability": "ability_material_analysis"
    },
    {
        "id": "q_modern_004",
        "type": "choice",
        "chapter_id": "chapter_xinhai_revolution",
        "difficulty": "medium",
        "question": "辛亥革命最伟大的历史功绩是？",
        "options": [
            "A. 建立了中华民国",
            "B. 推翻了清朝统治",
            "C. 结束了两千多年的君主专制制度",
            "D. 颁布了《中华民国临时约法》"
        ],
        "answer": "C",
        "explanation": "辛亥革命推翻了清朝统治，结束了中国两千多年的君主专制制度，建立了资产阶级共和国，这是其最伟大的历史功绩。",
        "keywords": ["辛亥革命", "君主专制", "民主共和"],
        "ability": "ability_historical_interpretation"
    },
    {
        "id": "q_modern_005",
        "type": "choice",
        "chapter_id": "chapter_may_fourth",
        "difficulty": "easy",
        "question": "五四运动的导火索是？",
        "options": [
            "A. 巴黎和会中国外交失败",
            "B. 北洋军阀黑暗统治",
            "C. 新文化运动的推动",
            "D. 俄国十月革命影响"
        ],
        "answer": "A",
        "explanation": "1919年巴黎和会上，中国作为战胜国，正当要求被拒绝，日本还接管了德国在山东的权益，激起了中国人民的强烈愤慨，引发了五四运动。",
        "keywords": ["五四运动", "巴黎和会", "外交失败"],
        "ability": "ability_chronology"
    },
    
    # ===== 中国现代史 =====
    {
        "id": "q_contemporary_001",
        "type": "choice",
        "chapter_id": "chapter_prc_founding",
        "difficulty": "easy",
        "question": "新中国成立的标志是？",
        "options": [
            "A. 三大战役胜利",
            "B. 渡江战役胜利",
            "C. 开国大典",
            "D. 西藏和平解放"
        ],
        "answer": "C",
        "explanation": "1949年10月1日，毛泽东在天安门城楼宣告中华人民共和国中央人民政府成立，这标志着新中国的诞生。",
        "keywords": ["新中国成立", "开国大典", "1949年"],
        "ability": "ability_chronology"
    },
    {
        "id": "q_contemporary_002",
        "type": "choice",
        "chapter_id": "chapter_reform_opening",
        "difficulty": "medium",
        "question": "改革开放的标志性事件是？",
        "options": [
            "A. 粉碎四人帮",
            "B. 十一届三中全会召开",
            "C. 深圳经济特区建立",
            "D. 家庭联产承包责任制"
        ],
        "answer": "B",
        "explanation": "1978年12月召开的十一届三中全会，作出了把党和国家工作重心转移到经济建设上来、实行改革开放的伟大决策，标志着改革开放的开始。",
        "keywords": ["改革开放", "十一届三中全会", "1978年"],
        "ability": "ability_chronology"
    },
    {
        "id": "q_contemporary_003",
        "type": "material",
        "chapter_id": "chapter_reform_opening",
        "difficulty": "hard",
        "question": """阅读材料，回答问题：

材料一："一九七九年，那是一个春天，有一位老人在中国的南海边画了一个圈……"——《春天的故事》

材料二：1980年，我国在深圳、珠海、汕头、厦门设立经济特区。

材料三：从1978年到2018年，中国GDP从3679亿元增长到90万亿元，年均增长9.5%，成为世界第二大经济体。

请回答：
（1）材料一中"画了一个圈"是什么意思？（3分）
（2）根据材料二，说明设立经济特区的目的。（4分）
（3）结合材料三，谈谈改革开放的历史意义。（7分）""",
        "answer": """（1）指在深圳等地设立经济特区，实行特殊的经济政策，对外开放。（3分）

（2）目的：引进外资、技术和管理经验（2分）；为全国的改革开放探索道路、积累经验（2分）。

（3）意义：
①使中国经济实现了快速发展，综合国力大幅提升，成为世界第二大经济体。（3分）
②改善了人民生活水平，实现了从温饱到小康的历史性跨越。（2分）
③推动了社会主义现代化建设，开辟了中国特色社会主义道路。（2分）
【或答：改革开放是决定当代中国命运的关键抉择，是实现中华民族伟大复兴的必由之路。】""",
        "scoring_points": [
            "经济特区",
            "引进外资技术",
            "经济快速发展",
            "人民生活改善",
            "中国特色社会主义"
        ],
        "keywords": ["改革开放", "经济特区", "深圳", "邓小平"],
        "ability": "ability_material_analysis"
    },
    
    # ===== 世界史 =====
    {
        "id": "q_world_001",
        "type": "choice",
        "chapter_id": "chapter_new_routes",
        "difficulty": "easy",
        "question": "发现美洲新大陆的航海家是？",
        "options": [
            "A. 迪亚士",
            "B. 达·伽马",
            "C. 哥伦布",
            "D. 麦哲伦"
        ],
        "answer": "C",
        "explanation": "1492年，哥伦布率领船队横渡大西洋，到达美洲，开辟了通往美洲的航路。",
        "keywords": ["哥伦布", "美洲", "新航路"],
        "ability": "ability_chronology"
    },
    {
        "id": "q_world_002",
        "type": "choice",
        "chapter_id": "chapter_industrial_revolution",
        "difficulty": "medium",
        "question": "第一次工业革命的标志性发明是？",
        "options": [
            "A. 珍妮纺纱机",
            "B. 改良蒸汽机",
            "C. 发电机",
            "D. 内燃机"
        ],
        "answer": "B",
        "explanation": "瓦特改良的蒸汽机为工业提供了强大动力，推动了第一次工业革命的发展，使人类进入'蒸汽时代'。",
        "keywords": ["工业革命", "蒸汽机", "瓦特"],
        "ability": "ability_chronology"
    },
    {
        "id": "q_world_003",
        "type": "choice",
        "chapter_id": "chapter_world_wars",
        "difficulty": "medium",
        "question": "第二次世界大战全面爆发的标志是？",
        "options": {
            "A": "德国突袭波兰",
            "B": "德国进攻苏联",
            "C": "日本偷袭珍珠港",
            "D": "英法对德宣战"
        },
        "answer": "A",
        "explanation": "1939年9月1日，德国突袭波兰，英法对德宣战，第二次世界大战全面爆发。",
        "keywords": ["二战", "德国", "波兰", "1939年"],
        "knowledge_point": "第二次世界大战",
        "ability": "ability_chronology"
    },
    
    # ===== 中国近代史 - 洋务运动 =====
    {
        "id": "q_modern_yangwu_001",
        "type": "choice",
        "chapter_id": "chapter_yangwu",
        "difficulty": "medium",
        "question": "洋务运动为什么最终失败？",
        "options": {
            "A": "缺乏先进技术",
            "B": "没有触动封建制度的根基",
            "C": "列强的反对和破坏",
            "D": "资金不足"
        },
        "answer": "B",
        "explanation": "洋务运动只学习西方的技术，不改变封建制度，'中体西用'的指导思想使得改革无法触及根本，甲午战争的失败标志着洋务运动的破产。",
        "keywords": ["洋务运动", "失败", "中体西用", "封建制度"],
        "knowledge_point": "洋务运动",
        "ability": "ability_historical_interpretation"
    },
    {
        "id": "q_modern_yangwu_002",
        "type": "choice",
        "chapter_id": "chapter_yangwu",
        "difficulty": "easy",
        "question": "洋务运动的代表人物不包括？",
        "options": {
            "A": "李鸿章",
            "B": "曾国藩",
            "C": "左宗棠",
            "D": "康有为"
        },
        "answer": "D",
        "explanation": "康有为是戊戌变法的代表人物，不是洋务运动的代表。洋务运动的代表人物有李鸿章、曾国藩、左宗棠、张之洞等。",
        "keywords": ["洋务运动", "代表人物"],
        "knowledge_point": "洋务运动",
        "ability": "ability_chronology"
    },
    
    # ===== 辛亥革命 =====
    {
        "id": "q_modern_xinhai_001",
        "type": "choice",
        "chapter_id": "chapter_xinhai",
        "difficulty": "medium",
        "question": "辛亥革命的历史意义是什么？",
        "options": {
            "A": "彻底完成了反帝反封建任务",
            "B": "推翻了清朝统治，结束了君主专制制度",
            "C": "建立了资产阶级共和国",
            "D": "改变了中国半殖民地半封建社会性质"
        },
        "answer": "B",
        "explanation": "辛亥革命推翻了清朝统治，结束了2000多年的君主专制制度，使民主共和观念深入人心。但没有改变中国半殖民地半封建社会的性质，没有完成反帝反封建任务。",
        "keywords": ["辛亥革命", "历史意义", "君主专制"],
        "knowledge_point": "辛亥革命",
        "ability": "ability_historical_interpretation"
    },
    {
        "id": "q_modern_xinhai_002",
        "type": "choice",
        "chapter_id": "chapter_xinhai",
        "difficulty": "easy",
        "question": "辛亥革命发生的时间是？",
        "options": {
            "A": "1911年",
            "B": "1912年",
            "C": "1919年",
            "D": "1921年"
        },
        "answer": "A",
        "explanation": "辛亥革命发生在1911年（辛亥年），武昌起义爆发于1911年10月10日，因此也称'双十起义'。",
        "keywords": ["辛亥革命", "1911年", "武昌起义"],
        "knowledge_point": "辛亥革命",
        "ability": "ability_chronology"
    },
    
    # ===== 中国共产党成立 =====
    {
        "id": "q_modern_cpc_001",
        "type": "choice",
        "chapter_id": "chapter_cpc",
        "difficulty": "hard",
        "question": "中国共产党成立的历史条件有哪些？（多选）",
        "options": {
            "A": "马克思主义在中国的传播",
            "B": "五四运动的推动",
            "C": "工人运动的发展",
            "D": "共产国际的帮助"
        },
        "answer": "ABCD",
        "explanation": "中国共产党成立的历史条件包括：思想基础（马克思主义传播）、阶级基础（工人运动发展）、干部基础（五四运动锻炼了骨干）、外部条件（共产国际帮助）。",
        "keywords": ["中国共产党", "成立条件", "1921年"],
        "knowledge_point": "中国共产党成立",
        "ability": "ability_historical_interpretation"
    },
    {
        "id": "q_modern_cpc_002",
        "type": "choice",
        "chapter_id": "chapter_cpc",
        "difficulty": "easy",
        "question": "中国共产党第一次全国代表大会召开的地点是？",
        "options": {
            "A": "北京",
            "B": "上海",
            "C": "广州",
            "D": "延安"
        },
        "answer": "B",
        "explanation": "1921年7月，中国共产党第一次全国代表大会在上海召开（后转移到浙江嘉兴南湖），宣告了中国共产党的诞生。",
        "keywords": ["中共一大", "上海", "1921年"],
        "knowledge_point": "中国共产党成立",
        "ability": "ability_chronology"
    },
    
    # ===== 戊戌变法 =====
    {
        "id": "q_modern_wuxu_001",
        "type": "choice",
        "chapter_id": "chapter_wuxu",
        "difficulty": "medium",
        "question": "戊戌变法失败的根本原因是？",
        "options": {
            "A": "变法时间太短",
            "B": "缺乏群众基础，脱离人民",
            "C": "慈禧太后和顽固派的反对",
            "D": "光绪帝没有实权"
        },
        "answer": "B",
        "explanation": "戊戌变法失败的根本原因是资产阶级维新派力量薄弱，脱离人民群众，缺乏群众基础。直接原因是慈禧太后为首的顽固派发动政变。",
        "keywords": ["戊戌变法", "失败原因"],
        "knowledge_point": "戊戌变法",
        "ability": "ability_historical_interpretation"
    },
    {
        "id": "q_modern_wuxu_002",
        "type": "choice",
        "chapter_id": "chapter_wuxu",
        "difficulty": "easy",
        "question": "戊戌变法的时间持续了多久？",
        "options": {
            "A": "103天",
            "B": "一年",
            "C": "两年",
            "D": "半年"
        },
        "answer": "A",
        "explanation": "戊戌变法从1898年6月11日光绪帝颁布'明定国是'诏书开始，到9月21日慈禧太后发动政变为止，历时103天，因此也称'百日维新'。",
        "keywords": ["戊戌变法", "百日维新", "103天"],
        "knowledge_point": "戊戌变法",
        "ability": "ability_chronology"
    },
    
    # ===== 材料分析题 =====
    {
        "id": "q_material_yangwu_001",
        "type": "material",
        "chapter_id": "chapter_yangwu",
        "difficulty": "medium",
        "question": "阅读下列材料，回答问题：\n\n材料：\"师夷长技以自强\"\"中学为体，西学为用\"\n\n（1）这些口号反映了哪次改革运动的指导思想？（2分）\n（2）这次运动创办了哪些著名企业？举例说明。（4分）\n（3）这次运动失败的标志是什么？为什么会失败？（4分）",
        "material": "\"师夷长技以自强\"\"中学为体，西学为用\"",
        "answer": "（1）洋务运动（或自强运动、洋务新政）\n\n（2）军事工业：安庆内军械所、江南制造总局、福州船政局等；民用工业：轮船招商局、开平煤矿、汉阳铁厂等。\n\n（3）失败标志：1894年甲午战争中北洋水师全军覆没。失败原因：①根本原因：没有触动封建制度的根基，只学技术不改制度；②直接原因：顽固派阻挠，列强不愿中国强大；③缺乏科学规划和统一部署。",
        "keywords": ["洋务运动", "材料题", "中体西用"],
        "knowledge_point": "洋务运动",
        "ability": "ability_text_evidence"
    },
    {
        "id": "q_material_xinhai_001",
        "type": "material",
        "chapter_id": "chapter_xinhai",
        "difficulty": "hard",
        "question": "阅读下列材料，回答问题：\n\n材料一：孙中山在《民报》发刊词中提出\"三民主义\"\n材料二：1912年元旦，中华民国临时政府在南京成立\n\n（1）'三民主义'的具体内容是什么？（3分）\n（2）辛亥革命的主要成果有哪些？（3分）\n（3）如何评价辛亥革命的历史地位？（4分）",
        "material": "材料一：孙中山在《民报》发刊词中提出\"三民主义\"\n材料二：1912年元旦，中华民国临时政府在南京成立",
        "answer": "（1）三民主义包括：①民族主义（驱除鞑虏，恢复中华）；②民权主义（创立民国）；③民生主义（平均地权）。\n\n（2）主要成果：①推翻了清朝统治，结束了两千多年的君主专制制度；②建立了中华民国，使民主共和观念深入人心；③颁布了《临时约法》；④推动了社会进步和思想解放。\n\n（3）历史地位：①是中国近代史上一次伟大的反帝反封建革命运动；②具有划时代意义，是中国近代化进程中的重要里程碑；③但没有改变中国半殖民地半封建社会的性质，革命任务没有完成。",
        "keywords": ["辛亥革命", "三民主义", "材料题"],
        "knowledge_point": "辛亥革命",
        "ability": "ability_text_evidence"
    },
    {
        "id": "q_material_cpc_001",
        "type": "material",
        "chapter_id": "chapter_cpc",
        "difficulty": "medium",
        "question": "阅读下列材料，回答问题：\n\n材料：1921年7月，中共一大在上海召开，会议确定党的名称为'中国共产党'，党的奋斗目标是推翻资产阶级，建立无产阶级专政。\n\n（1）中国共产党成立的时间和地点？（2分）\n（2）中国共产党成立的历史意义是什么？（4分）\n（3）中国共产党成立的条件有哪些？（4分）",
        "material": "1921年7月，中共一大在上海召开，会议确定党的名称为'中国共产党'，党的奋斗目标是推翻资产阶级，建立无产阶级专政。",
        "answer": "（1）时间：1921年7月；地点：上海（后转移到浙江嘉兴南湖）。\n\n（2）历史意义：①中国共产党的成立是中国历史上开天辟地的大事；②使中国革命面貌焕然一新；③为中国革命指明了方向；④中国革命从此有了坚强的领导核心。\n\n（3）成立条件：①思想基础：马克思主义在中国的传播；②阶级基础：工人阶级队伍壮大，工人运动发展；③组织基础：各地共产党早期组织的建立；④外部条件：共产国际的帮助；⑤干部基础：五四运动培养了一批先进分子。",
        "keywords": ["中国共产党", "中共一大", "材料题"],
        "knowledge_point": "中国共产党成立",
        "ability": "ability_text_evidence"
    }
]


def get_questions_by_chapter(chapter_id):
    """根据章节ID获取题目"""
    return [q for q in HISTORY_QUESTIONS if q.get('chapter_id') == chapter_id]


def get_questions_by_type(question_type):
    """根据题型获取题目"""
    return [q for q in HISTORY_QUESTIONS if q.get('type') == question_type]


def get_questions_by_difficulty(difficulty):
    """根据难度获取题目"""
    return [q for q in HISTORY_QUESTIONS if q.get('difficulty') == difficulty]


def search_questions(keyword):
    """根据关键词搜索题目"""
    results = []
    keyword = keyword.lower()
    
    for q in HISTORY_QUESTIONS:
        # 搜索题目内容
        if keyword in q.get('question', '').lower():
            results.append(q)
            continue
        
        # 搜索关键词
        for kw in q.get('keywords', []):
            if keyword in kw.lower():
                results.append(q)
                break
    
    return results

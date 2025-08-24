import random
import time

class HorrorMansionGame:
    def __init__(self, num_players):
        self.num_players = num_players
        self.players = []
        self.fear_level = 1
        self.max_fear_level = 6
        self.mansion_deck = []
        self.core_secrets = []
        self.explored_rooms = []
        self.hand_cards = []
        self.defeated_monsters = []
        self.game_over = False
        self.victory = False
        self.silence_mode = False
        self.silence_duration = 0
        self.trust_crisis = False
        self.trust_crisis_duration = 0
        self.last_action = ""
        self.d30_event_count = 0
        self.consecutive_d30 = 0
        self.next_turn_difficulty_penalty = False
        self.skip_mansion_turn = False
        self.skip_player_turn = False
        self.eye_of_mansion = False
        self.eye_duration = 0
        self.temp_fear_increase = False
        self.original_fear = 1
        self.defeated_monsters = []  # 添加缺失的变量

        # K牌秘密
        self.k_secrets = {
            "♠": {
                "name": "谋杀与怨念",
                "description": "古宅曾是一个残忍连环杀手的巢穴。他的恶灵即是古宅本身，渴望永远重复他的暴行。",
                "modifier": -2
            },
            "♥": {
                "name": "扭曲的爱",
                "description": "古宅的主人曾进行黑暗仪式企图复活死去的爱人，却将两者的灵魂痛苦地融合并束缚于此。",
                "modifier": 0
            },
            "♦": {
                "name": "贪婪的契约",
                "description": "宅邸的原主人与某个不可名状的存在签订了契约，古宅变成了一座活体监狱。",
                "modifier": "hand_bonus"
            },
            "♣": {
                "name": "异界裂隙",
                "description": "古宅建造在一个现实世界的薄弱点上，抑制着另一个充满噩梦的维度渗透进来。",
                "modifier": 2
            }
        }
        
        # D30事件表
        self.d30_events = {
            "1": {"name": "群魔乱舞", "effect": self.event_1, "description": "所有肖像画的眼睛开始流血并注视着玩家"},
            "2": {"name": "血肉之墙", "effect": self.event_2, "description": "墙壁变得柔软、温热并开始搏动"},
            "3": {"name": "时光倒流", "effect": self.event_3, "description": "场景切换回刚进入古宅时的样子"},
            "4": {"name": "窃窃私语", "effect": self.event_4, "description": "恶毒声音在每个人耳边低语最深处的秘密"},
            "5": {"name": "镜像自我", "effect": self.event_5, "description": "每个玩家都在倒影中看到另一个充满恶意的自己"},
            "6": {"name": "无尽回廊", "effect": self.event_6, "description": "通道被封锁，出口消失"},
            "7": {"name": "孩童歌谣", "effect": self.event_7, "description": "远处传来空灵、走调的孩童歌唱声"},
            "8": {"name": "提线木偶", "effect": self.event_8, "description": "一名玩家的手臂不由自主地抬起"},
            "9": {"name": "腐化盛宴", "effect": self.event_9, "description": "房间出现腐烂生蛆但却散发着香气的盛宴"},
            "10": {"name": "死者苏生", "effect": self.event_10, "description": "已故之人重新出现并变得更强大"},
            "11": {"name": "空间折叠", "effect": self.event_11, "description": "房间之间的空间关系发生扭曲变化"},
            "12": {"name": "记忆侵蚀", "effect": self.event_12, "description": "玩家的记忆被古宅逐渐吞噬"},
            "13": {"name": "虫巢爆发", "effect": self.event_13, "description": "无数虫类从各种缝隙中涌出"},
            "14": {"name": "哀悼之影", "effect": self.event_14, "description": "半透明的哀悼者身影在房间角落出现"},
            "15": {"name": "献祭要求", "effect": self.event_15, "description": "古宅要求玩家献上祭品"},
            "16": {"name": "时间跳跃", "effect": self.event_16, "description": "时间突然跳跃，蜡烛烧掉一大截"},
            "17": {"name": "寄生触手", "effect": self.event_17, "description": "油腻的触须状物从影子中伸出"},
            "18": {"name": "全视之眼", "effect": self.event_18, "description": "天花板上睁开一只巨大的眼睛"},
            "19": {"name": "声音剥夺", "effect": self.event_19, "description": "所有的声音瞬间消失"},
            "20": {"name": "过去重现", "effect": self.event_20, "description": "古宅中曾发生的悲剧事件重现在眼前"},
            "21": {"name": "扭曲生长", "effect": self.event_21, "description": "古宅的木质结构开始疯狂生长"},
            "22": {"name": "信任危机", "effect": self.event_22, "description": "古宅的低语在玩家之间播种猜疑"},
            "23": {"name": "重力失效", "effect": self.event_23, "description": "房间内的重力方向突然改变"},
            "24": {"name": "模仿者", "effect": self.event_24, "description": "门外传来模仿亲友的呼救声"},
            "25": {"name": "绝望具象", "effect": self.event_25, "description": "玩家的恐惧凝聚成黑色人形"},
            "26": {"name": "生命汲取", "effect": self.event_26, "description": "古宅从玩家身上吸取生命力"},
            "27": {"name": "强制交换", "effect": self.event_27, "description": "玩家之间的理智或生命值被强制交换"},
            "28": {"name": "门户洞开", "effect": self.event_28, "description": "地板上出现通往绝对黑暗的洞口"},
            "29": {"name": "古宅之心", "effect": self.event_29, "description": "玩家短暂感受到古宅那古老冰冷的意识"},
            "30": {"name": "古宅获胜", "effect": self.event_30, "description": "古宅展示了它真正的力量"}
        }
    
    def setup_game(self):
        """初始化游戏"""
        print("===== 古宅低语 - 游戏初始化 =====")
        
        # 创建玩家 - 允许自定义名称
        for i in range(self.num_players):
            name = input(f"请输入玩家{i+1}的名称: ")
            self.players.append({
                'name': name,
                'sanity': 15,  # 加强到15
                'health': 15,   # 加强到15
                'alive': True,
                'stunned': False,
                'restricted': False,
                'max_sanity': 15,  # 加强到15
                'max_health': 15   # 加强到15
            })
            print(f"欢迎 {name} 加入游戏！")
        
        # 创建牌堆
        self.create_decks()
        print("古宅牌堆和核心秘密已创建...")
        
        # 设置恐惧等级
        self.fear_level = 1
        print(f"初始恐惧等级: {self.fear_level}")
        
        print("游戏准备就绪！古宅的大门缓缓打开...")
        time.sleep(2)
    
    def create_decks(self):
        """创建扑克牌堆"""
        suits = ['♠', '♥', '♦', '♣']
        values = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
        
        full_deck = []
        for suit in suits:
            for value in values:
                full_deck.append({'suit': suit, 'value': value})
        
        # 移除四张K作为核心秘密
        self.core_secrets = [card for card in full_deck if card['value'] == 'K']
        random.shuffle(self.core_secrets)
        
        # 剩余的牌作为古宅牌堆
        self.mansion_deck = [card for card in full_deck if card['value'] != 'K']
        random.shuffle(self.mansion_deck)
        
        # 初始手牌为空
        self.hand_cards = []
        self.explored_rooms = []  # 初始化已探索房间列表
    
    def d4_roll(self):
        """投掷4面骰"""
        return random.randint(1, 4)
    
    def d6_roll(self):
        """投掷6面骰"""
        return random.randint(1, 6)
    
    def d30_roll(self):
        """投掷30面骰"""
        return random.randint(1, 30)
    
    def check_success(self, difficulty=None, player_idx=0):
        """进行检定"""
        if difficulty is None:
            difficulty = self.fear_level
        
        # 高恐惧等级增加检定难度
        if self.fear_level >= 5:
            difficulty += 1
            print(f"【恐惧笼罩】检定难度+1 (当前难度: {difficulty})")
        
        # 环境压抑效果
        if self.next_turn_difficulty_penalty:
            difficulty += 1
            print(f"【环境压抑】检定难度+1 (当前难度: {difficulty})")
        
        roll = self.d6_roll()
        print(f"投掷D6: {roll}, 难度: {difficulty}")
            
        return roll >= difficulty
    
    def player_turn(self, player_idx):
        """玩家回合"""
        player = self.players[player_idx]
        
        if not player['alive']:
            print(f"{player['name']} 已失去行动能力")
            return
        
        if self.skip_player_turn:
            print(f"由于时间跳跃，跳过{player['name']}的回合")
            self.skip_player_turn = False
            return
            
        if player['stunned']:
            print(f"{player['name']} 处于眩晕状态，跳过回合")
            player['stunned'] = False
            return
            
        if player['restricted']:
            print(f"{player['name']} 的行动受到限制，只能探索")
            self.last_action = "探索房间"
            self.explore_room(player_idx)
            player['restricted'] = False
            return
        
        print(f"\n===== {player['name']}的回合 =====")
        print(f"理智: {player['sanity']}/15, 生命: {player['health']}/15")  # 改为15
        
        # 在声音剥夺模式下，限制通信
        if self.silence_mode:
            print("【声音剥夺中】你无法听到任何声音，也无法说话")
        
        # 在信任危机模式下，限制合作
        if self.trust_crisis:
            print("【信任危机】玩家之间不能共享信息")
        
        # 玩家行动选择
        action = input("选择行动: (1)探索 (2)调查 (3)稳住心神: ")
        
        if action == "1":
            self.last_action = "探索房间"
            self.explore_room(player_idx)
        elif action == "2":
            self.last_action = "调查房间"
            self.investigate_room(player_idx)
        elif action == "3":
            self.last_action = "稳住心神"
            self.calm_mind(player_idx)
        else:
            print("无效行动，跳过回合")
    
    def explore_room(self, player_idx):
        """探索新房间"""
        if not self.mansion_deck:
            print("古宅已探索完毕！")
            return
        
        card = self.mansion_deck.pop()
        self.explored_rooms.append(card)
        print(f"探索到新房间: {card['suit']}{card['value']}")
        
        # 高恐惧等级增加遭遇难度
        encounter_difficulty = self.fear_level
        if self.fear_level >= 5:
            encounter_difficulty += 1
            print(f"【恐惧笼罩】遭遇难度增加")
        
        # 根据花色解析遭遇
        if card['suit'] == '♠':  # 黑桃 - 直接的恐怖
            print("一股寒意袭来...")
            if not self.check_success(difficulty=encounter_difficulty, player_idx=player_idx):
                damage = 1  # 伤害增加
                if self.fear_level >= 5:
                    damage = 2  # 伤害增加
                    print("【极端恐惧】伤害加倍！")
                print(f"你未能抵抗恐惧，失去{damage}点理智和{damage}点生命")
                self.players[player_idx]['sanity'] = max(0, self.players[player_idx]['sanity'] - damage)
                self.players[player_idx]['health'] = max(0, self.players[player_idx]['health'] - damage)
            else:
                print("你成功抵抗了恐惧")
        
        elif card['suit'] == '♥':  # 红心 - 扭曲的慰藉
            print("你看到了一些令人安心的东西...但感觉不太对劲")
            choice = input("选择恢复2点理智？(y/n): ")  # 恢复量增加
            if choice.lower() == 'y':
                self.players[player_idx]['sanity'] = min(15, self.players[player_idx]['sanity'] + 2)  # 改为15
                d4 = self.d4_roll()
                print(f"投掷D4: {d4}")
                if d4 >= (3 if self.fear_level < 5 else 2): # 高恐惧等级更容易发现假象
                    damage = 2 if self.fear_level >= 5 else 1
                    print(f"你发现那是假象，失去{damage}点理智")
                    self.players[player_idx]['sanity'] = max(0, self.players[player_idx]['sanity'] - damage)
        
        elif card['suit'] == '♦':  # 方块 - 资源与风险
            print("你找到了一些可能有用的东西...")
            if self.mansion_deck:
                hand_card = self.mansion_deck.pop()
                self.hand_cards.append(hand_card)
                print(f"获得手牌: {hand_card['suit']}{hand_card['value']}")
            
            d4 = self.d4_roll()
            print(f"投掷D4: {d4}, 恐惧等级: {self.fear_level}")
            
            # 增加D30事件触发概率
            d30_chance = 0
            if self.fear_level >= 4:
                d30_chance = 0.3  # 30%概率触发D30事件
            if self.fear_level >= 5:
                d30_chance = 0.5  # 50%概率触发D30事件
                
            if random.random() < d30_chance:
                print("你的行动惊动了古宅深处的存在！")
                self.trigger_d30_event()
            elif d4 >= (self.fear_level - 1 if self.fear_level >= 5 else self.fear_level):
                print("你惊动了什么！")
                self.mansion_action()
        
        elif card['suit'] == '♣':  # 梅花 - 谜团与痕迹
            print("你发现了奇怪的痕迹...")
            if self.check_success(difficulty=self.fear_level, player_idx=player_idx):
                if self.core_secrets:
                    secret = self.core_secrets[0]
                    print(f"你瞥见了古宅的秘密: {secret['suit']}{secret['value']}")
                else:
                    print("你没有发现更多秘密")
            else:
                damage = 2 if self.fear_level >= 5 else 1
                print(f"你什么也没看懂，反而感到困惑，失去{damage}点理智")
                self.players[player_idx]['sanity'] = max(0, self.players[player_idx]['sanity'] - damage)
        
        self.check_player_status()
    
    def investigate_room(self, player_idx):
        """调查房间"""
        if not self.explored_rooms:
            print("没有房间可以调查")
            return
        
        print("调查房间...")
        difficulty = self.fear_level
        if self.fear_level >= 5:
            difficulty += 1
            
        if self.check_success(difficulty=difficulty, player_idx=player_idx):
            if self.mansion_deck:
                card = self.mansion_deck.pop()
                self.hand_cards.append(card)
                print(f"你发现了一个线索: {card['suit']}{card['value']}")
                
                # 显示当前手牌
                print(f"当前手牌: {len(self.hand_cards)}张")
                for i, card in enumerate(self.hand_cards):
                    print(f"{i+1}. {card['suit']}{card['value']}")
                
                # 检查是否可以揭示秘密 - 根据恐惧等级调整所需手牌数量
                if self.fear_level <= 4:
                    required = 5  # 恐惧等级1-4时需要5张手牌
                else:
                    required = 3  # 恐惧等级5以上时需要3张手牌
                
                if len(self.hand_cards) >= required:
                    print(f"你已收集到{len(self.hand_cards)}张手牌 (需要{required}张来揭示秘密)")
                    choice = input("是否尝试揭示秘密？(y/n): ")
                    if choice.lower() == 'y':
                        self.reveal_secret()
            else:
                print("没有更多线索了")
        else:
            print("调查失败，没有发现任何东西")
            
            # 调查失败时也有可能触发D30事件
            if self.fear_level >= 4 and random.random() < 0.2:
                print("你的失败调查引起了古宅的注意！")
                self.trigger_d30_event()
    
    def calm_mind(self, player_idx):
        """稳住心神"""
        print("尝试稳住心神...")
        difficulty = self.fear_level
        if self.fear_level >= 5:
            difficulty += 1
            
        if self.check_success(difficulty=difficulty, player_idx=player_idx):
            recover = 3 if self.fear_level >= 5 else 2  # 恢复量增加
            self.players[player_idx]['sanity'] = min(15, self.players[player_idx]['sanity'] + recover)  # 改为15
            print(f"理智恢复{recover}点")
        else:
            print("未能稳住心神")
            
            # 稳住心神失败时也有可能触发D30事件
            if self.fear_level >= 4 and random.random() < 0.15:
                print("你的精神波动吸引了古宅的恶意！")
                self.trigger_d30_event()
    
    def trigger_d30_event(self):
        """触发D30事件"""
        self.d30_event_count += 1
        self.consecutive_d30 += 1
        
        print(f"\n=== D30事件 #{self.d30_event_count} ===")
        
        # 连续D30事件会增加强度
        intensity = min(3, self.consecutive_d30)
        if intensity > 1:
            print(f"【连续事件】这是连续第{self.consecutive_d30}个D30事件！效果增强")
        
        d30 = self.d30_roll()
        event_info = self.d30_events.get(str(d30), {"name": "未知事件", "effect": self.event_default})
        print(f"D30投掷: {d30} - {event_info['name']}")
        
        # 执行事件效果
        event_info['effect']()
        
        # 高恐惧等级下可能触发额外事件
        if self.fear_level >= 5 and random.random() < 0.3:
            print("【连锁反应】一个事件引发了另一个事件！")
            self.trigger_d30_event()
    
    def mansion_action(self):
        """执行古宅行动"""
        d4 = self.d4_roll()
        print(f"古宅行动投掷D4: {d4}")
        
        # 根据恐惧等级决定行动类型
        if self.fear_level <= 2:  # 低度威胁
            if d4 == 1 or d4 == 2:
                print("窸窣作响...无事发生，但令人不安")
            elif d4 == 3:
                print("幻象出现...")
                player_idx = random.randint(0, self.num_players-1)
                if self.players[player_idx]['alive'] and not self.check_success(player_idx=player_idx):
                    print(f"{self.players[player_idx]['name']} 未能抵抗幻象，失去1点理智") 
                    self.players[player_idx]['sanity'] = max(0, self.players[player_idx]['sanity'] - 1)
            elif d4 == 4:
                # 低恐惧等级也有概率触发D30事件
                if random.random() < 0.2:
                    print("古宅的不安凝聚成了实体！")
                    self.trigger_d30_event()
                else:
                    print("古宅的秘密逼近...")
                    if self.core_secrets:
                        secret = self.core_secrets[0]
                        print(f"你瞥见了古宅的秘密: {secret['suit']}{secret['value']}")
        
        elif self.fear_level <= 4:  # 高度威胁
            if d4 == 1:
                player_idx = random.randint(0, self.num_players-1)
                if self.players[player_idx]['alive']:
                    print(f"{self.players[player_idx]['name']} 受到物质攻击，失去2点生命")  # 伤害增加
                    self.players[player_idx]['health'] = max(0, self.players[player_idx]['health'] - 2)
            elif d4 == 2:
                print("精神攻击！所有玩家进行检定")
                for i, player in enumerate(self.players):
                    if player['alive'] and not self.check_success(player_idx=i):
                        print(f"{player['name']} 未能抵抗精神攻击，失去2点理智")  # 伤害增加
                        player['sanity'] = max(0, player['sanity'] - 2)
            elif d4 == 3:
                print("空间扭曲...房间位置发生变化")
                if self.explored_rooms:
                    random.shuffle(self.explored_rooms)
                    print("房间布局已改变")
            elif d4 == 4:
                print("高潮事件发生！")
                self.trigger_d30_event()
        
        else:  # 恐惧等级5-6 - 极度威胁
            print("【极度恐惧】古宅的恶意达到了顶峰！")
            if d4 == 1:
                # 物质攻击或D30事件
                if random.random() < 0.7:  # 70%概率触发D30事件
                    self.trigger_d30_event()
                else:
                    for player in self.players:
                        if player['alive']:
                            player['health'] = max(0, player['health'] - 3)  # 伤害增加
                    print("所有玩家受到3点生命伤害")
            elif d4 == 2:
                # 精神攻击或D30事件
                if random.random() < 0.7:  # 70%概率触发D30事件
                    self.trigger_d30_event()
                else:
                    print("强烈精神攻击！所有玩家进行检定")
                    for i, player in enumerate(self.players):
                        if player['alive']:
                            if not self.check_success(player_idx=i):
                                player['sanity'] = max(0, player['sanity'] - 3)  # 伤害增加
                                print(f"{player['name']} 未能抵抗精神攻击，失去3点理智")
                            else:
                                player['sanity'] = max(0, player['sanity'] - 2)  # 伤害增加
                                print(f"{player['name']} 部分抵抗了精神攻击，失去2点理智")
            elif d4 == 3:
                # 空间重构或D30事件
                if random.random() < 0.7:  # 70%概率触发D30事件
                    self.trigger_d30_event()
                else:
                    print("空间完全重构！")
                    keep = min(3, len(self.explored_rooms))
                    if self.explored_rooms:
                        self.explored_rooms = random.sample(self.explored_rooms, keep)
                        self.mansion_deck.extend([card for card in self.explored_rooms if card not in self.explored_rooms])
                        random.shuffle(self.mansion_deck)
                        print(f"只保留了{keep}个房间，其余房间被重新洗入牌堆")
            elif d4 == 4:
                # 双重D30事件
                print("双重高潮事件发生！")
                for i in range(2):
                    self.trigger_d30_event()
        
        self.check_player_status()
    
    def mansion_turn(self):
        """古宅回合"""
        if self.skip_mansion_turn:
            print("古宅因献祭而平静，跳过古宅回合")
            self.skip_mansion_turn = False
            return
            
        print("\n===== 古宅回合 =====")
        
        # 恐惧等级提升
        if self.fear_level < self.max_fear_level:
            self.fear_level += 1
            print(f"恐惧等级提升至: {self.fear_level}")
            
            # 恐惧等级特殊效果
            if self.fear_level == 3:
                print("【恐惧加深】古宅的低语变得更加清晰...")
            elif self.fear_level == 5:
                print("【极端恐惧】古宅的恶意几乎实体化，所有检定难度增加！")
            elif self.fear_level == 6:
                print("【绝望降临】古宅完全苏醒，你们的时间不多了！")
        
        # 重置连续D30计数
        self.consecutive_d30 = 0
        
        # 执行古宅行动
        self.mansion_action()
        
        # 检查恐惧等级特殊状态
        if self.silence_mode:
            self.silence_duration -= 1
            if self.silence_duration <= 0:
                self.silence_mode = False
                print("声音恢复了...")
        
        if self.trust_crisis:
            self.trust_crisis_duration -= 1
            if self.trust_crisis_duration <= 0:
                self.trust_crisis = False
                print("信任危机解除了...")
                
        if self.eye_of_mansion:
            self.eye_duration -= 1
            if self.eye_duration <= 0:
                self.eye_of_mansion = False
                print("全视之眼消失了...")
                
        if self.temp_fear_increase:
            self.fear_level = self.original_fear
            self.temp_fear_increase = False
            print("恐惧等级恢复正常")
            
        # 重置下一回合检定难度增加标记
        if self.next_turn_difficulty_penalty:
            self.next_turn_difficulty_penalty = False
        
        # 高恐惧等级下每回合自动触发D30事件的概率
        if self.fear_level >= 5 and random.random() < 0.4:
            print("古宅的恶意自发凝聚！")
            self.trigger_d30_event()
    
    def reveal_secret(self):
        """揭示秘密"""
        if not self.core_secrets:
            print("没有秘密可以揭示")
            return
        
        # 弃掉所有手牌
        print("弃掉所有手牌，尝试揭示秘密...")
        hand_count = len(self.hand_cards)
        self.hand_cards = []
        
        # 翻开核心秘密
        secret_card = self.core_secrets.pop(0)
        secret_info = self.k_secrets.get(secret_card['suit'], {
            "name": "未知的秘密",
            "description": "这是一个未知的秘密",
            "modifier": 0
        })
        
        print(f"古宅的核心秘密: {secret_card['suit']}{secret_card['value']} - {secret_info['name']}")
        print(secret_info['description'])
        
        # 最终对抗
        print("进行最终对抗...")
        difficulty = 10 + self.fear_level * 3
        d30_roll = self.d30_roll()
        print(f"投掷D30: {d30_roll}, 难度: {difficulty}")
        
        # 应用秘密修饰
        modifier = secret_info.get('modifier', 0)
        if modifier == "hand_bonus":
            # 特殊处理：每弃掉一张手牌，D30结果+2
            bonus = hand_count * 2
            d30_roll += bonus
            print(f"弃掉了{hand_count}张手牌，获得+{bonus}加值")
        else:
            d30_roll += modifier
            print(f"秘密修饰: {modifier}")
        
        if d30_roll > difficulty:
            print("你们成功了！理解了秘密并找到了出路")
            self.victory = True
            self.game_over = True
        else:
            print("古宅的最后疯狂吞噬了你们...")
            for player in self.players:
                player['sanity'] = 0
            self.game_over = True
    
    def check_player_status(self):
        """检查玩家状态"""
        for player in self.players:
            if player['sanity'] <= 0 or player['health'] <= 0:
                player['alive'] = False
                print(f"{player['name']} 已失去意识或发疯")
        
        # 检查是否所有玩家都失败
        alive_players = sum(1 for player in self.players if player['alive'])
        if alive_players == 0:
            print("所有玩家都失败了...游戏结束")
            self.game_over = True
    
    # ================= D30 事件效果实现 =================
    def event_default(self):
        """默认事件效果"""
        print("发生了难以名状的恐怖事件")
        alive_players = [p for p in self.players if p['alive']]
        if alive_players:
            player = random.choice(alive_players)
            damage = 3 if self.fear_level >= 5 else 2  # 伤害增加
            player['sanity'] = max(0, player['sanity'] - damage)
            print(f"{player['name']} 失去了{damage}点理智")

    def event_1(self):
        """群魔乱舞 - 所有肖像画的眼睛开始流血并注视着玩家"""
        print("所有墙上的肖像画的眼睛都开始流血并注视着玩家！诡异的低语在画框中回荡。")
        for player in self.players:
            if player['alive']:
                # 所有玩家都需要进行检定
                if not self.check_success(player_idx=self.players.index(player)):
                    damage = 3 if self.fear_level >= 5 else 2  # 伤害增加
                    player['sanity'] = max(0, player['sanity'] - damage)
                    print(f"{player['name']} 未能抵抗恐惧，失去{damage}点理智")
                else:
                    print(f"{player['name']} 成功避开了那些注视")

    def event_2(self):
        """血肉之墙 - 墙壁变得柔软、温热并开始搏动"""
        print("你们所在的房间墙壁突然变得柔软、温热，并开始有节奏地搏动，如同活物！")
        # 所有玩家都需要进行敏捷检定来躲避
        for player in self.players:
            if player['alive']:
                self.last_action = "躲避墙壁"
                if not self.check_success(player_idx=self.players.index(player)):
                    damage = 3 if self.fear_level >= 5 else 2  # 伤害增加
                    player['health'] = max(0, player['health'] - damage)
                    print(f"{player['name']} 被墙壁'舔舐'，受到{damage}点伤害")
                else:
                    print(f"{player['name']} 成功躲开了蠕动的墙壁")

    def event_3(self):
        """时光倒流 - 场景切换回刚进入古宅时的样子"""
        print("场景瞬间切换回你们刚进入古宅时的样子！一切都回到了最初的时刻。")
        # 保留已探索房间但失去所有手牌
        lost = len(self.hand_cards)
        self.hand_cards = []
        print(f"你们失去了所有{lost}张手牌")
        
        # 高恐惧等级下还会失去一些已探索房间
        if self.fear_level >= 5 and self.explored_rooms:
            lost_rooms = min(3, len(self.explored_rooms) // 2)
            for _ in range(lost_rooms):
                if self.explored_rooms:
                    room = self.explored_rooms.pop()
                    self.mansion_deck.append(room)
            random.shuffle(self.mansion_deck)
            print(f"{lost_rooms}个已探索房间被重新洗入牌堆")

    def event_4(self):
        """窃窃私语 - 一个清晰而恶毒的声音在每个人耳边低语"""
        print("一个清晰而恶毒的声音在每个人耳边低语一个他们最深处的秘密或恐惧！")
        for player in self.players:
            if player['alive']:
                damage = 3 if self.fear_level >= 5 else 2  # 伤害增加
                player['sanity'] = max(0, player['sanity'] - damage)
        damage = 3 if self.fear_level >= 5 else 2  # 伤害增加
        print(f"所有存活玩家失去{damage}点理智")

    def event_5(self):
        """镜像自我 - 每个玩家都在倒影中看到另一个充满恶意的自己"""
        print("每个玩家都在房间的玻璃或水渍倒影中看到另一个充满恶意的自己！那倒影似乎在嘲笑你们。")
        # 暂时增加恐惧等级
        self.original_fear = self.fear_level
        self.fear_level = min(self.max_fear_level, self.fear_level + 1)
        self.temp_fear_increase = True
        print(f"恐惧等级暂时提升至: {self.fear_level}")

    def event_6(self):
        """无尽回廊 - 通道被封锁，出口消失"""
        print("探索区所有通道被收回并洗回古宅牌堆，出口被暂时封锁了！")
        # 收回所有方块和梅花牌
        corridor_cards = [card for card in self.explored_rooms if card['suit'] in ['♦', '♣']]
        for card in corridor_cards:
            self.explored_rooms.remove(card)
            self.mansion_deck.append(card)
        random.shuffle(self.mansion_deck)
        print(f"{len(corridor_cards)}张通道牌被收回")
        
        # 高恐惧等级下还会失去一些手牌
        if self.fear_level >= 5 and self.hand_cards:
            lost = min(2, len(self.hand_cards))
            for _ in range(lost):
                if self.hand_cards:
                    self.hand_cards.pop()
            print(f"{lost}张手牌丢失了")

    def event_7(self):
        """孩童歌谣 - 远处传来空灵、走调的孩童歌唱声"""
        print("远处传来空灵、走调的孩童歌唱声，歌词模糊地叙述着古宅的悲剧！")
        self.fear_level = min(self.max_fear_level, self.fear_level + 1)
        print(f"恐惧等级提升至: {self.fear_level}")
        
        # 高恐惧等级下还会造成理智伤害
        if self.fear_level >= 5:
            for player in self.players:
                if player['alive']:
                    player['sanity'] = max(0, player['sanity'] - 2)  # 伤害增加
            print("所有存活玩家额外失去2点理智")

    def event_8(self):
        """提线木偶 - 一名玩家的手臂不由自主地抬起"""
        print("一名随机玩家的手臂不由自主地抬起，指向一个方向！")
        alive_players = [p for p in self.players if p['alive']]
        if alive_players:
            player = random.choice(alive_players)
            player['restricted'] = True
            
            # 高恐惧等级下会影响多名玩家
            if self.fear_level >= 5 and len(alive_players) > 1:
                additional_players = random.sample([p for p in alive_players if p != player], 
                                                  min(2, len(alive_players)-1))
                for p in additional_players:
                    p['restricted'] = True
                names = ", ".join([p['name'] for p in [player] + additional_players])
                print(f"{names} 的行动受到限制")
            else:
                print(f"{player['name']} 的行动受到限制")

    def event_9(self):
        """腐化盛宴 - 房间出现一桌腐烂生蛆但却散发着香气的盛宴"""
        print("房间的桌上突然出现一桌腐烂生蛆、但却散发着令人无法抗拒香气的盛宴！")
        choice = input("是否选择食用？(y/n): ")
        if choice.lower() == 'y':
            alive_players = [p for p in self.players if p['alive']]
            if alive_players:
                player = random.choice(alive_players)
                heal = 3 if self.fear_level >= 5 else 2  # 恢复量增加
                player['health'] = min(player['max_health'], player['health'] + heal)
                print(f"{player['name']} 恢复{heal}点生命，但永久失去1点最大理智值")
                # 减少最大理智值
                player['max_sanity'] = max(1, player['max_sanity'] - 1)
                player['sanity'] = min(player['sanity'], player['max_sanity'])

    def event_10(self):
        """死者苏生 - 已故之人重新出现并变得更强大"""
        print("一个死去的人重新出现，并变得更加强大！")
        if self.defeated_monsters:
            monster = self.defeated_monsters.pop()
            print(f"{monster['suit']}{monster['value']} 重新出现！")
            # 触发怪物遭遇，但难度增加
            difficulty_bonus = 2 if self.fear_level >= 5 else 1
            print(f"这个死者变得更强大，检定难度+{difficulty_bonus}")
            for player in self.players:
                if player['alive']:
                    self.last_action = "对抗死者"
                    if not self.check_success(difficulty=self.fear_level+difficulty_bonus, 
                                           player_idx=self.players.index(player)):
                        damage = 3 if self.fear_level >= 5 else 2  # 伤害增加
                        player['sanity'] = max(0, player['sanity'] - damage)
                        player['health'] = max(0, player['health'] - damage)
                        print(f"{player['name']} 未能抵抗死者，失去{damage}点理智和{damage}点生命")
                    else:
                        print(f"{player['name']} 成功抵抗了死者")

    def event_11(self):
        """空间折叠 - 房间之间的空间关系发生扭曲变化"""
        print("空间本身开始扭曲折叠，房间之间的关系变得混乱不堪！")
        if self.explored_rooms:
            # 随机重新排列所有已探索房间
            random.shuffle(self.explored_rooms)
            print("所有已探索房间的位置发生了随机变化")
            
            # 高恐惧等级下可能丢失一些房间
            if self.fear_level >= 5:
                lost_rooms = random.randint(1, min(2, len(self.explored_rooms)))
                for _ in range(lost_rooms):
                    if self.explored_rooms:
                        room = self.explored_rooms.pop()
                        self.mansion_deck.append(room)
                random.shuffle(self.mansion_deck)
                print(f"{lost_rooms}个房间在空间折叠中丢失了")

    def event_12(self):
        """记忆侵蚀 - 玩家的记忆被古宅逐渐吞噬"""
        print("古宅开始吞噬你们的记忆，过去的经历变得模糊不清！")
        for player in self.players:
            if player['alive']:
                # 玩家可能失去手牌或特殊能力
                if self.hand_cards and random.random() < 0.5:
                    lost_card = self.hand_cards.pop()
                    print(f"{player['name']} 忘记了关于{lost_card['suit']}{lost_card['value']}的记忆")
                
                # 一定概率失去理智
                if random.random() < 0.7:
                    damage = 2  # 伤害增加
                    player['sanity'] = max(0, player['sanity'] - damage)
                    print(f"{player['name']} 失去{damage}点理智")

    def event_13(self):
        """虫巢爆发 - 无数虫类从各种缝隙中涌出"""
        print("无数黑色甲虫、蜈蚣和其他不知名的虫类从地板缝隙、墙壁裂缝中涌出！")
        for player in self.players:
            if player['alive']:
                self.last_action = "躲避虫群"
                if not self.check_success(player_idx=self.players.index(player)):
                    damage = 3 if self.fear_level >= 5 else 2  # 伤害增加
                    player['health'] = max(0, player['health'] - damage)
                    print(f"{player['name']} 被虫群叮咬，受到{damage}点伤害")
                else:
                    print(f"{player['name']} 成功躲开了虫群")

    def event_14(self):
        """哀悼之影 - 半透明的哀悼者身影在房间角落出现"""
        print("一个半透明的女性身影出现在房间角落，低声啜泣着，空气中弥漫着悲伤与寒冷。")
        # 所有玩家进行理智检定
        for player in self.players:
            if player['alive']:
                if not self.check_success(player_idx=self.players.index(player)):
                    damage = 3 if self.fear_level >= 5 else 2  # 伤害增加
                    player['sanity'] = max(0, player['sanity'] - damage)
                    print(f"{player['name']} 被哀悼之影的悲伤感染，失去{damage}点理智")
        
        # 下一回合所有检定难度增加
        print("哀悼之影的存在让环境变得更加压抑，下一回合所有检定难度+1")
        self.next_turn_difficulty_penalty = True

    def event_15(self):
        """献祭要求 - 古宅要求玩家献上祭品"""
        print("古宅传达出一个明确的要求：需要献祭！")
        alive_players = [p for p in self.players if p['alive']]
        if alive_players and (self.hand_cards or len(alive_players) > 1):
            print("选择献祭：1)一张手牌 2)一名玩家的1点最大理智值")
            choice = input("请输入选择(1或2): ")
            
            if choice == "1" and self.hand_cards:
                card = self.hand_cards.pop()
                print(f"你们献祭了{card['suit']}{card['value']}，古宅暂时平静了")
                # 下一回合不会触发古宅行动
                self.skip_mansion_turn = True
            elif choice == "2" and len(alive_players) > 1:
                player = random.choice(alive_players)
                player['max_sanity'] = max(1, player['max_sanity'] - 1)
                player['sanity'] = min(player['sanity'], player['max_sanity'])
                print(f"{player['name']} 永久失去了1点最大理智值作为祭品，古宅暂时平静了")
                # 下一回合不会触发古宅行动
                self.skip_mansion_turn = True
            else:
                print("你们拒绝献祭，古宅的愤怒加剧了！")
                self.fear_level = min(self.max_fear_level, self.fear_level + 1)
                print(f"恐惧等级提升至: {self.fear_level}")

    def event_16(self):
        """时间跳跃 - 时间突然跳跃，蜡烛烧掉一大截"""
        print("时间突然跳跃，当你们回过神时，发现蜡烛已经烧掉了一大截！")
        # 跳过下一个玩家回合
        print("你们失去了一段时间，下一个玩家回合将被跳过")
        self.skip_player_turn = True
        
        # 高恐惧等级下可能失去更多
        if self.fear_level >= 5:
            # 随机失去一张手牌
            if self.hand_cards:
                lost_card = self.hand_cards.pop()
                print(f"在时间跳跃中，你们失去了{lost_card['suit']}{lost_card['value']}的记忆")

    def event_17(self):
        """寄生触手 - 油腻的触须状物从影子中伸出"""
        print("油腻的触须状物从玩家的影子中伸出，试图缠绕束缚！")
        alive_players = [p for p in self.players if p['alive']]
        if alive_players:
            player = random.choice(alive_players)
            print(f"{player['name']} 被寄生触手盯上了！")
            self.last_action = "挣脱触手"
            if not self.check_success(player_idx=self.players.index(player)):
                player['restricted'] = True
                player['health'] = max(0, player['health'] - 2)  # 伤害增加
                print(f"{player['name']} 被触手束缚并伤害，下回合只能探索")
            else:
                print(f"{player['name']} 成功挣脱了触手")

    def event_18(self):
        """全视之眼 - 天花板上睁开一只巨大的眼睛"""
        print("天花板上睁开一只巨大的、布满血丝的眼睛，冷漠地注视着一切！")
        # 所有玩家进行理智检定
        for player in self.players:
            if player['alive']:
                if not self.check_success(player_idx=self.players.index(player)):
                    damage = 3 if self.fear_level >= 5 else 2  # 伤害增加
                    player['sanity'] = max(0, player['sanity'] - damage)
                    print(f"{player['name']} 与全视之眼对视，失去{damage}点理智")
        
        # 全视之眼会让古宅知晓玩家行动
        print("在全视之眼的注视下，古宅知晓你们的一切行动")
        self.eye_of_mansion = True
        self.eye_duration = 2  # 持续2回合

    def event_19(self):
        """声音剥夺 - 所有的声音瞬间消失"""
        print("所有的声音瞬间消失，包括你们自己的心跳声和呼吸声！")
        self.silence_mode = True
        self.silence_duration = 3  # 持续3回合
        print("在接下来的三个回合中，所有玩家无法进行语言交流")

    def event_20(self):
        """过去重现 - 古宅中曾发生的悲剧事件重现在眼前"""
        print("你们瞬间目睹了古宅中曾发生的一起关键悲剧事件的幻象！")
        # 随机选择一个悲剧场景描述
        tragedies = [
            "一个家庭成员在餐厅被毒杀的瞬间",
            "一个孩子被锁在阁楼中慢慢饿死的最后时刻",
            "女主人发疯后纵火焚烧东翼的场景",
            "男主人在地下室进行黑暗仪式的过程"
        ]
        tragedy = random.choice(tragedies)
        print(f"你们看到了: {tragedy}")
        
        # 所有玩家进行理智检定
        for player in self.players:
            if player['alive']:
                if not self.check_success(player_idx=self.players.index(player)):
                    damage = 3 if self.fear_level >= 5 else 2  # 伤害增加
                    player['sanity'] = max(0, player['sanity'] - damage)
                    print(f"{player['name']} 被幻象震撼，失去{damage}点理智")
                else:
                    print(f"{player['name']} 从幻象中了解到了一些古宅的秘密")
                    # 成功抵抗的玩家可以获得一张手牌
                    if self.mansion_deck:
                        card = self.mansion_deck.pop()
                        self.hand_cards.append(card)
                        print(f"{player['name']} 获得了{card['suit']}{card['value']}作为洞察奖励")

    def event_21(self):
        """扭曲生长 - 古宅的木质结构开始疯狂生长"""
        print("古宅的木质结构开始疯狂生长，封堵门廊，创造新的通道！")
        # 随机封堵或开启通道
        if self.explored_rooms:
            # 随机选择一些房间被移除
            rooms_to_remove = random.randint(1, min(3, len(self.explored_rooms)))
            for _ in range(rooms_to_remove):
                if self.explored_rooms:
                    room = self.explored_rooms.pop()
                    self.mansion_deck.append(room)
            print(f"{rooms_to_remove}个房间被生长的木材封堵了")
            
            # 添加一些新房间
            rooms_to_add = random.randint(1, 2)
            for _ in range(rooms_to_add):
                if self.mansion_deck:
                    room = self.mansion_deck.pop()
                    self.explored_rooms.append(room)
                    print("出现了新的房间: {room['suit']}{room['value']}")
            
            random.shuffle(self.mansion_deck)

    def event_22(self):
        """信任危机 - 古宅的低语在你们之间播种猜疑"""
        print("古宅的低语在你们之间播种猜疑，你们开始怀疑彼此的动机！")
        self.trust_crisis = True
        self.trust_crisis_duration = 2
        print("在接下来的两个回合中，玩家之间不能共享信息")
        
        # 高恐惧等级下可能直接造成伤害
        if self.fear_level >= 5:
            for player in self.players:
                if player['alive'] and random.random() < 0.5:
                    player['sanity'] = max(0, player['sanity'] - 2)  # 伤害增加
                    print(f"{player['name']} 因猜疑而失去2点理智")

    def event_23(self):
        """重力失效 - 房间内的重力方向突然改变"""
        print("房间内的重力方向突然改变，持续几秒！所有未固定的物体都飘浮起来。")
        for player in self.players:
            if player['alive']:
                self.last_action = "适应重力变化"
                if not self.check_success(player_idx=self.players.index(player)):
                    damage = 3 if self.fear_level >= 5 else 2  # 伤害增加
                    player['health'] = max(0, player['health'] - damage)
                    player['stunned'] = True
                    print(f"{player['name']} 受到{damage}点伤害并被撞晕，下回合行动顺序置后")
                else:
                    print(f"{player['name']} 成功适应了重力变化")

    def event_24(self):
        """模仿者 - 门外传来模仿亲友的呼救声"""
        print("门外传来一位玩家亲友的呼救声，惟妙惟肖，令人难以分辨真伪！")
        alive_players = [p for p in self.players if p['alive']]
        if alive_players:
            target_player = random.choice(alive_players)
            print(f"声音模仿的是{target_player['name']}的亲友！")
            
            # 目标玩家必须进行检定
            self.last_action = "分辨真伪"
            if not self.check_success(player_idx=self.players.index(target_player)):
                print(f"{target_player['name']} 相信了呼救声，打开了门...")
                # 触发一个黑桃遭遇，且难度增加
                print("门外什么亲友都没有，只有一个可怕的存在！")
                for player in self.players:
                    if player['alive']:
                        damage = 3 if self.fear_level >= 5 else 2  # 伤害增加
                        player['sanity'] = max(0, player['sanity'] - damage)
                        player['health'] = max(0, player['health'] - damage)
                        print(f"{player['name']} 受到惊吓，失去{damage}点理智和{damage}点生命")
            else:
                print(f"{target_player['name']} 识破了模仿者的诡计，没有上当")

    def event_25(self):
        """绝望具象 - 玩家的恐惧凝聚成黑色人形"""
        print("玩家们的恐惧凝聚成一个短暂的黑色人形，在房间内一闪而过！")
        # 当前理智最低的玩家受影响最大
        alive_players = [p for p in self.players if p['alive']]
        if alive_players:
            # 找到理智最低的玩家
            min_sanity_player = min(alive_players, key=lambda x: x['sanity'])
            damage = 4 if self.fear_level >= 5 else 3  # 伤害增加
            min_sanity_player['sanity'] = max(0, min_sanity_player['sanity'] - damage)
            print(f"{min_sanity_player['name']} 的恐惧被具象化，失去{damage}点理智")
            
            # 其他玩家也受到影响
            for player in alive_players:
                if player != min_sanity_player:
                    player['sanity'] = max(0, player['sanity'] - 2)  # 伤害增加
                    print(f"{player['name']} 受到恐惧辐射，失去2点理智")

    def event_26(self):
        """生命汲取 - 古宅从玩家身上吸取生命力"""
        print("古宅似乎从你们身上吸取了生命力，你们感到异常虚弱！")
        for player in self.players:
            if player['alive']:
                # 同时减少理智和生命
                damage = 2  # 伤害增加
                player['sanity'] = max(0, player['sanity'] - damage)
                player['health'] = max(0, player['health'] - damage)
                print(f"{player['name']} 被吸取生命力，失去{damage}点理智和{damage}点生命")

    def event_27(self):
        """强制交换 - 玩家之间的理智或生命值被强制交换"""
        print("古宅的力量强制交换了玩家之间的某些属性！")
        alive_players = [p for p in self.players if p['alive']]
        if len(alive_players) >= 2:
            # 随机选择两名玩家
            players_to_swap = random.sample(alive_players, 2)
            p1, p2 = players_to_swap
            
            # 随机选择交换理智或生命
            if random.random() < 0.5:
                # 交换理智
                p1_sanity, p2_sanity = p1['sanity'], p2['sanity']
                p1['sanity'], p2['sanity'] = p2_sanity, p1_sanity
                print(f"{p1['name']} 和 {p2['name']} 的理智值被交换了")
            else:
                # 交换生命
                p1_health, p2_health = p1['health'], p2['health']
                p1['health'], p2['health'] = p2_health, p1_health
                print(f"{p1['name']} 和 {p2['name']} 的生命值被交换了")

    def event_28(self):
        """门户洞开 - 地板上出现通往绝对黑暗的洞口"""
        print("地板上出现一个通往绝对黑暗的洞口，从中散发出刺骨的寒意和呜咽声！")
        alive_players = [p for p in self.players if p['alive']]
        if alive_players:
            # 随机选择一名玩家靠近洞口
            player = random.choice(alive_players)
            print(f"{player['name']} 感觉被洞口吸引，慢慢靠近...")
            self.last_action = "抵抗洞口吸引"
            if not self.check_success(player_idx=self.players.index(player)):
                damage = 3 if self.fear_level >= 5 else 2  # 伤害增加
                player['health'] = max(0, player['health'] - damage)
                # 玩家下回合被移出游戏（代表被吸入洞口短暂困住）
                player['stunned'] = True
                print(f"{player['name']} 被吸入洞口，受到{damage}点伤害并被困住一回合")
            else:
                print(f"{player['name']} 抵抗了洞口的吸引，但洞口中传出的低语仍在回响")
                player['sanity'] = max(0, player['sanity'] - 2)  # 伤害增加
                print(f"{player['name']} 失去2点理智")

    def event_29(self):
        """古宅之心 - 玩家短暂感受到古宅那古老冰冷的意识"""
        print("你们短暂地感受到了古宅那古老、冰冷、毫无人性的意识！")
        # 玩家可以问一个问题，但需要付出代价
        alive_players = [p for p in self.players if p['alive']]
        if alive_players:
            player = random.choice(alive_players)
            print(f"{player['name']} 与古宅之心建立了连接，可以问一个关于古宅的是非问题")
            question = input("请输入你的问题（古宅只会回答是或否）: ")
            
            # 根据问题给出答案（这里简化处理，实际可以根据游戏状态回答）
            answers = ["是", "否"]
            answer = random.choice(answers)
            print(f"古宅之心的回答: {answer}")
            
            # 玩家需要永久失去1点最大理智值
            player['max_sanity'] = max(1, player['max_sanity'] - 1)
            player['sanity'] = min(player['sanity'], player['max_sanity'])
            print(f"{player['name']} 因接触古宅之心而永久失去了1点最大理智值")

    def event_30(self):
        """古宅获胜 - 古宅展示了它真正的力量"""
        print("古宅展示了它真正的力量！一首胜利的、扭曲的华尔兹音乐在宅中响起。")
        for player in self.players:
            if player['alive']:
                player['sanity'] = max(0, player['sanity'] - 3)  # 伤害增加
                player['health'] = max(0, player['health'] - 3)  # 伤害增加
        print("所有存活玩家失去3点理智和3点生命")
        
        # 高恐惧等级下效果更强
        if self.fear_level >= 5:
            print("古宅的力量进一步增强了！")
            for player in self.players:
                if player['alive']:
                    player['max_sanity'] = max(1, player['max_sanity'] - 1)
                    player['sanity'] = min(player['sanity'], player['max_sanity'])
            print("所有存活玩家永久失去1点最大理智值")
    
    def play_game(self):
        """主游戏循环"""
        self.setup_game()
        turn = 0
        
        while not self.game_over:
            print(f"\n{'='*20} 第 {turn+1} 回合 {'='*20}")
            
            # 玩家回合
            for i in range(self.num_players):
                if not self.game_over:
                    self.player_turn(i)
            
            # 古宅回合
            if not self.game_over:
                self.mansion_turn()
            
            turn += 1
            
            # 高恐惧等级的特殊规则
            if self.fear_level >= 5 and not self.game_over:
                print("\n【恐惧侵蚀】古宅的恶意持续侵蚀着你们...")
                for player in self.players:
                    if player['alive']:
                        player['sanity'] = max(0, player['sanity'] - 2)  # 伤害增加
                        print(f"{player['name']} 失去2点理智")
                self.check_player_status()
        
        # 游戏结束
        if self.victory:
            print("\n恭喜！你们成功逃离了古宅！")
            print(f"总共经历了 {self.d30_event_count} 次D30事件")
        else:
            print("\n古宅获得了胜利...你们将永远成为它的一部分")
            print(f"总共经历了 {self.d30_event_count} 次D30事件")
    


# 启动游戏
if __name__ == "__main__":
    try:
        num_players = int(input("请输入玩家人数 (1-4): "))
        if num_players < 1 or num_players > 4:
            print("玩家人数必须在1-4之间，使用默认值2")
            num_players = 2
            
        game = HorrorMansionGame(num_players)
        game.play_game()
    except ValueError:
        print("输入无效，使用默认玩家人数2")
        game = HorrorMansionGame(2)
        game.play_game()
    except Exception as e:
        print(f"游戏发生错误: {e}")
        print("重新启动游戏...")
        game = HorrorMansionGame(2)
        game.play_game()

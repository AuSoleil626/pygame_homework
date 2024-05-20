import pygame
from plane_sprites import *
CREATE_ITEM_EVENT=pygame.USEREVENT+2

class Prop_factory:  # 道具工厂类
    def __init__(self,player,screen):
        self.player = player  # 玩家
        self.prop_list = pygame.sprite.Group()  # 道具列表
        self.prop_num = 0  # 道具数量
        self.max_prop_num = 4  # 最大道具数量
        self.screen = screen  # 屏幕
        self.create_prop_timer = 0  # 道具创建定时器
        self.create_prop_interval = 200  # 道具创建间隔时间

    def create_prop(self):  # 产生道具
        prop_type = random.randint(0, 1)  # 随机产生道具类型
        if len(self.prop_list) >= self.max_prop_num:  # 道具数量达到最大值
            return
        if prop_type == 0:  # 产生生命道具
            prop = Prop_life(self.player)
        elif prop_type == 1:  # 产生炸鱼道具
            prop = Prop_improveFire(self.player)
        self.prop_list.add(prop)  # 将道具加入道具列表
        self.prop_num += 1  # 道具数量加1
    def update(self):
        # self.create_prop_timer += 1  # 道具创建定时器加1
        # if self.create_prop_timer >= self.create_prop_interval:  # 道具创建定时器到达间隔时间
        #     self.create_prop()  # 产生道具
        #     self.create_prop_timer = 0  # 重置定时器
        for prop in self.prop_list:
            prop.update()  # 更新道具位置
        self.prop_list.draw(self.screen)  # 绘制道具


class Prop_base(pygame.sprite.Sprite): # base class for all props # 固定道具大小为 60*60
    def __init__(self,image_path,player):
        super().__init__()
        self.player = player  # 玩家
        self.image = pygame.image.load(image_path)  # 定义prop的图像
        self.image = pygame.transform.scale(self.image, (60, 60))  # 缩放图像
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(0, SCREEN_RECT.width-60), random.randint(0, SCREEN_RECT.height-60))  # 随机初始化位置
        self.speed = [random.randint(1, 3), random.randint(1, 3)]  # 初始化移动速度
        self.image_group=[]
        self.image_index=0

    def update(self):
        self.rect.move_ip(self.speed)
        # 检测是否碰到边缘
        if self.rect.left < 0 or self.rect.right > SCREEN_RECT.width:
            self.speed[0] *= -1  # 当碰到左右边缘时反弹
        if self.rect.top < 0 or self.rect.bottom > SCREEN_RECT.height:
            self.speed[1] *= -1  # 当碰到上下边缘时反弹
        if self.rect.colliderect(self.player.rect):  # 当道具与玩家碰撞时
            self.collide_with_player()  # 调用子类的方法处理碰撞
    def collide_with_player(self):
        return

class Prop_life(Prop_base):  # 生命道具
    def __init__(self,player):
        super().__init__('./Pictures/奖励1/奖励1.png',player)
        self.life_num = 1  # 生命道具数量为1
        self.image_group.append(pygame.transform.scale(pygame.image.load('./Pictures/奖励1/奖励1.png'), (60, 60)))
        self.image_group.append(pygame.transform.scale(pygame.image.load('./Pictures/奖励1/奖励2.png'), (60, 60)))

    def collide_with_player(self):
        if self.player.health < self.player.max_health:  # 玩家生命值未满时
            sound_effect = pygame.mixer.Sound("./音效音乐/吃东西.mp3")
            sound_effect.play()
            self.player.change_health(self.life_num)  # 玩家增加生命值
            self.kill()  # 销毁生命道具
    def update(self):
        super().update()
        if self.image_index<=10:
            self.image=self.image_group[0]
        elif self.image_index<=20:
            self.image=self.image_group[1]
        else:
            self.image_index=0
        self.image_index+=1

class Prop_improveFire(Prop_base):
    def __init__(self,player):
        super().__init__('./Pictures/奖励2/奖励2.png',player)
        self.image_group.append(pygame.transform.scale(pygame.image.load('./Pictures/奖励2/奖励2.png'), (60, 60)))
        self.image_group.append(pygame.transform.scale(pygame.image.load('./Pictures/奖励2/奖励3.png'), (60, 60)))

    def collide_with_player(self):
        sound_effect = pygame.mixer.Sound("./音效音乐/吃东西.mp3")
        sound_effect.play()
        self.player.AddHeroComponent("ImproveFireComponent")
        self.kill()
    def update(self):
        super().update()
        if self.image_index<=10:
            self.image=self.image_group[0]
        elif self.image_index<=20:
            self.image=self.image_group[1]
        else:
            self.image_index=0
        self.image_index+=1
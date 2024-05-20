import random


import pygame
import math
from Plane_game_HeroComponent import *

# 游戏屏幕的尺寸
SCREEN_RECT = pygame.Rect(0, 0, 960, 478)
# 游戏的刷新帧率
FRAME_PER_SEC = 60
# 敌机的定时器常量
CREATE_ENEMY_EVENT = pygame.USEREVENT
# 英雄发射子弹事件
Hero_FIRE_EVENT = pygame.USEREVENT + 1




class GameSprite(pygame.sprite.Sprite):
    """游戏精灵基类"""
    def __init__(self, image_name, speed=1, Is_need_scale=False,mangitude=SCREEN_RECT.size,Is_need_rotate=True): # 这里的Is_need_scale参数用于判断是否需要缩放图片
        # 调用父类的初始方法
        super().__init__()
        self.image = pygame.image.load(image_name)
        #往右旋转270度
        if Is_need_rotate:
            self.image = pygame.transform.rotate(self.image, 270)
        if Is_need_scale:
            self.image = pygame.transform.scale(self.image, mangitude)
        # 记录精灵的矩形
        self.rect = self.image.get_rect()
        # 记录速度
        self.speed = speed
        # 精灵图片组
        self.image_group=[]
    def set_speed(self, speed):
        self.speed = speed
    def get_speed(self):
        return self.speed
    def update(self, *args):
        # 默认在水平方向移动
        self.rect.x -= self.speed


class Background(GameSprite):
    """游戏背景精灵"""

    def __init__(self, is_alt=False):
        # 1.调用父类方法实现精灵的创建(image/rect/speed)
        image_name = "./Pictures/BG/BG.png"
        super().__init__(image_name,1,True,SCREEN_RECT.size,False)
        # 2.判断是否交替图片，如果是，则设置初始位置
        if is_alt:
            self.rect.x = self.rect.width

    def update(self, *args):

        # 1.调用父类方法实现
        super().update()
        # 2.判断是否移出屏幕，如移出，将图像设置到屏幕右边缘
        if self.rect.x < -self.rect.width:
            self.rect.x = SCREEN_RECT.right

#从这开始的代码都是敌机相关
class EnemyFactory():
    def __init__(self,BulletFactory):
        self.enemies = pygame.sprite.Group()
        self.bosses = pygame.sprite.Group()
        self.BulletFactory=BulletFactory     #子弹工厂
    def createEnemy(self,a,EnemyType):
        if EnemyType=="Enemy_base":
            enemy = Enemy(a,self.BulletFactory)
            self.enemies.add(enemy)
        elif EnemyType=="EnemyBoss":
            enemy = EnemyBoss(a,self.BulletFactory)
            self.bosses.add(enemy)
        return


class Enemy(GameSprite):  #敌人基类
    """敌机精灵"""
    def __init__(self,a,BulletFactory,magnitude=(162,164)):
        # 1.调用父类方法创建敌机精灵，并指定敌机图像
        super().__init__("./Pictures/敌人01/敌人攻击01/敌人攻击01.png",1,True,magnitude,False)
        # 2.设置敌机的随机速度(初始) 1~3
        self.BulletFactory=BulletFactory
        self.speed = random.randint(1, 3)
        # 3.设置敌机的随机位置,从屏幕右边出现敌人
        self.rect.x = SCREEN_RECT.right
        self.rect.y = random.randint(0, SCREEN_RECT.height - self.rect.height)
        #设置独特ID
        self.id=a
        # 4.设置敌机定时器
        self.shoot_bullet_event_id= pygame.USEREVENT + a
        interval = random.randint(1500, 3000)
        pygame.time.set_timer(self.shoot_bullet_event_id, interval) # 定时器事件，每隔interval毫秒发送一次事件
        # 敌机血量
        self.health = 5
        self.isDie=False
        self.image_group_destroy=[]
        self.image_destroy_index=0
        self.load_image(magnitude)
        self.load_destroy_image()
    def load_destroy_image(self,magnitude=(162,164)):
        for i in range(19):
            self.image_group_destroy.append(pygame.transform.scale(pygame.image.load("./Pictures/敌人01/敌人击中01/敌人击中"+str(i+1)+".png"),magnitude))

            # self.image_group_destroy.append(
            #     pygame.transform.scale(pygame.image.load("./Pictures/敌人01/敌人击中01/敌人击中" + str(i + 1) + ".png"),
            #                            magnitude))
            # self.image_group_destroy.append(
            #     pygame.transform.scale(pygame.image.load("./Pictures/敌人01/敌人击中01/敌人击中" + str(i + 1) + ".png"),
            #                            magnitude))
            # self.image_group_destroy.append(
            #     pygame.transform.scale(pygame.image.load("./Pictures/敌人01/敌人击中01/敌人击中" + str(i + 1) + ".png"),
            #                            magnitude))
            # self.image_group_destroy.append(
            #     pygame.transform.scale(pygame.image.load("./Pictures/敌人01/敌人击中01/敌人击中" + str(i + 1) + ".png"),
            #                            magnitude))

    def load_image(self,magnitude=(162,164)):
        for i in range(4):
            self.image_group.append(pygame.transform.scale(pygame.image.load("./Pictures/敌人01/敌人攻击01/敌人攻击0"+str(i+1)+".png"),magnitude))
        self.image_index=0
    def update(self, *args):
        super().update()
        #减慢图片滚动速度
        if not self.isDie:
            if self.image_index<=10:
                self.image = self.image_group[0]
            elif self.image_index<=20:
                self.image = self.image_group[1]
            elif self.image_index<=30:
                self.image = self.image_group[2]
            elif self.image_index<=40:
                self.image = self.image_group[3]
            else:
                self.image_index=0
            self.image_index+=1
        else:
            self.speed=0
            self.update_Bossimage()


        # 2.判断是否飞左边屏幕，如是，则将敌机从所有组中删除
        if self.rect.left < 0:
            self.kill()
        # 3.将精灵从所有组中删除
            self.kill()

    def update_Bossimage(self):
        self.image = self.image_group_destroy[self.image_destroy_index]
        self.image_destroy_index+=1
        if self.image_destroy_index>=len(self.image_group_destroy):
            self.kill()
        return

    def cause_damage(self,damage):
        self.health-=damage
        if self.health<=0:
            self.health=0
            self.isDie=True
            print("敌机被击毁...")
            return True  #表示敌机被击毁
        return False   #表示敌机未被击毁

    def Fire(self):
        self.BulletFactory.createBullet(1,(self.rect.centerx,self.rect.centery))

    def __del__(self):
        print("敌机挂了　%s" % self.rect)

class EnemyBoss(Enemy):  #boss敌人
    """boss敌人精灵"""
    def __init__(self,a,BulletFactory):
        super().__init__(a,BulletFactory,(240,240))
        pygame.time.set_timer(self.shoot_bullet_event_id, 0) # 取消定时器事件，boss敌人不发射子弹
        self.speed=0.5
        self.maxhealth=50
        self.health = 50
        self.speedy=2
        self.movedistance=0
        self.timeinterval=0
        self.creat_bullet_interval=100
        # 1.设置boss敌人的随机速度(初始) 1~3
    def load_destroy_image(self):
        for i in range(19):
            self.image_group_destroy.append(pygame.transform.scale(pygame.image.load("./Pictures/BOSS/BOSS被击中/BOSS击中"+str(i+1)+".png"),(240,240)))
            self.image_group_destroy.append(
                pygame.transform.scale(pygame.image.load("./Pictures/BOSS/BOSS被击中/BOSS击中" + str(i + 1) + ".png"),
                                       (240, 240)))
            self.image_group_destroy.append(
                pygame.transform.scale(pygame.image.load("./Pictures/BOSS/BOSS被击中/BOSS击中" + str(i + 1) + ".png"),
                                       (240, 240)))
            self.image_group_destroy.append(
                pygame.transform.scale(pygame.image.load("./Pictures/BOSS/BOSS被击中/BOSS击中" + str(i + 1) + ".png"),
                                       (240, 240)))
            self.image_group_destroy.append(
                pygame.transform.scale(pygame.image.load("./Pictures/BOSS/BOSS被击中/BOSS击中" + str(i + 1) + ".png"),
                                       (240, 240)))


    def load_image(self,magnitude=(162,164)):
        for i in range(4):
            self.image_group.append(pygame.transform.scale(pygame.image.load("./Pictures/BOSS/BOSS进攻/BOSS进攻"+str(i+1)+".png"),magnitude))
        self.image_index=0
    def update(self):
        super().update()
        if not self.isDie:
            if self.movedistance<200:
                self.rect.x-=10
                self.movedistance+=10
            else:
                self.speed=0
                #开始向上移动，到达上边界后向下移动，再到达下边界后向上移动
                if self.rect.top<SCREEN_RECT.top:
                    self.speedy=2
                elif self.rect.bottom>SCREEN_RECT.bottom:
                    self.speedy=-2
                self.rect.y+=self.speedy

            # 到达时间间隔后发射子弹
            if self.timeinterval>=self.creat_bullet_interval:
                self.Fire()
                self.Fire2()
                self.timeinterval=0
            else:
                self.timeinterval+=1
    def cause_damage(self,damage):
        self.health-=damage
        if self.health<=0:
            self.health=0
            self.isDie=True
            print("boss敌人被击毁...")
            return True  #表示敌机被击毁
        return False   #表示敌机未被击毁

    def update_Bossimage(self):
        self.image = self.image_group_destroy[self.image_destroy_index]
        self.image_destroy_index+=1
        if self.image_destroy_index>=len(self.image_group_destroy):
            self.kill()

    def Fire(self):
        self.BulletFactory.createBullet(2,(self.rect.centerx,self.rect.centery))
    def Fire2(self):
        self.BulletFactory.createBullet(3,(self.rect.centerx,self.rect.centery))

class Hero(GameSprite):
    """英雄精灵"""
    def __init__(self,BulletFactory):
        super().__init__("./Pictures/主角/主角攻击/主角攻击1.png", 0,False,(70,70),False)
        # 设置初始位置
        self.rect.centerx = SCREEN_RECT.centerx
        self.rect.bottom = SCREEN_RECT.bottom - 120
        pygame.time.set_timer(Hero_FIRE_EVENT, 200)
        #设置玩家初始的y轴速度
        self.speedy = 0
        #设置玩家初始的生命值
        self.health=3
        self.max_health=3
        #设置玩家的子弹工厂
        self.BulletFactory=BulletFactory
        #设置玩家的组件数组
        self.Herocomponents=[]
        #设置玩家图片数组
        for i in range(4): #0-19
            self.image_group.append(pygame.image.load("./Pictures/主角/主角攻击/主角攻击"+str(i+1)+".png"))
            self.image_group.append(pygame.image.load("./Pictures/主角/主角攻击/主角攻击" + str(i + 1) + ".png"))
            self.image_group.append(pygame.image.load("./Pictures/主角/主角攻击/主角攻击" + str(i + 1) + ".png"))
            self.image_group.append(pygame.image.load("./Pictures/主角/主角攻击/主角攻击" + str(i + 1) + ".png"))
            self.image_group.append(pygame.image.load("./Pictures/主角/主角攻击/主角攻击" + str(i + 1) + ".png"))
        self.image_index=0

    def AddHeroComponent(self,ComponentName):
        if ComponentName=="ImproveFireComponent":
            self.Herocomponents.append(ImproveFireComponent(self))
        return
    #清空HeroComponents数组
    def removeAllHeroComponents(self):
        for component in self.Herocomponents:
            component.kill()
        self.Herocomponents=[]
    def removeHeroComponent(self,ComponentName):
        return

    def update(self, *args):
        # 轮流播放图片
        self.image_index = (self.image_index + 1) % len(self.image_group)
        self.image = self.image_group[self.image_index]

        # 英雄飞机在水平方向运动
        self.rect.x += self.speed
        # 英雄飞机在垂直方向运动
        self.rect.y += self.speedy
        # 限制英雄飞机的上下边界
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_RECT.bottom:
            self.rect.bottom = SCREEN_RECT.bottom
        # 判断屏幕边界
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_RECT.right:
            self.rect.right = SCREEN_RECT.right
        # 处理英雄的组件
        for component in self.Herocomponents:
            component.update()
        # 处理定时器事件


    def fire(self):
        print("发射子弹...")
        # 实现一次发射三枚子弹
        # 1.创建子弹精灵
        self.BulletFactory.createBullet(1,self.rect.center)

    def change_health(self,num): # 改变英雄的生命值,num为增加或减少的生命值,返回True表示仍然存活,False表示玩家死亡
        self.health+=num
        if self.health<=0:
            self.health=0
            return False
        if self.health>=3:
            self.health=3
        return True

# 子弹类都在下面
#
#
#
#
#子弹类

#子弹工厂类
class BulletFactoryBase():
    def __init__(self):
        self.bullets = pygame.sprite.Group()

    def createBullet(self,bulletIndex,location,angle=0): #目前最多可创建4中子弹，子类工厂可根据需求重写函数
        if bulletIndex==1:
            self.CreateBullet1(location)
        elif bulletIndex==2:
            self.CreateBullet2(location)
        elif bulletIndex==3:
            self.CreateBullet3(location)
        elif bulletIndex==4:
            self.CreateBullet4()

    def CreateBullet1(self,location):
        return
    def CreateBullet2(self,location):
        return
    def CreateBullet3(self):
        return
    def CreateBullet4(self):
        return


class BulletFactoryHero(BulletFactoryBase):
    def __init__(self):
        super().__init__()

    def CreateBullet1(self,location):
        bullet = HeroBullet()
        bullet.rect.centerx = location[0]
        bullet.rect.centery = location[1]
        self.bullets.add(bullet)

class BulletFactoryEnemy(BulletFactoryBase):
    def __init__(self):
        super().__init__()

    def CreateBullet1(self, location):
        bullet = EnemyBullet()
        bullet.rect.centerx = location[0]
        bullet.rect.centery = location[1]
        self.bullets.add(bullet)
    def CreateBullet2(self, location):
        bullet = BossBullet(10,155)
        #bullet.rotate()
        bullet.rect.centerx = location[0]
        bullet.rect.centery = location[1]
        self.bullets.add(bullet)

        bullet = BossBullet(10,-155)
        #bullet.rotate()
        bullet.rect.centerx = location[0]
        bullet.rect.centery = location[1]
        self.bullets.add(bullet)
    def CreateBullet3(self,location):
        bullet = BossBullet()
        bullet.rect.centerx = location[0]
        bullet.rect.centery = location[1]
        self.bullets.add(bullet)
###
##
###子弹工厂类结束
class BulletBase(pygame.sprite.Sprite):
    """子弹基类"""
    def __init__(self,speed,angle,damage=1):
        super().__init__()
        self.image = pygame.image.load("./Pictures/敌人01/子弹01/子弹01.png") # 加载子弹图片
        self.rect = self.image.get_rect()
        self.speed = speed
        self.angle = angle
        self.damage = damage
        self.rotate()
    def rotate(self):
        self.image = pygame.transform.rotate(self.image, self.angle-90)
        self.rect = self.image.get_rect()
        self.rect.centerx = self.rect.width/2
        self.rect.centery = self.rect.height/2
    def update(self, *args):
        #朝指定角度移动
        self.rect.x += self.speed * math.cos(math.radians(self.angle))
        self.rect.y -= self.speed * math.sin(math.radians(self.angle))
        #判断是否飞出屏幕的上下左右边界
        if self.rect.left < 0 or self.rect.right > SCREEN_RECT.right or self.rect.top < 0 or self.rect.bottom > SCREEN_RECT.bottom:
            self.kill()


class HeroBullet(BulletBase):   #Hero子弹精灵
    """英雄子弹精灵"""
    def __init__(self):
        super().__init__(10,0)
        self.updatebulletimage()
    def updatebulletimage(self): #玩家子弹是各种食物
        #随机一个整数

        self.pictureindex = random.randint(1, 14)
        #根据整数加载不同的子弹图片
        if self.pictureindex == 1:
            self.image = pygame.image.load("./Pictures/png2/1.png")
        elif self.pictureindex == 2:
            self.image = pygame.image.load("./Pictures/png2/2.png")
        elif self.pictureindex == 3:
            self.image = pygame.image.load("./Pictures/png2/3.png")
        elif self.pictureindex == 4:
            self.image = pygame.image.load("./Pictures/png2/4.png")
        elif self.pictureindex == 5:
            self.image = pygame.image.load("./Pictures/png2/5.png")
        elif self.pictureindex == 6:
            self.image = pygame.image.load("./Pictures/png2/6.png")
        elif self.pictureindex == 7:
            self.image = pygame.image.load("./Pictures/png2/7.png")
        elif self.pictureindex == 8:
            self.image = pygame.image.load("./Pictures/png2/8.png")
        elif self.pictureindex == 9:
            self.image = pygame.image.load("./Pictures/png2/9.png")
        elif self.pictureindex == 10:
            self.image = pygame.image.load("./Pictures/png2/10.png")
        elif self.pictureindex == 11:
            self.image = pygame.image.load("./Pictures/png2/11.png")
        elif self.pictureindex == 12:
            self.image = pygame.image.load("./Pictures/png2/12.png")
        elif self.pictureindex == 13:
            self.image = pygame.image.load("./Pictures/png2/13.png")
        elif self.pictureindex == 14:
            self.image = pygame.image.load("./Pictures/png2/14.png")

        self.image = pygame.transform.scale(self.image, (30, 30))
        self.rect = self.image.get_rect()

class EnemyBullet(BulletBase):
    """敌机子弹精灵"""
    def __init__(self,speed=10,angle=180,damage=1):
        super().__init__(speed,angle,damage)
        self.loopsprite = []
        self.loopspriteindex = 0
        self.size=(66,30)
        self.load_bullet()

    def load_bullet(self):
        self.loopsprite.append(pygame.transform.scale(pygame.image.load("./Pictures/敌人01/子弹01/子弹01.png"), self.size))
        self.loopsprite.append(pygame.transform.scale(pygame.image.load("./Pictures/敌人01/子弹01/子弹02.png"), self.size))
        self.image = self.loopsprite[0]
        self.rotate()
    def update(self):
        self.image = self.loopsprite[self.loopspriteindex]
        self.image = pygame.transform.rotate(self.image, self.angle-180)
        self.loopspriteindex = (self.loopspriteindex + 1) % len(self.loopsprite)

        self.rect.x += self.speed * math.cos(math.radians(self.angle))
        self.rect.y -= self.speed * math.sin(math.radians(self.angle))
        #判断是否飞出屏幕的上下左右边界
        if self.rect.left < 0 or self.rect.right > SCREEN_RECT.right or self.rect.top < 0 or self.rect.bottom > SCREEN_RECT.bottom:
            self.kill()

class BossBullet(EnemyBullet):
    def __init__(self,speed=10,angle=180):
        super().__init__(speed,angle,2)
    def load_bullet(self):
        self.loopsprite.append(pygame.transform.scale(pygame.image.load("./Pictures/BOSS/BOSS子弹/BOSS子弹.png"), self.size))
        self.image = self.loopsprite[0]
        self.rotate()

class EnemyBullet_explosion(EnemyBullet):
    def __init__(self):
        super().__init__()
        self.deltaDistance=0
    def explode(self):
        print("子弹爆炸...")
        self.explodeBullet = CircleBullet()
    def update(self):
        super().update()
        self.deltaDistance+=self.speed
        if self.deltaDistance>=150:
            self.explode()
            self.kill()

class CircleBullet(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.bullergroup = pygame.sprite.Group()
        self.CreateCircleBullet()
    def CreateCircleBullet(self):
        for i in range(8):
            bullet = BulletBase(10,i*45)
            self.bullergroup.add(bullet)
    def update(self):
        self.bullergroup.update()
        #self.bullergroup.draw(SCREEN)


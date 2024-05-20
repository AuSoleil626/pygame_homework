# This is the class for the Hero component of the Plane game

#玩家捡到某些道具后将英雄组件添加到角色身上，并控制角色的移动、攻击、技能等行为。
import random
class ImproveFireComponent:
    def __init__(self, hero):
        self.hero = hero
        self.create_bullet_timer = 0  # 子弹创建定时器
        self.create_bullet_interval = 50  # 子弹创建间隔时间
    def kill(self):
        return

    def update(self):
        # 子弹创建定时器
        self.create_bullet_timer += 1
        if self.create_bullet_timer >= self.create_bullet_interval:
            self.create_bullet_timer = 0
            self.hero.BulletFactory.createBullet(1,(self.hero.rect.centerx,self.hero.rect.centery+30*random.choice([1, -1])))


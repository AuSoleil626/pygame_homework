import threading

import pygame
from plane_sprites import *
from Plane_game_menu import *
from Plane_game_gameUI import *
from Plane_game_prop import *
class PlaneGame(object):
    """飞机大战主游戏"""
    def __init__(self,screen=None):
        print("游戏初始化")
        # 背景音乐
        pygame.mixer.init()
        pygame.mixer.music.load("./音效音乐/背景音乐.mp3")
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)
        #游戏窗口
        self.screen = screen
        #创建英雄子弹工厂以及敌机子弹工厂
        self.BulletFactoryHero=BulletFactoryHero()
        self.BulletFactoryEnemy=BulletFactoryEnemy()
        #创建精灵和精灵组
        self.__create_sprites()
        #游戏UI
        self.scoreboard=Scoreboard(screen)
        self.HealthUI=HealthUI(screen,self.hero)
        #创建敌机工厂
        self.enemy_factory=EnemyFactory(self.BulletFactoryEnemy)
        #游戏时钟
        self.clock=pygame.time.Clock()
        #创建敌人定时器
        pygame.time.set_timer(CREATE_ENEMY_EVENT,2000) #定时创建敌人
        #敌人初始ID
        self.enemy_id=3 #用来赋予每个敌机不同的ID，以便为每个敌机中的子弹设置不同的事件ID
        #创建道具定时器
        pygame.time.set_timer(CREATE_ITEM_EVENT,5000) #定时创建道具

        # 测试boss
        self.enemy_factory.createEnemy(1000, "EnemyBoss")
        #测试boss血条
        bosses=self.enemy_factory.bosses.sprites()
        self.BossHealthUI=BossHealthUI(screen,bosses[0])
        # 游戏状态
        self.game_state=True
        self.game_flag=True
        #Boss是否死亡
        self.BossIsDie=False


    def __create_sprites(self):
        """创建精灵和精灵组"""
        # 1.创建背景精灵和精灵组
        bg1=Background()
        bg2=Background(True)
        bg2.rect.x=bg2.rect.width
        self.back_group=pygame.sprite.Group(bg1,bg2) #设置两个背景的目的是为了实现无缝滚动
        # 2.创建敌机精灵组
        #self.enemy_group=pygame.sprite.Group()
        # 2.1创建敌机子弹精灵组
        #self.enemy_bullet_group=pygame.sprite.Group()
        # 3.创建英雄精灵组
        self.wait_to_destroy_group=pygame.sprite.Group() #等待被销毁的精灵组
        self.hero=Hero(self.BulletFactoryHero) #玩家只有一个，所以直接将其给到hero变量中
        self.hero_group=pygame.sprite.Group(self.hero)
        # 4.创建道具工厂
        self.prop_factory=Prop_factory(self.hero,self.screen)



        pass
    def start_game(self):
        print("游戏开始")
        while self.game_state:
            # 1.设置刷新帧率
            self.clock.tick(FRAME_PER_SEC)
            # 2.事件监听
            self.__event_handle()
            # 3.碰撞检测
            self.__check_collide()
            # 4.更新精灵组
            self.__update_sprites()
            # 5.更新屏幕显示
            pygame.display.update()
            pass
        #返回游戏成功或失败
        return self.game_flag
        pass
    def __event_handle(self):
        # 1.获取事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
                pass
            elif event.type == CREATE_ENEMY_EVENT:
                print("敌机出现...")
                self.enemy_factory.createEnemy(self.enemy_id,"Enemy_base")
                self.enemy_id+=1
                pass
            elif event.type==Hero_FIRE_EVENT:
                self.hero.fire()
            for enemy in self.enemy_factory.enemies:
                if event.type == enemy.shoot_bullet_event_id:
                    print("敌机发射子弹...")
                    #调用敌机子弹工厂类创建子弹
                    enemy.Fire()
                    pass

        # 2.按键控制英雄移动
        keys_pressed=pygame.key.get_pressed()

        if keys_pressed[pygame.K_RIGHT]:
            self.hero.speed=5
        elif keys_pressed[pygame.K_LEFT]:
            self.hero.speed = -5
            pass
        else:
            self.hero.speed=0
        if keys_pressed[pygame.K_UP]:
            self.hero.speedy = -5
        elif keys_pressed[pygame.K_DOWN]:
            self.hero.speedy = 5
        else:
            self.hero.speedy = 0
        # 3.英雄特殊按键
        if keys_pressed[pygame.K_b]:
            #不能杀boss
            print("清空...")
            self.enemy_factory.enemies.empty()
            self.BulletFactoryEnemy.bullets.empty()

    def __check_collide(self):
        """碰撞检测"""

        # 1.设置子弹摧毁敌机
        enemy_collide=pygame.sprite.groupcollide(self.BulletFactoryHero.bullets,self.enemy_factory.enemies,True,False)
        for bullet, hit_enemies in enemy_collide.items():
            # 当子弹击中敌人时，增加得分
            sound_effect = pygame.mixer.Sound("./音效音乐/砸扁.mp3")
            sound_effect.set_volume(0.2)
            sound_effect.play()
            for enemy in hit_enemies:
                if enemy.cause_damage(bullet.damage):
                    self.wait_to_destroy_group.add(enemy)
                    self.enemy_factory.enemies.remove(enemy)
                    # 敌机死亡，概率产生道具
                    if random.randint(1,10)<=7:
                        self.prop_factory.create_prop()
                    self.scoreboard.update_score(1)
                    if self.scoreboard.score>=50:
                        self.__game_over(True)
        if not self.BossIsDie:
            enemy_collide=pygame.sprite.groupcollide(self.BulletFactoryHero.bullets,self.enemy_factory.bosses,True,False)
            for bullet, hit_enemies in enemy_collide.items():
                # 当子弹击中boss时，增加得分
                sound_effect = pygame.mixer.Sound("./音效音乐/砸扁.mp3")
                sound_effect.set_volume(0.2)
                sound_effect.play()
                for enemy in hit_enemies:
                    if enemy.cause_damage(bullet.damage):
                        self.scoreboard.update_score(10) #击毁boss得到10分
                        self.BossIsDie=True
                        if self.scoreboard.score >= 50:
                            self.__game_over(True)
                        self.BossHealthUI=None
        enemies=pygame.sprite.spritecollide(self.hero,self.enemy_factory.enemies,True)
        # 2.1判断列表是否有内容
        if len(enemies)>0:
            if not self.hero.change_health(-1):
                self.hero.kill()
                self.__game_over(False)
        enemies=pygame.sprite.spritecollide(self.hero,self.enemy_factory.bosses,False)
        if len(enemies)>0:
            if not self.hero.change_health(-1):
                self.hero.kill()
                self.__game_over(False)
        # 判断玩家是否被敌机子弹击中
        bullets_enemy=pygame.sprite.spritecollide(self.hero,self.BulletFactoryEnemy.bullets,True)
        if len(bullets_enemy)>0:
            if not self.hero.change_health(-1):
                self.hero.kill()
                self.__game_over(False)

    def __update_sprites(self):
         """更新精灵组"""
         # 1.背景更新渲染显示
         self.back_group.update()
         self.back_group.draw(self.screen)
         # 2.敌机渲染更新显示
         self.enemy_factory.enemies.update()
         self.enemy_factory.bosses.update()
         self.enemy_factory.enemies.draw(self.screen)
         self.enemy_factory.bosses.draw(self.screen)
         # 3.英雄渲染更新显示
         self.hero_group.update()
         self.hero_group.draw(self.screen)
         # 4.英雄子弹渲染更新显示
         self.BulletFactoryHero.bullets.update()
         self.BulletFactoryHero.bullets.draw(self.screen)
         # 5.敌机子弹渲染更新显示
         self.BulletFactoryEnemy.bullets.update()
         self.BulletFactoryEnemy.bullets.draw(self.screen)
         # 6.显示分数
         self.scoreboard.show_score()
         # 7.道具渲染更新显示
         self.prop_factory.update()
         # 8.显示血条
         self.HealthUI.show_health()
         # 9.显示boss血条
         if self.BossHealthUI:
             self.BossHealthUI.draw()
         # 10.等待被销毁的精灵渲染更新显示
         self.wait_to_destroy_group.update()
         self.wait_to_destroy_group.draw(self.screen)
         pass



    def __game_over(self,game_flag=False):
        print("游戏结束")
        self.game_state=False
        self.game_flag=game_flag
        pass
    def __del__(self):
        pygame.mixer.music.stop()
    pass
if __name__=='__main__':
    pygame.init()
    screen = pygame.display.set_mode(SCREEN_RECT.size)
    pygame.display.set_caption("飞机大战")
    menu=Menu(screen)
    menu.run()
    del menu
    game=PlaneGame(screen)
    Gamestate=game.start_game()
    del game
    if Gamestate:
        print("游戏成功")
        successMenu=WinMenu(screen)
        successMenu.run()
    else:
        print("游戏失败")
        failedMenu=FailedMenu(screen)
        failedMenu.run()
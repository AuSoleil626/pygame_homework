import pygame
import sys
from plane_sprites import *

class Scoreboard:
    def __init__(self, screen, initial_score=0, font_size=36, font_color=(0, 0, 0)):
        self.screen = screen
        self.score = initial_score
        self.font = pygame.font.Font(None, font_size)
        self.font_color = font_color
        self.text = self.font.render('Score: ' + str(self.score), True, self.font_color)
        self.text_rect = self.text.get_rect(topleft=(10, 10))
        self.text_explain=self.font.render('Score greater than 50 to win the game!', True, self.font_color)
        self.text_explain_rect=self.text_explain.get_rect(topleft=(10, 50))

    def update_score(self, points):
        self.score += points
        self.text = self.font.render('Score: ' + str(self.score), True, self.font_color)

    def show_score(self):
        self.screen.blit(self.text, self.text_rect)
        self.screen.blit(self.text_explain, self.text_explain_rect)

class HealthUI:
    def __init__(self, screen, player):
        self.screen = screen
        self.player = player
        self.font = pygame.font.Font(None, 36)  # 设置字体和字号

    def show_health(self):
        health_text = f"Player Health: {self.player.health}"  # 获取玩家当前血量信息
        text_surface = self.font.render(health_text, True, (0, 0, 0))  # 创建文本表面
        text_rect = text_surface.get_rect()
        text_rect.topright = (self.screen.get_width() - 20, 20)  # 设置文本位置为屏幕右上角
        self.screen.blit(text_surface, text_rect)  # 在屏幕上绘制血量信息文本
class BossHealthUI:
    def __init__(self, screen, boss):
        #坐标在画面正上方
        self.x = SCREEN_RECT.centerx - 150
        self.y = 10
        self.screen = screen
        self.boss = boss
        self.max_health = self.boss.maxhealth
        self.health = self.max_health
        self.length = 300
        self.height = 20

    def draw(self):
        # 绘制血量条的底色
        self.health=self.boss.health
        pygame.draw.rect(self.screen, (255, 0, 0), (self.x, self.y, self.length, self.height))
        # 根据血量动态绘制血量条
        health_width = int((self.health / self.max_health) * self.length)
        pygame.draw.rect(self.screen, (0, 255, 0), (self.x, self.y, health_width, self.height))
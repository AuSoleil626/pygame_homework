import pygame
import sys
from plane_sprites import SCREEN_RECT

class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.running = True
        #开始游戏按键
        self.startimage = pygame.image.load("./Pictures/UI/SG.png")
        self.startimage = pygame.transform.scale(self.startimage, (350, 60))
        self.startimagerect = self.startimage.get_rect(center=(SCREEN_RECT.centerx, SCREEN_RECT.centery - 50))
        self.tempstartimage = self.startimage.copy()
        #退出游戏按键
        self.exitimage = pygame.image.load("./Pictures/UI/EG.png")
        self.exitimage = pygame.transform.scale(self.exitimage, (350, 60))
        self.exitimagerect = self.exitimage.get_rect(center=(SCREEN_RECT.centerx, SCREEN_RECT.centery+50))
        self.tempexitimage = self.exitimage.copy()
        #按钮大小

        self.menuimage = pygame.image.load("./Pictures/BG/BG.png")
        self.menuimage = pygame.transform.scale(self.menuimage, SCREEN_RECT.size)




    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    #判断鼠标点击位置
                    if self.startimagerect.collidepoint(event.pos):
                        #开始游戏
                        self.running = False
                    elif self.exitimagerect.collidepoint(event.pos):
                        #退出游戏
                        pygame.quit()
                        sys.exit()
                #鼠标悬浮时放大按钮
                if event.type == pygame.MOUSEMOTION:
                    if self.startimagerect.collidepoint(event.pos):
                        self.startimage = pygame.transform.scale(self.tempstartimage, (370, 70))
                        self.startimagerect = self.startimage.get_rect(center=(SCREEN_RECT.centerx, SCREEN_RECT.centery - 50))
                    else:
                        self.startimage = self.tempstartimage
                        self.startimagerect = self.startimage.get_rect(center=(SCREEN_RECT.centerx, SCREEN_RECT.centery - 50))
                    if self.exitimagerect.collidepoint(event.pos):
                        self.exitimage = pygame.transform.scale(self.tempexitimage, (370, 70))
                        self.exitimagerect = self.exitimage.get_rect(center=(SCREEN_RECT.centerx, SCREEN_RECT.centery+50))
                    else:
                        self.exitimage = self.tempexitimage
                        self.exitimagerect = self.exitimage.get_rect(center=(SCREEN_RECT.centerx, SCREEN_RECT.centery+50))


            self.screen.blit(self.menuimage, (0, 0))
            self.screen.blit(self.startimage, self.startimagerect)
            self.screen.blit(self.exitimage, self.exitimagerect)
            pygame.display.flip()

class FailedMenu:
    def __init__(self, screen):
        self.screen = screen
        self.running = True
        self.menuimage = pygame.image.load("./Pictures/BG/BG.png")
        self.menuimage = pygame.transform.scale(self.menuimage, SCREEN_RECT.size)
        self.failedimage = pygame.image.load("./Pictures/UI/MF.png")
    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            self.screen.blit(self.menuimage, (0, 0))
            #失败的图片居中显示
            self.failedimagerect = self.failedimage.get_rect(center=(SCREEN_RECT.centerx, SCREEN_RECT.centery))
            self.screen.blit(self.failedimage, self.failedimagerect)
            pygame.display.flip()
class WinMenu:
    def __init__(self, screen):
        self.screen = screen
        self.running = True
        self.menuimage = pygame.image.load("./Pictures/BG/BG.png")
        self.menuimage = pygame.transform.scale(self.menuimage, SCREEN_RECT.size)
        self.winimage = pygame.image.load("./Pictures/UI/MC.png")
    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            self.screen.blit(self.menuimage, (0, 0))
            #胜利的图片居中显示
            self.winimagerect = self.winimage.get_rect(center=(SCREEN_RECT.centerx, SCREEN_RECT.centery))
            self.screen.blit(self.winimage, self.winimagerect)
            pygame.display.flip()
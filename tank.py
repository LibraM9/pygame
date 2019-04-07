# -*- coding: utf-8 -*-
#@author: limeng
#@file: tank.py
#@time: 2019/4/6 22:29
"""
文件说明：
"""
import pygame, sys, time
from random import randint
from pygame.locals import *


class TankMain():
    # 开始游戏
    width = 600
    height = 500
    my_tank_missile_list = []
    my_tank = None
    wall = None
    # 创建一个我方坦克
    # enemy_list = []
    enemy_list = pygame.sprite.Group()  # 敌方坦克的族群
    explode_list = []
    # 敌方坦克的炮弹
    enemy_missile_list = pygame.sprite.Group()

    def startGame(self):
        pygame.init()  # pygame
        # 创建一个屏幕，屏幕的大小，宽和高，0为固定大小（0，RESIZEBLE,FULLSCREEN
        screem = pygame.display.set_mode((TankMain.width, TankMain.height), 0, 32)
        pygame.display.set_caption("管萍大战")

        TankMain.wall = Wall(screem, 60, 75, 30, 120)  # 创建一个墙

        TankMain.my_tank = My_Tank(screem)
        if len(TankMain.enemy_list) == 0:
            for i in range(1, 6):  # 敌方坦克随机数
                TankMain.enemy_list.add(Enemy_Tank(screem))  # 把敌方坦克放到组里
        while True:
            # if len(TankMain.enemy_list) < 5:
            #     TankMain.enemy_list.add(Enemy_Tank(screem))  # 把敌方坦克放到组里
            if TankMain.my_tank == None:
                pygame.time.wait(1000)
                TankMain.my_tank = My_Tank(screem)
            if len(TankMain.enemy_list) == 0:
                m_p = pygame.image.load("F:/迅雷下载/img/next.jpg").convert_alpha()
                screem.blit(m_p, (0,0))
                pygame.display.update()
            # color RGB（0,100,200）
            # 设置屏幕背景色为黑色
            screem.fill((0, 0, 0))
            TankMain.wall.display()
            TankMain.wall.hit_other()  # 碰撞检测并且显示墙
            # 显示左上角的文字
            for i, text in enumerate(self.write_text(), 0):
                screem.blit(text, (0, 5 + (13 * i)))  # 纵x横y
            self.get_event(TankMain.my_tank, screem)  # 获取事件，根据获取的事件处理
            if TankMain.my_tank:
                TankMain.my_tank.hit_enemy_missile()
                # 判断我方坦克跟炮弹是否碰撞
            if TankMain.my_tank and TankMain.my_tank.live:
                TankMain.my_tank.display()  # 我方坦克显示和移动
                TankMain.my_tank.move()
            else:
                TankMain.my_tank = None
                # TankMain.my_tank=None   两种删除坦克的方法
            # 显示重置
            for enemy in TankMain.enemy_list:
                enemy.display()  # 敌方坦克显示和随机移动
                enemy.random_move()
                enemy.random_fire()

            # 显示所有的我方炮弹
            for m in TankMain.my_tank_missile_list:
                if m.live:
                    m.display()
                    m.hit_tank()  # 炮弹打中敌方坦克
                    m.move()
                else:
                    TankMain.my_tank_missile_list.remove(m)
            for m in TankMain.enemy_missile_list:
                if m.live:
                    m.display()
                    m.move()
                else:
                    TankMain.enemy_missile_list.remove(m)

            for explode in TankMain.explode_list:  # 显示爆炸效果
                explode.display()

            time.sleep(0.05)  # 可以调坦克的速度，越小，速度越快
            pygame.display.update()
        # 获取所有的事件(敲击键盘，鼠标点击 都属于事件)

    def get_event(self, my_tank, screem):
        for event in pygame.event.get():
            if event.type == QUIT:  # 程序退出
                self.stopGame()
            if event.type == KEYDOWN and (not my_tank) and event.key == K_n:
                TankMain.my_tank = My_Tank(screem)
            if event.type == KEYDOWN and my_tank:
                if event.key == K_LEFT:
                    my_tank.direction = "L"  # 左移
                    my_tank.stop = False
                    # my_tank.move()
                if event.key == K_RIGHT:
                    my_tank.direction = "R"  # 右边移动
                    my_tank.stop = False
                    # my_tank.move()
                if event.key == K_UP:
                    my_tank.direction = "U"  # 上移
                    my_tank.stop = False
                    # my_tank.move()
                if event.key == K_DOWN:
                    my_tank.direction = "D"  # 下移
                    my_tank.stop = False
                    # my_tank.move()
                if event.key == K_ESCAPE:  # esc退出
                    self.stopGame()
                if event.key == K_SPACE:  # 发射炮弹
                    m = my_tank.fire()
                    m.good = True  # 我方坦克发射的炮弹
                    TankMain.my_tank_missile_list.append(m)
            if event.type == KEYUP and my_tank:
                if event.key == K_LEFT or event.key == K_RIGHT or event.key == K_DOWN or event.key == K_UP:
                    my_tank.stop = True

    # 停止游戏
    def stopGame(self):
        sys.exit()

    # 在屏幕左上角显示文字
    def write_text(self):
        font = pygame.font.SysFont("simsunnsimsun", 15)  # 定义一个字体
        text_sf1 = font.render("enemy tank:%d" % len(TankMain.enemy_list), True, (255, 0, 0))  # 根据字体创建一个文件的图像
        text_sf2 = font.render("my tank missile:%d" % len(TankMain.my_tank_missile_list), True, (255, 0, 0))
        return text_sf1, text_sf2


# 坦克大战中所有对象的父类
class BaseItem(pygame.sprite.Sprite):
    def __init__(self, screem):
        pygame.sprite.Sprite.__init__(self)
        self.screem = screem  # 所有类共享的属性

        # 吧坦克对应的图片显示在游戏窗口上

    def display(self):
        if self.live:
            self.image = self.images[self.direction]
            self.screem.blit(self.image, self.rect)


class Tank(BaseItem):
    # 定义类属性
    width = 35
    height = 35

    def __init__(self, screem, left, top):
        super(Tank, self).__init__(screem)
        # self.screem=screem#坦克在移动过程中需要用到屏幕
        self.direction = "D"  # 坦克的方向，默认向下
        self.speed = 5  # 坦克移动速度
        self.stop = False
        self.images = {}  # 坦克的所有图片，key 方向 value 图片（suface)
        self.images["L"] = pygame.image.load("F:/迅雷下载/img/lm.png")
        self.images["R"] = pygame.image.load("F:/迅雷下载/img/lm.png")
        self.images["U"] = pygame.image.load("F:/迅雷下载/img/lm.png")
        self.images["D"] = pygame.image.load("F:/迅雷下载/img/lm.png")
        self.image = self.images[self.direction]  # 坦克的图片由方向决定
        self.rect = self.image.get_rect()
        self.rect.left = left
        self.rect.top = top
        self.live = True  # 决定坦克生死
        self.oldleft = self.rect.left
        self.oldtop = self.rect.top

    def stay(self):
        self.rect.top = self.oldtop
        self.rect.left = self.oldleft

    def move(self):
        if not self.stop:  # 如果坦克不是停止状态
            self.oldleft = self.rect.left
            self.oldtop = self.rect.top
            if self.direction == "L":  # 如果坦克的方向向左，那么只需要改坦克的left就ok了。left在减小
                if self.rect.left > 0:  # 判断坦克是否在屏幕左边的边界上
                    self.rect.left -= self.speed
                else:
                    self.rect.left = 0
            elif self.direction == "R":  # 如果坦克方向向右，坦克的right增加就ok了。
                if self.rect.right < TankMain.width:  # 坦克已经在屏幕的最右边的话就不能往右移动了
                    self.rect.right += self.speed
                else:
                    self.rect.right = TankMain.width
            elif self.direction == "D":  # 如果坦克方向向下，坦克的bottom增加就ok了。
                if self.rect.bottom < TankMain.height:
                    self.rect.top += self.speed
                else:
                    self.rect.bottom = TankMain.height
            elif self.direction == "U":  # 如果坦克方向向上，坦克的top减小就ok了。
                if self.rect.top > 0:
                    self.rect.top -= self.speed
                else:
                    self.rect.top = 0

    def fire(self):
        m = Missile(self.screem, self)
        return m


class My_Tank(Tank):
    def __init__(self, screem):
        super(My_Tank, self).__init__(screem, 275, 400)  # 创建一个我方坦克，坦克显示在屏幕的中下部位置
        self.stop = True
        self.live = True

    def hit_enemy_missile(self):
        hit_list = pygame.sprite.spritecollide(self, TankMain.enemy_missile_list, False)
        for m in hit_list:  # 我方坦克中弹
            m.live = False
            TankMain.enemy_missile_list.remove(m)
            self.live = False
            explode = Explode(self.screem, self.rect)
            TankMain.explode_list.append(explode)


class Enemy_Tank(Tank):

    def __init__(self, screem):
        super(Enemy_Tank, self).__init__(screem, randint(1, 5) * 100, 200)
        self.speed = 4
        self.step = 8  # 坦克在一个方向移动6步

        self.get_random_direction()
        self.images["L"] = pygame.image.load("F:/迅雷下载/img/gp.png")
        self.images["R"] = pygame.image.load("F:/迅雷下载/img/gp.png")
        self.images["U"] = pygame.image.load("F:/迅雷下载/img/gp.png")
        self.images["D"] = pygame.image.load("F:/迅雷下载/img/gp.png")

    def get_random_direction(self):
        r = randint(0, 4)  # 得到一个坦克移动方向和停止的随机数
        if r == 4:
            self.stop = True
        elif r == 0:
            self.direction = "L"
            self.stop = False
        elif r == 1:
            self.direction = "R"
            self.stop = False
        elif r == 2:
            self.direction = "U"
            self.stop = False
        elif r == 3:
            self.direction = "D"
            self.stop = False

    # 敌方坦克移动6步后，在随机换方向接着移动
    def random_move(self):
        if self.live:
            if self.step == 0:
                self.get_random_direction()
                self.step = 6
            else:
                self.move()
                self.step -= 1

    def random_fire(self):
        r = randint(0, 50)
        if r == 10 or r == 25:
            m = self.fire()
            TankMain.enemy_missile_list.add(m)
        else:
            return


class Missile(BaseItem):
    width = 12
    height = 12

    def __init__(self, screem, tank):
        super(Missile, self).__init__(screem)
        self.tank = tank
        self.direction = tank.direction  # 炮弹的方向由所发射的坦克决定
        self.speed = 12  # 炮弹移动速度
        self.images = {}  # 炮弹的所有图片，key 方向 value 图片（suface)
        self.images["L"] = pygame.image.load("F:/迅雷下载/img/shell.png")
        self.images["R"] = pygame.image.load("F:/迅雷下载/img/shell.png")
        self.images["U"] = pygame.image.load("F:/迅雷下载/img/shell.png")
        self.images["D"] = pygame.image.load("F:/迅雷下载/img/shell.png")
        self.image = self.images[self.direction]  # 坦克的图片由方向决定
        self.rect = self.image.get_rect()
        self.rect.left = tank.rect.left + (tank.width - self.width) / 2
        self.rect.top = tank.rect.top + (tank.height - self.height) / 2
        self.live = True  # 决定炮弹生死
        self.food = False

    def move(self):
        if self.live:  # 如果炮弹活着
            if self.direction == "L":  # 如果坦克的方向向左，那么只需要改坦克的left就ok了。left在减小
                if self.rect.left > 0:  # 判断坦克是否在屏幕左边的边界上
                    self.rect.left -= self.speed
                else:
                    self.live = False
            elif self.direction == "R":  # 如果坦克方向向右，坦克的right增加就ok了。
                if self.rect.right < TankMain.width:  # 坦克已经在屏幕的最右边的话就不能往右移动了
                    self.rect.right += self.speed
                else:
                    self.live = False
            elif self.direction == "D":  # 如果坦克方向向下，坦克的bottom增加就ok了。
                if self.rect.bottom < TankMain.height:
                    self.rect.top += self.speed
                else:
                    self.live = False
            elif self.direction == "U":  # 如果坦克方向向上，坦克的top减小就ok了。
                if self.rect.top > 0:
                    self.rect.top -= self.speed
                else:
                    self.live = False

    # 炮弹击中坦克，1我方坦克击中敌方坦克，敌方坦克击中我方坦克
    def hit_tank(self):
        if self.good:  # 我方炮弹
            hit_list = pygame.sprite.spritecollide(self, TankMain.enemy_list, False)
            for e in hit_list:
                e.live = False
                TankMain.enemy_list.remove(e)  # 删除坦克
                self.live = False
                explode = Explode(self.screem, e.rect)  # 产生了一个爆炸对象
                TankMain.explode_list.append(explode)


# 爆炸类
class Explode(BaseItem):

    def __init__(self, screem, rect):
        super(Explode, self).__init__(screem)
        self.live = True
        self.images = [pygame.image.load("F:/迅雷下载/img/gp2.png"), \
                       pygame.image.load("F:/迅雷下载/img/gp2.png"), \
                       pygame.image.load("F:/迅雷下载/img/gp2.png"), \
                       pygame.image.load("F:/迅雷下载/img/gp2.png"), \
                       pygame.image.load("F:/迅雷下载/img/gp2.png"), \
                       pygame.image.load("F:/迅雷下载/img/gp2.png"), \
                       pygame.image.load("F:/迅雷下载/img/gp2.png"), \
                       pygame.image.load("F:/迅雷下载/img/gp2.png"), \
                       pygame.image.load("F:/迅雷下载/img/gp2.png"), \
                       pygame.image.load("F:/迅雷下载/img/gp2.png"), \
                       pygame.image.load("F:/迅雷下载/img/gp2.png"), ]  # 爆炸效果的图片
        self.step = 0
        self.rect = rect  # 爆炸的位置和炮弹碰到的坦克位置一样

    def display(self):
        if self.live:
            if self.step == len(self.images):  # 最后一张爆炸图片已经显示
                self.live = False
            else:
                self.image = self.images[self.step]
                self.screem.blit(self.image, self.rect)
                self.step += 1
        else:
            pass


# 游戏中的障碍物
class Wall(BaseItem):
    def __init__(self, screem, left, top, width, height):
        super(Wall, self).__init__(screem)
        self.rect = Rect(left, top, width, height)  # 墙的高度
        self.color = (255, 142, 0)  # 墙的颜色

    def display(self):
        self.screem.fill(self.color, self.rect)

    def hit_other(self):  # 检测墙与其他的碰撞
        if TankMain.my_tank:
            is_hit = pygame.sprite.collide_rect(self, TankMain.my_tank)
            if is_hit:
                TankMain.my_tank.stop = True
                TankMain.my_tank.stay()
            if len(TankMain.enemy_list) != 0:
                hit_list = pygame.sprite.spritecollide(self, TankMain.enemy_list, False)
                for e in hit_list:
                    e.stop = True
                    e.stay()


game = TankMain()
game.startGame()
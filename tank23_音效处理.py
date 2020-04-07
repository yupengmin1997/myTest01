# coding=utf-8
'''
新增功能：
    1.完善音效类
    2.添加开场音效
    3.我方坦克发射子弹添加音效


'''
import random
import time
import pygame
from pygame.sprite import Sprite

SCREEN_WIDTH = 700
SCREEN_HEIGHT = 600
BG_COLOR = pygame.Color(230,230,230)
TEXT_COLOR = pygame.Color(255,0,0)


# 定义一个基类
class BaseItem(Sprite):
    def __init__(self,color,width,height):
        pygame.sprite.Sprite.__init__(self)


class MainGame():
    window = None
    my_tank = None

    # 创建存储敌方坦克的列表
    enemyTankList = []
    # 定义敌方坦克的数量
    enemyTankCount = 5
    # 定义存储我方子弹的列表
    myBulletList = []
    # 定义存储敌方子弹的列表
    enemyBulletList = []
    # 存储爆炸效果的爆炸列表
    explodeList = []
    # 存储墙壁的列表
    wallList = []
    def __init__(self):
        pass

    def  startGame(self):
        # 加载主窗口
        # 初始化窗口
        pygame.display.init()
        # 这是窗口的大小及显示
        MainGame.window = pygame.display.set_mode([SCREEN_WIDTH,SCREEN_HEIGHT])
        # 初始化我方坦克
        self.createMyTank()
        # 初始化敌方坦克,添加到敌方坦克列表中
        self.createEnemyTank()
        # 初始化墙壁
        self.createWall()
        # 设置窗口的标题
        pygame.display.set_caption("坦克大战1.0")
        # 窗口一直显示
        while True:
            # 设置坦克移动的休眠时间
            time.sleep(0.02)
            # 设置窗口的颜色,背景色
            MainGame.window.fill(BG_COLOR)
            self.getEvent() # 调用获取事件的方法
            # 绘制文字
            # 将小的surface加入到主窗口中,需要设置坐标
            MainGame.window.blit(self.getTextSurface("敌方坦克剩余数量：%d"%len(MainGame.enemyTankList)),(10,10))
            # 显示坦克
            # 判断我方坦克是否存活
            if MainGame.my_tank and MainGame.my_tank.live:
                MainGame.my_tank.displayTank()
            else:
                # 删除我方坦克
                del MainGame.my_tank
                MainGame.my_tank = None
            # 循环遍历列表，展示敌方坦克
            self.blitEnemyTank()
            # 循环遍历显示我方坦克的子弹
            self.blitMyBullet()
            # 循环遍历显示敌方坦克的子弹
            self.blitEnemyBullet()
            # 循环遍历爆炸列表，展示爆炸效果
            self.blitExplode()
            # 循环遍历墙壁列表,显示墙壁
            self.blitWall()
            # 如果坦克的开关是开启时，坦克才可以移动
            if MainGame.my_tank and MainGame.my_tank.live:
                if not MainGame.my_tank.stop:
                    # 调用移动的方法
                    MainGame.my_tank.move()
                    # 检测我方坦克是否与墙壁发生碰撞
                    MainGame.my_tank.hitWall()
                    # 检测我方坦克与敌方坦克碰撞的方法
                    MainGame.my_tank.myTank_hit_enemyTank()

            pygame.display.update()

    # 创建墙壁的方法
    def createWall(self):
        # 创建墙壁
        for i in range(6):
            wall = Wall(i*140,270)
            # 将墙壁添加到列表中
            MainGame.wallList.append(wall)
    # 创建我方坦克的方法
    def createMyTank(self):
        MainGame.my_tank = MyTank(250, 330)
        # 创建Music对象
        music = Music("img/start.wav")
        # 播放音乐
        music.playMusic()

    # 创建敌方坦克
    def createEnemyTank(self):
        top = 100
        # 循环生成坦克数
        for i in range(MainGame.enemyTankCount):
            left = random.randint(0, 400)
            speed = random.randint(1, 4)
            enemy = EnemyTank(left,top,speed)
            # 添加到列表
            MainGame.enemyTankList.append(enemy)

    # 循环遍历墙壁列表，显示墙壁
    def blitWall(self):
        for wall in MainGame.wallList:
            # 判断墙壁的生存状态
            if wall.live:
                # 调用墙壁的显示方法
                wall.displayWall()
            else:
                # 从列表中删除
                MainGame.wallList.remove(wall)

    # 循环遍历敌方坦克列表，展示敌方坦克
    def blitEnemyTank(self):
        for enemyTank in MainGame.enemyTankList:
            # 判断敌方眼科是否存活。如果存活，则显示敌方坦克
            if enemyTank.live:
                enemyTank.displayTank()
                enemyTank.randMove()

                # 调动敌方子弹与墙壁是否发生碰撞
                enemyTank.hitWall()

                # 判断我方坦克是否存在
                if MainGame.my_tank and MainGame.my_tank.live:
                    # 检测敌方坦克与我方坦克碰撞的方法
                    enemyTank.enemyTank_hit_myTank()

                # 敌方坦克发射子弹
                enemyBullet = enemyTank.shot()

                # 判断敌方子弹是否为None，如果不为None则添加到子弹列表中
                if enemyBullet:
                    # 将敌方子弹存储到敌方子弹列表中
                    MainGame.enemyBulletList.append(enemyBullet)
            else: # 若敌方坦克不存活，则从敌方坦克列表中移除
                MainGame.enemyTankList.remove(enemyTank)

    # 循环遍历显示我方坦克的子弹
    def blitMyBullet(self):
        for myBullet in MainGame.myBulletList:
            # 加上子弹的状态判断，如果是True，则显示。如果是False，则在列表中删除。
            if myBullet.live:
                # 展示子弹
                myBullet.displayBullet()
                # 调用子弹移动的方法
                myBullet.move()

                #调用检测我方子弹与敌方坦克发生碰撞
                myBullet.myBullet_hit_enemyTank()
                # 调动我方子弹与墙壁发生碰撞
                myBullet.hitWall()
            # 在列表中删除
            else:
                MainGame.myBulletList.remove(myBullet)

    # 循环遍历显示敌方坦克的子弹
    def blitEnemyBullet(self):
        for enemyBullet in MainGame.enemyBulletList:
            if enemyBullet.live:
                enemyBullet.displayBullet()
                enemyBullet.move()

                # 调用敌方子弹与我方坦克的碰撞方法
                enemyBullet.enemyBullet_hit_myTank()
                # 调用地方子弹与墙壁碰撞
                enemyBullet.hitWall()
            else:
                MainGame.enemyBulletList.remove(enemyBullet)

    # 循环遍历爆炸列表，展示爆炸效果
    def blitExplode(self):
        for explode in MainGame.explodeList:
            # 判断是否活着
            if explode.live:
                # 展示
                explode.displayExplode()
            else:
                # 在爆炸列表中移除
                MainGame.explodeList.remove(explode)

    def endGame(self):
        print("谢谢使用，程序关闭...")
        quit()
    '''获取事件'''
    def getEvent(self):
        # 获取所有事件
        eventList = pygame.event.get()
        # 遍历事件
        for event in eventList:
            # 判断按下的键是关闭还是键盘按下的建
            if event.type == pygame.QUIT:  # 如果按下的键是退出，则关闭窗口
                self.endGame()
            elif event.type == pygame.KEYDOWN: # 如果按下的是键盘
                # 如果坦克不存在或是状态为False
                if not MainGame.my_tank:
                    # 判断按下Esc键让坦克重生
                    if event.key == pygame.K_ESCAPE:
                        # 让坦克重生，调用创建坦克的方法
                        self.createMyTank()
                # 如果坦克存在
                if MainGame.my_tank and MainGame.my_tank.live:
                    # 判断按下的是上、下、坐、右
                    if event.key == pygame.K_LEFT:
                        # 切换方向
                        MainGame.my_tank.direction = "L" # 设置当前坦克的属性
                        # 修改坦克的开关状态
                        MainGame.my_tank.stop = False
                        # MainGame.my_tank.move()  # 调用移动方法
                        print("按下左键，坦克向左移动")
                    elif event.key == pygame.K_RIGHT:
                        # 切换方向
                        MainGame.my_tank.direction = "R"  # 设置当前坦克的属性
                        # 修改坦克的开关状态
                        MainGame.my_tank.stop = False
                        # MainGame.my_tank.move()  # 调用移动方法
                        print("按下右键，坦克向右移动")
                    elif event.key == pygame.K_UP:
                        # 切换方向
                        MainGame.my_tank.direction = "U"  # 设置当前坦克的属性
                        # 修改坦克的开关状态
                        MainGame.my_tank.stop = False
                        # MainGame.my_tank.move()  # 调用移动方法
                        print("按下上键，坦克向上移动")
                    elif event.key == pygame.K_DOWN:
                        # 切换方向
                        MainGame.my_tank.direction = "D"  # 设置当前坦克的属性
                        # 修改坦克的开关状态
                        MainGame.my_tank.stop = False
                        # MainGame.my_tank.move()  # 调用移动方法
                        print("按下下键，坦克向下移动")
                    elif event.key == pygame.K_SPACE:
                        print("发射子弹...")

                        # 如果当前我方子弹列表的子弹数小于等于3时，才可以创建
                        if len(MainGame.myBulletList)<3:
                            # 创建我方坦克发射的子弹
                            myBullet = Bullet(MainGame.my_tank)
                            MainGame.myBulletList.append(myBullet)
                            # 创建我方坦克发射子弹音效方法
                            music = Music("img/fire.wav")
                            music.playMusic()

            # 松开方向键，坦克停止移动
            elif event.type == pygame.KEYUP:
                # 判断松开的键是上下左右时候，才停止坦克移动，子弹的发射不影响坦克的移动
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN or\
                    event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    if MainGame.my_tank and MainGame.my_tank.live:
                        MainGame.my_tank.stop = True
    # 左上角文字的绘制
    def getTextSurface(self,text):
        # 初始化字体模块
        pygame.font.init()
        # 查看所有字体的名称
        # print(pygame.font.get_fonts())
        # 获取字体Font对象
        font = pygame.font.SysFont("kaiti",18)
        # 绘制文字信息
        textSurface = font.render(text,True,TEXT_COLOR)
        return textSurface


class Tank(BaseItem):
    # 添加距离左边left，距离上边top
    def __init__(self,left,top):
        # 保存加载的图片
        self.images = {
            "U":pygame.image.load("img/p1tankU.gif"),
            "D":pygame.image.load("img/p1tankD.gif"),
            "L":pygame.image.load("img/p1tankL.gif"),
            "R":pygame.image.load("img/p1tankR.gif"),
        }
        # 方向
        self.direction = "U"
        # 根据图片的方向获取图片
        self.image = self.images[self.direction] # 返回一个小的surface
        # 根据图片获取区域
        self.rect = self.image.get_rect()
        # 设置区域的left 和 top
        self.rect.left = left
        self.rect.top = top
        # 坦克速度决定移动的快慢
        self.speed = 6
        # 设置坦克移动的开关
        self.stop = True
        self.live = True

        # 新增属性：原来的坐标
        self.oldLeft = self.rect.left
        self.oldTop = self.rect.top

    def shot(self):
        return Bullet(self)  # 返回生成子弹

    def move(self):
        # 移动后，对原来的坐标赋值
        self.oldLeft = self.rect.left
        self.oldTop = self.rect.top

        # 判断坦克的方向进行移动
        if self.direction == "L":
            if self.rect.left>0:
                self.rect.left -= self.speed
        elif self.direction == "U":
            if self.rect.top>0:
                self.rect.top -= self.speed
        elif self.direction == "D":
            if self.rect.top<SCREEN_HEIGHT-self.rect.height:
                self.rect.top += self.speed
        elif self.direction == "R":
            if self.rect.left<SCREEN_WIDTH-self.rect.height:
                self.rect.left += self.speed

    def displayTank(self):
        # 获取展示的对象
        self.image = self.images[self.direction]
        # 调用blit方法进行展示
        MainGame.window.blit(self.image,self.rect)

    # 将坐标设置为移动之前的坐标的方法
    def stay(self):
        self.rect.left = self.oldLeft
        self.rect.top = self.oldTop

    # 检测坦克是否与墙壁碰撞
    def hitWall(self):
        for wall in MainGame.wallList:
            if pygame.sprite.collide_rect(wall,self):
                # 将坐标设置为移动之前的坐标
                self.stay()


class MyTank(Tank):

    def __init__(self,left,top):
        # 调用父类的初始化方法
        super(MyTank, self).__init__(left,top)

    # 检测我方坦克与敌方坦克碰撞的方法
    def myTank_hit_enemyTank(self):
        for enemyTank in MainGame.enemyTankList:
            if pygame.sprite.collide_rect(self,enemyTank):
                self.stay()


class EnemyTank(Tank):
    def __init__(self,left,top,speed):
        # 调用父类的初始化方法
        super(EnemyTank,self).__init__(left,top)
        # 加载敌方坦克图片集
        self.images = {
            "U":pygame.image.load("img/enemy1U.gif"),
            "L":pygame.image.load("img/enemy1L.gif"),
            "R":pygame.image.load("img/enemy1R.gif"),
            "D":pygame.image.load("img/enemy1D.gif")
        }
        # 生成敌方坦克的方向，随机
        self.direction = self.randDirection()
        # 根据方向获取图片
        self.image = self.images[self.direction]
        # 设置区域
        self.rect = self.image.get_rect()
        # 对left和top进行赋值
        self.rect.left = left
        self.rect.top = top
        # 设置敌方坦克移动速度
        self.speed = 2
        # 移动开关
        self.flag = True
        # 新增一个步数变量
        self.step = 60
        # 坦克的生死
        self.live = True

    # 检测敌方坦克与我方坦克碰撞的方法
    def enemyTank_hit_myTank(self):
        if pygame.sprite.collide_rect(self,MainGame.my_tank):
            self.stay()

    # 随机生成方向
    def randDirection(self):
        num = random.randint(1,4)
        if num == 1:
            return "U"
        elif num == 2:
            return "L"
        elif num == 3:
            return "R"
        elif num == 4:
            return "D"

    # 坦克随机移动的方法
    def randMove(self):
        if self.step <= 0:
            # 修改方向
            self.direction = self.randDirection()
            # 让步数复位
            self.step = 60
        else:
            self.move()
            # 步数递减
            self.step -= 1

    # 重写shot方法
    def shot(self):
        # 随机生成100以内的整数
        num=random.randint(1,100)
        if num < 6:
            return Bullet(self)


# 子弹类
class Bullet(BaseItem):
    def __init__(self,tank):
        # 加载图片
        self.image = pygame.image.load("img/enemymissile.gif")
        # 坦克的方向决定子弹的方向
        self.direction = tank.direction
        # 获取区域
        self.rect = self.image.get_rect()
        # 子弹的left、top与方向有关
        if self.direction == "U":
            self.rect.left = tank.rect.left+tank.rect.width/2-self.rect.width/2
            self.rect.top = tank.rect.top-self.rect.height
        elif self.direction == "D":
            self.rect.left = tank.rect.left+tank.rect.width/2-self.rect.width/2
            self.rect.top = tank.rect.top+self.rect.height
        elif self.direction == "L":
            self.rect.left = tank.rect.left - tank.rect.width/2 - self.rect.width/2
            self.rect.top = tank.rect.top + tank.rect.width/2 -self.rect.width/2
        elif self.direction == "R":
            self.rect.left = tank.rect.left + tank.rect.width
            self.rect.top = tank.rect.top + tank.rect.width/2 - self.rect.width/2
        # 子弹移动速度
        self.speed= 5
        # 子弹的状态，是否碰到墙壁。如果碰到墙壁，状态修改。
        self.live = True

    # 子弹的移动
    def move(self):
        if self.direction == "U":
            if self.rect.top > 0:
                self.rect.top -= self.speed
            else:
                # 修改子弹的状态
                self.live = False
        elif self.direction == "D":
            if self.rect.top + self.rect.height < SCREEN_HEIGHT:
                self.rect.top += self.speed
            else:
                # 修改子弹的状态
                self.live = False
        elif self.direction == "L":
            if self.rect.left > 0:
                self.rect.left -= self.speed
            else:
                # 修改子弹的状态
                self.live = False
        elif self.direction == "R":
            if self.rect.left + self.rect.width < SCREEN_WIDTH:
                self.rect.left += self.speed
            else:
                # 修改子弹的状态
                self.live = False

    # 展示子弹的方法
    def displayBullet(self):
        # 将图片surface加载到窗口
        MainGame.window.blit(self.image,self.rect)


    # 我方子弹与敌方坦克的碰撞
    def myBullet_hit_enemyTank(self):
        # 检测我方坦克是否存活
        for enemyTank in MainGame.enemyTankList:
            if pygame.sprite.collide_rect(enemyTank,self):
                # 若发生碰撞，则修改敌方坦克和我方子弹的状态
                enemyTank.live = False
                self.live = False
                # 创建爆炸对象
                explode = Explode(enemyTank)
                # 将爆炸对象添加到爆炸列表中
                MainGame.explodeList.append(explode)

    # 敌方子弹与我方坦克的碰撞
    def enemyBullet_hit_myTank(self):
        if MainGame.my_tank and MainGame.my_tank.live:
            if pygame.sprite.collide_rect(MainGame.my_tank, self):
                # 发生碰撞，修改敌方子弹和我方坦克的状态
                self.live = False
                MainGame.my_tank.live = False
                # 创建爆炸对象
                explode = Explode(MainGame.my_tank)
                # 将爆炸对象添加到爆炸列表中
                MainGame.explodeList.append(explode)

    # 检测子弹与墙壁碰撞的方法
    def hitWall(self):
        # 循环遍历墙壁列表
        for wall in MainGame.wallList:
            # 检测每一个子弹是否与子弹碰撞
            if pygame.sprite.collide_rect(wall,self):
                # 碰撞之后，让子弹消失，修改子弹的生存状态
                self.live = False
                # 墙壁的生命值减小
                wall.hp -= 1
                if wall.hp<=0:
                    # 修改墙壁的生存状态
                    wall.live = False



class Wall():
    def __init__(self,left,top):
        # 加载墙壁图片
        self.image = pygame.image.load("img/steels.gif")
        # 获取墙壁的区域
        self.rect = self.image.get_rect()
        # 设置位置
        self.rect.left = left
        self.rect.top = top
        # 是否存活
        self.live = True
        # 设置生命值
        self.hp = 10

    # 展示墙壁的方法
    def displayWall(self):
        MainGame.window.blit(self.image,self.rect)


# 爆炸类
class  Explode():
    def __init__(self,tank):
        # 爆炸的位置由当前子弹打中的坦克位置决定的
        self.rect = tank.rect
        self.images=[
            pygame.image.load("img/blast0.gif"),
            pygame.image.load("img/blast1.gif"),
            pygame.image.load("img/blast2.gif"),
            pygame.image.load("img/blast3.gif"),
            pygame.image.load("img/blast4.gif")
        ]
        self.step = 0
        self.image = self.images[self.step]
        # 是否存活
        self.live = True

    # 展示爆炸效果,由五张图片构成
    def displayExplode(self):
        # 根据索引获取爆炸对象
        if self.step<len(self.images):
            self.image = self.images[self.step]
            self.step += 1
            # 添加到主窗口
            MainGame.window.blit(self.image, self.rect)
        else:
            # 修改已经加载过图片状态
            self.live = False
            self.step = 0


class Music():
    def __init__(self,filename):
        self.filename = filename
        # 加载音乐之前，初始化音乐混合器
        pygame.mixer.init()
        # 加载音乐
        pygame.mixer.music.load(self.filename)

    # 播放音乐
    def playMusic(self):
        pygame.mixer.music.play()


if __name__=="__main__":
    MainGame().startGame()
    # MainGame().getTextSurface()
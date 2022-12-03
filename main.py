import pygame
import time
import random

_display = pygame.display
_image = pygame.image
_sound = pygame.mixer.Sound
_music = pygame.mixer.music
version = "v1.0.2"


class Windows:
    window = None
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600
    COLOR_BLACK = pygame.Color(0, 0, 0)
    COLOR_WHITE = pygame.Color(255, 255, 255)
    COLOR_GREY = pygame.Color(160, 160, 160)

    def endGame(self):
        exit()


class InitGame(Windows):
    def __init__(self):
        _display.init()
        pygame.mixer.init()
        InitGame.window = _display.set_mode([Windows.SCREEN_WIDTH, Windows.SCREEN_HEIGHT])
        self.icon = _image.load('images/thzbc.png')
        self.background = _image.load('images/menu.png')
        _display.set_caption("thzbc " + version)
        _display.set_icon(self.icon)

    def startGame(self):
        while True:
            self.window.blit(self.background, (0, 0))
            self.getEvent()
            _display.update()

    def getEvent(self):
        eventList = pygame.event.get()
        for event in eventList:
            if event.type == pygame.QUIT:
                Windows().endGame()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_z:
                    MainGame.game_over = 0
                    MainGame().startGame()
                if event.key == pygame.K_ESCAPE:
                    Windows().endGame()
                if event.key == pygame.K_F11:
                    InitGame.window = _display.set_mode(([Windows.SCREEN_WIDTH, Windows.SCREEN_HEIGHT]),
                                                        pygame.FULLSCREEN, 32)
            else:
                pass


class MainGame(Windows):
    boom_List = []
    bullet_List = []
    enemy_Bullet_List = []
    enemy_List = []
    explode_List = []
    item_List = []
    cloud_List = []
    baka = None
    game_pause = False
    enemy_init_speed = 1
    enemy_shot_speed = 2
    enemy_status = 2
    game_over = 0
    immune_check = 0
    nowTime = 0

    def __init__(self):
        self.startTimeBullet = time.perf_counter()
        self.startTimeEnemy = time.perf_counter()
        self.startTimeEnemy = time.perf_counter()
        self.startTimeImmune = time.perf_counter()
        self.startTimeCloud = time.perf_counter()
        self.lastMusicTime = time.perf_counter()
        self.score = 0
        pygame.font.init()
        self.score_font = pygame.font.Font('Sansation.ttf', 40)
        self.power_font = pygame.font.Font('Sansation.ttf', 32)
        self.sum = _image.load('images/bg-sum.png')
        self.background = _image.load('images/bg.png')
        self.pause = _image.load('images/pause.png')
        self.boom_cg = _image.load('images/boom_cg.png')
        self.spell_image = _image.load('images/status_spell.png')
        self.player_image = _image.load('images/status_player.png')
        self.background_end = _image.load('images/end.png')
        self.baka = Player(200, 500)
        _music.load('sounds/bgm.mp3')
        _music.play(-1, 0)

    def gameEvent(self):
        eventList = pygame.event.get()
        for event in eventList:
            if event.type == pygame.QUIT:
                Windows().endGame()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_F11:
                    InitGame.window = _display.set_mode(([Windows.SCREEN_WIDTH, Windows.SCREEN_HEIGHT]),
                                                        pygame.FULLSCREEN, 32)
                if event.key == pygame.K_LSHIFT:
                    self.baka.image = self.baka.images['H']
                    self.baka.speed = 3
                if event.key == pygame.K_x and not self.baka.immune:
                    self.boom_init()
                if event.key == pygame.K_LEFT:
                    self.baka.move_left = False
                    self.baka.last_move_left = False
                if event.key == pygame.K_RIGHT:
                    self.baka.move_right = False
                    self.baka.last_move_left = True
                if event.key == pygame.K_UP:
                    self.baka.move_up = False
                    self.baka.last_move_up = False
                if event.key == pygame.K_DOWN:
                    self.baka.move_down = False
                    self.baka.last_move_left = True
                if event.key == pygame.K_z:
                    self.baka.shot = 0
                if event.key == pygame.K_HOME:
                    self.baka.bullet_power = 400
                    self.score = 100000
                    self.enemy_init_speed = 0.30
                if event.key == pygame.K_F7:
                    self.baka.spell = 10
                    self.score = 9000000000
                if event.key == pygame.K_F8:
                    self.baka.play = 10
                    self.score = 9000000000
                if event.key == pygame.K_ESCAPE:
                    s = _sound('sounds/pause.wav')
                    s.play()
                    self.lastMusicTime = time.perf_counter() - self.lastMusicTime
                    _music.stop()
                    self.game_pause = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.baka.move_left = True
                    self.baka.last_move_left = True
                elif event.key == pygame.K_RIGHT:
                    self.baka.move_right = True
                    self.baka.last_move_left = False
                elif event.key == pygame.K_UP:
                    self.baka.move_up = True
                    self.baka.last_move_up = True
                elif event.key == pygame.K_DOWN:
                    self.baka.move_down = True
                    self.baka.last_move_up = False
                elif event.key == pygame.K_z:
                    self.baka.shot = 1
                elif event.key == pygame.K_LSHIFT:
                    self.baka.image = self.baka.images['L']
                    self.baka.speed = 1

    def gamePause(self):
        eventList = pygame.event.get()
        for event in eventList:
            if event.type == pygame.QUIT:
                Windows().endGame()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_z:
                    s = _sound('sounds/continue.wav')
                    s.play()
                    _music.play(-1, self.lastMusicTime)
                    self.game_pause = False
                if event.key == pygame.K_F11:
                    InitGame.window = _display.set_mode(([Windows.SCREEN_WIDTH, Windows.SCREEN_HEIGHT]),
                                                        pygame.FULLSCREEN, 32)

    def checkEnemyInit(self):
        self.nowTime = time.perf_counter()
        if self.nowTime - self.startTimeEnemy >= self.enemy_init_speed:
            self.enemy_init()
            if self.enemy_init_speed >= 0.3:
                self.enemy_init_speed -= 0.0012
            self.startTimeEnemy = self.nowTime
            if self.enemy_status > 100000:
                self.enemy_status = 31
            elif self.score > 50000:
                self.enemy_status = 4
            elif self.score > 15000:
                self.enemy_status = 21
            elif self.score > 5000:
                self.enemy_status = 3

    def checkBulletInit(self):
        if self.nowTime - self.startTimeBullet >= 0.1:
            self.bullet_init()
            self.startTimeBullet = self.nowTime

    def checkBackgroundInit(self):
        InitGame.window.fill(Windows.COLOR_GREY)
        InitGame.window.blit(self.sum, (320, 30))
        if self.startTimeCloud == 0:
            self.startTimeCloud = self.nowTime
        if self.nowTime - self.startTimeCloud >= 4:
            y = random.randint(-20, 65)
            x = random.randint(-10, 350)
            s = 1
            c_type = random.randint(1, 2)
            cloud = BgItems(c_type, y, x, s)
            self.cloud_List.append(cloud)
            self.startTimeCloud = self.nowTime
        for c in self.cloud_List:
            c.move()
            c.display()
            if c.rect.top >= 600:
                self.cloud_List.remove(c)

    def checkExplodeInit(self):
        for exp in self.explode_List:
            exp.display()
            if self.nowTime - exp.explodeInitTime > 0.5:
                self.explode_List.remove(exp)

    def checkImmuneStatus(self):
        if self.baka.immune:
            self.baka.image = self.baka.images['I']
            if not self.immune_check:
                self.startTimeImmune = time.perf_counter()
                self.immune_check = 1
            if self.nowTime - self.startTimeImmune > 3:
                self.baka.immune = False
                self.baka.image = self.baka.images['H']
                self.immune_check = 0

    def game_status_display(self):
        InitGame.window.blit(self.background, (0, 0))
        for i in range(0, self.baka.spell):
            InitGame.window.blit(self.spell_image, (550 + i * 25, 180))
        for i in range(0, self.baka.play):
            InitGame.window.blit(self.player_image, (550 + i * 25, 135))
        score_surface = self.score_font.render(str("{:09d}".format(self.score)), False, (0, 0, 0))
        InitGame.window.blit(score_surface, (520, 80))
        power_surface = self.power_font.render(str("{:03d}".format(self.baka.bullet_power)), False, (0, 0, 0))
        InitGame.window.blit(power_surface, (565, 225))

    def startGame(self):
        while not self.game_over:
            while not self.game_pause and not self.game_over:
                self.checkBackgroundInit()
                self.checkEnemyInit()
                self.checkBulletInit()
                self.checkExplodeInit()
                self.gameEvent()
                self.baka.move()
                self.checkImmuneStatus()
                self.baka.display()
                self.enemy_display()
                self.enemy_bullet_init()
                self.checkItemLine()
                self.bullet_display()
                self.game_status_display()
                _display.update()
                time.sleep(0.005)
            while self.game_pause:
                InitGame.window.blit(self.pause, (0, 0))
                self.gamePause()
                _display.update()
                time.sleep(0.01)
            time.sleep(0.25)
        time.sleep(0.5)
        self.game_end()

    def enemy_init(self):
        left = random.randint(1, 410)
        top = random.randint(1, 50)
        if self.enemy_status < 10:
            e_type = random.randint(1, self.enemy_status)
        elif self.enemy_status < 100:
            e_type = self.enemy_status % 10
            for i in range(self.enemy_status // 10):
                e_type += random.randint(0, 2)
        e = Enemy(left, top, 1, e_type)
        e.hp += self.score // 5000
        MainGame.enemy_List.append(e)

    def enemy_display(self):
        for e in MainGame.enemy_List:
            e.display()
            e.move()
            if hitPlayer(self.baka.rect.center, e.rect.center, 3, e.rect.width / 2, 2):
                self.baka.death()
            if e.hp <= 0:
                self.score += e.score
                exp = Explode(e.rect)
                extra = random.randint(1, 600)
                if extra % 600 == 0:
                    e.item += 1000
                elif extra % 150 == 0:
                    e.item += 100
                self.item_init(e)
                deathSound = random.randint(1, 3)
                if deathSound == 1:
                    s = _sound('sounds/enemy_death01.wav')
                    s.set_volume(0.2)
                    s.play()
                elif deathSound == 2:
                    s = _sound('sounds/enemy_death02.wav')
                    s.set_volume(0.2)
                    s.play()
                elif deathSound == 3:
                    s = _sound('sounds/enemy_death03.wav')
                    s.set_volume(0.2)
                    s.play()
                self.explode_List.append(exp)
                MainGame.enemy_List.remove(e)
            if e.rect.top > 600:
                MainGame.enemy_List.remove(e)

    def checkItemLine(self):
        if self.baka.rect.top < 150:
            for i in self.item_List:
                i.move_top = (self.baka.rect.top - i.rect.top) / 5
                i.move_left = (self.baka.rect.left - i.rect.left) / 5

    def item_init(self, item):
        while item.item >= 1000:
            item.item -= 1000
            i = Item('U', item.rect)
            self.item_List.append(i)
        while item.item >= 100:
            item.item -= 100
            i = Item('B', item.rect)
            self.item_List.append(i)
        while item.item >= 10:
            item.item -= 10
            i = Item('P', item.rect)
            self.item_List.append(i)
        while item.item:
            item.item -= 1
            i = Item('S', item.rect)
            self.item_List.append(i)

    def itemFunction(self, item_type):
        if item_type == 'S':
            self.score += 50 + self.score // 800
        elif item_type == 'P':
            if self.baka.bullet_power < 400:
                self.baka.bullet_power += 1
        elif item_type == 'B':
            self.baka.spell += 1
            s = _sound('sounds/extend.wav')
            s.play()
        elif item_type == 'U':
            s = _sound('sounds/extend.wav')
            s.play()
            self.baka.play += 1

    def bullet_init(self):
        if self.baka.shot == 1:
            if self.baka.bullet_power < 50:
                b = PlayerBullet(self.baka, 1)
                MainGame.bullet_List.append(b)
            elif self.baka.bullet_power < 100:
                for i in range(6, 8):
                    b = PlayerBullet(self.baka, i)
                    MainGame.bullet_List.append(b)
            elif self.baka.bullet_power < 150:
                for i in range(1, 4):
                    b = PlayerBullet(self.baka, i)
                    MainGame.bullet_List.append(b)
            elif self.baka.bullet_power < 300:
                for i in range(1, 6):
                    b = PlayerBullet(self.baka, i)
                    MainGame.bullet_List.append(b)
            else:
                for i in range(1, 8):
                    b = PlayerBullet(self.baka, i)
                    MainGame.bullet_List.append(b)

    def bullet_display(self):
        for b in MainGame.bullet_List:
            b.display()
            b.move()
            b.hitEnemy()
            if b.live == 'F':
                self.score += 1
                MainGame.bullet_List.remove(b)
                continue
            if b.rect.top < 0 or b.rect.left < 0 or b.rect.left > 450:
                MainGame.bullet_List.remove(b)
        for b in MainGame.enemy_Bullet_List:
            b.display()
            b.move()
            if hitPlayer(self.baka.rect.center, b.rect.center, 3, b.rect.width / 2, 0.5):
                self.baka.death()
            if b.live == 'F' or b.rect.top < 0 or b.rect.top > 600 or b.rect.left < 0 or b.rect.left > 450:
                MainGame.enemy_Bullet_List.remove(b)
        for b in MainGame.boom_List:
            b.display()
            b.move()
            b.hitEnemy()
            if b.rect.top < -90 or b.rect.left < -90 or b.rect.left > 540:
                MainGame.boom_List.remove(b)
        for i in MainGame.item_List:
            i.display()
            i.move()
            i.playerGet(self.baka, i)
            if not i.live or i.rect.top > 610:
                self.itemFunction(i.type)
                MainGame.item_List.remove(i)
        if len(MainGame.boom_List) >= 4:
            self.display_cg()

    def enemy_bullet_init(self):
        for e in self.enemy_List:
            if self.nowTime - e.initTime > e.shot_speed:
                e.initTime = self.nowTime
                if e.type < 3:
                    left = random.randint(-2, 2)
                    top = random.randint(2, 3)
                else:
                    left = random.randint(-3, 3)
                    top = 2
                b = EnemyBullet(e.type, e.rect, left, top)
                MainGame.enemy_Bullet_List.append(b)

    def boom_init(self):
        if not self.baka.spell:
            s = _sound('sounds/spell_invalid.wav')
            s.play()
            return
        self.baka.spell -= 1
        self.baka.immune = True
        for i in self.item_List:
            i.move_top = (self.baka.rect.top - i.rect.top) / 5
            i.move_left = (self.baka.rect.left - i.rect.left) / 5
        left = [2, -2, -1, 1, -2]
        top = [-3, -3, -4, -4, -3]
        for i in range(-1, 4):
            b = Boom(left[i], top[i], self.baka.rect)
            s = _sound('sounds/boom.wav')
            s.play()
            self.boom_List.append(b)

    def display_cg(self):
        InitGame.window.blit(self.boom_cg, (0, 330))

    def game_end(self):
        _music.stop()
        InitGame.window.blit(self.background_end, (0, 0))
        self.bullet_List.clear()
        self.enemy_List.clear()
        self.enemy_Bullet_List.clear()
        self.boom_List.clear()
        self.item_List.clear()
        score_surface = self.score_font.render(str("{:09d}".format(self.score)), False, (0, 0, 0))
        InitGame.window.blit(score_surface, (280, 280))
        self.score = 0
        time.sleep(0.1)
        _display.update()
        while self.game_over:
            self.score = 0
            eventList = pygame.event.get()
            for event in eventList:
                if event.type == pygame.QUIT:
                    Windows().endGame()
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_ESCAPE:
                        self.game_over = 0


class Base(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite().__init__()
        self.live = 'T'


class Object(Base):
    def __init__(self):
        super().__init__()
        self.boom = _image.load('images/explode.png')

    def display(self):
        InitGame.window.blit(self.image, self.rect)


class Player(Object):
    bullet_power = 0
    postion = (500, 200)
    shot = 0
    speed_left = 0
    speed_top = 0

    def __init__(self, left, top):
        super().__init__()
        self.images = {
            'H': _image.load('images/player.png'),
            'L': _image.load('images/player-shift.png'),
            'I': _image.load('images/player-immune.png')
        }
        self.image = self.images['H']
        self.immune = False
        self.rect = self.image.get_rect()
        self.rect.left = left
        self.rect.top = top
        self.move_left = False
        self.move_right = False
        self.move_up = False
        self.move_down = False
        self.last_move_left = False
        self.last_move_up = False
        self.spell = 3
        self.speed = 3
        self.play = 2

    def move(self):
        if self.move_left and self.last_move_left:
            self.speed_left = -self.speed
        if self.move_right and not self.last_move_left:
            self.speed_left = self.speed
        if self.move_up and self.last_move_up:
            self.speed_top = -self.speed
        if self.move_down and not self.last_move_up:
            self.speed_top = self.speed
        if not self.move_left and not self.move_right:
            self.speed_left = 0
        if not self.move_up and not self.move_down:
            self.speed_top = 0
        self.rect.top += self.speed_top
        self.rect.left += self.speed_left
        if self.rect.left < 3:
            self.rect.left = 0
        if self.rect.left > 400:
            self.rect.left = 400
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.top > 547:
            self.rect.top = 547

    def death(self):
        if self.immune:
            return
        deathTime = time.perf_counter()
        startTime = time.perf_counter()
        s = _sound('sounds/death.wav')
        s.play()
        while deathTime - startTime <= 0.3 and not self.immune:
            deathTime = time.perf_counter()
            eventList = pygame.event.get()
            for event in eventList:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_x and self.spell:
                        self.spell -= 1
                        left = [2, -2, -1, 1, -2]
                        top = [-3, -3, -4, -4, -3]
                        for i in range(-1, 4):
                            b = Boom(left[i], top[i], self.rect)
                            MainGame.boom_List.append(b)
                            self.immune = True
        if self.immune:
            return
        MainGame.enemy_Bullet_List.clear()
        self.play -= 1
        if self.play != -1:
            self.rect.left = 200
            self.rect.top = 500
            self.spell = 3
            self.speed = 3
            self.bullet_power = self.bullet_power * 2 // 3
            self.immune = True
            self.move_left = False
            self.move_right = False
            self.move_up = False
            self.move_down = False
        if self.play == -1:
            MainGame.game_over = 1


class Enemy(Object):
    def __init__(self, left, top, speed, enemy_type):
        super().__init__()
        self.initTime = time.perf_counter()
        self.images = {
            1: _image.load('images/enemy-red.png'),
            2: _image.load('images/enemy-blue.png'),
            3: _image.load('images/enemy-black.png'),
            4: _image.load('images/enemy-cute.png'),
            5: _image.load('images/enemy-cute.png'),
        }
        self.type = enemy_type
        self.health = [1, 12, 12, 36, 36, 72]
        self.shot_speed_type = [10000, 2, 2, 0.8, 0.5, 0.5]
        self.score_type = [0, 15, 15, 30, 60, 200]
        self.item_type = [10000, 10, 1, 11, 22, 16]
        self.score = self.score_type[enemy_type]
        self.image = self.images[enemy_type]
        self.hp = self.health[enemy_type]
        self.item = self.item_type[enemy_type]
        self.shot_speed = self.shot_speed_type[enemy_type]
        self.rect = self.image.get_rect()
        self.rect.left = left
        self.rect.top = top
        self.speed = speed

    def move(self):
        self.rect.top += self.speed


class Bullet(Base):
    def __init__(self):
        super().__init__()

    def display(self):
        InitGame.window.blit(self.image, self.rect)

    def move(self):
        self.rect.left += self.move_left
        self.rect.top += self.move_top


class PlayerBullet(Bullet):
    def __init__(self, objects, bullet_type):
        super().__init__()
        self.image = _image.load('images/baka-bullet.png')
        self.rect = self.image.get_rect()
        self.bullet_rect = 'P'
        self.rect.left = objects.rect.left + objects.rect.width / 2 - self.rect.width / 2
        self.rect.top = objects.rect.top - self.rect.top
        left = [0, 0, 2, -2, 4, -4, 1, -1]
        top = [0, -9, -8, -8, -7, -7, -9, -9]
        self.move_top = top[bullet_type]
        self.move_left = left[bullet_type]

    def hitEnemy(self):
        for e in MainGame.enemy_List:
            if pygame.sprite.collide_rect(e, self):
                e.hp -= 2
                self.live = 'F'


def hitPlayer(player_pos, bullet_pos, p_r, b_r, hit_pos):
    # (player_radius;bullet_radius)
    # the bigger hit_pos the easier to get
    px = player_pos[0]
    py = player_pos[1] + 15
    bx = bullet_pos[0]
    by = bullet_pos[1] - 1
    return (px - bx) * (px - bx) + (py - by) * (py - by) < (p_r + b_r) * (p_r + b_r) * hit_pos


class EnemyBullet(Bullet):
    def __init__(self, object_type, object_rect, left, top):
        super().__init__()
        self.images = {
            1: _image.load('images/enemy-bullet-red.png'),
            2: _image.load('images/enemy-bullet-blue.png'),
            3: _image.load('images/enemy-bullet-black.png'),
            4: _image.load('images/enemy-bullet-white.png'),
            5: _image.load('images/enemy-bullet-white.png'),
        }
        self.image = self.images[object_type]
        self.rect = self.image.get_rect()
        self.move_left = left
        self.move_top = top
        self.rect.left = object_rect.left + object_rect.width / 2 - self.rect.width / 2
        self.rect.top = object_rect.top + object_rect.height


class Boom(Bullet):
    def __init__(self, left, top, start_rect):
        self.image = _image.load('images/boom.png')
        self.rect = self.image.get_rect()
        self.rect.left = start_rect.left
        self.rect.top = start_rect.top
        self.move_left = left
        self.move_top = top

    def hitEnemy(self):
        for e in MainGame.enemy_List:
            if pygame.sprite.collide_rect(e, self):
                e.hp = 0
        for b in MainGame.enemy_Bullet_List:
            if pygame.sprite.collide_rect(b, self):
                b.live = 'F'


class Explode:
    def __init__(self, object_rect):
        self.image = _image.load('images/explode.png')
        self.explodeInitTime = time.perf_counter()
        self.rect = self.image.get_rect()
        self.rect.left = object_rect.left
        self.rect.top = object_rect.top

    def display(self):
        InitGame.window.blit(self.image, self.rect)


class Item(EnemyBullet):
    def __init__(self, e_type, rect):
        self.images = {
            'P': _image.load('images/item-power.png'),
            'S': _image.load('images/item-point.png'),
            'U': _image.load('images/item-up.png'),
            'B': _image.load('images/item-boom.png')
        }
        self.live = True
        self.type = e_type
        self.image = self.images[e_type]
        self.rect = self.image.get_rect()
        self.move_left = 0
        self.move_top = 1
        self.rect.left = rect.left + random.randint(-25, 25)
        self.rect.top = rect.top

    def playerGet(self, player, item):
        if hitPlayer(player.rect.center, item.rect.center, player.rect.width / 2, item.rect.width / 2, 2):
            self.live = False
            return
        if hitPlayer(player.rect.center, item.rect.center, player.rect.width/2, item.rect.width/2, 5):
            item.move_top = (player.rect.top - item.rect.top)/5
            item.move_left = (player.rect.left - item.rect.left)/5


class BgItems(Bullet):
    def __init__(self, item_type, top, left, speed):
        self.items = {1: _image.load('images/bg-cloud-1.png'),
                      2: _image.load('images/bg-cloud-2.png')}
        self.image = self.items[item_type]
        self.rect = self.image.get_rect()
        self.rect.top = top
        self.rect.left = left
        self.move_top = speed
        self.move_left = 0


InitGame().startGame()

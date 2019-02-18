import sys
import time
import pygame


width = 640
height = 480
color_blue = (0,0,64)
color_white = (255,255,255)

pygame.init()

class scene:
    def __init__(self):
        self.nextScene = False
        self.playing = True

    def read_event(self, event):
        pass

    def update(self):
        pass

    def paint(self, display):
        pass

    def change_scene(self, scene):
        self.nextScene = scene

class Pellet(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("img/pellet.png")
        self.rect = self.image.get_rect()
        self.rect.center = (width / 2, height / 2)
        self.speed = [3, 3]

    def update(self):
        if self.rect.top <= 0:
            self.speed[1] = -self.speed[1]
        elif self.rect.right >= width or self.rect.left <= 0:
            self.speed[0] = -self.speed[0]
        self.rect.move_ip(self.speed)

class Palette(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("img/palette.png")
        self.rect = self.image.get_rect()
        self.rect.midbottom = (width / 2, height - 20)
        self.speed = [0, 0]

    def update(self, event):
        if event.key == pygame.K_LEFT and self.rect.left > 0:
            self.speed = [-8, 0]
        elif event.key == pygame.K_RIGHT and self.rect.right < width:
            self.speed = [8, 0]
        else:
            self.speed = [0, 0]
        self.rect.move_ip(self.speed)

class Brick(pygame.sprite.Sprite):
    def __init__(self, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("img/brick.png")
        self.rect = self.image.get_rect()
        self.rect.topleft = position

class Wall(pygame.sprite.Group):
    def __init__(self, cantBricks):
        pygame.sprite.Group.__init__(self)

        pos_x = 0
        pos_y = 20
        for i in range(cantBricks):
            brick = Brick((pos_x, pos_y))
            self.add(brick)
            pos_x += brick.rect.width
            if pos_x >= width:
                pos_x = 0
                pos_y += brick.rect.height

def game_over():
    fonts = pygame.font.SysFont('Arial', 72)
    text = fonts.render('Game over', True, color_white)
    text_rect = text.get_rect()
    text_rect.center = [width / 2, height / 2]
    display.blit(text, text_rect)
    pygame.display.flip()
    time.sleep(3)
    sys.exit()

def Punctuation():
    fonts = pygame.font.SysFont('Consolas', 20)
    text = fonts.render(str(punctuation).zfill(5), True, color_white)
    text_rect = text.get_rect()
    text_rect.topleft = [0, 0]
    display.blit(text, text_rect)

def Lives():
    fonts = pygame.font.SysFont('Consolas', 20)
    string_text = "Lives: " + str(lives).zfill(2)
    text = fonts.render(string_text, True, color_white)
    text_rect = text.get_rect()
    text_rect.topright = [width, 0]
    display.blit(text, text_rect)

display = pygame.display.set_mode((width, height))
pygame.display.set_caption("Game of Brick")
reloj = pygame.time.Clock()
pygame.key.set_repeat(30)

pellet = Pellet()
gamer = Palette()
wall = Wall(200)
punctuation = 0
lives = 3
waiting = True

while True:
    reloj.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            gamer.update(event)
            if waiting == True and event.key == pygame.K_SPACE:
                waiting = False
                if pellet.rect.centerx < width / 2:
                    pellet.speed = [3, -3]
                else:
                    pellet.speed = [-3, -3] 
    
    if waiting == False:
        pellet.update()
    else:
        pellet.rect.midbottom = gamer.rect.midtop

    if pygame.sprite.collide_rect(pellet, gamer):
        pellet.speed[1] = -pellet.speed[1]

    lista = pygame.sprite.spritecollide(pellet, wall, False)
    if lista:
        brick = lista[0]
        cx = brick.rect.centerx
        if cx < brick.rect.left or cx > brick.rect.right:
            pellet.speed[0] = -pellet.speed[0]
        else:
            pellet.speed[1] = -pellet.speed[1]
        wall.remove(brick)
        punctuation += 10
    
    if pellet.rect.bottom > height:
        lives -= 1
        waiting = True

    display.fill(color_blue)
    Punctuation()
    Lives()
    display.blit(pellet.image, pellet.rect)
    display.blit(gamer.image, gamer.rect)
    wall.draw(display)
    pygame.display.flip()

    if lives <= 0:
            game_over()

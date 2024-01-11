import pygame
import random
import os
import sys

from pygame.time import delay

text = "Level: 1"
counter = 0
HP = 50
level = 1

WIDTH = 400
HEIGHT = 650
FPS = 30

# Giving values to base colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Creating a game window
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My Game")
clock = pygame.time.Clock()

# Setting up a folder with textures
game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, 'img')
player_img = pygame.image.load(os.path.join(
    img_folder, 'playerShip3_blue.png')).convert()
rock_img = pygame.image.load(os.path.join(
    img_folder, 'meteorGrey_med1.png')).convert()
laser_img = pygame.image.load(os.path.join(
    img_folder, 'laserBlue03.png')).convert()
background = pygame.image.load(os.path.join(
    img_folder, 'darkPurple.png')).convert()
background_rect = background.get_rect()
hp_img = pygame.image.load(os.path.join(
    img_folder, 'hp.png')).convert()
Game_over_1_img = pygame.image.load(os.path.join(
    img_folder, 'Game_over_1.png')).convert()
Game_over_2_img = pygame.image.load(os.path.join(
    img_folder, 'Game_over_2.png')).convert()


# Setting up a folder with sounds
snd_dir = os.path.join(os.path.dirname(__file__), 'snd')
shoot_sound = pygame.mixer.Sound(os.path.join(snd_dir, 'pew.wav'))
expl_sounds = []
for snd in ['expl3.wav', 'expl6.wav']:
    expl_sounds.append(pygame.mixer.Sound(os.path.join(snd_dir, snd)))
pygame.mixer.music.load(os.path.join(snd_dir, 'Mars.wav'))
pygame.mixer.music.set_volume(0.4)


# Explosion animation setup
explosion_anim = {}
explosion_anim['lg'] = []
explosion_anim['sm'] = []
for i in range(9):
    filename = 'regularExplosion0{}.png'.format(i)
    img = pygame.image.load(os.path.join(img_folder, filename)).convert()
    img.set_colorkey(BLACK)
    img_sm = pygame.transform.scale(img, (42, 42))
    explosion_anim['sm'].append(img_sm)


# Player sprite setup
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = player_img
        self.image = pygame.transform.scale(player_img, (60, 48))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = 21
        self.rect.center = (WIDTH / 2, HEIGHT / 2)

    def update(self):   # Setting up Player sprite movements
        self.speedx = 0
        self.speedy = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speedx = -8
        if keystate[pygame.K_RIGHT]:
            self.speedx = 8
        if keystate[pygame.K_UP]:
            self.speedy = -8
        if keystate[pygame.K_DOWN]:
            self.speedy = 8
        if self.rect.left > WIDTH:  # Endless field
            self.rect.right = 0
        if self.rect.right < 0:
            self.rect.left = WIDTH
        if self.rect.top > HEIGHT:
            self.rect.top = HEIGHT
        if self.rect.bottom < 0:
            self.rect.bottom = 0
        self.rect.x += self.speedx
        self.rect.y += self.speedy

    def shoot(self):    # Setting up the shooting of Player sprite
        bullet = Bullet()
        shoot_sound.play()
        bullet.rect.center = (self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)


# Explosion sprite setup
class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = explosion_anim[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(explosion_anim[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = explosion_anim[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center


# Bullets sprite setup
class Bullet(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = laser_img
        self.image = pygame.transform.scale(laser_img, (6, 30))
        self.rect = self.image.get_rect()
        self.image.set_colorkey(BLACK)
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -18

    def update(self):
        self.rect.y += self.speedy
        keystate = pygame.key.get_pressed()
        if self.rect.bottom < 0:
            self.kill()


# Hp sprite setup
class Hp(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = hp_img
        self.rect = self.image.get_rect()
        self.image.set_colorkey(BLACK)
        self.rect.center = (10, 52)

    def update(self):
        self.rect.center = (HP * 1.5 - 100, 52)


# Asteroids sprite setup
class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = rock_img
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * 0.95 / 2)
        self.image.set_colorkey(BLACK)
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(4, 8)
        self.speedx = random.randrange(-2, 2)

    def update(self):   # Levels and speed setup
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.top > HEIGHT + 10 or self.rect.left < -40 or self.rect.right > WIDTH + 40:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            if level == 1:
                self.speedy = random.randrange(5, 12)
                self.speedx = random.randrange(-3, 3)
            elif level == 2:
                self.speedy = random.randrange(7,  15)
                self.speedx = random.randrange(-3, 3)
            elif level == 3:
                self.speedy = random.randrange(9,  17)
                self.speedx = random.randrange(-3, 3)
            elif level == 4:
                self.speedy = random.randrange(9,  21)
                self.speedx = random.randrange(-3, 3)
            elif level == 5:
                self.speedy = random.randrange(11,  23)
                self.speedx = random.randrange(-3, 3)


# Game_over_1 sprite setup
class Game_over1(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = Game_over_1_img
        self.image = pygame.transform.scale(Game_over_1_img, (450, 100))
        self.rect = self.image.get_rect()
        self.image.set_colorkey(BLACK)
        self.rect.center = (WIDTH + 250, HEIGHT / 2 - 50)
        self.speedx = 0

    def update(self):
        self.rect.x += self.speedx
        if counter > 0:
            self.speedx = -counter * 2
            if self.rect.left < 0:
                self.speedx = 0


# Game_over_2 sprite setup
class Game_over2(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = Game_over_2_img
        self.image = pygame.transform.scale(Game_over_2_img, (450, 100))
        self.rect = self.image.get_rect()
        self.image.set_colorkey(BLACK)
        self.rect.center = (150 - WIDTH, HEIGHT / 2 + 50)
        self.speedx = 0

    def update(self):
        self.rect.x += self.speedx
        if counter > 0:
            self.speedx = counter * 2
            if self.rect.right > WIDTH:
                self.speedx = 0


# Customize text
font_name = pygame.font.match_font('arial')


# Drawing text
def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, 20)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


# Adding a sprites to group All sprites
all_sprites = pygame.sprite.Group()
hps = Hp()
all_sprites.add(hps)
mobs = pygame.sprite.Group()
bullets = pygame.sprite.Group()
player = Player()
all_sprites.add(player)
for i in range(12):  # Number of asteroids
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)
Game_over_1 = Game_over1()
all_sprites.add(Game_over_1)
Game_over_2 = Game_over2()
all_sprites.add(Game_over_2)
score = 0

x = WIDTH // 2
y = HEIGHT // 2

pygame.mixer.music.play(loops=-1)

# Game loop
running = True
while running:
    clock.tick(FPS)     # Keeping the loop at the correct speed
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # check for closing window
            text = "Game over"
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()
    if score > 20 and score <= 40:  # Conditions for moving to the next level
        text = "Level: 2"
        level = 2
    elif score > 40 and score <= 60:
        text = "Level: 3"
        level = 3
    elif score > 60 and score <= 80:
        text = "Level: 4"
        level = 4
    elif score > 80:
        text = "Level: 5 (MAX)"
        level = 5
    if HP <= 0:
        counter += 1
        text = "Game over"
        if counter >= 90:
            running = False

    # Update
    all_sprites.update()
    hits = pygame.sprite.spritecollide(
        player, mobs, False, pygame.sprite.collide_circle)  # Collision check
    if hits:
        HP -= 1
        expl = Explosion(player.rect.center, 'sm')
        random.choice(expl_sounds).play()
        all_sprites.add(expl)
    hits = pygame.sprite.groupcollide(mobs, bullets, True, True)
    for hit in hits:
        score += 1
        m = Mob()
        all_sprites.add(m)
        expl = Explosion(hit.rect.center, 'sm')
        random.choice(expl_sounds).play()
        all_sprites.add(expl)
        mobs.add(m)

    # Rendering
    screen.fill(BLACK)
    screen.blit(background, background_rect)
    all_sprites.draw(screen)
    draw_text(screen, str("Score: "), 18, WIDTH / 2 - 3, 10)
    draw_text(screen, str(score), 18, WIDTH / 2 + 30, 10)
    draw_text(screen, str(text), 18, WIDTH / 2, 40)
    draw_text(screen, str("HP"), 18, 20, 10)
    draw_text(screen, str(HP), 18, 20, 40)
    pygame.display.flip()

pygame.quit()

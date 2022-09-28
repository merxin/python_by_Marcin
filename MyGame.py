import pygame
from sys import exit
import random

random.seed()
pygame.init()
W = 800
H = 600
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption('Dwarf')
FPS = 60
start_time = int(pygame.time.get_ticks() / 1000)
current_time = int(pygame.time.get_ticks() / 1000) - start_time
grass = pygame.image.load('imgs/grass.jpg').convert_alpha()
background = pygame.transform.scale(grass, (W, H))
player_pic = pygame.image.load('imgs/dwarf.jpg').convert_alpha()
run = True
gamefont = pygame.font.Font(None, 50)
gamefont2 = pygame.font.Font(None, 30)
text_surface = gamefont.render(f'Dwarf GAME', False, 'Black')
ready_surface = gamefont2.render(f'READY? - catch  chickens but beware of the dogs...', False, 'Orange')
ready_surface2 = gamefont2.render(f' w-up, a - left, s- down, d - right   click to start ?', False, 'Orange')
gameover_txt = gamefont.render("GAME OVER", True, ('Black'))


class Game:

    def __init__(self, level=1):
        self.level = level
        self.state = 'intro'

    # intro screen
    def intro(self):
        chicken.empty()
        player.empty()
        dog.empty()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:

                for i in range(game.level + 2):
                    chicken.add(Creature())
                for i in range(game.level + game.level // 3):
                    dog.add(Opponent())
                player.add(Player())
                self.state = 'main_game'

            screen.blit(background, (0, 0))
            screen.blit(ready_surface, (5, 300))
            screen.blit(ready_surface2, (5, 330))
            game.display_score()
            player.draw(screen)
            pygame.display.update()

    # main game
    def main_game(self):

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if collision_dog() == True:
                self.state = 'game_over'
            screen.blit(background, (0, 0))
            screen.blit(text_surface, (500, 10))
            player.draw(screen)
            player.update()
            chicken.draw(screen)
            chicken.update()
            dog.draw(screen)
            dog.update()
            collision_catch()
            game.display_score()
            pygame.display.update()
            if len(chicken) == 0:
                self.level += 1
                self.state = 'intro'


    # game over screen
    def game_over(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            screen.blit(background, (0, 0))
            screen.blit(text_surface, (500, 10))
            screen.blit(gameover_txt, (300, 300))
            pygame.display.update()
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.state = 'intro'
                self.level -= self.level - 1

    # managing game status
    def level_manager(self):
        if self.state == 'intro':
            self.intro()
        if self.state == 'main_game':
            self.main_game()
        if self.state == 'game_over':
            self.game_over()

    def display_score(self):
        current_time = int(pygame.time.get_ticks() / 1000) - start_time
        self.points = len(chicken)
        self.score_surf = gamefont.render(f'Chickens:{self.points}, Time:{current_time}', False, (40, 40, 40))
        self.score_rect = self.score_surf.get_rect(center=(300, 50))
        screen.blit(self.score_surf, self.score_rect)
        self.level_text = gamefont.render(f"Level{self.level}", 1, (255, 255, 255))
        screen.blit(self.level_text, (10, H - 50))


game = Game()


class Player(pygame.sprite.Sprite):
    start_pos = (300, 100)

    def __init__(self):
        super().__init__()
        self.start_pos = (300, 100)
        self.image = pygame.image.load('imgs/dwarf.jpg').convert_alpha()
        self.rect = player_pic.get_rect()
        self.rect.x, self.rect.y = self.start_pos
        self.speed = 3

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and self.rect.left >= 0:
            self.rect.x -= self.speed
        if keys[pygame.K_d] and self.rect.right <= W:
            self.rect.x += self.speed
        if keys[pygame.K_w] and self.rect.top >= 0:
            self.rect.y -= self.speed
        if keys[pygame.K_s] and self.rect.bottom <= H:
            self.rect.y += self.speed


class Creature(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('imgs/chicken.jpg').convert_alpha()
        self.rect = self.image.get_rect(midbottom=(300, 410))
        self.rect.x = random.randint(W / 2, W)
        self.rect.y = random.randint(H / 2, H)
        self.directionx = random.randint(1, 3) * 0.51
        self.directiony = random.randint(1, 3) * 0.51

    def update(self, speed=2.4):
        self.speed = speed
        self.rect.x += self.speed * self.directionx
        self.rect.y += self.speed * self.directiony
        if self.rect.y >= H - 15 or self.rect.x >= W - 15 or self.rect.y <= H - H + 10 or self.rect.x <= W - W + 10:
            if self.rect.y >= H - 20 or self.rect.y <= H - H:
                self.directiony = -self.directiony
            if self.rect.x >= W - 20 or self.rect.x <= W - W:
                self.directionx = -self.directionx


class Opponent(Creature):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('imgs/dog.jfif').convert_alpha()
        self.rect = self.image.get_rect(midbottom=(self.rect.x, self.rect.y))
        self.rect.x = random.randint(W / 2, W)
        self.rect.y = random.randint(H / 2, H)
        self.directionx = random.randint(1, 3) * 0.51
        self.directiony = random.randint(1, 3) * 0.51

    def update(self, speed=2.6):
        self.speed = speed
        self.rect.x += self.speed * self.directionx
        self.rect.y += self.speed * self.directiony
        if self.rect.y >= H - 15 or self.rect.x >= W - 15 or self.rect.y <= H - H + 10 or self.rect.x <= W - W + 10:
            if self.rect.y >= H - 20 or self.rect.y <= H - H:
                self.directiony = -self.directiony
            if self.rect.x >= W - 20 or self.rect.x <= W - W:
                self.directionx = -self.directionx


player = pygame.sprite.GroupSingle()
player.add(Player())
chicken = pygame.sprite.Group()
dog = pygame.sprite.Group()


# catchig chicken
def collision_catch():
    if pygame.sprite.spritecollide(player.sprite, chicken, True):
        return True
    else:
        return False


# collision with dog
def collision_dog():
    if pygame.sprite.spritecollide(player.sprite, dog, True):
        return True
    else:
        return False


while run:
    game.level_manager()

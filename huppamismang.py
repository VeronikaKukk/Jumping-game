import pygame
from sys import exit
import os
from random import randint, choice
#tutorial that I used https://www.youtube.com/watch?v=AY9MnQ4x3zk

class Hiir(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        hiir_walk1 = pygame.image.load(os.path.join("hiir1.png")).convert_alpha()
        hiir_walk2 = pygame.image.load(os.path.join("hiir2.png")).convert_alpha()
        self.hiir_walk = [hiir_walk1, hiir_walk2]
        self.hiir_index = 0
        self.hiir_jump = pygame.image.load(os.path.join("hiir3.png")).convert_alpha()
        
        self.image = self.hiir_walk[self.hiir_index]
        self.rect = self.image.get_rect(midbottom=(100,295))
        self.gravity = 0
        
        self.jump_sound = pygame.mixer.Sound(os.path.join("jump.mp3"))
        self.jump_sound.set_volume(0.4)
    def hiir_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >=295:
            self.gravity = -22
            self.jump_sound.play()
    
    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 295:
            self.rect.bottom = 295
    
    def animation_state(self):
        if self.rect.bottom < 295:
            self.image = self.hiir_jump
        else:
            self.hiir_index += 0.1
            if self.hiir_index >= len(self.hiir_walk):
                self.hiir_index = 0
            self.image = self.hiir_walk[int(self.hiir_index)]
    
    def update(self):
        self.hiir_input()
        self.apply_gravity()
        self.animation_state()

class Enemy(pygame.sprite.Sprite):
    def __init__(self,type):
        super().__init__()
        
        if type == 'kass':
            kass_frame1 = pygame.image.load(os.path.join("kass1.png")).convert_alpha()
            kass_frame2 = pygame.image.load(os.path.join("kass2.png")).convert_alpha()
            self.frames = [kass_frame1,kass_frame2]
            y_pos = 295
        else:
            tuulelohe_frame1 = pygame.image.load(os.path.join("tuulelohe.png")).convert_alpha()
            tuulelohe_frame2 = pygame.image.load(os.path.join("tuulelohe2.png")).convert_alpha()
            self.frames=[tuulelohe_frame1,tuulelohe_frame2]
            y_pos = randint(100,200)
        
        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom=(randint(900,1100),y_pos))
    
    def animation_state(self):
        self.animation_index += 0.1
        if self.animation_index >= len(self.frames):
            self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]
    
    def update(self):
        self.animation_state()
        self.rect.x -= 5
        self.destroy()
    
    def destroy(self):
        if self.rect.x <= -100:
            self.kill()

def display_score():
    current_time = int(pygame.time.get_ticks()/1000) -start_time
    score_surface = font.render("Score: "+str(current_time),False,(64,64,64))
    score_rect = score_surface.get_rect(center=(400,50))
    screen.blit(score_surface,score_rect)
    return current_time

def collision_sprite():
    if pygame.sprite.spritecollide(hiir.sprite,enemy_group,False):
        enemy_group.empty()
        return False
    else:
        return True

pygame.init()
pygame.display.set_caption("Jumping game")
clock = pygame.time.Clock()
width = 800
height = 400
screen = pygame.display.set_mode((width,height))
font = pygame.font.Font('yoster.ttf',30)
game_active = False
start_time = 0
score = 0

#groups
hiir = pygame.sprite.GroupSingle()
hiir.add(Hiir())

enemy_group = pygame.sprite.Group()

#background
sky_surface = pygame.image.load(os.path.join("taust.png")).convert()

#intro screen
intro_hiir = pygame.image.load(os.path.join("hiir1.png")).convert_alpha()
intro_surface = pygame.transform.scale2x(intro_hiir)
intro_rect = intro_surface.get_rect(center=(400,200))

game_name = font.render('Jumping game', False,(64,64,64))
game_name_rect = game_name.get_rect(center=(400,130))

game_message = font.render('Press space to start',False,(64,64,64))
game_message_rect = game_message.get_rect(center=(400,270))

#timer
enemy_timer = pygame.USEREVENT + 1
pygame.time.set_timer(enemy_timer,1400)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if game_active:
            if event.type == enemy_timer:
                enemy_group.add(Enemy(choice(['kass','tuulelohe','kass'])))
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                start_time = int(pygame.time.get_ticks()/1000)
    
    if game_active:
        screen.blit(sky_surface,(0,0))
        score = display_score()
        
        hiir.draw(screen)
        hiir.update()
        
        enemy_group.draw(screen)
        enemy_group.update()
        
        game_active = collision_sprite()
        
    else:
        screen.fill((135,206,250))
        screen.blit(intro_surface,intro_rect)
        
        score_message = font.render('Your score: '+str(score),False,(64,64,64))
        score_message_rect = score_message.get_rect(center=(400,270))
        screen.blit(game_name,game_name_rect)
        
        if score == 0:
            screen.blit(game_message,game_message_rect)
        else:
            screen.blit(score_message,score_message_rect)
    
    pygame.display.update()
    clock.tick(60)
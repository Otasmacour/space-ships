from random import randint
import pygame
from pygame.locals import *
import os
pygame.mixer.init()
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)

width, height = 900, 500
win = pygame.display.set_mode((width,height))
pygame.display.set_caption("lodě")

border_width = 10
border = pygame.Rect(width//2 -5, 0, border_width, height)

bullet_hit_sound = pygame.mixer.Sound(os.path.join("Assets","bullet hit.mp3"))
bullet_fire_sound = pygame.mixer.Sound(os.path.join("Assets","bullet fire.mp3"))
collect_sound = pygame.mixer.Sound(os.path.join("Assets","collect.mp3"))
bullet_fire_sound.set_volume(0.2)
collect_sound.set_volume(0.3)
fps = 60
velocity = 5
bullet_velocity = 7
max_bullets = 5
healt_adding = 3
spaceship_width, spaceship_height = 55,40

bonus_number = 0
x = 0
y = 0

red_health_points = 10
blue_health_points = 10

blue_hit = pygame.USEREVENT + 1
red_hit = pygame.USEREVENT + 2

left_white_bar = pygame.Rect(10,10,100,20)
right_white_bar = pygame.Rect(790,10,100,20)

bonus_image = pygame.image.load(
    os.path.join("Assets","bonus.png"))
blue_spaceship_image = pygame.image.load(
    os.path.join("Assets","spaceship_blue.png"))
blue_spaceship = pygame.transform.rotate(pygame.transform.scale(
    blue_spaceship_image, (spaceship_width, spaceship_height)),90)

red_spaceship_image = pygame.image.load(
    os.path.join("Assets","spaceship_red.png"))
red_spaceship = pygame.transform.rotate(pygame.transform.scale(
    red_spaceship_image, (spaceship_width, spaceship_height)),270)

background = pygame.transform.scale(pygame.image.load(
    os.path.join("Assets","space.jpg")),(width,height))

healthbar_image = pygame.image.load(os.path.join("Assets","bonus.png"))
healthbar = pygame.transform.scale(healthbar_image,(80,80))

def handle_bullets(blue_bullets,red_bullets,blue,red):
    for bullet in blue_bullets:
        bullet.x += bullet_velocity
        if red.colliderect(bullet): 
            pygame.event.post(pygame.event.Event(red_hit))
            blue_bullets.remove(bullet) 
            bullet_hit_sound.play()
        elif bullet.x > width: #when bullet is out off screen
            blue_bullets.remove(bullet)
        
    for bullet in red_bullets:
        bullet.x -= bullet_velocity
        if blue.colliderect(bullet):
            pygame.event.post(pygame.event.Event(blue_hit ))
            red_bullets.remove(bullet)
            bullet_hit_sound.play()
        elif bullet.x < 0:
            red_bullets.remove(bullet)
    #bullet colision
    for red_bullet in red_bullets:
        for blue_bullet in blue_bullets:
            if red_bullet.colliderect(blue_bullet):
                red_bullets.remove(red_bullet)
                blue_bullets.remove(blue_bullet)
def blue_movement(keys_pressed,blue): 
    if keys_pressed[pygame.K_a] and blue.x - velocity > 0: #lef
            blue.x -= velocity
    if keys_pressed[pygame.K_d] and blue.x + velocity < width - velocity and blue.x < width/2 - spaceship_width+10:
        blue.x += velocity
    if keys_pressed[pygame.K_w]: #up
        if blue.y - velocity >= 30:
            blue.y -= velocity
    if keys_pressed[pygame.K_s]:
        if blue.y + velocity <= height - spaceship_height - 18:# down
            blue.y += velocity
def red_movement(keys_pressed,red):
    if keys_pressed[pygame.K_LEFT]and red.x - velocity >= 0 and red.x > width/2 + 6 :
        red.x -= velocity
    if keys_pressed[pygame.K_RIGHT]:
        if red.x + velocity <= width - spaceship_width + 18: #right
            red.x += velocity
    if keys_pressed[pygame.K_UP]: #up
        if red.y - velocity >= 30:
            red.y -= velocity
    if keys_pressed[pygame.K_DOWN]:
        if red.y + velocity <= height - spaceship_height - 18:# down
            red.y += velocity
def draw_window(
    red, blue,red_bullets,blue_bullets,blue_health_points,red_health_points,x,y,bonus_number):
    left_health_bar = pygame.Rect(10,10,10*blue_health_points,20)
    right_health_bar = pygame.Rect(890-10*red_health_points,10,10*red_health_points,20)
    win.blit(background,(0,0))
    pygame.draw.rect(win,BLACK, border)
    pygame.draw.rect(win,WHITE,left_white_bar)
    pygame.draw.rect(win,WHITE,right_white_bar)
    pygame.draw.rect(win,RED,left_health_bar)
    pygame.draw.rect(win,RED,right_health_bar)
    if red_health_points > 0 and blue_health_points > 0:
        if bonus_number > 300:
            win.blit(healthbar,(x,y))

    if blue_health_points > 0:
        win.blit(blue_spaceship, (blue.x, blue.y))
    if red_health_points > 0:
        win.blit(red_spaceship, (red.x, red.y))
    
    if red_health_points > 0 and blue_health_points > 0:
        for bullet_1 in red_bullets:
            pygame.draw.rect(win,RED,bullet_1)
        for bullet_2 in blue_bullets:
            pygame.draw.rect(win,BLUE,bullet_2)
    pygame.display.update()
def main(blue_health_points,red_health_points,bonus_number,x,y):
    red = pygame.Rect(700,300,spaceship_width,spaceship_height)
    blue = pygame.Rect(100,300,spaceship_width,spaceship_height)
    red_bullets = []
    blue_bullets = []
    clock = pygame.time.Clock()

    red_automat_run = False
    red_up = True
    red_to_side = True
    blue_automat_run = False
    blue_up = True
    blue_to_side = True

    number = 0

    run = True
    while run:
        clock.tick(fps)
        number += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == red_hit:
                red_health_points -= 1
            if event.type == blue_hit:
                blue_health_points -= 1
            if event.type == pygame.KEYDOWN:
                if event.key == K_q:
                    run = False
                if event.key == K_r:
                    bonus_number = 10
                    red.x, red.y = 700, 300
                    blue.x, blue.y = 100, 300
                    red_health_points, blue_health_points = 10, 10
                    blue_automat_run = False
                    red_automat_run = False
                    red_bullets, blue_bullets = [], []
                if event.key == K_SPACE and len(blue_bullets) < max_bullets:
                    bullet = pygame.Rect(blue.x+blue.width,blue.y+blue.height//2 - 2, 10,5)
                    blue_bullets.append(bullet)
                    bullet_fire_sound.play()
                if event.key == K_RSHIFT and len(red_bullets) < max_bullets:
                    bullet = pygame.Rect(red.x,red.y+red.height//2 - 2, 10,5)
                    red_bullets.append(bullet)
                    bullet_fire_sound.play()
                
                #automatic movement and shooting:                
                if event.key == K_m:
                    if red_automat_run:
                        red_automat_run = False
                    else:
                        red_automat_run = True
                if event.key == K_n:
                    if blue_automat_run:
                        blue_automat_run = False
                    else:
                        blue_automat_run = True
        if red_automat_run:
            random_number = randint(0,12)
            if random_number == 1:
                bullet = pygame.Rect(red.x,red.y+red.height//2 - 2, 10,5)
                red_bullets.append(bullet)
                bullet_fire_sound.play()
            if red_up:
                if red.y > 10:
                    red.y -= (velocity + randint(1,3))
                else:
                    red_up = False
            else:
                if red.y < 450:
                    red.y += velocity + randint(1,3)
                else:
                    red_up = True
            if red_to_side:
                if red.x > width / 2 + 6:
                    red.x -= velocity
                else:
                    red_to_side = False
            else:
                if red.x < 900 - 40:
                    red.x += velocity + 2
                else:
                    red_to_side = True
        if blue_automat_run:
            random_number = randint(0,12)
            if random_number == 1:
                bullet = pygame.Rect(blue.x,blue.y+blue.height//2 - 2, 10,5)
                blue_bullets.append(bullet)
                bullet_fire_sound.play()
            if blue_up:
                if blue.y > 10:
                    blue.y -= (velocity + randint(1,3))
                else:
                    blue_up = False
            else:
                if blue.y < 450:
                    blue.y += velocity + randint(1,3)
                else:
                    blue_up = True
            if blue_to_side:
                if blue.x < width / 2 - 45:
                    blue.x += velocity
                else:
                    blue_to_side = False
            else:
                if blue.x > 6:
                    blue.x -= velocity 
                else:
                    blue_to_side = True
        if red_health_points <= 0 or blue_health_points <= 0:
            red_automat_run = False
            blue_automat_run = False
            red_bullets = []
            blue_bullets = []
        bonus_number += 1
        if bonus_number % 300 == 0:
            random_half_of_screen = randint(1,2)
            if random_half_of_screen == 1:
                x = randint(0,380)
                y = randint(30,height - 80)
            else:
                x = randint(455,width - 80)
                y = randint(30,height - 80)
        if bonus_number > 300:
            blue_X = blue.x + 15
            blue_Y = blue.y + 26
            srdce_x = x + 30
            srdce_y = y + 40
            blue_x_rozdíl = max(blue_X,srdce_x) - min(blue_X,srdce_x)
            blue_y_rozdíl = max(blue_Y,srdce_y) - min(blue_Y,srdce_y)
            red_X = red.x + 15
            red_Y = red.y + 26
            srdce_x = x + 30
            srdce_y = y + 40
            red_x_rozdíl = max(red_X,srdce_x) - min(red_X,srdce_x)
            red_y_rozdíl = max(red_Y,srdce_y) - min(red_Y,srdce_y)

            if blue_x_rozdíl < 30 and blue_y_rozdíl < 30:
                bonus_number = 150
                blue_health_points += healt_adding
                collect_sound.play()
            elif red_x_rozdíl < 30 and red_y_rozdíl < 30:
                bonus_number = 150
                red_health_points += healt_adding
                collect_sound.play()
        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[K_x]:
            blue_health_points += 1
        if keys_pressed[K_u]:
            red_health_points += 1
        blue_movement(keys_pressed,blue)
        red_movement(keys_pressed,red)
        handle_bullets(blue_bullets,red_bullets,blue,red)
        draw_window(red,blue,red_bullets,blue_bullets,blue_health_points,red_health_points,x,y,bonus_number)
main(blue_health_points,red_health_points,bonus_number,x,y)

import pygame
import sys
from os import system
from pygame.locals import*
import RPi.GPIO as gp
import time

gp.setmode(gp.BCM)
input1=5
input2=6
input3=13
input4=19

gp.setup(input1,gp.IN,pull_up_down = gp.PUD_UP)
gp.setup(input2,gp.IN,pull_up_down = gp.PUD_UP)
gp.setup(input3,gp.IN,pull_up_down = gp.PUD_UP)
gp.setup(input4,gp.IN,pull_up_down = gp.PUD_UP)

pygame.init()

WINDOW_HEIGHT = 1080
WINDOW_WIDTH = 1920
BLACK = (0, 0, 0)
# ADD_NEW_FLAME_RATE = 25
CLOCK = pygame.time.Clock()
# font = pygame.font.SysFont('forte', 20)

menu_img = pygame.image.load('menu.jpg')
canvas = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('intro')


def game_start():
    canvas.fill(BLACK)
    home_img = pygame.image.load('home.jpg')
    canvas.blit(home_img, (0,0))
    pygame.mixer.music.load('bgm.mp3')
    pygame.mixer.music.play(-1)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        input1=gp.input(5)
        input2=gp.input(6)
        input3=gp.input(13)
        input4=gp.input(19)
        
        if (input2 == False) and (input3 == False): #or (input3 == False) or (input4 == False):
            pygame.mixer.music.load('click.mp3')
            pygame.mixer.music.play()
            menu()
        pygame.display.update()

def menu():
    canvas.fill(BLACK)
    menu_img = pygame.image.load('mode.jpg')
    canvas.blit(menu_img, (0,0))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        input1=gp.input(5)
        input2=gp.input(6)
        input3=gp.input(13)
        input4=gp.input(19)
        if (input1 == False) and (input2 == False):
            pygame.mixer.music.load('click.mp3')
            pygame.mixer.music.play()
            import realrsp
            
        elif (input3 == False) and (input4 == False):
            pygame.mixer.music.load('click.mp3')
            pygame.mixer.music.play()
            game_menu()
        pygame.display.update()

def game_menu():
    canvas.fill(BLACK)
    menu_img = pygame.image.load('gamemenu.jpg')
    canvas.blit(menu_img, (0,0))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        input1=gp.input(5)
        input2=gp.input(6)
        input3=gp.input(13)
        input4=gp.input(19)      
        if (input1 == False) and (input3 == False):
            pygame.mixer.music.load('click.mp3')
            pygame.mixer.music.play()
            import newshoot
            #shootinggame.runGame()
        elif (input2 == False) and (input4 == False):
            pygame.mixer.music.load('click.mp3')
            pygame.mixer.music.play()
            import mario
#            mario.start_game()
        elif (input1 == False) and (input4 == False):
            pygame.mixer.music.load('click.mp3')
            pygame.mixer.music.play()
            import Tetris
            
#            import tetlis
#            tetlis.Tetris(16, 30).run()
        pygame.display.update()

game_start()



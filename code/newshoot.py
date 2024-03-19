import pygame
import sys
import random
from time import sleep

import RPi.GPIO as gp
from os import system
from time import sleep
from pygame.locals import *
import signal

SHUTDOWN_GPIO = 26

# always use Broadcom numbers
gp.setmode(gp.BCM)
input1=5
input2=6
input3=13
input4=19

gp.setup(input1,gp.IN,pull_up_down = gp.PUD_UP)
gp.setup(input2,gp.IN,pull_up_down = gp.PUD_UP)
gp.setup(input3,gp.IN,pull_up_down = gp.PUD_UP)
gp.setup(input4,gp.IN,pull_up_down = gp.PUD_UP)


#real code
padWidth = 1920  # 게임 화면의 가로
padHeight = 1080 # 게임 화면의 세로
rockImage = ['me1.png','me2.png','me3.png','me4.png','me5.png','me6.png','me7.png',\
             'me8.png','me9.png','me10.png','me11.png','me12.png','me13.png','me14.png','me15.png']
explosionImage = ['bomb1.png','bomb2.png','bomb3.png','bomb4.png']
# explosionSound = ['explosion1.wav', 'explosion2.wav', 'explosion3.wav','explosion4.wav']
explosionSound = ['explosion2.wav']
# 운석을 맞춘 개수 계산
def writeScore(count):
    global gamePad
    font = pygame.font.Font('NanumSquareB.ttf',25) # 글자 크기
    text = font.render('없앤 운석의 수: ' + str(count), True, (255,255,255)) #255는 RGB
    gamePad.blit(text,(5,0)) # 글자 위치
# best score
def writeBestScore():
    global gamePad
    fr = open('gamelog_shooting.txt', 'r')
    font = pygame.font.Font('NanumSquareB.ttf',25)
    line = fr.readline()
    text = font.render('최고 기록: ' + str(line), True, (255,255,255))
    gamePad.blit(text,(5,30))
# 운석을 맞춘 개수 계산
def writePassed(count):
    global gamePad
    font = pygame.font.Font('NanumSquareB.ttf',25) # 글자 크기
    text = font.render('지구에 떨어진 운석 수: ' + str(count), True, (255,255,255)) #255는 RGB
    gamePad.blit(text,(1625,0)) # 글자 위치
# 
def writePressed(text):
    global gamePad
    textfont = pygame.font.Font('NanumSquareB.ttf',50)
    text = textfont.render(text, True, (255, 255, 255))
    textpos = text.get_rect()
    textpos.center = (padWidth/2, padHeight/2)
    gamePad.blit(text, textpos)
    pygame.display.update()
    
# 게임 메세지 출력
def writeMessage(text):
    global gamePad, gameOverSound
    textfont = pygame.font.Font('NanumSquareB.ttf',200)
    text = textfont.render(text, True, (255, 255, 255))
    textpos = text.get_rect()
    textpos.center = (padWidth/2, padHeight/2)
    gamePad.blit(text, textpos)
    pygame.display.update()
    pygame.mixer.music.stop() # 배경 음악 정지
    gameOverSound.play()    # 게임 오버 사운드
    gameOverSound.play()
    gameOverSound.play()
    sleep(5)  # 이초 쉬고 다시 실행해줘
    pygame.mixer.music.play(-1) # 배경 음악 재생
    import home1107
    home1107.game_start()

# 전투기가 운석과 충돌했을때 메세지 출력
def crash():
    global gamePad
    writeMessage('BOMB!!!')

# 게임오버 메세지 보이기
def gameOver():
    global gamePad
    writeMessage('GAME OVER')
    


# 게임에 등장하는 객체를 드로잉
def drawObject(obj, x, y):
    global gamePad
    gamePad.blit(obj, (x,y)) # 해당하는 오브젝트를 x,y 위치로부터 그려
    
def loop_func(num):
    global gamePad, bgd
    gamePad = pygame.display.set_mode((padWidth, padHeight))
    bgd = pygame.image.load('howtoshooting.png')
    for i in range(num):                
        drawObject(bgd, 0, 0)
        pygame.display.update() # 게임화면을 다시 그림
        sleep(1)

def initGame():
    global gamePad, clock, background, fighter, missile, gameOverSound, missileSound # explosion 잠깐 지움 
    pygame.init()
    gamePad = pygame.display.set_mode((padWidth, padHeight))
    pygame.display.set_caption('지구를지켜라!')                              # 게임이름
    background = pygame.image.load('background.png')             # 게임그림
    fighter = pygame.image.load('rocket1.png')                       # 전투기 그림
    missile = pygame.image.load('m1.png')                   # 미사일 그림
#    explosion = pygame.image.load('bomb1.png')             # 폭발 그림
    pygame.mixer.music.load('music.mp3')
    pygame.mixer.music.play(-1)
    missileSound = pygame.mixer.Sound('shot2.wav')
    #error!!!!!!
    gameOverSound = pygame.mixer.Sound('gameover.wav')
    clock = pygame.time.Clock()



def runGame():
    global gamePad, Clock, background, fighter, missile, explosion, missileSound
    
    #전투기 크기
    fighterSize = fighter.get_rect().size
    fighterWidth = fighterSize[0]
    fighterHeight = fighterSize[1]
    # 초기 위치
    x = padWidth * 0.45
    y = padHeight * 0.85 # 처음 우주선 위치
    fighterX = 0

    # 무기좌표
    missileXY = []

    # 운석 랜덤 생성
    rock = pygame.image.load(random.choice(rockImage))
    rockSize = rock.get_rect().size # 운석크기
    rockWidth = rockSize[0]
    rockHeight = rockSize[1]
    destroySound = pygame.mixer.Sound(random.choice(explosionSound))
    # 운석 초기 위치 설정
    # rockX = 0 # 일단 넣어봄
    rockX = random.randrange(0, abs(padWidth - rockWidth))
    rockY = 0
    rockSpeed = 12

    # 전투기 미사일에 돌이 맞았을 경우 True
    isShot = False
    shotCount = 0
    rockPassed = 0

    while True:
        missileSound.play()
        missileX = x + fighterWidth / 2
        # 미사일이 전투기 가운데서 나갈수 있게 x좌표 잡기
        missileY = y - fighterHeight/2
        missileXY.append([missileX, missileY])

        for event in pygame.event.get():
            if event.type == QUIT:      # 게임프로그램 종료
                pygame.quit()
                sys.exit()

#        if event.type in [pygame.KEYDOWN]:
        input1=gp.input(5)
        input2=gp.input(6)
        input3=gp.input(13)
        input4=gp.input(19)        
        if (input1 == False) and (input2 == False): # and (input3 == False) and (input4 == False): #전투기 왼쪽으로 이동
            fighterX -= 10
            writePressed('PRESSED')
            
        else: # 전투기 오른쪽으로 이동
            fighterX += 10

        drawObject(background, 0, 0)        # 배경화면 그리기. (화면이 꽉찻기에 필요없음)
        # 누르는 키에 따라 전투기 위치 재조정
        x += fighterX
        if x < 0 :
            x = 0
        elif x > padWidth - fighterWidth: # 전투기의 width값에서
            x = padWidth - fighterWidth   # pad에서 width값을 뺀 나머지 값은 X위치로; 더 이상 오른쪽으로 못나가게

        # 전투기가 운석과 충돌했는지 체크
        if y < rockY + rockHeight:
            if(rockX > x and rockX < x + fighterWidth) or  \
            (rockX + rockWidth > x and rockX + rockWidth < x + fighterWidth):
                f = open('gamelog_shooting.txt', 'r')
                bestScore = f.readline()
                bestScore = int(bestScore)
                if (shotCount > bestScore ):
                    f = open( 'gamelog_shooting.txt', 'w')
                    # :로 나누어 플레이어의 이름과 점수 저장
                    shotCount = str(shotCount)
                    f.write(shotCount)
                    f.close()
                    crash()
                else:
                    crash()

        drawObject(fighter, x, y)   # 전투기를 게임 화면의 (x,y)좌표에 그리기

        # 미사일 발사 화면에 그리기
        if len(missileXY) != 0:
            for i, bxy in enumerate(missileXY): #미사일 요소에 대한 반복
                bxy[1] -= 25 # 총알의 y좌표 -10(위로 이동)
                missileXY[i][1] = bxy[1]

                # 미사일이 운석을 맞추었을 경우
                if bxy[1] < rockY:
                    if bxy[0] > rockX and bxy[0] < rockX + rockWidth:
                        missileXY.remove(bxy) # 미사일이 운석 범위에 들어가면 미사일지우기
                        isShot = True
                        shotCount += 1

                if bxy[1] <= 0: # 미사일이 화면 밖을 벗어나면
                    try:
                        missileXY.remove(bxy) # 미사일 제거
                    except :
                        pass
        if len(missileXY) != 0: # 다시한번 그려주
            for bx, by in missileXY:
                drawObject(missile, bx, by)

        # 운석 맞춘 점수 표시
        writeScore(shotCount)
        writeBestScore()
        rockY += rockSpeed # 운석 아래로 움직임

        # 운석이 지구로 떨어진경우
        if rockY > padHeight:
            # 새로운 운석(랜덤)
            rock = pygame.image.load(random.choice(rockImage))
            rockSize = rock.get_rect().size # 운석크기
            rockWidth = rockSize[0]
            rockHeight = rockSize[1]
            rockX = random.randrange(0, abs(padWidth - rockWidth))
            rockY = 0
            rockPassed +=1
        # 3개이상 놓치면 게임오버
        if rockPassed == 3:
            f = open('gamelog_shooting.txt', 'r')
            bestScore = f.readline()
            bestScore = int(bestScore)
            if (shotCount > bestScore ):
                f = open( 'gamelog_shooting.txt', 'w')
                # :로 나누어 플레이어의 이름과 점수 저장
                shotCount = str(shotCount)
                f.write(shotCount)
                f.close()
                gameOver()
            else:
                gameOver()
            
        # 놓친 운석 수 표시
        writePassed(rockPassed)
        # 운석을 맞춘경우
        if isShot:
            # 운석폭발
            clock.tick(60)
            explosion = pygame.image.load(random.choice(explosionImage))
            drawObject(explosion, rockX, rockY) # 운석폭팔 그리기
            destroySound.play()
            drawObject(explosion, rockX + 1, rockY + 12)
            destroySound.play()
            drawObject(explosion, rockX + 12, rockY - 5)
            destroySound.play()
            drawObject(explosion, rockX - 12, rockY + 15)
            destroySound.play()
            drawObject(explosion, rockX - 8, rockY - 12)
            destroySound.play()

            # 새로운 운석(랜덤)
            rock = pygame.image.load(random.choice(rockImage))
            rockSize = rock.get_rect().size
            rockWidth = rockSize[0]
            rockHeight = rockSize[1]
            rockX = random.randrange(0, abs(padWidth - rockWidth))
            rockY = 0
            # destroySound = pygame.mixer.Sound(random.choice(explosionSound))
            isShot = False

            #운석 맞추면 속도 증가
            rockSpeed += 0.2
            if rockSpeed >= 20: #10보다 높으면 게임 불가능하기에
                rockSpeed = 20


        drawObject(rock, rockX, rockY)  #운석 그리기

        pygame.display.update() # 게임화면을 다시 그림

        clock.tick(60)      # 게임 화면의 초당 프레임수를 60으로 설정

    pygame.quit()           # pygame 종료

loop_func(10)
initGame()
runGame()

while (True) :
    try :
        sleep(5)
    finally :
        gp.cleanup()

# This button causes program to exit
# exit_button = ExitBtn(SHUTDOWN_GPIO)

# check if we should exit every half second
# while exit_button.check_continue():
#     sleep(0.5)

# All done so exit
# device.destroy()
# gp.cleanup()
        


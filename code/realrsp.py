import random
import cv2
import cvzone
from cvzone.HandTrackingModule import HandDetector
import time
import RPi.GPIO as gp
from pygame import mixer

gp.setmode(gp.BCM)
input1=5
input2=6
input3=13
input4=19

gp.setup(input1,gp.IN,pull_up_down = gp.PUD_UP)
gp.setup(input2,gp.IN,pull_up_down = gp.PUD_UP)
gp.setup(input3,gp.IN,pull_up_down = gp.PUD_UP)
gp.setup(input4,gp.IN,pull_up_down = gp.PUD_UP)

cap = cv2.VideoCapture(0)
cap.set(3, 960)
cap.set(4, 720)

detector = HandDetector(maxHands=1)

timer = 0
stateResult = False
startGame = False
scores = [0, 0]  # [AI, Player]


while True:
    imgBG = cv2.imread("./imgBG.png")
    success, img = cap.read()
        
    imgScaled = cv2.resize(img, (960, 720), None)
    imgScaled = imgScaled[90:960, 120:720]
            # Find Hands
    hands, img = detector.findHands(imgScaled)  # with draw
    
    
    if startGame:
        
        if stateResult is False:
            timer = time.time() - initialTime
            cv2.putText(imgBG, str(int(timer)), (930, 650), cv2.FONT_HERSHEY_PLAIN, 6, (255, 0, 255), 4)

            if timer > 3:
                stateResult = True
                timer = 0

                if hands:
                    playerMove = None
                    hand = hands[0]
                    fingers = detector.fingersUp(hand)
                    if fingers == [0, 0, 0, 0, 0]:
                        playerMove = 1
                    if fingers == [1, 1, 1, 1, 1]:
                        playerMove = 2
                    if fingers == [0, 1, 1, 0, 0]:
                        playerMove = 3

                    randomNumber = random.randint(1, 3)
                    imgAI = cv2.imread(f'./Resources/{randomNumber}.png', cv2.IMREAD_UNCHANGED)
                    imgBG = cvzone.overlayPNG(imgBG, imgAI, (224, 465))

                        # Player Wins
                    if (playerMove == 1 and randomNumber == 3) or \
                            (playerMove == 2 and randomNumber == 1) or \
                            (playerMove == 3 and randomNumber == 2):
                        scores[1] += 1

                        # AI Wins
                    if (playerMove == 3 and randomNumber == 1) or \
                            (playerMove == 1 and randomNumber == 2) or \
                            (playerMove == 2 and randomNumber == 3):
                        scores[0] += 1

    if imgBG is not None:
        imgBG[351:981, 1193:1793] = imgScaled

    if stateResult:
        imgBG = cvzone.overlayPNG(imgBG, imgAI, (224, 465))

    cv2.putText(imgBG, str(scores[0]), (628, 313), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 6)
    cv2.putText(imgBG, str(scores[1]), (1685, 313), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 6)
    
    key = cv2.waitKey(1)
    
    input1=gp.input(5)
    input2=gp.input(6)
    input3=gp.input(13)
    input4=gp.input(19)
    
    import howtostretch
    cv2.imshow("BG", imgBG)
    
    
    if key == (input1 == False) or (input2 == False) :
        startGame = True
        initialTime = time.time()
        stateResult = False
        
    elif key == (input3 == False) or (input4 == False) :
        cv2.destroyAllWindows()
        import home1107
        home1107.game_start()
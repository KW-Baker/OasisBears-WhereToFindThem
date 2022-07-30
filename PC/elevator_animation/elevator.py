# Implement By Stack
from time import time
import pygame
from pygame import image
from pygame.locals import QUIT
import keyboard
import time
width = 800
height = 507
barSize = 150
doorSize = 400
del_x = 5

#Color RGB
color_bg = (0, 0, 0)
color_white = (255, 255, 255)
color_lightGray = (200, 200, 200)
color_darkGray = (100, 100, 100)
color_red = (255,0,0)
# Image path
img_path = './elevator_animation/img_elevator.png'
running = True
# set rectangle: Rect(left, top, width, height)
door_1 = pygame.Rect(width, barSize, 0, height)
door_1_x ,door_1_y = (316, 409)
door_1.center = (door_1_x, door_1_y)
# Panel Info.
panel_x1, panel_y1 = (310, 75)
panel_x2, panel_y2 = (550, 195)
# global curr_floor, up_down, floor_state, floor_x, floor_y
floor_x = 800
floor_y = 90
curr_floor = 1
up_down = 'down'
status = {'o':False, 'c':False, '1':False, '2':True, '3':False, '4':False, '5':False, '6':True, '7':False, '8':False, '9':True, '10':False}
floor_state = []
flag = False
# Traverse Status Dictionary
def traverse():
    global floor_state, up_down
    floor_state = []
    #load image
    screen.fill(color_white)
    elevator = pygame.image.load(img_path)
    elevator.convert()
    screen.blit(elevator, (0,0))
    # Word
    x, y = (800, 150)
    text = font_small.render('Input Floor', True, color_bg)
    pygame.draw.rect(screen, color_bg,[735, 75, 300, 60], 5)
    screen.blit(text, (floor_x, floor_y))
    # Transpose status dictionary to array
    for k in status:
        if k != 'o' and k != 'c':
            if status[k] == True:
                floor_state.append(int(k))

    # Print the floor & Detect if the elevator should stop

    if up_down == 'up': # UP
        for i in range(1,11):
            if i in floor_state:
                temp = font_small.render(str(i), True,color_bg)
                screen.blit(temp, (x+ 80, y) )
                y += 40

    else : #DOWN
        for i in range(10,0,-1):
            if i in floor_state:
                temp = font_small.render(str(i), True,color_bg)
                screen.blit(temp, (x+ 80, y) )
                y += 40

    if not floor_state :
        up_down = 'idle'

# Panel Control
def panel_control():
    global up_down, curr_floor, flag
    # Determine to go up or down
    bigger_num = []
    smaller_num = []
    for f in floor_state:
        if f >= curr_floor :
            bigger_num.append(f)
        elif f < curr_floor :
            smaller_num.append(f)
    bigger_num.sort()
    smaller_num.sort()
    bigger_num_gap = smaller_num_gap = 0
    if bigger_num : 
        bigger_num_gap = bigger_num[0] - curr_floor
    if smaller_num : 
        smaller_num_gap = curr_floor - smaller_num[-1]
    if bigger_num_gap and smaller_num_gap : 
        if bigger_num_gap <= smaller_num_gap :
            up_down = 'up'
        else :
            up_down = 'down'
    
    if up_down == 'up':
        for i in range(curr_floor,floor_state[-1]+1):
            print("Floor = ",str(i))
            traverse()
            temp = font_big.render(str(i), True, color_red)
            screen.blit(temp, (panel_x1, panel_y1))
            screen.blit(temp, (panel_x2, panel_y2))
            pygame.display.update()
            time.sleep(1)
            if i in floor_state:
                Open_Close(i)
                status[str(i)] = False
            curr_floor = i
            print("Floor = " + str(i) + ",Flag = " + str(flag))
        up_down = 'down'

    elif up_down == 'down':
        print("Enter down")
        print(floor_state[0])
        for i in range(curr_floor,floor_state[0]-1,-1):
            traverse()
            temp = font_big.render(str(i), True, color_red)
            screen.blit(temp, (panel_x1, panel_y1) )
            screen.blit(temp, (panel_x2, panel_y2))
            pygame.display.update()
            time.sleep(1)
            if i in floor_state:
                Open_Close(i)
                status[str(i)] = False
            curr_floor = i
        up_down = 'up'
    temp = font_big.render(str(curr_floor), True, color_red)
    screen.blit(temp, (panel_x1, panel_y1) )
    screen.blit(temp, (panel_x2, panel_y2))
    pygame.display.update()
            
# Scheduling function
def input_floor(screen, status):
    traverse()
    panel_control()

# Door Open and Close
def Open_Close(floor):
    # Panel Floor Number
    temp = font_big.render(str(floor), True, color_red)
    # Open Door
    while door_1.w <= 379.5:
        screen.blit(temp, (panel_x1, panel_y1))
        screen.blit(temp, (panel_x2, panel_y2))
        pygame.display.update()
        screen.blit(elevator, (0,0))
        door_1.center = (door_1_x, door_1_y)
        door_1.w += del_x
        pygame.draw.rect(screen, color_white, door_1)
        clock.tick(30)
        pygame.display.update()
    screen.blit(temp, (panel_x1, panel_y1))
    screen.blit(temp, (panel_x2, panel_y2))
    pygame.display.update()
    time.sleep(1)
    # Close Door
    while door_1.w >= 0:
        screen.blit(temp, (panel_x1, panel_y1))
        screen.blit(temp, (panel_x2, panel_y2))
        pygame.display.update()
        screen.blit(elevator, (0,0))
        door_1.center = (door_1_x, door_1_y)
        door_1.w -= del_x
        pygame.draw.rect(screen, color_white, door_1)
        clock.tick(30)
        pygame.display.update()
    screen.blit(temp, (panel_x1, panel_y1))
    screen.blit(temp, (panel_x2, panel_y2))
    pygame.display.update()
    time.sleep(1)


if __name__ == '__main__':
    # initialize
    pygame.init()

    # build screen
    global screen 
    screen = pygame.display.set_mode((1300, 700))
    # set window title
    pygame.display.set_caption("elevator")
    # fill window
    screen.fill(color_white)
    #Font Info.
    font_small = pygame.font.Font('freesansbold.ttf', 32)
    font_big = pygame.font.Font('freesansbold.ttf', 64)
    # font
    dead_font = pygame.font.SysFont(None, 60)
    clock = pygame.time.Clock()

    #load image
    elevator = pygame.image.load(img_path)
    elevator.convert()
    screen.blit(elevator, (0,0))

    
    # pygame.display.update()
    switch = 'idle'
    

    while running:
        clock.tick(60) # 30 exe/secs
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
        if keyboard.is_pressed('o'):
            switch = 'open'
        elif keyboard.is_pressed('c'):
            switch = 'close'
        # set door
        input_floor(screen, status)
        
        pygame.display.update()
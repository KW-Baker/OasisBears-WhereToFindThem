import pygame
import keyboard
import time
import socket
import threading

isConnect = True
img_path = './PC/elevator_animation/img_elevator.png'


# define color
color_white = (255, 255, 255)
color_red = (255, 0, 0)
color_black = (0, 0, 0)

## set position ##
# Panel Info.
panel_x1, panel_y1 = (310, 75)
panel_x2, panel_y2 = (550, 195)



# set rectangle
rect = pygame.Rect(800, 150, 0, 507)
rect_x, rect_y = (316, 409)
rect.center = (rect_x, rect_y)

##
current_floor = 1
button_signal = ''
up_down = ""
queing_floor = []
moving_start_time = 0


## define time
# 
MAX_HOLD_TIME = 4

moving_delay = 1.5

moving_start_time = 0
hold_time = 0




del_x = 5


state_list = ["IDLE", "MOVING", "OPENING", "CLOSING", "HOLD"]
IDLE = 0
MOVING = 1
OPENING = 2
CLOSING = 3
HOLD = 4

state = IDLE


def animation():
    print("animation start")
    open_close_door()
    arrange_input_floor()

    # state
        # IDLE
        # MOVING
        # CLOSING
        # OPENING
        # HOLD
    
    if(state == IDLE):
        print("state: IDLE")
        idle()

    elif(state == MOVING):
        print("state: MOVING")
        moving()

    
    elif(state == CLOSING):
        print("state: CLOSING")
        closing()

    
    elif(state == OPENING): 
        print("state: OPENING")  
        opening()

    
    elif(state == HOLD):
        print("state: HOLD")
        hold()


    # scheduling
    # 判斷是上樓還下樓
    # sorting
        # 上樓 ascending
        # 下樓 decending

    # screen = pygame.display.set_mode((1300, 700))
    # screen.fill(color_white)
    # elevator = pygame.image.load(img_path)
    # elevator.convert()
    # screen.blit(elevator, (0,0))

    render()

    pygame.display.update()
    




def socket_recv():
    global button_signal
    print("start")
    data = conn.recv(1024) #1024
    print(data.decode())
    button_signal = data.decode()
    time.sleep(1)



def open_close_door():
    global button_signal
    global state
    if state != MOVING:
        if button_signal == 'o':
            state = OPENING
        elif button_signal == 'c':
            state = CLOSING


def arrange_input_floor():
    global queing_floor
    global up_down
    global button_signal
    try:
        floor_number = int(button_signal)
    except:
        button_signal = ''
    if not((button_signal == 'o') or (button_signal == 'c') or (button_signal == '')):
        if len(queing_floor) == 0:
            if (current_floor > floor_number): # DOWN FLOOR
                up_down = "down"

            elif (current_floor < floor_number): # UP FLOOR
                up_down = "up"
        
        if up_down == "up":
            if floor_number > current_floor:
                queing_floor.append(floor_number)
                queing_floor = list(set(queing_floor))
                queing_floor.sort(reverse = False)

        
        elif up_down == "down":
            if floor_number < current_floor:
                queing_floor.append(floor_number)
                queing_floor = list(set(queing_floor))
                queing_floor.sort(reverse = True)
                
        
        print("up_down: ", up_down)
        print("queing_floor: ", queing_floor)
    button_signal = ''

def render():
    screen = pygame.display.set_mode((1300, 700))
    screen.fill(color_white)
    elevator = pygame.image.load(img_path)
    elevator.convert()
    screen.blit(elevator, (0,0))
    temp = font_big.render(str(current_floor), True, color_red)
    screen.blit(temp, (panel_x1-current_floor//10*20, panel_y1))
    screen.blit(temp, (panel_x2-current_floor//10*17, panel_y2))
    #
    text = font_small.render('Input Floor:', True, color_black)
    screen.blit(text, (800, 125))
    for i,j in enumerate(queing_floor):
        temp = font_big.render(str(j), True, color_black)
        screen.blit(temp, (800+50*i, 195))
    #
    text = font_small.render('State:', True, color_black)
    screen.blit(text, (800, 300))

    text = font_small.render(state_list[state], True, (237,125,49))
    screen.blit(text, (800, 370))

    text = font_small.render("Going", True, color_black)
    screen.blit(text, (800, 475))

    text = font_small.render(up_down, True, color_black)
    screen.blit(text, (960, 475))

    pygame.draw.rect(screen, (color_white), rect)


def idle():
    global state
    global moving_start_time
    global up_down

    if len(queing_floor) == 0:
        up_down = ""
        state = IDLE
    else:
        if button_signal == 'o':
            state = OPENING
        
        elif button_signal == 'c':
            state = CLOSING
        
        else:
            state = MOVING
            moving_start_time = time.time()


    screen = pygame.display.set_mode((1300, 700))
    screen.fill(color_white)
    elevator = pygame.image.load(img_path)
    elevator.convert()
    screen.blit(elevator, (0,0))

    temp = font_big.render(str(current_floor), True, color_red)
    screen.blit(temp, (panel_x1, panel_y1))
    screen.blit(temp, (panel_x2, panel_y2))



def moving():
    global current_floor
    global state
    global moving_start_time
    # print("moving_start_time: ",moving_start_time)

    if time.time()-moving_start_time > moving_delay:
        if up_down == "up":
            current_floor += 1
        elif up_down == "down":
            current_floor -= 1
        moving_start_time = time.time()
    
    if current_floor == queing_floor[0]:
        del queing_floor[0]
        state = OPENING
   
    
    

        
def opening():
    global screen
    global state
    global hold_time

    if rect.w <= 379.5:
        rect.center = (rect_x, rect_y)
        rect.w += del_x
    else:
        state = HOLD
        hold_time = time.time()

def closing():
    global screen
    global state
    global hold_time

    if rect.w >= 0:
        rect.center = (rect_x, rect_y)
        rect.w -= del_x
    else:
        state = IDLE


def hold():
    global state
    global hold_time

    if time.time() - hold_time > MAX_HOLD_TIME:
        state = CLOSING
    
def keyboard_input():
    global button_signal
    if keyboard.is_pressed('1'):
        button_signal = '1'
        print("input signal: ", button_signal)
    elif keyboard.is_pressed('2'):
        button_signal = '2'
        print("input signal: ", button_signal)
    elif keyboard.is_pressed('3'):
        button_signal = '3'
        print("input signal: ", button_signal)
    elif keyboard.is_pressed('4'):
        button_signal = '4'
        print("input signal: ", button_signal)
    elif keyboard.is_pressed('5'):
        button_signal = '5'
        print("input signal: ", button_signal)
    elif keyboard.is_pressed('6'):
        button_signal = '6'
        print("input signal: ", button_signal)
    elif keyboard.is_pressed('7'):
        button_signal = '7'
        print("input signal: ", button_signal)
    elif keyboard.is_pressed('8'):
        button_signal = '8'
        print("input signal: ", button_signal)
    elif keyboard.is_pressed('9'):
        button_signal = '9'
        print("input signal: ", button_signal)
    elif keyboard.is_pressed('0'):
        button_signal = '9123456780'
        print("input signal: ", button_signal)
    elif keyboard.is_pressed('o'):
        button_signal = 'o'
        print("input signal: ", button_signal)
    elif keyboard.is_pressed('c'):
        button_signal = 'c'
        print("input signal: ", button_signal)

if __name__ == '__main__':

    pygame.init()
    font_big = pygame.font.Font('freesansbold.ttf', 56)
    font_small = pygame.font.Font('freesansbold.ttf', 48)

    screen = pygame.display.set_mode((1300, 700))
    screen.fill(color_white)
    elevator = pygame.image.load(img_path)
    elevator.convert()
    screen.blit(elevator, (0,0))
    


    if isConnect:
        # HOST = '192.168.50.252'
        HOST = '172.20.10.7'

        # 建立例項
        sk = socket.socket()

        # 定義需要繫結的ip和埠
        ip_port = (HOST, 8888)

        # 繫結監聽
        sk.bind(ip_port)

        # 最大連線數
        sk.listen(5)
    
    while True:
        if isConnect:
            print("正在進行等待接收收據......")
            conn, address=sk.accept()
            msg = "連線成功!"

        while True:
            ## Socket
            print("=======================================")

            keyboard_input()
            ##!!!!!!!!!!!Threading
            if isConnect:
                t1 = threading.Thread(target = socket_recv)
                t1.start()
                # data = conn.recv(1024) #1024
                # print(data.decode())
                # button_signal = data.decode()
            
            animation()    

            

            
            
            
            # open_close_door()
            # arrange_input_floor()

            # # state
            #     # IDLE
            #     # MOVING
            #     # CLOSING
            #     # OPENING
            #     # HOLD
            
            # if(state == IDLE):
            #     print("state: IDLE")
            #     idle()

            # elif(state == MOVING):
            #     print("state: MOVING")
            #     moving()

            
            # elif(state == CLOSING):
            #     print("state: CLOSING")
            #     closing()

            
            # elif(state == OPENING): 
            #     print("state: OPENING")  
            #     opening()

            
            # elif(state == HOLD):
            #     print("state: HOLD")
            #     hold()

        
            # # scheduling
            # # 判斷是上樓還下樓
            # # sorting
            #     # 上樓 ascending
            #     # 下樓 decending

            # # screen = pygame.display.set_mode((1300, 700))
            # # screen.fill(color_white)
            # # elevator = pygame.image.load(img_path)
            # # elevator.convert()
            # # screen.blit(elevator, (0,0))

            

            # render()

            # pygame.display.update()

            # if isConnect:
                # t1.join()
                # t2.join()

           
        conn.close()
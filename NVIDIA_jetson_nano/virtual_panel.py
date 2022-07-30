import cv2
from cvzone.HandTrackingModule import HandDetector
# pip install cvzone == "1.5"
import time

import socket
import serial


def virtual_panel(client, isConnect = False, idleTime = 15, startTime = 0):
    # IP = '172.20.10.8'
    # PORT = 8888
    startTime = time.time()
    pTime = 0

    # if isConnect:
    #     client = socket.socket()
    #     ip_port = (IP, PORT)
    #     client.connect(ip_port)

    # floor_state = { 'o':False, 'c':False,
    #                 '1':False, '2':False, '3':False, '4':False, '5':False,
    #                 '6':False, '7':False, '8':False, '9':False, '10':False}
    button_signal = ""
    pre_button_signal = ""
    # parameter
    x_button_shift = 900
    x_shift = 15
    y_shift = 50

    floor_num = 10
    button_num = floor_num + 2



    cap = cv2.VideoCapture(0)
    cap.set(3, 1280) #1280
    cap.set(4,720) #720

    pTime = 0

    detector = HandDetector(detectionCon=100, maxHands=1) #(0.8, 2)
    keys = [[" 9 ","10 "],
            [" 8 ", " 7 "],
            [" 6 ", " 5 "],
            [" 4 ", " 3 "],
            [" 2 ", " 1 "],
            [">|<", "<|>"]]


    def drawALL(img, buttonList):
        for button in buttonList:
            x, y = button.pos
            w, h = button.size
            cv2.rectangle(img, button.pos, (x + w, y + h), (96, 164, 244), cv2.FILLED)
            cv2.putText(img, button.text, (x + x_shift, y + y_shift), 
                        cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, 1, (244, 164, 96), 5)
        return img


    def generate_signal(text):
        if   text == " 1 ":
            signal = "1"
        elif text == " 2 ":
            signal = "2"
        elif text == " 3 ":
            signal = "3"
        elif text == " 4 ":
            signal = "4"
        elif text == " 5 ":
            signal = "5"
        elif text == " 6 ":
            signal = "6"
        elif text == " 7 ":
            signal = "7"
        elif text == " 8 ":
            signal = "8"
        elif text == " 9 ":
            signal = "9"
        elif text == "10 ":
            signal = "10"
        elif text == ">|<":
            signal = "c"
        elif text == "<|>":
            signal = "o"
        else:
            signal = ""
        
        print("signal: ", signal)
    
        return signal


    class Button():
        def __init__(self,pos, text, size=[75,75]):
            self.pos = pos
            self.size = size
            self.text = text
        
    


    buttonList = []
    for i in range(len(keys)):
        for j, key in enumerate(keys[i]):
            buttonList.append(Button([90 * j + x_button_shift, 90 * i + 5], key)) #120



    COM_PORT ="/dev/ttyTHS1" #'COM5'
    BAUD_RATES = 115200
    try:
        ser = serial.Serial(COM_PORT, BAUD_RATES)
    except:
        print("Can not find serial port!")


    while True:
        # if isConnect:
        #     data = client.recv(1024)
        #     print(data.decode())

        success, img = cap.read()
        img_flip = cv2.flip(img,1)
        hands, img = detector.findHands(img_flip, flipType=False)
        # hands = detector.findHands(img_flip, draw=False) # No Draw
        
        img = drawALL(img, buttonList)

        if hands:
            hand1 = hands[0]
            lmList = hand1["lmList"]

            if lmList:
                for button in buttonList:
                    x, y = button.pos
                    w, h = button.size

                    if x < lmList[8][0] < x+w and y < lmList[8][1] < y+h:
                        cv2.rectangle(img, button.pos, (x + w, y + h), (47, 115, 205), cv2.FILLED)
                        cv2.putText(img, button.text, (x + x_shift, y + y_shift), 
                                    cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, 1, (244, 164, 96), 5)
                        l, _, _ = detector.findDistance(lmList[8], lmList[12], img)
                        # print(l) #distance

                        if l<50: #dell 50 #c310 95
                            cv2.rectangle(img, button.pos, (x + w, y + h), (0, 0, 255), cv2.FILLED)
                            cv2.putText(img, button.text, (x + x_shift, y + y_shift), 
                                    cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, 1, (244, 164, 96), 5)
                            
                            
                            # floor_state = generate_signal(button.text, floor_state)
                            button_signal = generate_signal(button.text)
                            
        if isConnect: 
            if not((button_signal == 'o') or (button_signal == 'c') or (button_signal == '')):
                if button_signal != pre_button_signal:
                    msg_input = button_signal
                    client.send(msg_input.encode())
                    pre_button_signal = button_signal
            else:
                msg_input = button_signal
                client.send(msg_input.encode())
                button_signal = ''
                pre_button_signal = button_signal
        
            # data = client.recv(1024)
            # print(data.decode())
            


        cTime = time.time()
        fps = (1 / (cTime - pTime)) if (cTime - pTime)>0 else 100
        pTime = cTime

        cv2.putText(img, f'FPS: {int(fps)}', (1080, 70), cv2.FONT_HERSHEY_PLAIN,
                3, (0, 0, 255), 3)                  
        

        cv2.imshow("Image", img)

        cv2.waitKey(1)
        
        try:
            if ser.in_waiting:          
                data_raw = ser.readline()  
                data = data_raw.decode()
                print(data)
                if data.strip() == "Y":
                    startTime = time.time()
        except:
            pass

        if time.time()-startTime >= idleTime: #Idle over 10 seconds
            # cap.release()
            # cv2.destroyAllWindows()
            return False

    # cap.release()
    # cv2.destroyAllWindows()

# if __name__ == "__main__":
#     # virtual_panel(client, isConnect = False)
from uart import uart
from virtual_panel import  virtual_panel
import time
import socket
import cv2

from hcsr04 import object_trigger





if __name__ == "__main__":
    idleTime = 20
    pTime = 0
    

    # Socket
    IP = '172.20.10.7'
    # IP = '172.20.10.8'
    PORT = 8888

    

    # Serial Port
    COM_PORT = "/dev/ttyTHS1" #'COM5'
    BAUD_RATES = 115200

    isConnect = True

    face_detector = True
    object_detector = True
    trigger = False
    face_trig = "N"

    startTime = 0

    
    if isConnect:
        client = socket.socket()
        ip_port = (IP, PORT)
        client.connect(ip_port)
        print(client)
    else:
        client = False

    print("############START#############")

    if face_detector:
        while True:
            if trigger == False:
                try:
                    face_trig, trigger = uart(COM_PORT ,BAUD_RATES)
                    # print("uart_trig = ",uart_trig) #for debug
                    # print("trigger",trigger) #for debug
                except:
                    print("COM port error !")

            else:
                if face_trig == "-1":
                    print("KeyboardInterrupt !")
                else:
                    if face_trig == "Y" or (object_trigger() and object_detector):
                        print("=======Triggered state========")
                        startTime = time.time()
                        trigger = virtual_panel(client, isConnect, idleTime, startTime)
                    
                    else:
                        print("==========IDLE state==========")
                        trigger = False
                        cv2.destroyAllWindows()
                            



    else:
        virtual_panel(client, isConnect, idleTime, startTime=time.time())

    

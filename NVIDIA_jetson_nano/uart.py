import serial
import time

def uart(COM_PORT = 'COM3',BAUD_RATES = 115200):
    try:
        ser = serial.Serial(COM_PORT, BAUD_RATES)   # Initialize serial port
        try:
            while True:
                # print(ser.in_waiting)
                while ser.in_waiting:  
                    data_raw = ser.readline() 
                    data = data_raw.decode()   # UTF-8 decode
                    # print('Original data from ESP32-CAM:', data_raw) #for debug
                    # print('Recieved data from ESP32-CAM:', data) #for debug
                    # print(type(data))
                    return data.strip(),True

        except KeyboardInterrupt:
            ser.close()    
            print('Serial closed')

            return "-1"
    except:
        print("Can not find serial port!")

if __name__ == "__main__":
    uart(COM_PORT = "/dev/ttyTHS1",BAUD_RATES = 115200)
    
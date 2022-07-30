import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)

GPIO_TRIGGER = 19
GPIO_ECHO = 21

GPIO.setup(GPIO_TRIGGER, True)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)

def distance():
    GPIO.output(GPIO_TRIGGER, True)
    time.sleep(0.00001)

    GPIO.output(GPIO_TRIGGER, False)

    StartTime = time.time()
    StopTime = time.time()
    
    
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()

    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()

    TimeElapsed = StopTime - StartTime
    distance = (TimeElapsed * 34300) / 2
    return distance

def object_trigger():
    dist = distance()
    if dist < 100:
        return True
    else:
        return False

if __name__ == '__main__':
    try:
        while True:
            # dist = distance()
            # print("Measured Distance = %.1f" %dist)
            
            print(object_trigger())

            time.sleep(1)
            

    except KeyboardInterrupt:
        print("Measurement stopped by User")
        GPIO.cleanup()
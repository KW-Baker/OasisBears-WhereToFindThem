import cv2
import keyboard
import time
import os
import random
import numpy as np

DEGREE = 20
NUM = 100
USER = "jeff"
PATH = './' + USER 
if not os.path.isdir(PATH):
    os.mkdir(PATH)

img_cnt = 0

wCam, hCam = 640, 480

x = 270
y = 190

w = 200
h = 200

DIM = (100,100)
 
cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)





def rotation(src):
    h,w = src.shape[:2]
    rotation_matrix = cv2.getRotationMatrix2D((w/2, h/2), random.randrange(-1*DEGREE,DEGREE,1),  random.uniform(1.0, 1.5))
    rotated_img = cv2.warpAffine(src, rotation_matrix, (w,h))
    # cv2.imshow("rotated_img", rotated_img)
    return rotated_img


def brightness(src):
    bright_img = np.zeros(src.shape, src.dtype)
    alpha = random.uniform(0.5, 2.0)
    beta = random.randrange(-25, 25, 1)

    for y in range(src.shape[0]):
        for x in range(src.shape[1]):
                bright = alpha*src[y,x] + beta
                bright_img[y,x] = np.clip(bright, 0, 255)

    # cv2.imshow("bright_img", bright_img)

    return bright_img


def flip(src):
    flip_img = cv2.flip(src,3)
    # cv2.imshow("flip_img", flip_img)
    return flip_img


def sharp(src):
    sharppening = np.array( [[-1,-1,-1],
                             [-1,10,-1],
                             [-1,-1,-1]])
    sharp_img = cv2.filter2D(src, -1, sharppening)
    # cv2.imshow("sharp_img", sharp_img)

    return sharp_img

def blur(src):
    kernel_size = random.randrange(3,5)
    kernel = np.ones((kernel_size,kernel_size), np.float32) / 25
    blur_img = cv2.filter2D(src,-1,kernel)
    
    # cv2.imshow("blur_img", blur_img)

    return blur_img




def gauss_noise(src):
    mean = 0
    sigma = 0.1
    src = src / 255
    noise = np.random.normal(mean, sigma, src.shape)
    noise_img = src + noise
    noise_img = np.clip(noise_img, 0, 1)
    noise_img = np.uint8(noise_img*255)

    noise = np.uint8(noise*255)
    # cv2.imshow("noise", noise)
    # cv2.imshow("noise_img", noise_img)

    return noise_img

def data_aug(src):
    dst = src

    if(random.randint(0,1)):
        print("rotation")
        dst = rotation(dst)
        
    if(random.randint(0,1)):
        print("brightness")
        dst = brightness(dst)

    if(random.randint(0,1)):
        print("flip")
        dst = flip(dst)

    if(random.randint(0,1)):
        print("sharp")
        dst = sharp(dst)

    if(random.randint(0,1)):
        print("blur")
        dst = blur(dst)

    
    # cv2.imshow("dst", dst)

    return dst



# img_path = PATH + '/' + USER + '1.jpg'

# image = cv2.imread(img_path)
# cv2.imshow("src", image)

# rot_img = rotation(image)
# bright_img = brightness(image)
# flip_img = flip(image)
# sharp_img = sharp(image)
# blur_img = blur(image)
# noise_img = gauss_noise(image)



# while True:
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

while(True):
    ret, frame = cap.read()

    # cv2.imshow('frame', frame)
    gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)

    
    # cv2.imshow("Gray", gray)

    crop_img = gray[y:y+h, x:x+w]
    # resized = cv2.resize(gray, DIM, interpolation = cv2.INTER_AREA)
    cv2.imshow("crop_img", crop_img)


    if keyboard.is_pressed("c"):
        for i in range(5):
            img_cnt += 1
            img_path = PATH + '/' + str(USER)  + str(img_cnt) + '.jpg'
            print(img_path)
            aug_img = data_aug(crop_img)
            cv2.imshow("aug_img", aug_img)
            cv2.imwrite(img_path, aug_img)

    if(img_cnt == NUM):
        print("Collect data is finish!")
        break


        

    
    # if keyboard.is_pressed("c"):
    #     # print("You pressed c")
    #     time.sleep(0.2)
    #     img_cnt += 1
    #     img_path = PATH + '/' + str(USER)  + str(img_cnt) + '.jpg'
    #     print(img_path)
    #     cv2.imwrite(img_path, gray)

        

    #     continue


    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


cap.release()


cv2.destroyAllWindows()
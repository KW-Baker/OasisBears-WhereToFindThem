import cv2
import os
import random
import numpy as np
from matplotlib import pyplot as plt
import keyboard

# Import tensorflow dependencies - Functional API
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Layer, Conv2D, Dense, MaxPooling2D, Input, Flatten
import tensorflow as tf


import time





def preprocess(file_path):
    
    # Read in image from file path
    byte_img = tf.io.read_file(file_path)
    
    # Load in the image
    img = tf.io.decode_jpeg(byte_img)
    
    # Preprocessing step - resizing the image to be 100x100x3
    img = tf.image.resize(img, (100,100))
    
    # Scale image to be between 0 and 1
    img = img / 255.0
    
    return img



class L1Dist(Layer):
    
    # Init method - inheritance
    def __inint__(self, **kwargs):
        super().__init__()
    
    # Magic happens here - similarity caculation
    def call(self, input_embedding, validation_embedding):
        return tf.math.abs(input_embedding - validation_embedding)



def verify(model ,detection_threshold, verification_threshold):
    # Build results array
    results = []
    for image in os.listdir('application_data\\verification_images'):
        input_img = preprocess('application_data\\input_image\\input_image.jpg')
        validation_img = preprocess('application_data\\verification_images\\' + str(image))
        
        # Make Predictions
        result = model.predict(list(np.expand_dims([input_img, validation_img], axis=1)))
        results.append(result)
        
        
    # Detection Threshold:Metric above which a predictino is considered positive
    detection = np.sum(np.array(results) > detection_threshold)
    # print("np.array(results)", np.array(results))
    
    # Verification Threshold: Proportion of positive predictions / total positive samples
    verification = detection / len(os.listdir('application_data\\verification_images'))
    print("Verification:", verification)

    verified = verification > verification_threshold
    
    return results, verified
    
# v5

# Reload model
model = tf.keras.models.load_model('siamesemodel_v5.h5',\
                                  custom_objects={'L1Dist':L1Dist, 'MSE':tf.losses.MeanSquaredError})
								  
								  
	

	
cap = cv2.VideoCapture(0)



 

while True:
    print("=============================")
    start = time.time()
    ret, frame = cap.read()
    
    frame = frame[120:120+250,200:200+250, :]
    
    # cv2.imshow('Verification', frame)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    cv2.imshow('Verification', gray)




    # Verification trigger
    # if keyboard.is_pressed("V"):
        # Save input image to application_data/input_image folder
    cv2.imwrite('application_data\\input_image\\input_image.jpg', gray)
    

    # Run verification
    results, verified = verify(model, 0.5, 0.91)
    


    
    
    # print(verified)




    
    # cv2.imwrite('application_data\\input_image\\input_image.jpg', gray)
    

    # # Run verification
    # results, verified = verify(model, 0.5, 0.5)
    # # print(verified)


    end = time.time()
    print("Infrence time:", format(end-start))

    if verified:
        print("VERIFIED")
    else:
        print("UNVERIFIED")

    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
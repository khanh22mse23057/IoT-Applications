from keras.models import load_model  # TensorFlow is required for Keras to work
import cv2  # Install opencv-python
import numpy as np
import time
import imutils
from config import *
import face_recognitions 
import constants as CONS
import base64

onDetection = None
PATH =  "./input_model"
def on_publish(client, userdata, mid):
    print("Image published to Adafruit!")


def processImage(image, state, onDetection):

    resized = imutils.resize(image, width=400)
    #res, frame = cv2.imencode('.jpg', image)  # from image to binary buffer            
    # Encode the resized image to JPG format with compression quality of 5%
    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 50]
    # Compress the image
    result, encimg = cv2.imencode('.jpg', resized, encode_param)
    # Calculate the size of the encoded image in bytes
    size_in_bytes = encimg.shape[0]

    # Check if the size is less than 1KB
    if size_in_bytes < 102400 :
        onDetection(image, base64.b64encode(encimg), state)
        time.sleep(1)  
    else:
        print("Image size exceeds 100KB limit")  

def start(onDetection):
    run_detection(onDetection)
    # t = threading.Thread(target=run_detection, args=[onDetection])
    # t.start()

def run_detection(onDetection):

    count = -1
    # Disable scientific notation for clarity
    np.set_printoptions(suppress=True)
    # Load the model
    model = load_model(f"{PATH}/keras_Model.h5", compile=False)
    # Load the labels
    class_names = open(f"{PATH}/labels.txt", "r").readlines()
    # CAMERA can be 0 or 1 based on default camera of your computer
    if checkIpCamera():
        camera = cv2.VideoCapture(CAMERA_IP_URL)
    else:
        camera = cv2.VideoCapture(0)
    # camera = cv2.VideoCapture(0)
    last_class_name = None
    known_face_encodings, known_face_names = face_recognitions.encode_faces()

    while True:
            if CONS.IsQuit:
                break
            # Grab the webcamera's image.
            ret, _image = camera.read()

            # Resize the raw image into (224-height,224-width) pixels
            image = cv2.resize(_image, (224, 224), interpolation=cv2.INTER_AREA)

            # Show the image in a window
            cv2.imshow("Webcam Image", image)

            # Make the image a numpy array and reshape it to the models input shape.
            image = np.asarray(image, dtype=np.float32).reshape(1, 224, 224, 3)

            # Normalize the image array
            image = (image / 127.5) - 1

            # Predicts the model
            prediction = model.predict(image, verbose=None)
            index = np.argmax(prediction)
            class_name = class_names[index]
            confidence_score = prediction[0][index]

            # Print prediction and confidence score
            if last_class_name != class_name :
                last_class_name = class_name
                # print("Class:", class_name[2:], end="")
                # print("Confidence Score:", str(np.round(confidence_score * 100))[:-2], "%")

                        
            if count % 1000 == 0:
                processImage(_image, class_name[2:], onDetection)
                time.sleep(0.1)

            # face_recognitions.recognize(known_face_encodings, known_face_names, _image)
            # # Display the resulting image
            # cv2.imshow('Video', _image)           
            count = count + 1 

            # Listen to the keyboard for presses.
            keyboard_input = cv2.waitKey(1)

            # 27 is the ASCII for the esc key on your keyboard.
            if keyboard_input == 27:
                break

    camera.release()
    cv2.destroyAllWindows()

    



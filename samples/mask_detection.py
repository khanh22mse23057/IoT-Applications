from keras.models import load_model  # TensorFlow is required for Keras to work
from PIL import Image, ImageOps  # Install pillow instead of PIL
import numpy as np
import cv2  # Install opencv-pytho
import base64
import time


def on_publish(client, userdata, mid):
    print("Image published to Adafruit!")

def run_camera(client):
    # Disable scientific notation for clarity
    np.set_printoptions(suppress=True)

    # Load the model
    model = load_model(".\input_model\keras_Model.h5", compile=False)

    # Load the labels
    class_names = open(".\input_model\labels.txt", "r").readlines()

    # CAMERA can be 0 or 1 based on default camera of your computer
    camera = cv2.VideoCapture(0)

    count = 1
    while True:
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
            prediction = model.predict(image)
            index = np.argmax(prediction)
            class_name = class_names[index]
            confidence_score = prediction[0][index]

            # Print prediction and confidence score
            print("Class:", class_name[2:], end="")
            print("Confidence Score:", str(np.round(confidence_score * 100))[:-2], "%")
            

            feed_id= ("mse11-mask_detection" if class_name[2:] == "mask" else "mse11-unmask_detection")
            if count > 0:
                small_Img = cv2.resize(image, (300, 300), interpolation=cv2.INTER_AREA)  
                res, frame = cv2.imencode('.jpg', small_Img)  # from image to binary buffer            
                client.publish(feed_id, base64.b64encode(frame))
                client.on_publish = on_publish
                count = count - 1
                #client.loop(2)
                time.sleep(1)                
                
            # Listen to the keyboard for presses.
            keyboard_input = cv2.waitKey(1)

            # 27 is the ASCII for the esc key on your keyboard.
            if keyboard_input == 27:
                break

    camera.release()
    cv2.destroyAllWindows()


        

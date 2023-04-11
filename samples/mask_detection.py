from keras.models import load_model  # TensorFlow is required for Keras to work
import cv2  # Install opencv-python
import numpy as np
import base64
import time
import imutils
 

def on_publish(client, userdata, mid):
    print("Image published to Adafruit!")

def image_pushing(client, image, state):

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
        client.publish("imask", base64.b64encode(encimg))
        client.publish("message", state)
        client.on_publish = on_publish
        time.sleep(1)  
    else:
        print("Image size exceeds 100KB limit")   

        
def run_detection(client):

    count = -1
    # Disable scientific notation for clarity
    np.set_printoptions(suppress=True)
    # Load the model
    model = load_model(".\\input_model\\keras_Model.h5", compile=False)
    # Load the labels
    class_names = open(".\\input_model\\labels.txt", "r").readlines()
    # CAMERA can be 0 or 1 based on default camera of your computer
    camera = cv2.VideoCapture(0)
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

            if count % 5 == 0:
                image_pushing(client, _image, class_name[2:])
            count = count + 1  

            # Listen to the keyboard for presses.
            keyboard_input = cv2.waitKey(1)

            # 27 is the ASCII for the esc key on your keyboard.
            if keyboard_input == 27:
                break

    camera.release()
    cv2.destroyAllWindows()

    



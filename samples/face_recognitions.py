import face_recognition
import cv2
import numpy as np
import sys
import os


# This is a super simple (but slow) example of running face recognition on live video from your webcam.
# There's a second example that's a little more complicated but runs faster.
# PLEASE NOTE: This example requires OpenCV (the `cv2` library) to be installed only to read from your webcam.
# OpenCV is *not* required to use the face_recognition library. It's only required if you want to run this
# specific demo. If you have trouble installing it, try any of the other demos that don't require it instead.
def encode_faces():
    known_face_encodings =[]
    known_face_names = []
    folder_dir = "./images"
    for image in os.listdir(folder_dir):
        try:
            face_image = face_recognition.load_image_file(f"{folder_dir}/{image}")
            face_encoding = face_recognition.face_encodings(face_image)[0]

            known_face_encodings.append(face_encoding)
            known_face_names.append(image)
        except:
            print("There is no face")
    print(known_face_names)

    return known_face_encodings, known_face_names

def run_face_recognition(client):

    known_face_encodings, known_face_names = encode_faces()

    # Get a reference to webcam #0 (the default one)
    video_capture = cv2.VideoCapture(0)
    while True:
        # Grab a single frame of video
        ret, frame = (video_capture.read())
        #frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)

        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_frame = np.ascontiguousarray(frame[:, :, ::-1])
        # Find all the faces and face enqcodings in the frame of video
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

        # Loop through each face in this frame of video
        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)

            name = "Unknown"

            # If a match was found in known_face_encodings, just use the first one.
            # if True in matches:
            #     first_match_index = matches.index(True)
            #     name = known_face_names[first_match_index]

            # Or instead, use the known face with the smallest distance to the new face
            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = known_face_names[best_match_index]

            # Draw a box around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

            # Draw a label with a name below the face
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

            if name == "Unknown":
                username = input("Enter username:")
                print("Username is: " + username)
                cv2.imwrite('./images/' + username + '.jpg', frame)
                cv2.imshow("User Capture", frame)
                print('taking pictures')

        # Display the resulting image
        cv2.imshow('Video', frame)

        key = cv2.waitKey(1)

        if key == ord('x'):
            username = input("Enter username:")
            print("Username is: " + username)
            cv2.imwrite('./images/' + username + '.jpg', frame)
            cv2.imshow("User Capture", frame)
            print('taking pictures')


        #Hit 'q' on the keyboard to quit!
        if key == ord('q'):
            break

    # Release handle to the webcam
    video_capture.release()
    cv2.destroyAllWindows()
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import json
import constants as CONS
databaseURL = "https://khanhpnp-mse-default-rtdb.firebaseio.com"

default_app  = None
ref  = None
# Subscribe to real-time changes at the '/users' node

faces_ref = None

def init():
    cred = credentials.Certificate("./team03-fsbmse-firebase.json")
    global default_app , ref
    default_app = firebase_admin.initialize_app(cred , {
    'databaseURL': databaseURL
    })
    ref = db.reference()
    global faces_ref
    faces_ref = ref.child('faces')
    users_ref_stream = faces_ref.listen(handle_data_change)


# Define a callback function to handle incoming data changes
def handle_data_change(event):
    try:

        # print(f"Data changed at {event.path}: {event.data}")
        print(f"Data changed at {event.path}")
        # Get the updated user's age and update the value at local
        if event.path == '/':
            faces_ref = ref
        else:
            child_path = event.path.lstrip('/')
            path = str(child_path).split("/")

            if str(path[1]) == "name":
                print(f"Value: {event.data}")
                CONS.FaceDataSet[str(path[0])] = event.data
            # faces_ref = ref.child(path[0])
            # face = faces_ref.get()
            # update_face_dataset(face)
    except Exception as e: print(e)

def add_face(postId, data):
    _id = postId.replace(" ", "") # remove all spaces
    _id = _id.lower() # convert to lowercase

    ref.child('faces').child(_id).set(data)


    
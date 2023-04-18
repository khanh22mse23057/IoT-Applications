import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import json

databaseURL = "https://khanhpnp-mse-default-rtdb.firebaseio.com"

default_app  = None
ref  = None
def init():
    cred = credentials.Certificate("./team03-fsbmse-firebase.json")
    global default_app , ref
    default_app = firebase_admin.initialize_app(cred , {
    'databaseURL': databaseURL
    })
    ref = db.reference('/')


def addFaceData(image, name):
    print(name)

def writePost(postId, data):
    # postId = title.replace(" ", "") # remove all spaces
    # postId = title.lower() # convert to lowercase
    ref.set({postId : data})


    
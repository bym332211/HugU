import cv2
import base64
from PIL import Image
import sys
import io
import numpy as np


cascPath = 'D:\workspace_python\HugU\HugU\haar\haarcascade_frontalface_default.xml'
faceCascade = cv2.CascadeClassifier(cascPath)

# video_capture = cv2.VideoCapture(0)
def test(args):
    print("asdf")
    # for arg in args:
    #     print(str(arg))
    filepath = str(args[1])
    # filepath = 'D:\\demo\\img.txt'
    f = open(filepath, 'r')
    base64str = f.read()
    faceRecognaize(base64str)
    return "test"

def data_uri_to_cv2_img(uri):
    encoded_data = uri.split(',')[1]
    nparr = np.fromstring(encoded_data.decode('base64'), np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    return img


def readb64(base64_string):
    print("start readb64")
    imgdata = base64.b64decode(str(base64_string))
    image = Image.open(io.BytesIO(imgdata))
    print("end readb64")
    return cv2.cvtColor(np.array(image), cv2.COLOR_BGR2RGB)


def faceRecognaize(base64str):
    print("start faceRecognaize")
    print(base64str)
    frame = readb64(base64str)
    # cv2.imshow(frame)


    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    print("1111")
    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30),
        # flags=cv2.cv.CV_HAAR_SCALE_IMAGE
        flags=0
    )
    # cv2.imshow('Video', frame)
    # Draw a rectangle around the faces
    try :
        print("2222")
        if faces.any():
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

            # Display the resulting frame

            print("found")
            print("end faceRecognaize")
            return True
        else :
            print("not found")
            print("end faceRecognaize")
            return False
    except:
        print("error")
        print("end faceRecognaize")

test(sys.argv)
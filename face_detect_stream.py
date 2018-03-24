import base64
import io
import numpy as np
import face_recognition
import cv2
import os
import re
import datetime



import sys
from PIL import Image

class faceDetectStream():
    def __init__(self, args):
        self.getBaseEncodings()
        filepath = str(args[1])
        # filepath = 'D:\\demo\\img.txt'
        f = open(filepath, 'r')
        self.base64str = f.read()
        self.url = 0
        self.speed = 4
        self.v_size = 1


    def readb64(self):
        print("start readb64")
        imgdata = base64.b64decode(str(self.base64str))
        image = Image.open(io.BytesIO(imgdata))
        print("end readb64")
        return cv2.cvtColor(np.array(image), cv2.COLOR_BGR2RGB)

    def getBaseEncodings(self):
        path = "D:\workspace_python\HugU\HugU\input"
        allfilelist = os.listdir(path)
        self.base_encodings = {}
        for file in allfilelist:
            filepath = os.path.join(path, file)
            base_image = face_recognition.load_image_file(filepath)
            name = filepath.replace(path + "\\", "")
            m = re.search("(.*)\..*$", name)
            name = m.group(1)
            base_face_encoding = face_recognition.face_encodings(base_image)[0]
            self.base_encodings.__setitem__(name, base_face_encoding)

    def faceRecog(self):
        # Initialize some variables
        face_locations = []
        face_encodings = []
        frame = self.readb64()

        # Resize frame of video to 1/4 size for faster face recognition processing
        # if  frame is not None:
        try:
            small_frame = cv2.resize(frame, (0, 0), fx=1/self.v_size, fy=1/self.v_size)
        except :
            print('error')
            return "error"
        face_locations = face_recognition.face_locations(small_frame)
        face_encodings = face_recognition.face_encodings(small_frame, face_locations)

        face_names = {}
        for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
            for base_name in self.base_encodings:
                base_encoding = self.base_encodings[base_name]
                match = face_recognition.compare_faces([base_encoding], face_encoding,tolerance=0.5)
                distance = face_recognition.face_distance([base_encoding], face_encoding)
                name = "unknow"
                if match[0]:
                    name = base_name
                    face_names.__setitem__(str(distance), name)
            if name != "unknow":
                for k in sorted(face_names.keys()):
                    print(face_names[k])
                    break
            else :
                print('unknow')
            return

if __name__ == "__main__":
    starttime = datetime.datetime.now()
    print(starttime)
    fd = faceDetectStream(sys.argv)
    fd.faceRecog()
    endtime = datetime.datetime.now()
    print(endtime - starttime)
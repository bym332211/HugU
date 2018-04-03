import os
import sys
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)

import base64
import io
import numpy as np
import face_recognition
import cv2

import re
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from PIL import Image


class faceDetectStream():
    # def readfile(self, args):
    #     self.getBaseEncodings()
    #     # filepath = str(args[1])
    #     filepath = 'D:\\demo\\img.txt'
    #     f = open(filepath, 'r')
    #     self.base64str = f.read()
    #     self.url = 0
    #     self.speed = 4
    #     self.v_size = 1

    def __init__(self):
        self.getBaseEncodings()

    def readb64(self):
        print("start readb64")
        imgdata = base64.b64decode(str(self.base64str))
        image = Image.open(io.BytesIO(imgdata))
        print(str(self.base64str))
        print("end readb64")
        return cv2.cvtColor(np.array(image), cv2.COLOR_BGR2RGB)

    def getBaseEncodings(self):
        path = "./input"
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

    def faceRecog(self, argstr):
        # Initialize some variables
        face_locations = []
        face_encodings = []
        if argstr:
            self.base64str = argstr
        frame = self.readb64()

        # Resize frame of video to 1/4 size for faster face recognition processing
        # if  frame is not None:
        try:
            # small_frame = cv2.resize(frame, (0, 0), fx=1/self.v_size, fy=1/self.v_size)
            small_frame = frame
        except :
            print('error')
            return "unknow"
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
            if face_names:
                for k in sorted(face_names.keys()):
                    result =  face_names[k]
                    print("found", face_names[k])
                    break
            else :
                print('unknow')
                result = 'unknow'
            return result

# if __name__ == "__main__":
#     starttime = datetime.datetime.now()
#     print(starttime)
#     fd = faceDetectStream(sys.argv)
#     fd.faceRecog()
#     endtime = datetime.datetime.now()
#     print(endtime - starttime)
fd = faceDetectStream()
class AjaxHandler(tornado.web.RequestHandler):
    def get(self):
        # fd.readfile('D:\\demo\\img.txt')
        argstr = self.get_argument("base64str")
        userName = fd.faceRecog(argstr)
        if userName:
            self.write(userName)
        else:
            self.write("unknow")

    def post(self):
        argstr = self.get_argument("base64str")
        userName = fd.faceRecog(argstr)
        if userName:
            self.write(userName)
        else:
            self.write("unknow")

class hello(tornado.web.RequestHandler):
    def get(self):
        self.write("hello")

def main():
        # a = abc()
        # a.start()
        # fd.readfile('D:\\demo\\img.txt')
        tornado.options.parse_command_line()
        # settings = {
        #     "static_path": os.path.join(os.path.dirname(__file__), "web/static")
        # }  # 配置静态文件路径
        application = tornado.web.Application([
            (r"/ajax", AjaxHandler),
            (r"/hello", hello),
        ])
        http_server = tornado.httpserver.HTTPServer(application)
        http_server.listen(82)
        tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()
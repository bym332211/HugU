import face_recognition
import cv2
from PIL import Image, ImageDraw
import _datetime
# This is a demo of running face recognition on live video from your webcam. It's a little more complicated than the
# other example, but it includes some basic performance tweaks to make things run a lot faster:
#   1. Process each video frame at 1/4 resolution (though still display it at full resolution)
#   2. Only detect faces in every other frame of video.

# PLEASE NOTE: This example requires OpenCV (the `cv2` library) to be installed only to read from your webcam.
# OpenCV is *not* required to use the face_recognition library. It's only required if you want to run this
# specific demo. If you have trouble installing it, try any of the other demos that don't require it instead.

# Get a reference to webcam #0 (the default one)
# url = 'http://192.168.0.105:8080/video'
# url = 'http://192.168.100.104:8080/video'
# url = './input/byb.mp4'
url = 0
alertfile = './alerm/alerm.wav'
fps = 0
output_video = False
output_img = False
speed = 4
v_size = 2.5
# v_size=1
alermFlg = False

huzi = cv2.imread("./input/huzi.jpg")
img = cv2.imread("./input/timg.jpg")
if url:
    while fps == 0:
        print('starting video capture')
        video_capture = cv2.VideoCapture(url)
        fps = video_capture.get(cv2.CAP_PROP_FPS)
else :
    video_capture = cv2.VideoCapture(url)

fourcc = video_capture.get(cv2.CAP_PROP_FOURCC)
exposure = video_capture.get(cv2.CAP_PROP_EXPOSURE)
print(exposure)
# video_capture.set(cv2.CAP_PROP_EXPOSURE, -0.5)

size = (int(video_capture.get(cv2.CAP_PROP_FRAME_WIDTH) / v_size), int(video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT) / v_size))

if output_video:
    output_movie = cv2.VideoWriter('./output/output.avi', -1, fps, size)

# videoWriter = cv2.VideoWriter('./byb/bybout.mp4', 6, fps, size)
# Load a sample picture and learn how to recognize it.
# base_image = face_recognition.load_image_file("./input/h.jpg")
# base_face_encoding = face_recognition.face_encodings(base_image)[0]

# Initialize some variables
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True

# Grab a single frame of video

cnt = 0
execcnt = 0
ret, frame = video_capture.read()

print(ret)
while ret:
    cnt += 1
    if not cnt % speed == 0:
        ret, frame = video_capture.read()
        continue
    execcnt += 1
    # Resize frame of video to 1/4 size for faster face recognition processing
    # if  frame is not None:
    try:
        small_frame = cv2.resize(frame, (0, 0), fx=1/v_size, fy=1/v_size)
    except :
        print('error')

    # Only process every other frame of video to save time
    if process_this_frame:
        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(small_frame)
        face_encodings = face_recognition.face_encodings(small_frame, face_locations)
        face_landmarks_list = face_recognition.face_landmarks(small_frame)


        face_names = []
        for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
            # match = face_recognition.compare_faces([base_face_encoding], face_encoding,tolerance=0.5)
            name = "Unknown"
            face_names.append(name)

    process_this_frame = not process_this_frame

    if execcnt % 4 == 0:
        if output_img:
            cv2.imwrite('./output/' + str(_datetime.datetime.now().strftime('%Y%m%d%H%M%S')) + "_Unknow"  + str(
                execcnt) + '.jpg', small_frame)

    # Display the results
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        # Scale back up face locations since the frame we detected in was scaled to 1/4 size
        # top *= 2
        # right *= 2
        # bottom *= 2
        # left *= 2

        # Draw a box around the face
        red = (0, 0, 255)
        green = (0, 255, 0)
        if name == 'Unknown':
            color = green
        else :
            color = red
        cv2.rectangle(small_frame, (left, top), (right, bottom), color, 2)

        # Draw a label with a name below the face
        cv2.rectangle(small_frame, (left, bottom - 15), (right, bottom), color, cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(small_frame, name, (left + 6, bottom - 6), font, 0.5, (255, 255, 255), 1)

        cv2.addWeighted(img, 0.7, img, 0.3, 0)
        if output_img:
            cv2.imwrite('./output/' + str(_datetime.datetime.now().strftime('%Y%m%d%H%M%S')) + "_" + str(name) + str(execcnt) + '.jpg', small_frame)

    # videoWriter.write(frame)  # 写视频帧
    # Display the resulting image
    try:
        cv2.imshow('Video', small_frame)
        if output_video:
            output_movie.write(small_frame)
    except :
        print('error')

    ret, frame = video_capture.read()
    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
print(cnt, execcnt)

# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()
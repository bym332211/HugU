import cv2

vc = cv2.VideoCapture(0)
ret, frame = vc.read()
print(ret)
while ret:
    cv2.imshow('test', frame)
    cv2.waitKey(1)
    exposure = vc.get(cv2.CAP_PROP_EXPOSURE)
    brightness = cv2.CAP_PROP_BRIGHTNESS
    print(exposure, brightness)
    cv2.CAP_PROP_AUTO_EXPOSURE
    vc.set(cv2.CAP_PROP_BRIGHTNESS, 15)
    ret, frame = vc.read()
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


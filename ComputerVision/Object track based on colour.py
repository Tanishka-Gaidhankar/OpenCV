import imutils  # Resize
import cv2

redLower = (36,100,50)
redUpper = (90,255,255)

camera = cv2.VideoCapture(0)  # Cam Ini

while True:

    (grabbed, frame) = camera.read()  # Read the Frame

    frame = imutils.resize(frame, width=1000)  # resize

    blurred = cv2.GaussianBlur(frame, (11, 11), 0)  # X - standard deviation

    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

    mask = cv2.inRange(hsv, redLower, redUpper)  # Mask the blue colour
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)

    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)[-2]
    center = None
    if len(cnts) > 0:
        c = max(cnts, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
        if radius > 10:
            cv2.circle(frame, (int(x), int(y)), int(radius),
                       (0, 255, 255), 2)
            cv2.circle(frame, center, 5, (0, 0, 255), -1)
            print("cm", center, radius)
            if radius > 250:
                print("stop")
            else:
                if (center[0] < 150):
                    print("Right")
                elif (center[0] > 450):
                    print("Left")
                elif (radius < 250):
                    print("Front")
                else:
                    print("Stop")

    cv2.imshow("Frame", frame)

    key = cv2.waitKey(1)
    if key == ord("q"):
        break

camera.release()
cv2.destroyAllWindows()

import cv2

haar_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")  # Loading Algorithm

cam = cv2.VideoCapture(0)  # Initializing camera id

while True:  # Infinite loop

    _, img = cam.read()  # Reading frame from camera

    grayImg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = haar_cascade.detectMultiScale(grayImg, 1.3, 4)  # Getting coordinates

    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 3)  # Drawing a rectangle

    cv2.imshow("FaceDetection", img)  # Display the frame

    key = cv2.waitKey(10)
    print(key)
    if key == ord("q"):
      break

cam.release()
cv2.destroyAllWindows()

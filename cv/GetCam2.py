import cv2

#IP camera information

cap = cv2.VideoCapture('http://192.168.0.101:15213/index')
cap = cv2.VideoCapture('http://192.168.0.101:15213/videostream.cgi?loginuse=admin&loginpas=wavesharespotpear')

if cap.isOpened():
    print('opened video stream successfully')


while (cap.isOpened()):
    ret, frame = cap.read()

    if not ret:
        print('did not receive frame')

    # Our operations on the frame come here
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Display the resulting frame
    cv2.imshow('frame', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()


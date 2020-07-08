import numpy as np
import cv2 as cv


def nothing(x):
    pass


def defineColor():
    global r
    global g
    global b
    img = np.zeros((300, 512, 3), np.uint8)
    cv.namedWindow('image')
    # create trackbars for color change
    cv.createTrackbar('R', 'image', 0, 255, nothing)
    cv.createTrackbar('G', 'image', 0, 255, nothing)
    cv.createTrackbar('B', 'image', 0, 255, nothing)
    # create switch for ON/OFF functionality
    next_step = '0 : OFF \n1 : O'
    cv.createTrackbar(next_step, 'image', 0, 1, nothing)
    while 1:
        cv.imshow('image', img)
        k = cv.waitKey(1) & 0xFF
        if k == 27:
            cv.destroyAllWindows()
            return None

        # get current positions of four trackbars
        r = cv.getTrackbarPos('R', 'image')
        g = cv.getTrackbarPos('G', 'image')
        b = cv.getTrackbarPos('B', 'image')
        turn_on = cv.getTrackbarPos(next_step, 'image')
        if turn_on == 1:
            return [r, g, b]

        img[:] = [b, g, r]


lower_color = np.array(defineColor())
upper_color = np.array(defineColor())

cap = cv.VideoCapture(0)
while 1:
    # Take each frame
    _, frame = cap.read()
    # Convert BGR to HSV
    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    # define range of blue color in HSV
    lower_blue = np.array([110, 50, 50])
    upper_blue = np.array([130, 255, 255])
    # Threshold the HSV image to get only blue colors
    mask = cv.inRange(hsv, lower_color, upper_color)
    # Bitwise-AND mask and original image
    res = cv.bitwise_and(frame, frame, mask=mask)
    cv.imshow('frame', frame)
    cv.imshow('mask', mask)
    cv.imshow('res', res)
    k = cv.waitKey(5) & 0xFF
    if k == 27:
        break
cv.destroyAllWindows()

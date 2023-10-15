import math
import cv2
import numpy as np
# import mouse
from playsound import playsound
from threading import Thread
from ast import literal_eval
# from pynput.mouse import Button, Controller
import pyautogui
import time

pyautogui.FAILSAFE = False

X  = 0
Y = 0
PX = 0
PY = 0
DOWN = False
PREVDOWN = False

def warpImage(image, points):
    src_pts = np.float32(points)
    dst_pts = np.float32([[0, 0], [1000, 0], [1000, 1000], [0, 1000]])

    mat = cv2.getPerspectiveTransform(src_pts, dst_pts)

    warped_image = cv2.warpPerspective(image, mat, (1000, 1000))

    return warped_image

def start(root, pointsstr, maskparamsmalformed, width, height):
    global X 
    global Y 
    global PX  
    global PY
    global DOWN
    global PREVDOWN
    points = literal_eval(pointsstr)
    maskparamsstr = ''.join([letter for letter in maskparamsmalformed if letter not in("array()")])
    maskparams = literal_eval(maskparamsstr)

    lower, upper = np.array(maskparams[0]), np.array(maskparams[1])
    
    root.withdraw()

    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Could not open camera.")
        exit()

    hold = []
    count = 0
    drawmode = False
    previous = None

    while True:
        check, frame = cap.read()
        if not check:
            break

        frame = warpImage(frame, points)  # Warp the frame

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        _, binary = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY)

        contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        pts = None
        contourpts = []

        if len(contours) != 0:
            for contour in contours:
                if cv2.contourArea(contour) > 10:
                    x, y, w, h = cv2.boundingRect(contour)
                    x = (x+(x+w))//2
                    y = (y+(y+h))//2
                    pts = (x, y)
                    contourpts.append(pts)

        check = set(contourpts)

        if len(check) > 1:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            gray = cv2.GaussianBlur(gray, (5,5), 0)
            minv, maxv, minl, maxl = cv2.minMaxLoc(gray)
            pts = maxl

        if not setHold(count, hold, pts):
            count += 1

        if pts is not None:
            getHoldVar = getHold(hold)
            # print(f"gethold var, {getHoldVar}")
            if getHold(hold):
                count = 0
                drawmode = changeMode(drawmode)

            # print(f"draw mode {drawmode},   {pts}")
            PX = X
            PY = Y 
            X =  pts[0]
            Y = pts[1]
            PREVDOWN = DOWN
            DOWN = True
            # if drawmode:
            #     temp = draw(pts, width, height, previous)
            #     previous = temp
            # else:
            drag(X, Y, PX, PY, DOWN,  width, height)
            pyautogui.mouseDown()
        else:
            if drawmode:
                # mouse.release("left")
                previous = None
                pyautogui.mouseUp()
            else:
                # print("release mouse")
                # mouse.release("left")
                DOWN = False
                pyautogui.mouseUp()
        print(f"down {DOWN}, x and y, {X},{Y}")
        blank = np.ones((300, 300))
        cv2.putText(blank, "Press ESC to quit", (20, 150), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 0), 1, cv2.LINE_AA)
        cv2.imshow("Lightscreen", blank)
        
        if cv2.waitKey(1) & 0xFF == 27:
            break
        if cv2.getWindowProperty("Lightscreen", cv2.WND_PROP_VISIBLE) < 1:
            break

    cap.release()
    cv2.destroyAllWindows()
    root.deiconify()


def setHold(count, hold, pts):
    if count < 20:
        hold.append(pts)
        return False
    else:
        hold.append(pts)
        hold.pop(0)
        return True

def getHold(hold):
    if None not in hold and len(hold) == 20:
        res = 0
        for p in hold:
            holdcopy = hold.copy()
            holdcopy.remove(p)
            cur = max([(math.sqrt((p[0]-c[0])**2+(p[1]-c[1])**2)) for c in holdcopy])
            if cur > res:
                res = cur
        if res < 5:
            hold.clear()
            return True
    return False

def changeMode(drawmode):
    # Thread(target=lambda:sound(drawmode)).start()
    if drawmode:
        return False
    else:
        return True
    
# def sound(drawmode):
#     print("play sound")
#     return None

# def sound2(drawmode):
#     if drawmode:
#         playsound("/home/rpi2/Desktop/lightscreen-touchscreen-detection/data/sound/dragging.mp3")
#     else:
#         playsound("/home/rpi2/Desktop/lightscreen-touchscreen-detection/data/sound/drawing.mp3")


def drag(x, y, px,py, down, w, h):
    global PREVDOWN
    if down:
        x = (x/1000)*w 
        y = (y/1000)*h
        if PREVDOWN  == False: 
            pyautogui.moveTo(x, y)
            PREVDOWN = down
        pyautogui.moveTo(x,y)
        # mouse.drag(x, y, px,py)
    # x = (pos[0]/1000)*w 
    # y = (pos[1]/1000)*h
    # print("drag")
    # mouse.drag(x, y)
    # pyautogui.click()
    # mouse.click()
    # mouse2.press(Button.left)

# def draw(pos, w, h, previous):
#     print("draw")
#     x = (pos[0]/1000)*w
#     y = (pos[1]/1000)*h
#     mouse.move(x, y, True)

#     if previous is not None:
#         mouse.drag(previous[0], previous[1], x, y)
#     return (x,y)
# def draw(pos, w, h, previous):
#     print("draw")
#     x = (pos[0] / 1000) * w
#     y = (pos[1] / 1000) * h

#     if previous is not None:
#         # Calculate the number of intermediate points
#         num_points = int(max(abs(x - previous[0]), abs(y - previous[1])))
#         if num_points == 0:
#             num_points = 1

#         # Calculate the step size for each intermediate point
#         step_x = (x - previous[0]) / num_points
#         step_y = (y - previous[1]) / num_points

#         # Generate and move the cursor through the intermediate points
#         for i in range(num_points + 1):
#             intermediate_x = previous[0] + i * step_x
#             intermediate_y = previous[1] + i * step_y
#             mouse.move(intermediate_x, intermediate_y)
#             # time.sleep(0.01)  # Adjust the sleep duration for smoother drawing

#     # Move the cursor to the final position
#     mouse.move(x, y)
#     return (x, y)

import numpy as np
from PIL import ImageGrab
import cv2
import cv2 as cv
import time
from directkeys import ReleaseKey, PressKey, W, A, S, D
import math

# 영상에서 라인(차선)을 인식straight하고 그려주는 함수
def draw_lines(img, lines):
    try:
        if lines is not None:
            for i in range(0, len(lines)):
                rho = lines[i][0][0]
                theta = lines[i][0][1]
                a = math.cos(theta)
                b = math.sin(theta)
                x0 = a * rho
                y0 = b * rho
                x1 = int(x0 + 1000 * (-b))
                y1 = int(y0 + 1000 * (a))
                x2 = int(x0 - 1000 * (-b))
                y2 = int(y0 - 1000 * (a))

                pt1 = (x1, y1)
                pt2 = (x2, y2)
                cv.line(img, pt1, pt2, (0, 0, 255), 2, cv.LINE_AA)

                if a>=0 :
                    right()
                    print('right')

                    PressKey(S)
                    time.sleep(0.1)
                    ReleaseKey(S)
                elif a<0 :
                    left()
                    print('left')

                    PressKey(S)
                    time.sleep(0.1)
                    ReleaseKey(S)
        '''
        for line in linesP:
            coords = line[0]
            pt1 = (coords[0], coords[1])
            pt2 = (coords[2], coords[3])
            cv2.line(img, pt1, pt2, [0,0,255], 3, cv.LINE_AA)
        '''


    except:
        pass

def roi(img, vertices):
    # img 크기만큼의 영행렬을 mask 변수에 저장하고
    mask = np.zeros_like(img)

    # vertices 영역만큼의 Polygon 형상에만 255의 값을 넣습니다
    cv2.fillPoly(mask, vertices, [255, 255, 255])

    # img와 mask 변수를 and (비트연산) 해서 나온 값들을 masked에 넣고 반환합니다
    masked = cv2.bitwise_and(img, mask)
    return masked


def process_img(original_image):  # 원본: 200 300 180

    original_image = cv2.resize(original_image, (500, 350))  # 원본 Window 리사이즈

    processed_img = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)
    processed_img = cv2.Canny(processed_img, threshold1=50, threshold2=300)  # GRAY

    c_img = cv.cvtColor(processed_img, cv.COLOR_GRAY2BGR)

    # ROI 구간 설정
    vertices = np.array([[10, 320], [10, 260], [240, 220], [260, 220], [500, 260], [500, 320]])

    # roi()를 사용해 그 영역만큼 영상을 자릅니다
    processed_img = roi(processed_img, [vertices])
    c_img = roi(c_img, [vertices])

    # Line
    lines = cv2.HoughLines(processed_img, 1, np.pi / 180, 120)
    draw_lines(c_img, lines)   # cv.line()

    return processed_img, c_img


# 전진하는 함수 (W)
def straight():
    PressKey(W)
    time.sleep(0.8)
    ReleaseKey(W)

    ReleaseKey(A)
    ReleaseKey(D)

# 좌측으로 이동하는 함수 (A)
def left():
    PressKey(A)
    time.sleep(0.2)
    ReleaseKey(A)
    ReleaseKey(W)
    ReleaseKey(D)


# 우측으로 이동하는 함수(D)
def right():
    PressKey(D)
    time.sleep(0.2)
    ReleaseKey(D)
    ReleaseKey(A)
    ReleaseKey(W)

# countDown
for i in list(range(3))[::-1]:
    print(i + 1)
    time.sleep(1)

while (True):
    straight()
    print('straight')

    # 화면의 0,80 좌표로 부터 800*600 사이즈의 크기를 캡처한다.
    screen = np.array(ImageGrab.grab(bbox=(0, 80, 800, 600)))   # PIL.imageGrab()
    new_screen, c_img = process_img(screen)     # ROI넣고, Line넣은 가공된 이미지

    #cv2.imshow('window', new_screen)
    cv.imshow("Detected Lines (in red) - Standard Hough Line Transform", c_img)

    # q를 누르면 종료된다.
    if cv2.waitKey(25) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
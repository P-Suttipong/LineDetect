import numpy as np
import cv2
    
    
img = cv2.imread('sideroad.jpg')

scale_percent = 30
width = int(img.shape[1] * scale_percent / 100)
height = int(img.shape[0] * scale_percent / 100)
dim = (width, height)

print(dim)

if(img.shape[1] > 1600):
    resized = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
    crop = resized[0:height, int((width/2)-int(width*0.2)) : int((width/2)+int(width*0.2))]
else:
    resized = img
    crop = resized[0:img.shape[0], int((img.shape[1]/2)-int(img.shape[1]*0.2)) : int((img.shape[1]/2)+int(img.shape[1]*0.2))]

gray = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)
edges = cv2.Canny(gray,250,200)
if(cv2.HoughLines(edges, 1, np.pi/180.0, 100, np.array([])).any() != None):
    lines = cv2.HoughLines(edges, 1, np.pi/180.0, 100, np.array([]))
else:
    lines = [[]]


R = 0
G = 0
B = 0

countRoadLine = 0

for line in lines:
    rho, theta = line[0]
    a = np.cos(theta)
    b = np.sin(theta)
    x0 = a*rho
    y0 = b*rho
    x1 = int(x0 + 1000*(-b))
    y1 = int(y0 + 1000*(a))
    x2 = int(x0 - 1000*(-b))
    y2 = int(y0 - 1000*(a))

    p1 = (x1, y1)
    p2 = (x2, y2)

    print(p1,p2)

    if(x2 - x1 != 0):
        m = (y2-y1)/(x2-x1)
        # print(abs(m))
    else: m = 0

    if(abs(m) > 2):
        # print("Side Road")
        R = 255
        B = 0
        countRoadLine = countRoadLine + 1
        # print(p1,p2)
    else:
        R = 0
        B = 255

    cv2.line(crop,(x1,y1),(x2,y2),(B,G,R),2)

if(countRoadLine > 0):
    print("PARK AT SIDE RODE")
else :
    print("None")
    

cv2.imshow('Original',resized)
cv2.imshow('crop',crop)
cv2.waitKey(0)
cv2.destroyAllWindows()
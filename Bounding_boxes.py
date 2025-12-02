#need to figure out best way to implement this into existing codebase

import pytesseract
import cv2
def bbox():
    """
    bounding box detection
    """
    image = cv2.imread("./index_02.JPG")
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur =cv2.GaussianBlur(gray,(7,7),0)
    thresh = cv2.threshold(blur,0,225,cv2.THRESH_BINARY_INV +cv2.THRESH_OTSU)[1]
    kernal = cv2.getStructuringElement(cv2.MORPH_RECT, (3,13))
    dilate = cv2.dilate(thresh,kernal,iterations=1)
    cnts = cv2.findContours(dilate,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    cnts = sorted(cnts, key=lambda x: cv2.boundingRect(x)[0])
    for c in cnts:
        x,y,w,h = cv2.boundingRect(c)
        if h > 200 and w > 20:
            roi = image[y:y+h, x:x+h]
            cv2.imwrite("./index_02_roi.JPG", roi)
            cv2.rectangle(image, (x,y),(x+w,y+h), (36, 255, 12),2)


    cv2.imwrite("new_copy.png", image)

bbox()
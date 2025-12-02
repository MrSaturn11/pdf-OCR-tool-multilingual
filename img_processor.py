import cv2 
import numpy as np

class OCRProcessor:
    def __init__(self, path):
        self.img = cv2.imread(path)
        if self.img is None:
            raise FileNotFoundError(f"could not find image {path}")

    def show_img(self):
        """
        displays the current stored image  
        """
        cv2.namedWindow("Preview", cv2.WINDOW_NORMAL)
        cv2.imshow("Preview", self.img)
        cv2.waitKey(0)
        return self.img
    
    def invert(self):
        """
        invert colors
        """
        self.img = cv2.bitwise_not(self.img)
        return self.img
    
    def gray(self):
        """
        grayscale image
        """
        if len(self.img.shape) ==3:
            self.img = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
        return self.img
    
    def bw(self):
        """
        black & white threshold
        """
        if len(self.img.shape) == 3:
            self.gray()
        _, self.img = cv2.threshold(self.img, 200, 255, cv2.THRESH_BINARY)
        return self.img
    
    def noise_removal(self):
        """
        removes noise
        """
        kernel = np.ones((1,1), np.uint8)
        image = cv2.dilate(self.img, kernel, iterations=1)
        image = cv2.erode(image, kernel, iterations=1)
        image = cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel)
        self.img = cv2.medianBlur(image, 3)

        return self.img
    
    def thicken(self):
        """
        thickens font
        """
        image = cv2.bitwise_not(self.img)
        kernel = np.ones((3,3), np.uint8)
        image = cv2.dilate(image, kernel, iterations=1)
        self.img = cv2.bitwise_not(image)
        return self.img
    
    def remove_borders(self, shrink=0): 
        """
        Removes whitespace borders by cropping to the combined area of all text/content.
        """
        if len(self.img.shape) == 3:
            gray = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
        else:
            gray = self.img

        edges = cv2.Canny(gray, 50, 150)

        kernel = np.ones((5,5), np.uint8)
        dilated = cv2.dilate(edges, kernel, iterations=3)

        contours, _ = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        if len(contours) == 0:
            return self.img


        h_img, w_img = self.img.shape[:2]
        min_x, min_y = w_img, h_img
        max_x, max_y = 0, 0

        found_content = False

        for cnt in contours:
            if cv2.contourArea(cnt) > 200: 
                found_content = True
                x, y, w, h = cv2.boundingRect(cnt)
                
                min_x = min(min_x, x)
                min_y = min(min_y, y)
                max_x = max(max_x, x + w)
                max_y = max(max_y, y + h)

        if not found_content:
            return self.img

       
        x_new = max(0, min_x + shrink)
        y_new = max(0, min_y + shrink)
        
        w_new = (max_x - shrink) - x_new
        h_new = (max_y - shrink) - y_new

        if w_new <= 0 or h_new <= 0:
            return self.img 

        self.img = self.img[y_new:y_new+h_new, x_new:x_new+w_new]

        return self.img

    def getSkewAngle(self) -> float:
        """
        compute skew angle
        """
        newImage = self.img.copy()

        if len(newImage.shape) ==3:
            gray = cv2.cvtColor(newImage, cv2.COLOR_BGR2GRAY)
        else:
            gray = newImage
        
        blur = cv2.GaussianBlur(gray, (9, 9), 0)
        thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (30, 5))
        dilate = cv2.dilate(thresh, kernel, iterations=5)

        contours, _ = cv2.findContours(dilate, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        contours = sorted(contours, key=cv2.contourArea, reverse=True)

        minAreaRect = cv2.minAreaRect(contours[0])
        angle = minAreaRect[-1]

        if angle < -45:
            angle = 90 + angle

        return -angle

    def rotateImage(self, angle: float):
        """
        rotate image around center
        """
        (h, w) = self.img.shape[:2]
        center = (w // 2, h // 2)
        M = cv2.getRotationMatrix2D(center, angle, 1.0)
        self.img = cv2.warpAffine(self.img, M, (w, h), flags=cv2.INTER_CUBIC,
                                  borderMode=cv2.BORDER_REPLICATE)

    
        return self.img

    def deskew(self):
        """
        fix image tilt automatically
        """
        angle = self.getSkewAngle()
        corrected_angle = -angle
        self.rotateImage(corrected_angle)
    






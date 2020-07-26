import numpy as np
import cv2
import imutils
import sys
import pytesseract
import pandas as pd
import time

image = cv2.imread('v1.jpg')

image = imutils.resize(image, width=500)

cv2.imshow("Original Image", image)


gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
cv2.imshow("1 - Grayscale Conversion", gray)

gray = cv2.bilateralFilter(gray, 11, 17, 17)
#cv2.imshow("2 - Bilateral Filter", gray)

edged = cv2.Canny(gray, 170, 200)
cv2.imshow("4 - Canny Edges", edged)
contours, hierarchy = cv2.findContours(edged, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
#(new, cnts, _) = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
contours=sorted(contours, key = cv2.contourArea, reverse = True)[:30] 
NumberPlateCnt = None 

count = 0
for c in contours:
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c,0.02 * peri, True)
        if len(approx) == 4:  
            NumberPlateCnt = approx 
            break

# Masking the part other than the number plate
mask = np.zeros(gray.shape,np.uint8)
new_image = cv2.drawContours(mask,[NumberPlateCnt],0,255,-1)
new_image = cv2.bitwise_and(image,image,mask=mask)
cv2.namedWindow("Final_image",cv2.WINDOW_NORMAL)
cv2.imshow("Final_image",new_image)

from datetime import datetime
# datetime object containing current date and time
now = datetime.now()
 
#print("current time and date =", now)
# dd/mm/YY H:M:S
dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
print("date and time =", dt_string)

from PIL import Image
from pytesseract import image_to_string

#tesseract image.jpg stdout -l eng --oem 1 --psm 3
#Configuration for tesseract
config = ('-l eng --oem 1 --psm 3')

tesseract_cmd = 'C:\\Program Files (x86)\\Tesseract-ORC\\tesserect'
#Run tesseract OCR on image
text = pytesseract.image_to_string(new_image, config=config)

#Data is stored in CSV file
raw_data = {'date': dt_string, 
        'v_number': [text]}

df = pd.DataFrame(raw_data, columns = ['date', 'v_number'])
#df.to_csv('empdata.csv')
# Print recognized text
print(text)

str_y=text;
 
emp_list = ['MH12DE1433','| HR26DK8337]','KL 65K 7111']
emp_list.sort()        

if str_y in emp_list:
        print ("employee vehicle")
        df.to_csv('empdata.csv')
else :
        print ("visiter vehicle")
        df.to_csv('carflow.csv')
        
cv2.waitKey(0)

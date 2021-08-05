import cv2
import json
import random
import sys, os
import operator
from PIL import Image

# 執行此檔可以開啟攝像頭收集training data(圖片)
# 注意勿開啟過久，會存入大量圖片

CLIP_X1,CLIP_Y1,CLIP_X2,CLIP_Y2 = 160,140,400,360

cap = cv2.VideoCapture(0)
i = 0
wzs = 158
image_q = cv2.THRESH_BINARY

while True:
    _, FrameImage = cap.read()
    FrameImage = cv2.flip(FrameImage, 1)
    cv2.imshow("", FrameImage)
    cv2.rectangle(FrameImage, (CLIP_X1, CLIP_Y1), (CLIP_X2, CLIP_Y2), (0,255,0) ,1)

    ROI = FrameImage[CLIP_Y1:CLIP_Y2, CLIP_X1:CLIP_X2]
    ROI = cv2.resize(ROI, (128, 128))
    ROI = cv2.cvtColor(ROI, cv2.COLOR_BGR2GRAY)
    _, output = cv2.threshold(ROI, wzs, 255, image_q)
    
    SHOWROI = cv2.resize(ROI, (256, 256))
    _, output2 = cv2.threshold(SHOWROI, wzs, 255, image_q)
    cv2.imshow("ROI", output2)

    #將檔案以.jpg存入/test/資料夾中
    cv2.imwrite('./test/'+str(i)+'.jpg',output2) 
    i += 1
    cv2.waitKey(100)

    interrupt = cv2.waitKey(10)
    if interrupt & 0xFF == ord('q'): #按q關閉視窗
        break

cap.release()
cv2.destroyAllWindows()

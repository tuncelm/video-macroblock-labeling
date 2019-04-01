#
# Written by Mehmet Tuncel Copyright (C)
# Date: 23.01.2019
# Filename: macroBlockLabelling
# Version: 1.0
# How to run:
#    python3  macroBlockLabelling_v1.1.py forest_fire.h264 fire.txt
# Keyboards:
# n: next frame
# r: reload
# w: write recorded macroblock numbers
# q: quit
# s: switch between erasing and drawing

import cv2
import numpy as np
import sys

drawing = False    # True if the left button of mouse is pressed.
erasing = False   # True if the right button of mouse is pressed.
switch = 1

# Mouse callback function.
def draw_circle(event,x,y,flags,param):
    global drawing
    global erasing
    global fire
    global switch

    if switch:
            # Drawing
	    if event == cv2.EVENT_LBUTTONDOWN:
	        drawing = True

	    elif event == cv2.EVENT_MOUSEMOVE:
	        if drawing == True and (0 <= x < wImage) and (0 <= y < hImage):
	            #print "%d,%d" % (x,y)
	            x = x - (x % 16)
	            y = y - (y % 16)
	            cv2.rectangle(img,(x,y),(x+16,y+16),(0,0,255),1)
	            fire[y//16, x//16] = 1

	    elif event == cv2.EVENT_LBUTTONUP:
	        drawing = False
	        #print "%d,%d" % (x,y)
	        if (0 <= x < wImage) and (0 <= y < hImage):
	            x = x - (x % 16)
	            y = y - (y % 16)
	            cv2.rectangle(img,(x,y),(x+16,y+16),(0,0,255),1)
	            fire[y//16, x//16] = 1
    else:
	    # Erasing.
	    if event == cv2.EVENT_LBUTTONDOWN:
	        erasing = True

	    elif event == cv2.EVENT_MOUSEMOVE:
	        if erasing == True and (0 <= x < wImage) and (0 <= y < hImage):
	            #print "%d,%d" % (x,y)
	            x = x - (x % 16)
	            y = y - (y % 16)
	            cv2.rectangle(img,(x,y),(x+16,y+16),(0,255,0),1)
	            fire[y//16, x//16] = 0;

	    elif event == cv2.EVENT_LBUTTONUP:
	        erasing = False
	        #print "%d,%d" % (x,y)
	        if (0 <= x < wImage) and (0 <= y < hImage):
	            x = x - (x % 16)
	            y = y - (y % 16)
	            cv2.rectangle(img,(x,y),(x+16,y+16),(0,255,0),1)
	            fire[y//16, x//16] = 0;

def reloadImage(img, imgCopy,hMacroblock, wMacroblock):
    img[:] = imgCopy
    for i in range(hMacroblock):
        for j in range(wMacroblock):
             if fire[i,j] == 1:
                x = i*16
                y = j*16
                cv2.rectangle(img,(y,x),(y+16,x+16),(0,0,255),1)



def appendFile(fire,count,hMacroblock,wMacroblock,f):
    macroblockRecordNumber = 0
    for i in range(hMacroblock):
        for j in range(wMacroblock):
            if fire[i,j] == 1:
                macroblockRecordNumber = macroblockRecordNumber + 1

    iter = 0
    if macroblockRecordNumber > 0:
        f.write("%d: " % count)
        for i in range(hMacroblock):
            for j in range(wMacroblock):
                if fire[i,j] == 1:
                    iter = iter + 1
                    if iter == macroblockRecordNumber:
                        f.write("%d;\n" % (j + i*wMacroblock))
                    else:
                        f.write("%d, " % (j + i*wMacroblock))

f = open(str(sys.argv[2]), "a")

cv2.namedWindow("image",1)
#img = cv2.imread("image.jpg");
#hImage, wImage = img.shape[:2]

cap = cv2.VideoCapture(str(sys.argv[1]))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
fps = int(cap.get(cv2.CAP_PROP_FPS))
hImage = frame_height
wImage = frame_width

print('frame width is %d px frame height is %d px ' % (frame_width, frame_height))
print('frame length is %d ' %(frame_length))
print('The video is %d fps' %(fps))


hMacroblock = int(np.ceil(hImage/16.0))
wMacroblock = int(np.ceil(wImage/16.0))
macroblockNumber = hMacroblock * wMacroblock
print ("%d,%d - %d" % (hImage,wImage,macroblockNumber))
print ("%d,%d - %d" % (hMacroblock,wMacroblock,macroblockNumber))


ret,img = cap.read()
cv2.imshow('image',img)   
print ("Frame: 0 ")  
count = 0
c = ''

fire = np.zeros((hMacroblock, wMacroblock), np.uint8)
imgCopy = np.array(img)

cv2.setMouseCallback('image',draw_circle)



while(cap.isOpened()):
    #cv2.imshow('image',img)
    c = chr(cv2.waitKey(20) & 0xFF)
    if ret==True:    
        cv2.imshow('image',img)
        #cv2.imwrite("frame%d.jpg" % count, frame)

        while c == 'n':
            c = ''
            count = count + 1
            ret,img = cap.read()
            imgCopy = np.array(img)
            fire = np.zeros((hMacroblock, wMacroblock), np.uint8)      
            print ("Frame: %d " % count )
        if c == 'r':
            reloadImage(img, imgCopy,hMacroblock, wMacroblock)
        if c == 'w':
            appendFile(fire,count,hMacroblock,wMacroblock,f)
            print("    Written ")
            
            for i in range(hMacroblock):
               for j in range(wMacroblock):
                 if fire[i,j] == 1:
                    print("%d, " % (j + i*wMacroblock),end=''),
            print("")
        if c == 's':
            switch = (switch + 1) % 2
            
    else:
        break

    if c == 'q':
        break

f.close()    
cap.release()
cv2.destroyAllWindows()

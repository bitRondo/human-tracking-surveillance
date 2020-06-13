import numpy as np
import cv2 as cv
import Person
import time
import threading

from .videoAnalysis import Analyzer
from .Person import MyPerson

    

class HumanTrackingSystem(threading.Thread):
    lock = threading.Lock()
    outputFrame = None
    def __init__(self):
        threading.Thread.__init__(self,  name = "HumanTracker", daemon=True)
        

    def run(self):  

        cap = cv.VideoCapture('Test Files/testvideo.mp4')

        h = 480
        w = 640
        frameArea = h*w
        areaTH = frameArea/250

        up_limit = int(h/5)
        down_limit = int(4*h/5)
        left_limit = int(w/5)
        right_limit = int(4*w/5)


        #Background Substractor
        fgbg = cv.createBackgroundSubtractorMOG2(detectShadows = True)

        #Structuring elements for morphographic filters
        kernelOp = np.ones((3,3),np.uint8)
        kernelOp2 = np.ones((5,5),np.uint8)
        kernelCl = np.ones((11,11),np.uint8)

        #Variables
        persons = []
        max_p_age = 40
        pid = 1

        while(True):
            if (not cap.isOpened()):
                cap = cv.VideoCapture('Test Files/TestVideo.avi')

            ret, frame = cap.read()

            for i in persons:
                i.age_one() #age every person one frame


            #Apply background subtraction
            fgmask = fgbg.apply(frame)
            fgmask2 = fgbg.apply(frame)

            #Binariazcion to remove shadows (gray color)
            try:
                ret,imBin= cv.threshold(fgmask,200,255,cv.THRESH_BINARY)
                ret,imBin2 = cv.threshold(fgmask2,200,255,cv.THRESH_BINARY)
                #Opening (erode-> dilate) to remove noise.
                mask = cv.morphologyEx(imBin, cv.MORPH_OPEN, kernelOp)
                mask2 = cv.morphologyEx(imBin2, cv.MORPH_OPEN, kernelOp)
                #Closing (dilate -> erode) to join white regions.
                mask =  cv.morphologyEx(mask , cv.MORPH_CLOSE, kernelCl)
                mask2 = cv.morphologyEx(mask2, cv.MORPH_CLOSE, kernelCl)
            except:
                break

            #RETR_EXTERNAL returns only extreme outer flags. All child contours are left behind.
            contours, hierarchy = cv.findContours(mask2,cv.RETR_EXTERNAL,cv.CHAIN_APPROX_SIMPLE)
            for cnt in contours:
                area = cv.contourArea(cnt)
                if area > areaTH:

                    M = cv.moments(cnt)
                    cx = int(M['m10']/M['m00'])
                    cy = int(M['m01']/M['m00'])
                    x,y,w,h = cv.boundingRect(cnt)

                    new = True
                    for i in persons:
                        if abs(x-i.getX()) <= w and abs(y-i.getY()) <= h:       # the object is close to one that was detected before
                            
                            new = False
                            i.updateCoords(cx,cy)

                    if new == True:
                        Analyzer.increment()
                        p = Person.MyPerson(pid,cx,cy, max_p_age)
                        persons.append(p)
                        pid += 1

                    cv.circle(frame,(cx,cy), 5, (0,0,255), -1)
                    img = cv.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)

            for i in persons:
                if i.age>i.max_age:
                    index = persons.index(i)
                    persons.pop(index)
                    del i  

            with self.lock:
                outputFrame = frame.copy()

        cap.release()
        cv.destroyAllWindows()
        
    def generate(self):
        # grab global references to the output frame and lock variables
        global outputFrame, lock

        # loop over frames from the output stream
        while True:
            # wait until the lock is acquired
            with self.lock:
                # check if the output frame is available, otherwise skip
                # the iteration of the loop
                if outputFrame is None:
                    continue

                # encode the frame in JPEG format
                (flag, encodedImage) = cv2.imencode(".jpg", outputFrame)

                # ensure the frame was successfully encoded
                if not flag:
                    continue

            # yield the output frame in the byte format
            yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + 
                bytearray(encodedImage) + b'\r\n')

    def video_feed():
	# return the response generated along with the specific media
	# type (mime type)
	    return Response(generate(),
		    mimetype = "multipart/x-mixed-replace; boundary=frame")
    # k = cv.waitKey(30) & 0xff
    # if k == 27:
    #     break
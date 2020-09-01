import numpy as np
import cv2 as cv
import time
import threading
from .Person import Person

from django.http import StreamingHttpResponse 
from  django.views.decorators import gzip

lock = threading.Lock()
outputFrame = None

newPersons=0

class HumanTrackingSystem(threading.Thread):


    def __init__(self):
        threading.Thread.__init__(self,  name = "HumanTracker", daemon=True)
        

    def run(self):  
        people=0
        cap = cv.VideoCapture('videoAnalysis/Test Files/TestVideo.mp4')
        h = 480
        w = 640
        frameArea = h*w
        areaTH = frameArea/250

        #Background Substractor
        fgbg = cv.createBackgroundSubtractorMOG2(detectShadows = True)

        #Structuring elements for morphographic filters
        kernelOp = np.ones((3,3),np.uint8)
        kernelOp2 = np.ones((5,5),np.uint8)
        kernelCl = np.ones((11,11),np.uint8)
 
        #Variables
        persons = []
        maxAge = 40
        pid = 1
        frameCounter = 0
        while(True):
            frameCounter+=1
            if frameCounter == cap.get(cv.CAP_PROP_FRAME_COUNT):
                frameCounter = 0
                cap.set(cv.CAP_PROP_POS_FRAMES, 0)
            ret, frame = cap.read()

            
            for i in persons:
                i.ageOneFrame() #age every person one frame


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

                    moment = cv.moments(cnt)
                    cx = int(moment['m10']/moment['m00'])
                    cy = int(moment['m01']/moment['m00'])

                    x,y,w,h = cv.boundingRect(cnt)

                    newTracker = True
                    for i in persons:
                        if abs(cx-i.getX()) <= w and abs(cy-i.getY()) <= h:       # the object is close to one that was detected before
                            
                            newTracker = False
                            i.updateCoords(cx,cy)

                    if newTracker == True:
                        global lock,newPersons
                        newPersons+=1
                        people+=1
                        p = Person(pid,cx,cy, maxAge)
                        persons.append(p)
                        pid += 1

                    centroid = cv.circle(frame,(cx,cy), 5, (0,0,255), -1)
                    boundingBox = cv.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
            cv.putText(frame,str(people),(10,30),cv.FONT_HERSHEY_SIMPLEX,1,(209, 80, 0, 255),2,cv.LINE_AA)
            #delete old trackers
            index=0
            while True:
                if index==len(persons):
                    break
                if persons[index].age>persons[index].maxAge:
                    temp = persons.pop(index)
                    del temp
                else:
                    index+=1  
            
            with lock:
                 global outputFrame
                 outputFrame = frame.copy()

            #cv.imshow('Frame',frame)
            k = cv.waitKey(30) & 0xff
            if k == 27:
                break
        cap.release()
        cv.destroyAllWindows()



    
def getNew():
    global newPersons
    temp=newPersons
    newPersons=0
    return temp

def getFrame():
    ret, jpeg = cv.imencode('.jpg', outputFrame)
    return jpeg.tobytes()









# def generate():
#     global outputFrame,lock
#     # loop over frames from the output stream
#     while True:
#         # wait until the lock is acquired
#         yield(b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

# @gzip.gzip_page
# def video_feed(request):
#     print ("video")
# # return the response generated along with the specific media
# # type (mime type)
#     return StreamingHttpResponse(generate(),content_type="multipart/x-mixed-replace;boundary=frame")
#     # k = cv.waitKey(30) & 0xff
#     # if k == 27:
#     #     break
#     #,streaming_content = "multipart/x-mixed-replace; boundary=frame"


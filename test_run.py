# ~/virtualenv/ROBOTICS_studios/bin



'''*************************************************
*                                                  *
*             import class & library               *
*                                                  *
*************************************************'''
import sys
import os

import cv2

from detect_haarCascade import haarCascade

def connectCamera():
    cap = cv2.VideoCapture(0)
    while 1:
        ret, frame = cap.read()

        if ret == None:
            sys.exit("can't connect camera")
        else :
            frame2 = hc.detectHaarCascade(frame)
            cv2.imshow('frame',frame)
            cv2.imshow('frame2',frame2)
            if cv2.waitKey(1)& 0xff == ord('q'):
                cv2.destroyAllWindows()
                cap.release()
                break

hc = haarCascade()
# connectCamera()
hc.deleteCascadeFile()
# hc.deleteMainCascadeFile()
hc.copyCascadeFile()


hc.testCascade()

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

def main():

    inputKey = str(sys.argv[0])
    hc = haarCascade()
    # connectCamera()
    # hc.deleteCascadeFile()
    # hc.deleteMainCascadeFile()
    # hc.copyCascadeFile()
    # hc.testCascade()

    if inputKey == '' or inputKey == 'help' :
        sys.exit('python [param]\nmethod:\t 1 or renewCascade\n\t\t 2 or test\n\t\t3 or removeAllCascade\n')

    elif inputKey == '1' or inputKey == 'renewCascade' :
        '''remove old cascade files and copy new cascade files.'''
        hc.deleteCascadeFile()
        hc.copyCascadeFile()

    elif inputKey == '2' or inputKey == 'test':
        ''' test cascade accuracy file files.'''
        hc.testCascade()

    elif inputKey == '3' or inputKey == 'removeAllCascade':
        ''' remove all main cascade files.'''
        hc.deleteMainCascadeFile()

if __name__ == '__main__':
    main()
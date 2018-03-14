# ~/virtualenv/ROBOTICS_studios/bin

'''*************************************************
*                                                  *
*                  import library                  *
*                                                  *
*************************************************'''

import os
import sys
import platform

import numpy as np
import cv2

'''*************************************************
*                                                  *
*               define dirConnector                *
*                                                  *
*************************************************'''

class haarCascade():
    '''for detect text from camera with 30 haar-cascade classifier and manage classifier files'''
    def __init__(self):

        if platform.system() == 'Linux':
            self.dirCom = '/'
        elif platform.system() == 'Windows':
            self.dirCom = '\\'
        else :
            self.dirCom = '/'

        self.multiClassifiers = []
        self.listOfClass = [0,1,2,3,4,5,6,7,8,9]+['zero','one','two','three','four','five','six',
                'seven','eight','nine']+['ZeroTH','OneTH','TwoTH','ThreeTH','FourTH','FiveTH','SixTH',
                'SevenTH','EightTH','NineTH']

    def callClassifiers(self):
        ''' call all classifier '''

        self.multiClassifiers = [cv2.CascadeClassifier('cascade_file'+self.dirCom+str(i)) for i in os.listdir('cascade_file')]
        return 0

    def detectHaarCascade(self,image):
        '''for detect text from camera with 30 haar-cascade classifier '''
        if self.multiClassifiers == [] :
            self.callClassifiers()

        img = image
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        for selectClassifier in self.multiClassifiers:
            output = selectClassifier.detectMultiScale(gray, 1.3, 5)
            # print(str(len(output)))
            for (x, y, w, h) in output:
                cv2.rectangle(img, (x,y), (x+w,y+h), (255, 0, 0), 2)

        return img

    def copyCascadeFile(self):
        '''copy real cascade file from folder output_data to folder cascade_file. '''
        for selectClass in self.listOfClass :
            os.system('cp output_data'+self.dirCom+str(selectClass)+self.dirCom+'cascade.xml cascade_file'+self.dirCom+str(selectClass)+'.xml' )
        return 0
    
    def deleteCascadeFile(self):
        '''delete cascade file in folder cascade_file. '''

        for f in [i for i in os.listdir('cascade_file')] :
            os.remove(os.path.join('cascade_file',f))
        return 0

    def deleteMainCascadeFile(self):
        '''delete all cascade file in folder output_data. '''

        for selectClass in self.listOfClass :
            for f in [i for i in os.listdir('output_data'+self.dirCom+str(selectClass))] :
                os.remove(os.path.join('output_data'+self.dirCom+str(selectClass),f))
        return 0
        
    # cascade = cv2.CascadeClassifier('')





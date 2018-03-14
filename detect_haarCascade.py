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

    def __init__(self):

        if platform.system() == 'Linux':
            self.dirCom = '/'
        elif platform.system() == 'Windows':
            self.dirCom = '\\'
        else :
            self.dirCom = '/'

    def detectHaarCascade(self,image):
        pass


    # cascade = cv2.CascadeClassifier('')





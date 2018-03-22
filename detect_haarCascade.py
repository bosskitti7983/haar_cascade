# ~/virtualenv/ROBOTICS_studios/bin

'''*************************************************
*                                                  *
*                  import library                  *
*                                                  *
*************************************************'''

import os
import sys
import platform
from time import sleep

import numpy as np
import cv2
from PIL import Image
from math import sqrt

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
        self.listOfClass = [0,1,2,3,4,5,6,7,8,9]+['zero','one','two','three','four','five','six','seven','eight','nine']+['ZeroTH','OneTH','TwoTH','ThreeTH','FourTH','FiveTH','SixTH','SevenTH','EightTH','NineTH']
        self.suffix = ['test','train','validate']

    def callClassifiers(self,feature):
        ''' call all classifier '''
        if feature == 'HAAR':
            self.multiClassifiers = {str(i):cv2.CascadeClassifier('cascade_file'+self.dirCom+str(i)) for i in os.listdir('cascade_file')}
        elif feature == 'HOG':
            self.multiClassifiers = {str(i):cv2.HOGDescriptor('cascade_file'+self.dirCom+str(i)) for i in os.listdir('cascade_file')}

        elif  feature == 'LBP':
            pass
        return 0

    def detectHaarCascade(self,image,feature):
        '''for detect text from camera with 30 haar-cascade classifier '''

        self.callClassifiers(feature=feature)
        img = image
        # gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        returnData = []
        for selectClassifier in list(self.multiClassifiers):
            if feature == 'HAAR':
                output = self.multiClassifiers[selectClassifier].detectMultiScale(img, 3.2, 5)
            elif feature == 'HOG':
                output,w = self.multiClassifiers[selectClassifier].detectMultiScale(img,winStride=(8,8),padding=(16,16), scale=1.05, useMeanshiftGrouping=False)
            elif feature == 'LBP':
                pass
            # print(str(len(output)))
            # print(output)
            output2 = []
            
            if len(output) != 0:
                
                for (x, y, w, h) in output :
                    if (w+h)/2 >24:
                        output2.append((x,y,w,h))
                        cv2.rectangle(image, (x,y), (x+w,y+h), 0, 1)
                        returnData.append(str(selectClassifier.split('.')[0]))
                        # cv2.imshow('win',image)
                        # cv2.waitKey(0)
                        # image=img

        return returnData

	    

    def testCascade(self,feature):
        ''' test classifier by test data. '''	
        keepData={}
        for j in range(0,30): # 30 class
            object = self.listOfClass[j]
            f = open('dataCompress'+self.dirCom+'dataset_'+str(object)+'_all_'+self.suffix[0]+'.txt','r')
            image = str(f.read()).split('\n')[:-1]
            f.close()
            keepData[object] = 0			
            print("test : " +str(object))
            for i in range(len(image)):
                image[i] = np.fromstring(image[i], dtype=float, sep=',')
                image[i] = np.array(image[i], dtype=np.uint8)*255
                image[i] = np.reshape(image[i],(int(sqrt(len(image[i]))),int(sqrt(len(image[i])))))
                # image[i] = cv2.resize(image[i],(100,100))

                
                # img = Image.fromarray((image[i]*255).astype(np.uint8))
                if i%int(len(image)/10) == 0:
                    print(str(int(i*100/len(image)))+'/100')
                
                detect = self.detectHaarCascade(image=image[i],feature=feature)
                if str(object) in str(detect)  : # str(object[0]) == str(object) and len(object) == 1
                    keepData[object]+=1

            print("\nsuccess : " +str(object))
            keepData[object] = int(keepData[object])*100/len(image)
            print(str(object) +':'+str(keepData[object])+'/100.00\n')
            sleep(3)
        print(keepData)

        return 0

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





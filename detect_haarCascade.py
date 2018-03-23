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
*              define init condition               *
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

        self.scaleWeightHeight = 0.5
        self.testResizeH = 50

        self.multiClassifiers = []
        self.listOfClass = [0,1,2,3,4,5,6,7,8,9]+['zero','one','two','three','four','five','six','seven','eight','nine']+['ZeroTH','OneTH','TwoTH','ThreeTH','FourTH','FiveTH','SixTH','SevenTH','EightTH','NineTH']
        self.suffix = ['test','train','validate']

        '''*************************************************
        *                                                  *
        *             define anoymus function              *
        *                                                  *
        *************************************************'''

        self.WHfromArray1D = lambda arraySize : ( int(sqrt(arraySize*self.scaleWeightHeight)), int(sqrt(arraySize/self.scaleWeightHeight)) )

    def callClassifiers(self,feature):
        ''' call all classifier '''
        if feature == 'HAAR':
            self.multiClassifiers = {str(i):cv2.CascadeClassifier('cascade_file'+self.dirCom+str(feature)+self.dirCom+str(i)) for i in os.listdir('cascade_file'+self.dirCom+str(feature))}
        elif feature == 'HOG':
            self.multiClassifiers = {str(i):cv2.HOGDescriptor('cascade_file'+self.dirCom+str(feature)+self.dirCom+str(i)) for i in os.listdir('cascade_file'+self.dirCom+str(feature))} 
            # for classi in os.listdir('cascade_file'+self.dirCom+str(feature)):
            #     self.multiClassifiers[classi].setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector()) 
        elif  feature == 'LBP':
            self.multiClassifiers = {str(i):cv2.CascadeClassifier('cascade_file'+self.dirCom+str(feature)+self.dirCom+str(i)) for i in os.listdir('cascade_file'+self.dirCom+str(feature))}
        return 0

    def detectHaarCascade(self,image,feature):
        '''for detect text from camera with 30 haar-cascade classifier '''

        if self.multiClassifiers == []:
            self.callClassifiers(feature=feature)
        img = image

        returnData = []
        for selectClassifier in list(self.multiClassifiers):
            if feature == 'HAAR':
                output = self.multiClassifiers[selectClassifier].detectMultiScale(img, scaleFactor= 3.2,minNeighbors= 5)
            elif feature == 'HOG':
                output,w = self.multiClassifiers[selectClassifier].compute(img,winStride=(4,4),padding=(8,8))
                # output,w = self.multiClassifiers[selectClassifier].detectMultiScale(img,winStride=(4,4),padding=(8,8), scale=1.05)
            elif feature == 'LBP':
                output = self.multiClassifiers[selectClassifier].detectMultiScale(img,  scaleFactor= 3.2,minNeighbors= 5)

            output2 = []
            
            if len(output) != 0:
                
                for (x, y, w, h) in output :
                    if (w+h)/2 >sum(Image.open('main_img'+self.dirCom+os.listdir('main_img')[0]).size):
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
        keepDataAll = {}
        for i in range(0,30): # 30 class
            keepDataAll[str(self.listOfClass[i])]={}
            for j in range(0,30): # inloop 30 class
                keepDataAll[str(self.listOfClass[i])].update({str(self.listOfClass[j]):0})
        
        self.callClassifiers(feature=feature)
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
                image[i] = np.reshape(image[i],(self.WHfromArray1D(len(image[i]))))
                image[i] = cv2.resize(image[i],(int(self.testResizeH/self.scaleWeightHeight),int(self.testResizeH)))

                if i%int(len(image)/10) == 0:
                    print(str(int(i*100/len(image)))+'/100')
                
                detect = self.detectHaarCascade(image=image[i],feature=feature)
                if str(object) in str(detect)  : # str(object[0]) == str(object) and len(object) == 1
                    keepData[object]+=1

                for dete in detect:
                    keepDataAll[str(object)][str(dete)] +=1

            for kAll in self.listOfClass:
                
                keepDataAll[str(object)][str(kAll)] = int(keepDataAll[str(object)][str(kAll)])*100/len(image)
            print("\nsuccess : " +str(object))
            keepData[object] = int(keepData[object])*100/len(image)
            print(str(object) +':'+str(keepData[object])+'/100.00\n')
            print(keepDataAll[str(object)])
            
        print(keepData)
        print(keepDataAll)
        return 0

    def copyCascadeFile(self,feature ):
        '''copy real cascade file from folder output_data to folder cascade_file. '''
        for selectClass in self.listOfClass :
            os.system('cp output_data'+self.dirCom+str(selectClass)+self.dirCom+'cascade.xml cascade_file'+self.dirCom+str(feature.upper())+self.dirCom+str(selectClass)+'.xml' )
        return 0

    def deleteCascadeFile(self,feature = ['HAAR','HOG','LBP']):
        '''delete cascade file in folder cascade_file. '''

        for featureType in feature:
            for f in [i for i in os.listdir('cascade_file'+self.dirCom+str(featureType))] :
                os.remove(os.path.join('cascade_file'+self.dirCom+str(featureType),f))
        return 0

    def deleteMainCascadeFile(self):
        '''delete all cascade file in folder output_data. '''

        for selectClass in self.listOfClass :
            for f in [i for i in os.listdir('output_data'+self.dirCom+str(selectClass))] :
                os.remove(os.path.join('output_data'+self.dirCom+str(selectClass),f))
        return 0
        





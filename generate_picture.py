#"D:\virtualenv\ROBOTICS_studios\Scripts\activate"

import os
import sys

from PIL import Image
from math import sqrt
import numpy as np

'''*************************************************
*                                                  *
*              config generate number              *
*                                                  *
*************************************************'''
numCount = 0
numKeep = 0
limitFilePerClass = 50

'''*************************************************
*                                                  *
*                   prepare data                   *
*                                                  *
*************************************************'''

suffix = ['test','train','validate']
listOfClass = [0,1,2,3,4,5,6,7,8,9]+['zero','one','two','three','four','five','six',
                    'seven','eight','nine']+['ZeroTH','OneTH','TwoTH','ThreeTH','FourTH','FiveTH','SixTH',
                    'SevenTH','EightTH','NineTH']

'''*************************************************
*                                                  *
*                   remove old data                *
*                                                  *
*************************************************'''
try:
    fileList= [f for f in os.listdir('dataExtract')]
    for f in fileList:
        os.remove(os.path.join('dataExtract',f)) 

except Exception:
    print("not file in dataExtract folder")

'''*************************************************
*                                                  *
*              read & generate data                *
*                                                  *
*************************************************'''

for s in range(0,3): # 3 suffix
    for j in range(0,30): # 30 class
        object = listOfClass[j]
        f = open('dataCompress\\dataset_'+str(object)+'_all_'+suffix[s]+'.txt','r')
        image = str(f.read()).split('\n')[:-1]
        f.close()

        numKeep += numCount
        numCount = 0
        for i in range(len(image)):
            
            path = 'dataExtract\\'+str(object)+'_'+suffix[s]+'-'+str(numCount)+'.png'

            image[i] = np.fromstring(image[i], dtype=float, sep=',')
            image[i] = np.array(image[i])
            image[i] = np.reshape(image[i],(int(sqrt(len(image[i]))),int(sqrt(len(image[i])))))

            img = Image.fromarray((image[i]*255).astype(np.uint8))
            img.save(path)

            if numCount > limitFilePerClass-1 :
                break
            if (numCount%int(limitFilePerClass/2)) == 0 :
                print("generate"+str(numKeep+numCount)+ ":"+str(object) +"-"+str(numCount))

            numCount+=1
# ~/virtualenv/ROBOTICS_studios/bin/python


'''*************************************************
*                                                  *
*                  import library                  *
*                                                  *
*************************************************'''

import os
import sys
from random import choice

from PIL import Image
from math import sqrt
import numpy as np



'''*************************************************
*                                                  *
*                   main library                   *
*                                                  *
*************************************************'''

def main():
    inputKey = sys.argv[1:]
    if str(inputKey[0]) == 'help':
        print('prepare_haarCascade [method] [param] \nmethod:\tresize\t\tcreate_bg\tgen_image')
        print('param:\tmain image\tmain class\tnumber per class\n\ttrain-0 24\tone\t\t50')
    elif str(inputKey[0]) == 'resize':
        try :
            resize_image(selectFile = (str(inputKey[1])+'.png'), size = int(inputKey[2]))
        except Exception :
            resize_image()
    elif str(inputKey[0]) == 'create_bg':
        try :
            create_bg_txt(select_value = str(inputKey[1]))
        except Exception :
            sys.exit('not found argument')
    elif str(inputKey[0]) == 'gen_image':
        try :
            generate_picture(limitFilePerClass = int(inputKey[1]))
        except Exception :
            generate_picture()

def resize_image(selectFile = 'test-0.png', size = 24):

    print('select file *'+selectFile +" : " +str(size))        
    '''*************************************************
    *                                                  *
    *                  config main image               *
    *                                                  *
    *************************************************'''

    

    '''*************************************************
    *                                                  *
    *                   remove old data                *
    *                                                  *
    *************************************************'''
    try:
        fileList= [f for f in os.listdir('data')]
        for f in fileList:
            os.remove(os.path.join('data',f)) 
    except Exception:
        print("error to remove file in data folder")

    try:
        fileList= [f for f in os.listdir('main_img')]
        for f in fileList:
            os.remove(os.path.join('main_img',f)) 
    except Exception:
        print("error to remove file in main_img folder")

    '''*************************************************
    *                                                  *
    *            resize and select main image          *
    *                                                  *
    *************************************************'''

    path = 'dataExtract'
    fileList= [f for f in os.listdir(path)]
    for f in fileList:
        img = Image.open(path+'\\'+f)
        if img.height < int(size):
            sys.exit('size is bigger than '+str(img.height))

        img = img.resize((int(size),int(size)),Image.ANTIALIAS)
        img.save('data\\'+f)

        if f.split('_')[1] == selectFile:
            img.save('main_img\\'+f)


def create_bg_txt(select_value):
    
    '''*************************************************
    *                                                  *
    *            remove & create old file              *
    *                                                  *
    *************************************************'''

    if os.path.isfile('bg_pos.txt') :
        os.remove('bg_pos.txt')
    if os.path.isfile('bg_neg.txt') :
        os.remove('bg_neg.txt')

    f_pos = open("bg_pos.txt","w+")
    f_neg = open("bg_neg.txt","w+")
    
    '''*************************************************
    *                                                  *
    *                 random data list                 *
    *                                                  *
    *************************************************'''
    
    listData = os.listdir('data')
    randomList = []
    while len(listData) > 0 :
        randomData = choice(listData)
        randomList.append(randomData)
        listData.remove(randomData)    
 
    '''*************************************************
    *                                                  *
    *            split positive and negative           *
    *                                                  *
    *************************************************'''

    listOfClass = [0,1,2,3,4,5,6,7,8,9]+['zero','one','two','three','four','five','six',
                    'seven','eight','nine']+['ZeroTH','OneTH','TwoTH','ThreeTH','FourTH','FiveTH','SixTH',
                    'SevenTH','EightTH','NineTH']

    if str(select_value) in str(listOfClass):
        for f in randomList:
            if str(f.split('_')[0]) == str(select_value):
                f_pos.write("data\\"+f+"\n")
            else:
                f_neg.write("data\\"+f+"\n")
    else:
        sys.exit('out of class')


def generate_picture(limitFilePerClass = 50):
    '''*************************************************
    *                                                  *
    *              config generate number              *
    *                                                  *
    *************************************************'''
    numCount = 0
    numKeep = 0
    

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
        print("error to remove file in dataExtract folder")

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



if __name__ == '__main__':
    main()
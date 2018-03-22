import sys
import os

import numpy as np
import cv2
from matplotlib import pyplot as plot
import tkinter as tk

def main():
    # scale = 2
    histrogramX=[]
    histrogramY=[]

    inputKey = sys.argv[1:3]
    if inputKey == []:
        sys.exit('no input argument')
    else :
        scale = int(inputKey[1])
        inputKey = str(inputKey[0])

    # inputKey = '0_validate-0.png'

    img = cv2.imread(str(inputKey),0)

    h,w = img.shape

    for h_i in range(0,h,scale):
        keepValue=0
        for i in range(h_i,h_i+scale):
            keepValue+=sum(img[i])    
        histrogramY.append(keepValue)

    for w_i in range(0,w,scale):
        keepValue=0
        for j in range(w_i,w_i+scale):
            keepValue+=sum(img.transpose()[j])
        histrogramX.append(keepValue)

    plot.subplot(221)
    plot.title('histY')
    # plot.plot(histrogramY, [i for i in range(0,h,scale)] )
    plot.barh(np.arange(int(h/scale)),histrogramY,0.35,color ='b')
    
    plot.subplot(222)
    plot.title('image')
    plot.imshow(img)
    # plot.subplot(211)
    # plot.plot([j for j in range(0,w,scale)], [0 for j in range(0,w,scale)])
    plot.subplot(212)
    plot.title('histX')
    # plot.plot([j for j in range(0,w,scale)], histrogramX)
    plot.bar(np.arange(int(w/scale)),histrogramX,0.35,color ='b')
    # plot.hist(img.flattern(),256,[0,256],color='b')
    plot.show()
    

if __name__ == '__main__':
    main()
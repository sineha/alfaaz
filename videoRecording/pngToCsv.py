from PIL import Image, ImageFilter
import os
import natsort
import csv
import numpy as np

def imageprepare(argv):
    im = Image.open(argv).convert('L')
    img = im.resize((28, 28), Image.ANTIALIAS).filter(ImageFilter.SHARPEN)
    value = np.asarray(img.getdata(), dtype=np.int)
    value1 = value.flatten()
    return value1

def Picking_Frames():
    AllFrames = os.listdir("final-frames/")
    AllFrames = (natsort.natsorted(AllFrames,reverse=False))
    return  AllFrames

def findingCSV():
    row_list = []
    formatting = []
    for i in range(1,785):
        temp = "pixel" + str(i)
        formatting.append(temp)
    row_list.append(formatting)
    Frame_names=Picking_Frames()
    if len(Frame_names)>0:
        for each in Frame_names:
            path = "final-frames/"+each
            x=imageprepare(path)
            row_list.append(x)

        with open('sign_mnist_test.csv', 'w+', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(row_list)
            mydir = "final-frames/"
            for f in os.listdir(mydir):
                os.remove(os.path.join(mydir, f)) 
        return True

    return False    
       
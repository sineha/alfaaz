from PIL import Image
import cv2
import os
import natsort

def finalFrameExtraction():
    AllFrames = os.listdir("video-frames/")
    AllFrames = (natsort.natsorted(AllFrames,reverse=False))
    
    for frame in AllFrames:
        print("image filteration")
        path = "video-frames/"+frame  
        # Open the image by specifying the image path.
        image_file = Image.open(path)
        # the default
        name = "final-frames/"+frame
        image_file.save(name, quality=95)
  


    mydir = "video-frames/"
    for f in os.listdir(mydir):
        os.remove(os.path.join(mydir, f))

    
    




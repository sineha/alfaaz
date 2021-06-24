import cv2

def VideoFrames():

    print("Taking out frames")

    vidcap = cv2.VideoCapture('Video2.avi')
    cap= cv2.VideoCapture('Video2.avi')

    # framespersecond= int(cap.get(cv2.CAP_PROP_FPS))
    sec = 10
    frameRate = 10.0 #it will capture image in each 10 second   
    vidcap.set(cv2.CAP_PROP_POS_MSEC,sec*1000)
    hasFrames,image = vidcap.read()
    if hasFrames:
        cv2.imwrite("video-frames/"+str(sec)+".png", image)     # save frame as JPG file
        print("First Frame ",image)
    success = hasFrames
    while success:
        sec = sec + frameRate
        vidcap.set(cv2.CAP_PROP_POS_MSEC,sec*1000)
        hasFrames,image = vidcap.read()
        if hasFrames:
            cv2.imwrite("video-frames/"+str(sec)+".png", image)
            print("Frame For ",sec)
        success = hasFrames    
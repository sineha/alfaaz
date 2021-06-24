from django.shortcuts import render
from django.http import HttpResponse,StreamingHttpResponse
from videoRecording.camera import VideoCamera
from videoRecording.framesFromVideo import VideoFrames 
# from videoRecording.extractingFinalFrames import finalFrameExtraction
from videoRecording.pngToCsv import findingCSV
from videoRecording.model import output
from videoRecording.removeOutput import removefile
import cv2
from django.http import JsonResponse
from videoRecording.filterImages import finalFrameExtraction
import threading

loop = True
asyn = False
FrameCapture = True
global t

def printit():
  global t
  t = threading.Timer(7.0, printit)
  t.start()
  global FrameCapture
  FrameCapture = not FrameCapture
  print("boolean ",FrameCapture)
  print("TIMER")


def home(request):
    return render(request, 'index.html')


def start_Recording(request):
    removefile()
    global FrameCapture
    FrameCapture = True
    printit()
    return render(request,'liveStream.html',{'notification':''})


def stop(request):
    global loop
    global asyn
    global t
    loop = False
    while True:
        if asyn:
            t.cancel()
            print("Translation Start")
            # VideoFrames()
            finalFrameExtraction()
            cond = findingCSV()
            # finalFrameExtraction()           
            output()
            global FrameCapture
            FrameCapture = True
            printit()
            return render(request,'liveStream.html',{'notification':''})
    
    
def gen(camera):
    print("Camera Generation")
    global loop
    global asyn
    global FrameCapture
    loop = True
    i = 0

    while loop:
        frame = camera.get_frame(i)
        yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
        i = i + 1      
        cv2.imwrite("compare-frames/" + str(i) + ".png", camera.gesture)  
        if FrameCapture == True:
            cv2.imwrite("video-frames/" + str(i) + ".png", camera.gesture) 
            FrameCapture = False

    out2 = cv2.VideoWriter('Video2.avi',cv2.VideoWriter_fourcc(*'DIVX'), 25, camera.size2)
    for img in (camera.img_array):
        out2.write(img)
    out2.release()
    print("Video written")
    asyn = True
    

def video_feed(request):
    print("Video Feed Started")
    return StreamingHttpResponse(gen(VideoCamera()),
                    content_type='multipart/x-mixed-replace; boundary=frame')


def translate(request):
    global loop
    global asyn
    global t
    loop = False
    while True:
        if asyn:
            t.cancel()
            print("Translation Start")
            # VideoFrames()
            finalFrameExtraction()
            cond = findingCSV()
            # finalFrameExtraction()           
            output()
            file = open('output.txt',mode='r')
            converted = file.read()
            file.close()
            converted = "YOUR SIGNS CONVERTED TO TEXT : " + converted
            return render(request, 'index.html',{'output':converted,'flag':True})
           
            
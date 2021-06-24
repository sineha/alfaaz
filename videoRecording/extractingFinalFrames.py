import os
import cv2
import natsort
from shutil import copyfile
import sys


def finalFrameExtraction():
    AllFrames = os.listdir("video-frames/")
    AllFrames = (natsort.natsorted(AllFrames,reverse=False))
    print(AllFrames)
    prev1 = 0
    prev = 0
    result = []
    first = 1
    for frame in AllFrames:

        print()
        path = "compare-frames/"+frame
        image_to_compare = cv2.imread(path)
        if prev1 != 0:
            try:
           # print("checking frame ",frame)
                original = prev
           # 1) Check if 2 images are equals
                if original.shape == image_to_compare.shape:
               # print("The images have same size and channels")
                    difference = cv2.subtract(original, image_to_compare)
                    b, g, r = cv2.split(difference)

               # if cv2.countNonZero(b) == 0 and cv2.countNonZero(g) == 0 and cv2.countNonZero(r) == 0:
               #     print("The images are completely Equal")
               # else:
               #     print("The images are NOT equal")

           # 2) Check for similarities between the 2 images
                sift = cv2.xfeatures2d.SIFT_create()
                kp_1, desc_1 = sift.detectAndCompute(original, None)
                kp_2, desc_2 = sift.detectAndCompute(image_to_compare, None)

                index_params = dict(algorithm=0, trees=5)
                search_params = dict()
                flann = cv2.FlannBasedMatcher(index_params, search_params)

                matches = flann.knnMatch(desc_1, desc_2, k=2)

                good_points = []
                for m, n in matches:
                    if m.distance < 0.6 * n.distance:
                        good_points.append(m)

           # Define how similar they are
                number_keypoints = 0
                if len(kp_1) <= len(kp_2):
                    number_keypoints = len(kp_1)
                else:
                    number_keypoints = len(kp_2)

                if number_keypoints > 0:
                    sim = len(good_points) / number_keypoints * 100
               # print("How good it's the match: ", sim)
                    if first == 1:
                        temp = frame.split(".")[0]
                        temp = int(temp)
                        temp = str(temp) + ".png"
                        result.append(temp)
                        first = 2
                    elif (sim < 25):
                        ind = AllFrames.index(frame)
                        ind = ind + 1
                        temp = AllFrames[ind]
                        result.append(temp)

                   # temp = str(temp) +".jpg"
                else:
                    first = 1


            except Exception as e:
                print("Error ",e)
                first = 1

        prev =  image_to_compare
        prev1 = 1

    pre = ""
    final = []



    for i in range(0,len(result)):
        if pre != "":
            val = result[i]
            ind = AllFrames.index(val)
            ind = ind - 1
            if pre != AllFrames[ind]:
                final.append(val)
        else:
            final.append(result[i])
        pre = result[i]
    print(final)
    for x in final :
        filepath = 'video-frames/' + x
        save_path = 'final-frames/' + x
        copyfile(filepath, save_path)

    mydir = "video-frames/"
    for f in os.listdir(mydir):
        os.remove(os.path.join(mydir, f))

    mydir = "compare-frames/"
    for f in os.listdir(mydir):
        os.remove(os.path.join(mydir, f))

# AllFrames = os.listdir("F:/pycharmProjects/SignsReading/final-frames/")
# AllFrames = (natsort.natsorted(AllFrames,reverse=False))
# i=0
# mydir = "final-frames/"
# for frame in AllFrames:
#     path = "final-frames/" + frame
#     image_to_reshape = cv2.imread(path)
#     print(image_to_reshape)
#     img = cv2.resize(image_to_reshape,(200,200))
#     cv2.imwrite("compare/" + str(i) + ".png", img)
#     i = i + 1
    # os.remove(os.path.join(mydir, frame))
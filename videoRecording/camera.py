import cv2,os,urllib.request
import numpy as np
import math
import wx
class VideoCamera(object):
    def __init__(self):
        self.cap = cv2.VideoCapture(0,cv2.CAP_DSHOW);  
        self.bg = cv2.flip(self.cap.read()[1], 1);
        self.w = np.shape(self.bg)[1];
        self.h = np.shape(self.bg)[0];
        self.bg = self.bg[1:self.h - 199, 250:self.w].copy();
        self.app = wx.App(False);
        (self.sx, self.sy) = wx.GetDisplaySize();
        self.img_array = []
        self.size2 = 0
        self.gesture = ""

    def __del__(self):
        self.cap.release()
        cv2.destroyAllWindows();

    def get_frame(self,i):
    
        frame = cv2.flip(self.cap.read()[1], 1);
        roi = frame[1:self.h - 199, 250:self.w].copy();
        temp_roi = roi.copy();
        self.img_array.append(temp_roi)
        self.gesture = temp_roi
        self.gesture= cv2.flip(self.gesture, 1)

        fmask = cv2.absdiff(self.bg, roi, 0);
        fmask = cv2.cvtColor(fmask, cv2.COLOR_BGR2GRAY);
        fmask = cv2.threshold(fmask, 10, 255, 0)[1];
        ####### Morphological Processing #########
        fmask = cv2.erode(fmask, cv2.getStructuringElement(cv2.MORPH_ERODE, (2, 2)), iterations=2);
        mask1 = cv2.morphologyEx(fmask, cv2.MORPH_CLOSE, \
                             cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (4, 4)));
        mask1 = cv2.erode(mask1, cv2.getStructuringElement(cv2.MORPH_ERODE, (2, 2)), iterations=2);

        
        fg_frame = cv2.bitwise_and(roi, roi, mask=mask1);

        height, width, layers = fg_frame.shape

        size = (width, height)
        self.size2 = size
        # self.gesture =mask1
        # cv2.imwrite("compare-frames/" + str(i) + ".png", fg_frame)

        gr_frame = cv2.cvtColor(fg_frame, cv2.COLOR_BGR2GRAY);
        gr_frame = cv2.blur(gr_frame, (10, 10));
        bw_frame = cv2.threshold(gr_frame, 50, 255, 0)[1];
        ############ Tracking the hand contour ################
        con = cv2.findContours(bw_frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0];
        try:
            my_con = max(con, key=cv2.contourArea);
        except:
            my_con = np.array([[[1, 0], [1, 2], [2, 3]]], dtype=np.int32);
        pass;
        try:
            if cv2.contourArea(my_con) > 90:

                hull = cv2.convexHull(my_con, True);

                leftmost = tuple(hull[hull[:, :, 0].argmin()][0])
                rightmost = tuple(my_con[my_con[:, :, 0].argmax()][0])
                topmost = tuple(hull[hull[:, :, 1].argmin()][0])
                bottommost = tuple(my_con[my_con[:, :, 1].argmax()][0])

                temp = bottommost[0] + 30  # getting the bottom middle of the hand
                cv2.line(roi, topmost, (topmost[0], self.h - 280), (0, 242, 225), 2);
                cv2.line(roi, leftmost, (topmost[0], bottommost[1] - 80), (0, 242, 225), 2);

                cv2.circle(roi, topmost, 5, (255, 0, 0), -1);
                cv2.circle(roi, leftmost, 5, (0, 120, 255), -1);
                cv2.circle(roi, (temp, bottommost[1]), 5, (230, 0, 255), -1);
                x1 = topmost[0];
                y1 = topmost[1];
                x2 = bottommost[0] + 20;
                y2 = bottommost[1];
                x3 = leftmost[0];
                y3 = leftmost[1];
                m1 = (y2 - y1) / (x2 - x1)
                m2 = (y3 - y2) / (x3 - x2)
                tan8 = math.fabs((m2 - m1) / (1 + m1 * m2));
                angle = math.atan(tan8) * 180 / math.pi;
                length = math.sqrt(math.pow((y2 - y1), 2) + math.pow((x2 - x1), 2))
                
                x = sx - ((topmost[0] - 50) * sx / (self.w - 340));
                y = (topmost[1] * sy / (self.h - 281));
            # mouse.move(sx - x, y, absolute=True, duration=.1);

                cv2.putText(roi, str('%d,%d' % (sx - x, y)), topmost, cv2.FONT_HERSHEY_SIMPLEX, .5, (255, 255, 255), 1,
                        cv2.LINE_AA)
        except:
            pass;
        
        frame[1:self.h - 199, 250:self.w] = roi;
        cv2.rectangle(frame, (250, 1), (self.w - 1, self.h - 200), (0, 255, 0), 2);
        cv2.rectangle(frame, (300, 1), (self.w - 40, self.h - 280), (255, 0, 0), 2);

        ret, jpeg = cv2.imencode('.jpg', frame)

        return jpeg.tobytes()

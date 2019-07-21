import numpy as np
import cv2
import pyttsx3

engine = pyttsx3.init()

cap = cv2.VideoCapture(0)

def run_main():

    while(True):
        # Capture frame-by-frame
        ret, frame = cap.read()
        cv2.imshow("frame",frame)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray_blur = cv2.GaussianBlur(gray, (15, 15), 0)
        circles = cv2.HoughCircles(gray_blur,cv2.HOUGH_GRADIENT,1,20, param1=50,param2=30,minRadius=0,maxRadius=0)
       
        largestRadius = 0
        if circles is not None:
            circles = np.uint16(np.around(circles))
            for i in circles[0,:]:
                if largestRadius < i[2]:
                    largestRadius = i[2]
            print(largestRadius)
            change = 0
            for i in circles[0,:]:
                    cv2.circle(frame,(i[0],i[1]),i[2],(0,255,0),2)
                    cv2.circle(frame, (i[0], i[1]),2, (0,0,255), 3)
                    radius = i[2]
                    ratio = ((radius*radius) / (largestRadius*largestRadius))
                    print(radius)
                    if(ratio >= 0.90 and radius >= 55):
                        change = change + .25
                    elif((ratio >=0.70) and (ratio < 0.90) and (radius >= 49) and (radius <= 51)):
                        change = change + 0.05
                    elif((ratio >= 0.55) and (ratio < 0.70) and (radius >= 45) and (radius <= 47)):
                        change = change + 0.01
                    elif(ratio < 0.55):
                        change = change + 0.1
            print(change)
            font = cv2.FONT_HERSHEY_SIMPLEX
            text = "Total value: " + str("%.2f" % round(change,2)) + " American Dollars"
            cv2.putText(frame, text, (0,400), font, 0.5, (0, 0, 0), 2, cv2.LINE_AA)
            cv2.imshow('Detected coins',frame)
            engine.say("You have "+text)
            engine.runAndWait()
          
    # When everything done, release the capture  
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    run_main()
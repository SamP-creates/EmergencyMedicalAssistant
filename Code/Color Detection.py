import cv2
import numpy as np
##import tkinter as tk
cap = cv2.VideoCapture(0)

def findcolor(high,low,color,imageFrame):
    # Convert BGR to HSV colorspace
    hsvFrame = cv2.cvtColor(imageFrame, cv2.COLOR_BGR2HSV)

    # Set range for red color 
    red_lower = np.array(low, np.uint8)
    red_upper = np.array(high, np.uint8)
    
    # define mask
    red_mask = cv2.inRange(hsvFrame, red_lower, red_upper)

    # to detect only that particular color
    kernal = np.ones((5, 5), "uint8")

    # red color
    red_mask = cv2.dilate(red_mask, kernal)
    res_red = cv2.bitwise_and(imageFrame, imageFrame, mask=red_mask)

    # Creating contour to track red color
    contours, hierarchy = cv2.findContours(red_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for pic, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        if (area > 600):
            x, y, w, h = cv2.boundingRect(contour)
            imageFrame = cv2.rectangle(imageFrame, (x, y),(x + w, y + h),(int((high[0]+low[0])/2), int((high[1]+low[1])/2), int((high[2]+low[2])/2)), 2)
            cv2.putText(imageFrame, str(color), (x, y-10),cv2.FONT_HERSHEY_SIMPLEX, 0.5,(int((high[0]+low[0])/2), int((high[1]+low[1])/2), int((high[2]+low[2])/2)))
    #display
    frames = np.rot90(imageFrame) # Rotate the frame
    frames = cv2.cvtColor(frames, cv2.COLOR_BGR2RGB)
##    display = pygame.surfarray.make_surface(frames)
##    display = pygame.transform.flip(display, True, False)
##    display = pygame.transform.scale(display,(sX,sY))
##    rect = display.get_rect()
##    rect.center = (sX/2,sY/2)
##    screen.blit(display,rect)

while True:
        ret, frame = cap.read() # Read a frame from the camera
        blurred_image = cv2.GaussianBlur(frame, (5, 5), 100000000)
        
        if not ret:
            break # Exit if frame not captured

        # Convert the frame from BGR to HSV color space
        hsv_frame = cv2.cvtColor(blurred_image, cv2.COLOR_BGR2HSV)

        lower_color1 = np.array([0, 0, 0])
        upper_color1 = np.array([255, 255, 255])
        
        start_point = (275, 260)
        end_point = (325, 260)
        color = (0, 0, 0)
        thickness = 5
        pixel_color_bgr = hsv_frame[300, 260]  # Accessing by [row, column] or [y, x]
        cv2.line(blurred_image, start_point, end_point, color, thickness)
        print(pixel_color_bgr)

        # YELLOW
        lightYellowLow   = [22, 80, 140]
        lightYellowHigh  = [30, 145, 190]
        findcolor(lightYellowHigh, lightYellowLow, "light yellow",blurred_image)

        darkYellowLow   = [15, 80, 110]
        darkYellowHigh  = [22, 175, 155]
        findcolor(darkYellowHigh, darkYellowLow, "dark yellow",blurred_image)

        # GREEN
        lightGreenLow  = [29, 54, 85]
        lightGreenHigh = [100,255, 130]
        findcolor(lightGreenHigh, lightGreenLow, "light green",blurred_image)
        
        ##Have not done dark green
        darkGreenLow   = [40, 150, 50]
        darkGreenHigh  = [72, 79, 69]
        findcolor(darkGreenHigh, darkGreenLow, "dark green",blurred_image)


        blue_value = pixel_color_bgr[0]
        green_value = pixel_color_bgr[1]
        red_value = pixel_color_bgr[2]


        mask = cv2.inRange(hsv_frame, lower_color1, upper_color1)


        result = cv2.bitwise_and(blurred_image, blurred_image, mask=mask)


        ##cv2.imshow('Original Frame', frame)
        ##blurred_image = cv2.GaussianBlur(frame, (5, 5), 100000000)
        cv2.imshow('Blurred Image', blurred_image)
        ######cv2.imshow('Detected Color (Blue)', result)


        if cv2.waitKey(1) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break

cap.release()
cv2.destroyAllWindows()

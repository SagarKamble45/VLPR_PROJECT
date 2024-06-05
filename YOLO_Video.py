from ultralytics import YOLO
import cv2
import math
import pandas as pd
from add_data_to_db import *


def cam_detection(path_x):
    video_capture = path_x
    
    cap=cv2.VideoCapture(video_capture)

    frame_width=int(cap.get(3))
    frame_height = int(cap.get(4))

    # out=cv2.VideoWriter('output.avi', cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), 10, (frame_width, frame_height))

    model=YOLO("F:\MAIN_PROJECT\VLPR WEB FLASK\Trained_Model.pt")
    classNames = ["license_plate"]
         
    while True:
        success, img = cap.read()
        # Doing detections using YOLOv8 frame by frame
        #stream = True will use the generator and it is more efficient than normal
        results=model(img,stream=True)
        #Once we have the results we can check for individual bounding boxes and see how well it performs
        # Once we have have the results we will loop through them and we will have the bouning boxes for each of the result
        # we will loop through each of the bouning box
        for r in results:
            boxes=r.boxes
            for box in boxes:
                x1,y1,x2,y2=box.xyxy[0]
                x1,y1,x2,y2=int(x1), int(y1), int(x2)+10, int(y2)
                cv2.rectangle(img, (x1,y1), (x2,y2), (255,0,255),3)
                conf=math.ceil((box.conf[0]*100))/100
                cls=int(box.cls[0])
                class_name=classNames[cls]
                label=f'{class_name}{conf}'
                text1=''
                if conf > 0.8 :
                    # cv2.imwrite(f'output/actual_img/{class_name}_{counter}_{conf}.jpg', img)
                    cropped_img = img[y1:y2, x1:x2]
                    # cv2.imshow("cropped img",cropped_img)
                    # cv2.imwrite(f'output/cropped_img/{class_name}_{counter}_{conf}.jpg', cropped_img)

                    license_plate_crop_gary=cv2.cvtColor(cropped_img, cv2.COLOR_BGR2GRAY)
                    # cv2.imshow("cropped img_1",license_plate_crop_gary)
                    _,license_plate_crop_thresh=cv2.threshold(license_plate_crop_gary, 64, 255, cv2.THRESH_BINARY_INV)
                    # cv2.imshow("cropped img",license_plate_crop_thresh)
                    # text2, text_conf1 = read_license_plate(license_plate_crop_thresh)

                    text1, text_conf = read_license_plate(cropped_img) #detecting the text by using easyocr
                    # text1, text_conf = read_license_plate(license_plate_crop_thresh) #detecting the text by using easyocr

                    if text1 is not None :
                        text_conf=float(text_conf) # Confidence score of OCR is convert in float
                        text_length = len(text1) # length of the detected text
                        

                        if text_conf > 0.3 and text_length > 9: 
                            data=format_license(text1) #formating the text 
                            if license_complies_format(data) :
                                l_pname='{}.jpg'.format(data)
                                _,lptext=livecam_to_database(l_pname,data, text_conf)
                                if livecam_to_database:
                                    cv2.imwrite(f"F:\MAIN_PROJECT\VLPR WEB FLASK\output\IMAGES\LIVE_CAM_IMG\{lptext}.jpg", img)
                            
                t_size = cv2.getTextSize(label, 0, fontScale=1, thickness=2)[0]
                c2 = x1 + t_size[0], y1 - t_size[1] - 3
                cv2.rectangle(img, (x1,y1), c2, [255,0,255], -1, cv2.LINE_AA)  # filled
                cv2.putText(img, class_name, (x1,y1-2),0, 1,[255,255,255], thickness=1,lineType=cv2.LINE_AA)
        yield img
cv2.destroyAllWindows()






def video_detection(path_x):
    video_capture = path_x
    cap=cv2.VideoCapture(video_capture)


    frame_width=int(cap.get(3))
    frame_height = int(cap.get(4))
    # out=cv2.VideoWriter('output.avi', cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), 10, (frame_width, frame_height))

    model=YOLO("F:\MAIN_PROJECT\VLPR WEB FLASK\Trained_Model.pt")
    classNames = ["license_plate"]
                    
    while True:
        success, img = cap.read()
        # Doing detections using YOLOv8 frame by frame
        #stream = True will use the generator and it is more efficient than normal
        results=model(img,stream=True)
        #Once we have the results we can check for individual bounding boxes and see how well it performs
        # Once we have have the results we will loop through them and we will have the bouning boxes for each of the result
        # we will loop through each of the bouning box
        for r in results:
            boxes=r.boxes
            for box in boxes:
                x1,y1,x2,y2=box.xyxy[0]
                x1,y1,x2,y2=int(x1), int(y1), int(x2)+10, int(y2)              
                cv2.rectangle(img, (x1,y1), (x2,y2), (255,0,255),3)
                conf=math.ceil((box.conf[0]*100))/100
                cls=int(box.cls[0])
                class_name=classNames[cls]
                label=f'{class_name}{conf}'
                text1=''
                if conf > 0.8 :
                    # cv2.imwrite(f'output/actual_img/{class_name}_{counter}_{conf}.jpg', img)
                    cropped_img = img[y1:y2, x1:x2]
                    # cv2.imshow("cropped img",cropped_img)
                    # cv2.imwrite(f'output/cropped_img/{class_name}_{counter}_{conf}.jpg', cropped_img)
                    
                    # text=text_detection.read_license_plate(img)

                    license_plate_crop_gary=cv2.cvtColor(cropped_img, cv2.COLOR_BGR2GRAY)
                    
                    _,license_plate_crop_thresh=cv2.threshold(license_plate_crop_gary, 64, 255, cv2.THRESH_BINARY_INV)
                    
                    text1, text_conf = read_license_plate(cropped_img)
                    # text2, text_conf1 = read_license_plate(license_plate_crop_thresh)
                    print(text1)


                    if text1 is not None :

                        
                        text_conf=float(text_conf)
                        text_length = len(text1)
                        

                        if text_conf > 0.3 and text_length > 9: 
                            data=format_license(text1) #formating the text 
                            if license_complies_format(data) :
                                l_pname='{}.jpg'.format(data)
                                success,lptext=video_to_database(l_pname,data, conf)
                                if success:
                                    cv2.imwrite(f"F:\MAIN_PROJECT\VLPR WEB FLASK\output\IMAGES\VIDEO_IMG\{lptext}.jpg", img)

                    t_size = cv2.getTextSize(label, 0, fontScale=1, thickness=2)[0]
                    c2 = x1 + t_size[0], y1 - t_size[1] - 3
                    cv2.rectangle(img, (x1,y1), c2, [255,0,255], -1, cv2.LINE_AA)  # filled
                    cv2.putText(img, class_name, (x1,y1-2),0, 1,[255,255,255], thickness=1,lineType=cv2.LINE_AA)
        yield img
cv2.destroyAllWindows()

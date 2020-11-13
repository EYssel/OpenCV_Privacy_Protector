from face_blurring import anonymize_face_pixelate
from face_blurring import anonymize_face_simple
import hide_subimage
import cv2
import numpy
from PIL import Image
import os
import sys
from tkinter import filedialog

def merge_image(choice, path):
    print("Merging image, choice = " + str(choice))
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    license_plate_cascade = cv2.CascadeClassifier('haarcascade_russian_plate_number.xml')

    img = cv2.imread(path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    if(choice == 1):
        merged = obscure_objects(face_cascade,img,gray,100,100)
        save_path = filedialog.asksaveasfilename(defaultextension='.png')
        cv2.imwrite(save_path, numpy.array(merged))
        cv2.imshow("Blurred Image", numpy.array(merged))
        
    elif(choice == 2):
        merged = obscure_objects(license_plate_cascade,img, gray,100,100)
        save_path = filedialog.asksaveasfilename(defaultextension='.png')
        cv2.imwrite(save_path, numpy.array(merged))
        cv2.imshow("Blurred Image", numpy.array(merged))

def merge_video(choice, path):
    print("Merging video, choice = " + str(choice))
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    license_plate_cascade = cv2.CascadeClassifier('haarcascade_russian_plate_number.xml')
    
    if(choice == 1):
        #save_path = filedialog.asksaveasfilename()
        blur_video(choice, path, face_cascade)
    elif(choice == 2):
        #save_path = filedialog.asksaveasfilename()
        blur_video(choice, path, license_plate_cascade) 

#def unmerge_video

def open_video_capture(path):
    cap = cv2.VideoCapture(path)
    return cap

def blur_video(choice, path, cascade):
    cap = cv2.VideoCapture(path)
    save_path = filedialog.asksaveasfilename()

    frame_width = int(cap.get(3))
    frame_height = int(cap.get(4))

    size = (frame_width, frame_height)
    
    empty = Image.new('RGB', size)
    merged = Image.new('RGB', size)
    
    result = cv2.VideoWriter(save_path,  
                         cv2.VideoWriter_fourcc(*'HFYU'), 
                         5, size) 
    while True:
        _, img = cap.read()

        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

        
        
        merged = obscure_objects(cascade, img, gray, 100, 100)
        if(merged != False):
            merged = numpy.array(merged)
            result.write(merged)
            cv2.putText(merged,"Press Esc to stop Video feed",(25, 25),fontFace=cv2.FONT_HERSHEY_PLAIN,fontScale=1,color=(0, 255, 0))
            cv2.imshow("Blurred Video", merged)
        
        k = cv2.waitKey(30)
        if k == 27:
            break
    cap.release()
    cv2.destroyAllWindows()

def blur_objects(choice):
    frame_count = 0
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    side_cascade = cv2.CascadeClassifier('haarcascade_profileface.xml')
    eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')
    license_plate_cascade = cv2.CascadeClassifier('haarcascade_russian_plate_number.xml')
    
    if(choice == 0):
        # To capture video from webcam
        cap = cv2.VideoCapture(0)
        # To use a video file as input
        #cap = cv2.VideoCapture('4.mp4')
    
        frame_width = int(cap.get(3))
        frame_height = int(cap.get(4))
    
        size = (frame_width, frame_height)
    elif(choice == 1):
        cap = cv2.VideoCapture(0)
        file_path = filedialog.askopenfilename()
        img = cv2.imread(file_path)
        size = (img.shape[1], img.shape[0])

    result = cv2.VideoWriter('merged_webcam.avi',  
                         cv2.VideoWriter_fourcc(*'HFYU'), 
                         5, size) 
    
    decision = -1
    empty = Image.new('RGB', (cv2.CAP_PROP_FRAME_WIDTH, cv2.CAP_PROP_FRAME_HEIGHT))
    merged = Image.new('RGB', (cv2.CAP_PROP_FRAME_WIDTH, cv2.CAP_PROP_FRAME_HEIGHT))
    unmerged = Image.new('RGB', (cv2.CAP_PROP_FRAME_WIDTH, cv2.CAP_PROP_FRAME_HEIGHT))
    while True:
        
        # Read the frame
        #_, img = cap.read()
        
        #print(img.shape)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        if(decision == 0):
            
            merged = obscure_objects(face_cascade, img, gray, 100, 100)
            #merged = obscure_objects(side_cascade, img, gray, 50, 50)
            cv2.destroyWindow('original')
            if(merged != False):
                result.write(numpy.array(merged))
                cv2.putText(merged,"Press Esc to stop Video feed",(25, 25),fontFace=cv2.FONT_HERSHEY_PLAIN,fontScale=1,color=(0, 0, 255))
                cv2.imshow('merged', numpy.array(merged))
                if(choice == 1):
                    decision = -99
            #print("Unmerging...")
            #unmerged = numpy.copy(numpy.array(hide_subimage.unmerge(merged)))
            #cv2.imshow('unmerged', unmerged)
            #print("Done.")

        elif(decision == 1):
            merged = obscure_objects(license_plate_cascade, img, gray, 150, 150)
            cv2.destroyWindow('original')
            if(merged != False):
                cv2.imshow('merged', numpy.array(merged))
                result.write(numpy.array(merged))
                decision = -99
            #unmerged = numpy.copy(numpy.array(hide_subimage.unmerge(merged)))
            #cv2.imshow('unmerged', unmerged)  
        elif(decision != -99):
            cv2.imshow('original', numpy.array(img))
            #print("Waiting for input...")
        #decision = -1
        
        
        k = cv2.waitKey(30)
        if k == ord('f'):
            decision = 0
            print("Selected Faces...")
        elif k == ord('r'):
            decision = 1
            print("Selected license plates...")
        elif k == 27:
            break
    frame_count = frame_count + 1
    result.release()
    cap.release()
    cv2.destroyAllWindows()

def unmerge_image():
    file_path = filedialog.askopenfilename()
    save_path = filedialog.asksaveasfilename(defaultextension='.png')
    merged = cv2.imread(file_path)
    cv2.imshow("Blurred Image", merged)

    unmerged = numpy.copy(numpy.array(hide_subimage.unmerge(Image.fromarray(merged))))
    cv2.imshow("Unmerged",unmerged)

    cv2.imwrite(save_path, unmerged)

def unmerge_video():
    file_path = filedialog.askopenfilename()
    save_path = filedialog.asksaveasfilename()
    cap = cv2.VideoCapture(file_path)
    
    frame_width = 100
    frame_height = 100
    
    size = (frame_width, frame_height) 

    result = cv2.VideoWriter(save_path,  
                         cv2.VideoWriter_fourcc(*'MJPG'), 
                         5, size) 
    
    unmerged = Image.new('RGB', (frame_width, frame_height) )
    while True:
        # Read the frame
        _, merged = cap.read()
        try:
            
            
            #print("Unmerging...")
            unmerged = numpy.copy(numpy.array(hide_subimage.unmerge(Image.fromarray(merged))))
            result.write(numpy.array(unmerged))
            cv2.putText(merged,"Press Esc to stop Video feed",(25, 25),fontFace=cv2.FONT_HERSHEY_PLAIN,fontScale=1,color=(0, 255, 0))
            cv2.imshow('Blurred',merged)
            cv2.imshow('Unblurred', unmerged)
            #print("Done.")
            k = cv2.waitKey(30)
            if k == 27:
                break
        except:
            break
    result.release()
    cap.release()
    cv2.destroyAllWindows()
### FUNCTIONS ###


def obscure_objects(cascade, img, gray, w, h):
    object_w = w
    object_h = h
    # Detect the objects
    objects = cascade.detectMultiScale(gray, 1.1, 4)
    #objects = numpy.array(objects)
    try:
        print(objects.shape)
    except AttributeError:
        print("No objects in frame...")
        return False
    # Draw the rectangle around each face
    merged = Image.new('RGB', (object_w, object_h))
    ROI_Collage = numpy.copy(numpy.zeros(img.shape,dtype=numpy.uint8)) #(face_h, object_w*objects.shape[0]/2,3)
    #print(str(ROI_Collage.shape) + " --- " + str(img.shape))
    prevX = 0
    prevY = 0
    count = 1

    for (x, y, w, h) in objects:
        print(count)
        ROI = numpy.copy(img[y:y+h, x:x+w])
        ROI_Collage[prevY:prevY+object_h, prevX:prevX+object_w] = cv2.resize(img[y:y+h, x:x+w],(object_h, object_w))
        prevX = prevX + object_w
        blur = numpy.copy(anonymize_face_simple(anonymize_face_pixelate(ROI,9),3.0))
        if(prevX + w > ROI_Collage.shape[1]):
            prevX = 0
            prevY = prevY+object_h
        elif(prevY + h > ROI_Collage.shape[0]):
            prevY = 0
            prevX = 0
                    
        img[y:y+h, x:x+w] = numpy.copy(blur)
        count = count+1
    print("Merging...")        
    new_image = hide_subimage.merge_images(Image.fromarray(numpy.uint8(img)), Image.fromarray(numpy.uint8(ROI_Collage)))
                        
    return new_image

def license_plate_detection(license_plate_cascade, img, gray):
    ### LICENSE PLATES ###
            
    license_plates = license_plate_cascade.detectMultiScale(gray, 1.1, 4)
    
    merged = Image.new('RGB', (50, 50))
    #print(img.shape)
    ROI_Collage = numpy.copy(numpy.zeros(img.shape,dtype=numpy.uint8))

    prevX = 0
    prevY = 0
    count = 1

    for (x, y, w, h) in license_plates:
        print("Adding license plate " + str(count) +" to collage")
        
        
        ROI_Collage[prevY:prevY+h, prevX:prevX+w] = (img[y:y+h, x:x+w])
        prevX = prevX + w
        
        if(prevX + w > ROI_Collage.shape[1]):
            prevX = 0
            prevY = prevY+h
        elif(prevY + h > ROI_Collage.shape[0]):
            prevY = 0
            prevX = 0
        
        count = count + 1

    for (x, y, w, h) in license_plates:
        ROI = numpy.copy(img[y:y+h, x:x+w])
        #blur = anonymize_face_pixelate(ROI, 3)
        blur = numpy.copy(anonymize_face_simple(ROI, 3))
        img[y:y+h, x:x+w] = numpy.copy(blur)
        
    new_image = hide_subimage.merge_images(Image.fromarray(numpy.uint8(img)), Image.fromarray(numpy.uint8(ROI_Collage)))
    merged = new_image




#if(decision == 2):

    ## EYES ###
    
#    eyes = eye_cascade.detectMultiScale(gray, 1.1, 4)
    
#    for (x, y, w, h) in eyes:
#        ROI = img[y:y+h, x:x+w]
#        ROI = numpy.flip(ROI)
#        blur = anonymize_face_pixelate(ROI, 5)
#        img[y:y+h, x:x+w] = blur
#        cv2.circle(img, (int(x+(w/2)), int(y+(h/2))),15, (255, 0, 0), 2)
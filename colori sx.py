import cv2 as cv
import numpy as np

camsx = cv.VideoCapture(0)
while True:
    ret, frame = camsx.read()
    
    #convertire da BGR a HSV
    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    
    #definisco il range di colori per il rosso in BGR
    lower_red = np.array([159, 50, 70])
    upper_red = np.array([180, 255, 255 ])
    
    #definisco il range di colori di giallo
    lower_yellow = np.array([18 , 130 , 95])
    upper_yellow = np.array([40 , 255 , 255])
    
    #definisco il range di colori di verde
    lower_green = np.array([36, 50, 70])
    upper_green = np.array([89, 255, 255])
    
    #definisco il range di colori di nero
    lower_black = np.array([0, 0, 0])
    upper_black = np.array([205, 85, 76])
    
    # fa il mascheramento converte tramite hsv da BGR a HSV
    maskr = cv.inRange(hsv, lower_red, upper_red)
    masky = cv.inRange(hsv, lower_yellow, upper_yellow)
    maskg = cv.inRange(hsv, lower_green, upper_green)
    maskb = cv.inRange(hsv, lower_black, upper_black)
    
    #mostra sia il mascheramento che il video
    cv.imshow('video',frame)
    cv.imshow('mascheramento rosso',maskr)
    cv.imshow('mascheramento giallo',masky)
    cv.imshow('mascheramento verde',maskg)
    cv.imshow('mascheramento nero',maskb)
    print(frame[100,100])
   
    #va inserito in ogni programma
    if cv.waitKey(1) & 0xFF == ord('q'):
        break
camsx.release()
cv.destroyAllWindows()
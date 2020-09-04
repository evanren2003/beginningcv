from __future__ import print_function
import argparse
import cv2
import random
import numpy as np

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required = True,
	help = "Path to the image")
args = vars(ap.parse_args())

image = cv2.imread(args["image"])
cv2.imshow("Original", image)
cv2.waitKey(0)

#this is just basic image reading/displaying
#also i want to test pushing to github because i forgot

for i in range(image.shape[0]//2): #inverts colors
    for j in range(image.shape[1]//2):
        (b,g,r) = image[i,j]
        image[i,j] = (255-b,255-g,255-r)

#next, generate random shapes and use the or/and operator :O

cv2.imshow("Updated",image)
cv2.waitKey(0)

imageCopy = cv2.imread(args["image"]) #this is a copy
shapesImage = np.zeros(image.shape[:2],dtype="uint8") #will show just the shapes
shapeList = ["rec","circle"] #create a list to take a random element from
for i in range(4):#what did i just do bruh
    blank = np.zeros(image.shape[:2],dtype="uint8")
    shape = random.choice(shapeList)
    #creates a random circle or rectangle with size in a given range
    if (shape == "rec"):
        startY = random.choice(range(0,image.shape[0]//8))
        endY = random.choice(range(image.shape[0]*7//8,image.shape[0]))
        startX = random.choice(range(0,image.shape[1]//8))
        endX = random.choice(range(image.shape[1]*7//8,image.shape[1]))
        cv2.rectangle(blank,(startX,startY),(endX,endY),255,-1)
        image = cv2.bitwise_not(image,image,mask = blank)
    else:
        centerX = random.choice(range(image.shape[1]*3//8,image.shape[1]*5//8))
        centerY = random.choice(range(image.shape[0]*3//8,image.shape[0]*5//8))
        minDim = min(image.shape[0],image.shape[1])
        radius = random.choice(range(minDim*5//16,minDim*3//8))
        cv2.circle(blank,(centerX,centerY),radius,255,-1)
        image = cv2.bitwise_not(image,image,mask = blank)
    #applies the random shape as a mask to image
    # image = cv2.bitwise_and(image,image,mask = blank)
    #using xor because it's easier to tell where the shapes actually are
    shapesImage = cv2.bitwise_xor(shapesImage,blank)

cv2.imshow("Random Shapes",image)
cv2.waitKey(0)
cv2.imshow("Shapes Image",shapesImage)
cv2.waitKey(0)

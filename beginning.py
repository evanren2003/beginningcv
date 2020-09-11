from __future__ import print_function
from matplotlib import pyplot as plt
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

#loop through the top left corner
for i in range(image.shape[0]//2): #inverts colors
    for j in range(image.shape[1]//2):
        (b,g,r) = image[i,j]
        image[i,j] = (255-b,255-g,255-r) #inverts the r,g,b value for these pixels

cv2.imshow("Updated",image)
cv2.waitKey(0)

shapesImage = np.zeros(image.shape[:2],dtype="uint8") #will show just the shapes
shapeList = ["rec","circle"] #create a list to take a random element from
for i in range(4):#what did i just do bruh
    blank = np.zeros(image.shape[:2],dtype="uint8")
    shape = random.choice(shapeList)
    #creates a random circle or rectangle with size in a given range
    if (shape == "rec"):
		#randomly generate rectangle coordiantes
        startY = random.choice(range(0,image.shape[0]//8))
        endY = random.choice(range(image.shape[0]*7//8,image.shape[0]))
        startX = random.choice(range(0,image.shape[1]//8))
        endX = random.choice(range(image.shape[1]*7//8,image.shape[1]))
        cv2.rectangle(blank,(startX,startY),(endX,endY),255,-1)
        image = cv2.bitwise_not(image,image,mask = blank)
    else:
		#randomly generate center and radius
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

######################################################

imageCopy = cv2.imread(args["image"]) #this is a copy

(blue, green, red) = cv2.split(imageCopy) #blue,green,red have single value elements
zeros = np.zeros(image.shape[:2],dtype = "uint8")

cv2.imshow("bluegreen", cv2.merge([blue,green,zeros]))
cv2.waitKey(0)
cv2.imshow("greenred", cv2.merge([zeros,green,red]))
cv2.waitKey(0)
cv2.imshow("redblue", cv2.merge([blue,zeros,red]))
cv2.waitKey(0)
#next split the image into its rgb and then take the inverse of those?
#think of something creative

cv2.imshow("blue",cv2.merge([blue,zeros,zeros]))
cv2.waitKey(0)

channels = cv2.split(imageCopy) #so I don't have to deal with a list
colors = ("b","g","r")

plt.figure()
plt.title("Color Histogram")
plt.xlabel("Bins")
plt.ylabel("Number of Pixels")

for (channel,color) in zip(channels,colors): #show different color channels
	hist = cv2.calcHist([channel],[0],None,[256],[0,256])
	plt.plot(hist, color = color)
	plt.xlim([0,256])

plt.show()
cv2.waitKey(0)

plt.clf() #clears it

origHist = cv2.calcHist([imageCopy], [0], None, [256], [0, 256])
plt.plot(origHist)
plt.show()
cv2.waitKey(0)

for i in range(imageCopy.shape[0]):
	for j in range(imageCopy.shape[1]):
		#implement an if statement if the thing is black or white
		#so u dont get the random rainbow colors
		(b,g,r) = imageCopy[i,j]
		blueChange = random.choice(range(0,10))
		greenChange = random.choice(range(0,10))
		redChange = random.choice(range(0,10))
		imageCopy[i,j] = (b-blueChange,g-greenChange,r-redChange)

cv2.imshow("adjusted", imageCopy)
cv2.waitKey(0)

newChannels = cv2.split(imageCopy)
newColors = ("b","g","r")

########does this even make sense????
#what is happpening

for (channel,color) in zip(newChannels,newColors): #show different color channels
	hist = cv2.calcHist([channel],[0],None,[256],[0,256])
	plt.plot(hist, color = color)
	plt.xlim([0,256])

plt.show()
cv2.waitKey(0)

#look at different levels of blur (mess around with the arguments)

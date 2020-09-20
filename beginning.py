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

swappedImage = image.copy() #making a copy here for future use

shapesImage = np.zeros(image.shape[:2],dtype="uint8") #will show just the shapes
shapeList = ["rec","circle"] #create a list to take a random element from
for i in range(4):
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
    #image = cv2.bitwise_and(image,image,mask = blank)
    #using xor because it's easier to tell where the shapes actually are
    shapesImage = cv2.bitwise_xor(shapesImage,blank)

cv2.imshow("Random Shapes",image)
cv2.waitKey(0)
cv2.imshow("Shapes Image",shapesImage)
cv2.waitKey(0)

imageCopy = cv2.imread(args["image"]) #I could've (or should've) used image.copy

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

cv2.imshow("blue",cv2.merge([blue,zeros,zeros])) #not sure why i did this but it's here
cv2.waitKey(0)

channels = cv2.split(imageCopy) #channel variable is a list :O
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
		#generate random values for b,g,r and subtract that from each pixel
		(b,g,r) = imageCopy[i,j]
		blueChange = random.choice(range(7,25)) #random value from 7 to 24
		greenChange = random.choice(range(7,25))
		redChange = random.choice(range(7,25))
		imageCopy[i,j] = (b-blueChange,g-greenChange,r-redChange) #change value of original pixel

cv2.imshow("adjusted", imageCopy)
cv2.waitKey(0)

newChannels = cv2.split(imageCopy)
newColors = ("b","g","r")

for (channel,color) in zip(newChannels,newColors): #look at the new histogram after image has been modified
	hist = cv2.calcHist([channel],[0],None,[256],[0,256])
	plt.plot(hist, color = color)
	plt.xlim([0,256])

plt.show()
cv2.waitKey(0)


(height,width) = swappedImage.shape[:2]
center = (width//2,height//2)
#rotate the image by 180 degrees
rot = cv2.getRotationMatrix2D(center,180,1.0)
rotated = cv2.warpAffine(swappedImage, rot, (width,height))
cv2.imshow("rotated by 180", rotated)
cv2.waitKey(0)

for i in range(rotated.shape[0]//2): #invert colors of another corner
    for j in range(rotated.shape[1]//2):
        (b,g,r) = rotated[i,j]
        rotated[i,j] = (255-b,255-g,255-r)

cv2.imshow("corners inverted", rotated)
cv2.waitKey(0)

mixedImage = image.copy() #I tried this with a numpy array at first but couldn't get it to work
#the original value of this image doesn't matter since the pixels are getting changed
#any image can go here as long as the dimensions are right
#gonna swap around pieces of the image
for i in range(rotated.shape[0]//2): #oops should probably use a variable for rotated.shape(1,2)
	for j in range(rotated.shape[1]//2):
		#assigns pixel values according to the original image, but
		#they are in different order, so the image appears to have its corner swapped
		mixedImage[i,j] = rotated[i+(rotated.shape[0])//2,j+(rotated.shape[1])//2]
		mixedImage[i+(rotated.shape[0])//2,j] = rotated[i,j+(rotated.shape[1])//2]
		mixedImage[i,j+(rotated.shape[1])//2] = rotated[i+(rotated.shape[0])//2,j]
		mixedImage[i+(rotated.shape[0])//2,j+(rotated.shape[1])//2] = rotated[i,j]

#use image transformation and the numpy copy method to make a copy of the image
#and take values from the original amtrix but in different order
#so the topright and bottom left corners get swapped
#and top left and bottom right corners get swapped
#for example
#12 becomes 43
#34         21

cv2.imshow("mixed image", mixedImage)
cv2.waitKey(0)

#invert the center square
for i in range(rotated.shape[0]//2):
	for j in range(rotated.shape[1]//2):
		(b,g,r) = mixedImage[i+rotated.shape[0]//4,j+rotated.shape[1]//4]
		mixedImage[i+rotated.shape[0]//4,j+rotated.shape[1]//4] = (255-b,255-g,255-r)

cv2.imshow("center square inverted", mixedImage)
cv2.waitKey(0)

#testing 5 as argument for the 3 differnt types of blurs
blur = cv2.blur(mixedImage, (5,5))
gaussian = cv2.GaussianBlur(mixedImage, (5,5), 0)
median = cv2.medianBlur(mixedImage, 5)

cv2.imshow("average blur", blur)
cv2.waitKey(0)
cv2.imshow("gaussian blur", gaussian)
cv2.waitKey(0)
cv2.imshow("median blur", median)
cv2.waitKey(0)

#just seeing what happens when the arguments are set VERY BIG for the different blurs
mediumMedian = cv2.medianBlur(mixedImage, 51)
cv2.imshow("mediumMedian", mediumMedian)
cv2.waitKey(0)

mediumGaussian = cv2.GaussianBlur(mixedImage, (51,51), 0)
cv2.imshow("mediumGaussian", mediumGaussian)
cv2.waitKey(0)

mediumBlur = cv2.blur(mixedImage, (51,51))
cv2.imshow("BLur", mediumBlur)
cv2.waitKey(0)

bigBlur = cv2.blur(mixedImage, (101,101))
cv2.imshow("BLUR", bigBlur)
cv2.waitKey(0)

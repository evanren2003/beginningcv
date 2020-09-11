import numpy as np
import argparse
import imutils
import cv2

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required = True,
help = "Path to the image")
args = vars(ap.parse_args())

image = cv2.imread(args["image"])
cv2.imshow("Original", image)

r = 76.0/image.shape[1]
dim = (76, int(image.shape[0]*r))

resized = cv2.resize(image,dim,interpolation = cv2.INTER_NEAREST)
cv2.imshow("Resized (Width)", resized)

resized = imutils.resize(image, width = 150)
cv2.imshow("Resized via Function", resized)
cv2.waitKey(0)

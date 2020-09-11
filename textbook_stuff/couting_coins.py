from __future__ import print_funtion
import numpy as np
import argparse
import cv2

def grab_contours(cnts):
    if len(cnts) == 2:
        cnts = cnts[0]

    elif len(cnts) == 3:
       cnts = cnts[1]

    else:
       raise Exception(("Contours tuple must have length 2 or 3,"
       "otherwise OpenCV changed their cv2.findContours return signature yet again."
       "Refer to OpenCV’s documentation in that case."))

    return cnts

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required = True, help = "Path to the image")
args = vars(ap.parse_args())

image = cv2.imread(args["image"])
image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
image = cv2.GaussianBlur(image, (12, 12), 0)
cv2.imshow("Blurred", image)

canny = cv2.Canny(image, 40, 160)
cv2.imshow("Canny", canny)
cv2.waitKey(0)

cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2 .CHAIN_APPROX_SIMPLE)
cts = grab_contours(cnts)

print("I count {} coins in this image".format(len(cnts)))

coins = image.copy()
cv2.drawContours(coins, cnts, -1, (255, 0, 180), 2)
cv2.imshow("Coins", coins)
cv2.waitKey(0)

for (i, c) in enumerate(cnts):
    (x, y, w, h) = cv2.boundingRect(c)

    print("Coin #{}".format(i + 1))
    coin = image[y:y + h, x:x + w]
    cv2.imshow("Coin", coin)

    mask = np.zeros(image.shape[:2], dtype = "uint8")
    ((centerX, centerY), radius) = cv2.minEnclosingCircle(c)
    cv2.circle(mask, (int(centerX), int(centerY)), int(radius), 255, -1)
    mask = mask[y:y + h, x:x + w]
    cv2.imshow("Masked Coin", cv2.bitwise_and(coin, coin, mask = mask))
    cv2.waitKey(0)

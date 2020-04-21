from matplotlib import pyplot as io
import numpy as np
from PIL import Image
from random import randint
import math
import copy

# Generate k coordinates within the size of img and store in dictionary
# clusterNum: [coordX, coordY]
def generatePoints(k, img):
    clusters = {}
    for i in range(k):
        x = randint(0, len(img))
        y = randint(0, len(img[0]))
        r, g, b = int(img[x][y][0]), int(img[x][y][1]), int(img[x][y][2])
        clusters[i] = [x, y, r, g, b]

    return clusters

# Image to array
def imgToArray(imgName):
    img = io.imread(imgName) #image is saved as rows * columns * 3 array
    return img


#Array to image file
def arrayToImg(imgArray, k, imgName):
    """
    # Example of how the array should be formatted
    array = np.zeros([10,20,3], dtype = np.uint8)
    array[:,:10] = [255, 128, 0] # Orange left side
    array[:,10:] = [0,0,255] # Blue right side
    print(array)
    """
    img = Image.fromarray(imgArray)
    img.save(str(k) + 'k' + imgName + '.png')


if __name__ == "__main__":
    # Cluster, K, values to test
    kVals = [2, 5, 10, 15, 20]

    # Get image filename from user
    filename = input("Enter image filename: ")
    imgName = filename.split('.')[0]
    # Convert image to array
    img = imgToArray(filename)

    # Get number of rows and columns in the image
    rows = len(img)
    cols = len(img[0])
    # Run Kmeans algorithm on image for each given k value
    for k in kVals:
        # Generate k random coordinates as beginning clusters
        clusters = generatePoints(k, img)

        newClusters = {}
        clusterGroup = {}
        while True:
            newClusters = {}
            clusterGroup = {}

            # Assign each pixel to closest cluster (in respect to RGB values)
            for r in range(rows):
                for c in range(cols):
                    pxlRGB = img[r][c]
                    distances = []
                    for clustRow, clustCol, clustR, clustG, clustB in clusters.values():

                        """
                        # If (x,y) of pixels are factored in it creates interesting images!
                        dSum = math.pow(clustRow - r, 2)
                        dSum += math.pow(clustCol - c, 2)
                        """
                        dSum = math.pow(clustR - int(pxlRGB[0]), 2)
                        dSum += math.pow(clustG - int(pxlRGB[1]), 2)
                        dSum += math.pow(clustB - int(pxlRGB[2]), 2)
                        dist = math.sqrt(dSum)

                        distances.append(dist)
                    clusterGroup[(r, c)] = distances.index(min(distances))

            # Calculate the new coordinates for each cluster by meaning coordinates of all pixels belonging
            # to each cluster
            for j in range(k):
                xSum, ySum, rSum, gSum, bSum = (0, 0, 0, 0, 0)
                total = 0
                for r in range(rows):
                    for c in range(cols):
                        if clusterGroup[(r, c)] == j:
                            pxlRGB = img[r][c]

                            xSum += r
                            ySum += c
                            rSum += pxlRGB[0]
                            gSum += pxlRGB[1]
                            bSum += pxlRGB[2]
                            total += 1

                xAvg = xSum / total
                yAvg = ySum / total
                rAvg = rSum / total
                bAvg = bSum / total
                gAvg = gSum / total

                newClusters[j] = [int(xAvg), int(yAvg), int(rAvg), int(gAvg), int(bAvg)]

            # If cluster locations do not change, then the algorithm is finished
            if clusters == newClusters:
                break
            clusters = copy.deepcopy(newClusters)

        # Create a new array and assign the new pixel values
        newImg = np.zeros([rows,cols,3], dtype = np.uint8)
        for r in range(rows):
            for c in range(cols):
                cg = clusterGroup[(r, c)]
                rgbVals = newClusters[cg][2:]
                newImg[r, c] = rgbVals

        # Convert the array to an image
        arrayToImg(newImg, k, imgName)

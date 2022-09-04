# ----------BEGIN CONFIGURATION----------

# the frame-delimiting number of consecutive black columns
blackThreshold = 20

# -----------END CONFIGURATION-----------

import cv2
import argparse

# ----------BEGIN FUNCTIONS----------

# transpose provided >=2-D list one level deep
def getShallowTranspose (arr):
    return [list(ele) for ele in zip(*arr)]

# detect columns that are (nearly) all black
def isBlackCol (col):
    return not bool([True for ele in getShallowTranspose(col) if 
                 sum(ele) / len(col) > 10])

# -----------END FUNCTIONS-----------

# ----------BEGIN ARGUMENTS----------

parser = argparse.ArgumentParser()

# destination directory for processed images
parser.add_argument("destination_directory",
                    metavar='D',
                    type=str,
                    help="destination directory for this round of cropped frames (must exist and be empty)")

# list of images to extract frames (in order)
parser.add_argument("images", 
                    metavar='I', 
                    type=str, 
                    nargs='+', 
                    help="list of images to process; must be entered in chronological order")

args = parser.parse_args()

# -----------END ARGUMENTS-----------

# ----------BEGIN INITIALIZATION----------

# initialize frames list
frames = []

# initialize active frame column list
activeFrame = []

# initialize black counter
blackCounter = 0

# -----------END INITIALIZATION-----------

# iterate over each provided image
for image in images:
    
    # load in the next image
    activeImage = cv2.imread(image)   

    # get a list of the image's columns
    activeImageCols = getShallowTranspose(activeImage)

    # iterate over each of the image's columns
    for col in activeImageCols:
        
        # append colored columns to the active frame
        if not isBlackCol(col):
            activeFrame.append(col)
            continue
        
        # append black columns within the threshold to the active frame, if present
        if isBlackCol(col) and activeFrame and blackCounter < blackThreshold:
            activeFrame.append(col)
            blackCounter += 1
            continue
        
        if isBlackCol(col) and blackCounter == blackThreshold:
            frames.append(activeFrame[0:-blackCounter])
            activeFrame = []
            blackCounter = 0
            continue

# 1. check column
# 1a. if not black and active frame not empty, append to active frame
# 1b. if black and active frame not empty, increment black counter
# 1c. if black counter has reached threshold, remove previous [black counter]
#     columns from active frame, append active frame to finished frames list,
#     clear active frame
# 1d. if black and active frame empty, do nothing
# 1e. if not black and active frame empty, append to active frame
# 2. increment column counter
# 2a. if end of image, load next image and continue as normal

"""Library implementation of GSOC'19 Eval task."""

from datetime import datetime
from pytz import timezone
import os
import h5py
import pandas as pd
import numpy as np
from scipy.signal import medfilt
import matplotlib.pyplot as plt

lst = []

def getUTC(filePath, length):
    """Convert filename from UNIX time in nanoseconds to UTC time.

    Takes a file path as input and the length of the UNIXTime chars
    in the name (18 in the task). Returns a utc datetime
    object. Assuming input is always in nanoseconds.
    """
    fileName = os.path.splitext(os.path.basename(filePath))[0]
    unixTime = int(fileName[:length])//(10**9)
    utcTime = utc.localize(datetime.utcfromtimestamp(unixTime))
    return utcTime

def getLocalTime(utcTime, tzone):
    """Convert utcTime to specific timezone and returns datetime obj.

    Simple function that takes a utcTime obj and pytz timezone as input
    and returns a localized datetime obj.
    """
    localTime = utcTime.astimezone(tzone)
    return localTime


def getCSV(filePath, name):
    """Open .h5 file and classifies contents as specified in the GSOC Task.

    Uses the classify helper function to recursively reach every node and
    classifies using h5py types. For now, numpy TypeErrors are handled via
    'UnknownType'. Furthermore, some attributes do not apply to Groups and
    are represented by 'None'
    """
    categories = ['Name','Structure', 'DataType', 'Shape', 'Size']
    fileInput = h5py.File(filePath, 'r')
    fileInput.visititems(classify)
    db = pd.DataFrame(lst, columns = categories)
    db.to_csv(name + '.csv',index=False)
    return db

def arrayPNG(imageData, imageHeight, imageWidth):
    """Convert 1D array of image data to 2D png output image.

    Takes arrays ImageData, ImageHeight and ImageWidth as input.
    Exports a PNG image.
    """
    imageArray = np.reshape(imageData, (imageHeight[0], imageWidth[0]))
    img = medfilt(imageArray)
    imgplot = plt.imshow(img)
    plt.imsave('test.png', img)

def classify(name, obj):
    """Callable Func to recursively iterate .h5 file and return rows in a df."""
    name = name.split("/")[-1]
    if(isinstance(obj, h5py.Dataset)):
        try:
            lst.append([name, 'Dataset', obj.dtype, obj.shape, obj.size])
        except TypeError:
            lst.append([name, 'Dataset', 'Unknown Type', obj.shape, obj.size])
    elif(isinstance(obj, h5py.Group)):
        lst.append([name, 'Group', None, None, None])

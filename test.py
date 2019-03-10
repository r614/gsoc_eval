"""Testing script for the taskLibrary."""

from taskLibrary import *

path = '1541962108935000000_167_838.h5'
length = 18

utc = getUTC(path, length)
cernZone = timezone('Europe/Zurich')
cernTime = getLocalTime(utc,cernZone)

database = getCSV(path, 'test')


fileInput = h5py.File(path, 'r')
imagedatapath = fileInput['AwakeEventData']['XMPP-STREAK']['StreakImage']
imageData = imagedatapath['streakImageData']
imageHeight = imagedatapath['streakImageHeight']
imageWidth = imagedatapath['streakImageWidth']

image = arrayPNG(imageData, imageHeight, imageWidth)

import xml.dom.minidom
import re
import utm
import math
import collections


class LoadGCPs:

    def __init__(self):

        LoadGCPs.kmlDoc = xml.dom.minidom.parse('doc.kml')
        LoadGCPs.gcpData = LoadGCPs.kmlDoc.getElementsByTagName('SimpleData')
        LoadGCPs.gcpNo = []
        LoadGCPs.gcpLongitudeUTM = []
        LoadGCPs.gcpLongitude = []
        LoadGCPs.gcpLatitudeUTM = []
        LoadGCPs.gcpLatitude = []
        LoadGCPs.gcpAltitude = []
        LoadGCPs.gcpCode = []
        LoadGCPs.xCoordinates = []
        LoadGCPs.yCoordinates = []
        LoadGCPs.no_X_Y = collections.OrderedDict()

        for s in LoadGCPs.gcpData[::5]:
            LoadGCPs.gcpNo.append(s.childNodes[0].nodeValue)

        for s in LoadGCPs.gcpData[1::5]:
            LoadGCPs.gcpLongitudeUTM.append(s.childNodes[0].nodeValue)

        for s in LoadGCPs.gcpData[2::5]:
            LoadGCPs.gcpLatitudeUTM.append(s.childNodes[0].nodeValue)

        for s in LoadGCPs.gcpData[3::5]:
            LoadGCPs.gcpAltitude.append(s.childNodes[0].nodeValue)

        for s in LoadGCPs.gcpData[4::5]:
            LoadGCPs.gcpCode.append(s.childNodes[0].nodeValue)

        for long, lat in zip(LoadGCPs.gcpLongitudeUTM, LoadGCPs.gcpLatitudeUTM):
            temp = utm.to_latlon(float(long), float(lat), 43, 'U')
            LoadGCPs.gcpLongitude.append(temp[0])
            LoadGCPs.gcpLatitude.append(temp[1])
            LoadGCPs.xCoordinates.append(6371 * math.cos(temp[1]) * math.cos(temp[0]))
            LoadGCPs.yCoordinates.append(6371 * math.cos(temp[1]) * math.sin(temp[0]))

        for gcpCode, xCoordinate, yCoordinate in zip(LoadGCPs.gcpCode, LoadGCPs.xCoordinates, LoadGCPs.yCoordinates):
            if gcpCode.startswith("GPS"):
               continue
            else:
                LoadGCPs.no_X_Y[gcpCode] = [gcpCode, xCoordinate, yCoordinate]


class LoadImages:

    def __init__(self):

        LoadImages.kmlDoc = xml.dom.minidom.parse('location.kml')
        LoadImages.imagesData = LoadImages.kmlDoc.getElementsByTagName('Placemark')
        LoadImages.imageNames = []
        LoadImages.imagePaths = []
        LoadImages.imageCoordinates = []
        LoadImages.imageLongitude = []
        LoadImages.imageLatitude = []
        LoadImages.xCoordinates = []
        LoadImages.yCoordinates = []

        for placemark in LoadImages.imagesData:

            name = placemark.getElementsByTagName('name')[0]
            if name.childNodes[0].data != 'path':
                LoadImages.imageNames.append(name.childNodes[0].data)

            description = placemark.getElementsByTagName('description')
            for data in description:
                table = str(data.childNodes[0].data)
                img_src = re.findall(r'\"(.+?)\"', table)
                LoadImages.imagePaths.append(img_src[0])

            points = placemark.getElementsByTagName('Point')
            for point in points:
                LoadImages.imageCoordinates.append(point.getElementsByTagName('coordinates')[0].childNodes[0].data.strip().split(','))

        #counter = 0
        for imageData in LoadImages.imageCoordinates:

            #counter += 1
            LoadImages.imageLongitude.append(imageData[0])
            LoadImages.imageLatitude.append(imageData[1])
            LoadImages.xCoordinates.append(6371 * math.cos(float(imageData[0])) * math.cos(float(imageData[1])))
            LoadImages.yCoordinates.append(6371 * math.cos(float(imageData[0])) * math.sin(float(imageData[1])))





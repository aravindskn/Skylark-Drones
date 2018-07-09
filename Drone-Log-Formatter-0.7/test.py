import piexif
exif_dict = piexif.load("DSC02924.JPG")
print(exif_dict)
gps_ifd = {
            piexif.GPSIFD.GPSAltitude: 123
        }
exif_bytes = piexif.dump(exif_dict)
"""
Copyright (C) 2016 Skylark Drones
Geotagger class geotags images using two methods which are CAM msg synchronisation and time-offset method.
"""

import logging
from os import path, listdir, makedirs
from fnmatch import filter
from sys import exit
from shutil import copy
from fractions import Fraction
from datetime import datetime
import piexif
import flightcolumndict as fcd
import flightmath as fm

if __name__ == '__main__':
    logger = logging.getLogger("DroneLogFormatter")
else:
    logging.basicConfig(format='[%(levelname)s]: %(message)s')
    logger = logging.getLogger("Geotagger")
    logger.setLevel(logging.INFO)


class Geotagger(object):

    cam_msgs = []
    CAM_MSGS_HEADER = {'CAM': fcd.Dict().get_flight_columns()['CAM']}

    @staticmethod
    def geotag_images(cam_file_path, raw_images_folder, geotagged_images_folder, geotag_tolerance, flight_start_time, flight_end_time):
        """High level geotag photos function

        This is the high level function used to geotag images using either the CAM msg
        synchronisation method or the time-offset method depending on the number of
        CAM msgs and photos available.

        Args:
            :param cam_file_path: Absolute path of CAM msgs log file (str)
            :param raw_images_folder: Absolute path of raw images folder (str)
            :param geotagged_images_folder: Absolute path of geotagged images folder (str)
            :param geotag_tolerance: Geotag time tolerance (float)
            :param flight_start_time: Flight start time (datetime)
            :param flight_end_time: Flight end time (datetime)
        """
        Geotagger.verify_raw_images_folder(raw_images_folder)
        Geotagger.verify_cam_file_exists(cam_file_path)
        Geotagger.create_geotag_folder(geotagged_images_folder)

        Geotagger.get_cam_msgs(cam_file_path)
        filtered_images = Geotagger.filter_images(raw_images_folder, flight_start_time.replace(tzinfo=None), flight_end_time.replace(tzinfo=None))

        logger.debug("Checking the count of CAM msgs and number of raw photos for geotagging.")
        same_image_cam_count = Geotagger.check_one_to_one_count(cam_file_path, filtered_images)

        if same_image_cam_count:
            logger.info("Number of raw photos and CAM msgs are the same. "
                        "Suggested geotagging method: CAM Message Synchronisation")
            Geotagger.cam_msg_geotag(raw_images_folder, geotagged_images_folder, filtered_images)
        else:
            logger.info("Going for Time offset geotagging method as number of CAM msgs and raw photos are different.")
            Geotagger.time_offset_geotag(raw_images_folder, geotagged_images_folder, geotag_tolerance, filtered_images)

    @staticmethod
    def gps_deg_to_dms(lat, lng):
        """Convert GPS coords from decimals to degrees, minutes, seconds and hemisphere

        Args:
            :param lat: GPS Latitude in decimals (str)
            :param lng: GPS Longitude in decimals (str)

        Returns:
            dict: GPS Latitude and Longitude in degrees, minutes, seconds and hemisphere
            Example: {
                        'Lat': {'Deg': 35, 'Min': 23, 'Sec': 45.555, 'Hem': 'N'},
                        'Lng': {'Deg': 23, 'Min': 31, 'Sec': 55.555, 'Hem': 'E'}
                     }
        """
        lat_hemisphere = "S" if lat[:1] == "-" else "N"
        lng_hemisphere = "W" if lng[:1] == "-" else "E"

        lat = abs(float(lat))
        lng = abs(float(lng))

        lat_deg = int(lat)
        lng_deg = int(lng)

        temp_lat_min = (lat - lat_deg) * 60
        lat_min = int(temp_lat_min)
        lat_sec = (temp_lat_min - lat_min) * 60

        # TODO Verify accuracy of GPS lng
        temp_lng_min = (lng - lng_deg) * 60
        lng_min = int(temp_lng_min)
        lng_sec = (temp_lng_min - lng_min) * 60

        return {
            'Lat': {'Deg': lat_deg, 'Min': lat_min, 'Sec': lat_sec, 'Hem': lat_hemisphere},
            'Lng': {'Deg': lng_deg, 'Min': lng_min, 'Sec': lng_sec, 'Hem': lng_hemisphere}
        }

    @staticmethod
    def gps_dms_decimals_to_fractions(coordinates):
        """Convert GPS degrees, minutes and seconds into fractions

        GPS coordinates inputted in degrees, minutes and seconds (dms) is converted into
        fraction. This is a requirement for writing exif tags to an image as specified in
        the official exif documentation at http://www.cipa.jp/std/documents/e/DC-008-2012_E.pdf

        Args:
            :param coordinates: GPS Coordinates (dict)

        Returns:
            dict: GPS coordinates in fractions
        """
        lat_deg = Fraction(coordinates['Lat']['Deg']).limit_denominator(1)
        lat_min = Fraction(coordinates['Lat']['Min']).limit_denominator(10)
        lat_sec = Fraction(coordinates['Lat']['Sec']).limit_denominator(10)

        lng_deg = Fraction(coordinates['Lng']['Deg']).limit_denominator(1)
        lng_min = Fraction(coordinates['Lng']['Min']).limit_denominator(10)
        lng_sec = Fraction(coordinates['Lng']['Sec']).limit_denominator(10)

        return {
            'Lat': {
                'Deg': (lat_deg.numerator, lat_deg.denominator),
                'Min': (lat_min.numerator, lat_min.denominator),
                'Sec': (lat_sec.numerator, lat_sec.denominator),
                'Hem': coordinates['Lat']['Hem']
            },

            'Lng': {
                'Deg': (lng_deg.numerator, lng_deg.denominator),
                'Min': (lng_min.numerator, lng_min.denominator),
                'Sec': (lng_sec.numerator, lng_sec.denominator),
                'Hem': coordinates['Lng']['Hem']
            }
        }

    @staticmethod
    def write_gps_exif(coordinate, altitude, read_image_path, write_image_path):
        """Write gps exif data into an image

        Args:
            :param coordinate: GPS coordinates in fractions (dict)
            :param altitude: Altitude in fractions (list)
            :param read_image_path: Absolute path of image that needs to be geotagged (str)
            :param write_image_path: Absolute path of geotagged image (str)
        """
        exif_dict = piexif.load(read_image_path)
        gps_ifd = {
            piexif.GPSIFD.GPSLatitudeRef: coordinate['Lat']['Hem'],
            piexif.GPSIFD.GPSLatitude: (
                (coordinate['Lat']['Deg']),
                (coordinate['Lat']['Min']),
                (coordinate['Lat']['Sec'])
            ),
            piexif.GPSIFD.GPSLongitude: (
                (coordinate['Lng']['Deg']),
                (coordinate['Lng']['Min']),
                (coordinate['Lng']['Sec'])
            ),
            piexif.GPSIFD.GPSLongitudeRef: coordinate['Lng']['Hem'],
            piexif.GPSIFD.GPSAltitude: altitude
        }
        exif_dict['GPS'] = gps_ifd
        exif_bytes = piexif.dump(exif_dict)
        piexif.insert(exif_bytes, write_image_path)

    @staticmethod
    def filter_images(raw_images_folder, flight_start_time, flight_end_time):
        """Filter images based on flight start and end time

        Args:
            :param raw_images_folder: Absolute path of raw images folder (str)
            :param flight_start_time: Flight start time in local time (datetime)
            :param flight_end_time: Flight end time in local time (datetime)

        Returns:
             list: Filtered images list
        """
        images = filter(listdir(raw_images_folder), '*.jpg')
        filtered_images = []
        logger.debug("Cleaning up images list by eliminating those outside the flight duration")
        for image in images:
            image_creation_time = datetime.strptime(Geotagger.read_creation_time_exif(raw_images_folder + image), '%Y:%m:%d %H:%M:%S')
            if flight_start_time <= image_creation_time <= flight_end_time:
                filtered_images.append({'Image': image, 'Creation_Time': image_creation_time})

        return filtered_images

    @staticmethod
    def cam_msg_geotag(raw_images_folder, geotagged_images_folder, images, emitProgess=None):
        """Perform CAM msg geotagging

        This will do a 1-to-1 geotagging of images using CAM msg synchronisation. This
        function will fail if no of images do not match no of CAM msgs.

        Args:
            :param raw_images_folder: Absolute path of raw images folder (str)
            :param geotagged_images_folder: Absolute path of folder where geotagged images will be saved (str)
            :param images: Filtered images list (list)
            :param emitProgess: Notify GUI after geotagging an image (function)
        """
        for index, image in enumerate(images):
            coordinate = Geotagger.gps_dms_decimals_to_fractions(Geotagger.gps_deg_to_dms(Geotagger.cam_msgs[index]['Lat'], Geotagger.cam_msgs[index]['Lng']))
            altitude = Fraction(Geotagger.cam_msgs[index]['Abs_Alt']).limit_denominator(100)
            altitude = (altitude.numerator, altitude.denominator)
            logger.debug("Geotagging [{}/{}]: {}".format(index+1, len(images), raw_images_folder+image['Image']))
            if emitProgess is not None:
                emitProgess()
            copy(raw_images_folder+image['Image'], geotagged_images_folder)
            Geotagger.write_gps_exif(coordinate, altitude, raw_images_folder+image['Image'], geotagged_images_folder+image['Image'])

    @staticmethod
    def time_offset_geotag(raw_images_folder, geotagged_images_folder, geotag_tolerance, images, emitProgess=None):
        """Perform time-offset geotagging

        This will calculate the time diff between the first CAM msg and first image creation time to get a time diff.
        This time diff will then be used to match CAM msgs to their corresponding image file. If it matches, then the
        GPS coordinates of the CAM msg is written to the image exif tag.

        Args:
            :param raw_images_folder: Absolute path of raw images folder (str)
            :param geotagged_images_folder: Absolute path of geotagged images folder (str)
            :param geotag_tolerance: Geotag tolerance (float)
            :param images: Filtered images list (list)
            :param emitProgess: Notify GUI after geotagging an image (function)
        """
        first_image_creation_time = images[0]['Creation_Time']
        first_cam_msg_time = fm.FlightMath().gps_to_local(int(Geotagger.cam_msgs[0]['GPSWeek']), int(Geotagger.cam_msgs[0]['GPSTime'])/1000).replace(tzinfo=None)
        global_time_diff = first_cam_msg_time - first_image_creation_time

        logger.debug("First image creation time: {}".format(first_image_creation_time))
        logger.debug("First cam msg time: {}".format(first_cam_msg_time))
        logger.debug("Calculated time diff: {} seconds".format(global_time_diff.total_seconds()))

        total_image_geotagged = 0

        for index, image in enumerate(images):
            image_creation_time = image['Creation_Time']

            for sub_index, cam_line in enumerate(Geotagger.cam_msgs):
                cam_msg_time = fm.FlightMath().gps_to_local(int(Geotagger.cam_msgs[sub_index]['GPSWeek']),int(Geotagger.cam_msgs[sub_index]['GPSTime'])/1000).replace(tzinfo=None)
                new_cam_msg_time = cam_msg_time + -1 * global_time_diff
                diff = image_creation_time - new_cam_msg_time

                if abs(diff.total_seconds()) <= geotag_tolerance:
                    coordinate = Geotagger.gps_dms_decimals_to_fractions(Geotagger.gps_deg_to_dms(Geotagger.cam_msgs[sub_index]['Lat'], Geotagger.cam_msgs[sub_index]['Lng']))
                    altitude = Fraction(Geotagger.cam_msgs[sub_index]['Abs_Alt']).limit_denominator(100)
                    altitude = (altitude.numerator, altitude.denominator)
                    copy(raw_images_folder + image['Image'], geotagged_images_folder)
                    logger.debug("Geotagging [{}/{}]: {}".format(index + 1, len(images), raw_images_folder + image['Image']))
                    Geotagger.write_gps_exif(coordinate, altitude, raw_images_folder + image['Image'], geotagged_images_folder + image['Image'])
                    total_image_geotagged += 1
                    if emitProgess is not None:
                        emitProgess()
                    #Geotagger.cam_msgs.remove(cam_line)
                    break

        logger.debug("CAM Msg list: {}".format(Geotagger.cam_msgs))
        logger.debug("Total images geotagged: {}/{}".format(total_image_geotagged, len(images)))

        if not total_image_geotagged == len(images):
            logger.critical("Not all raw images were geotagged!")

    @staticmethod
    def read_creation_time_exif(read_image_path):
        """Read image creation time from jpg exif tags

        Args:
            :param read_image_path: Absolute path of image path (str)
        """
        exif_dict = piexif.load(read_image_path)
        return exif_dict['Exif'][piexif.ExifIFD.DateTimeOriginal].decode()

    @staticmethod
    def get_cam_msgs(cam_file_path):
        """Grab useful flight data from the CAM msg line

        Args:
            :param cam_file_path: Absolute path of CAM msgs file path (str)

        Raises:
            IOError: If file cannot be found
        """
        try:
            logger.debug("Reading CAM file: {}".format(cam_file_path))
            with open(cam_file_path, 'r') as cam_file:
                for index, line in enumerate(cam_file):
                    line.rstrip()
                    line_parts = line.split(",")
                    line_parts = [s.strip() for s in line_parts]
                    if index == 0:
                        fcd.Dict.get_column_header('CAM', line_parts, Geotagger.CAM_MSGS_HEADER, 0)
                        logger.debug("CAM msgs header: {}".format(Geotagger.CAM_MSGS_HEADER))
                    else:
                        Geotagger.cam_msgs.append({
                            'Lat': line_parts[Geotagger.CAM_MSGS_HEADER['CAM']['Lat']['Index']],
                            'Lng': line_parts[Geotagger.CAM_MSGS_HEADER['CAM']['Lng']['Index']],
                            'Abs_Alt': line_parts[Geotagger.CAM_MSGS_HEADER['CAM']['Abs_Alt']['Index']],
                            'GPSTime': line_parts[Geotagger.CAM_MSGS_HEADER['CAM']['GPSTime']['Index']],
                            'GPSWeek': line_parts[Geotagger.CAM_MSGS_HEADER['CAM']['GPSWeek']['Index']]
                        })
            cam_file.close()
            logger.debug("CAM Msgs (for Geotagging): {}".format(Geotagger.cam_msgs))
        except IOError:
            logger.critical("Unable to open CAM msgs file required for geotagging. Please check the readability of the "
                            "file. Aborting!")
            exit()

    @staticmethod
    def create_geotag_folder(folder_path):
        """Create output geotag folder if it doesn't exist

        Args:
            :param folder_path: Absolute path of geotag folder (str)
        """
        logger.debug("Creating output geotag folder if it doesn't exist")
        geotag_folder_exist = path.isdir(folder_path) and path.exists(folder_path)

        if not geotag_folder_exist:
            makedirs(folder_path)

    @staticmethod
    def verify_raw_images_folder(folder_path):
        """Verify existence of raw images folder

        Args:
            :param folder_path: Absolute path of folder (str)
        """
        logger.debug("Verifying existence of raw images")
        raw_images_exist = path.isdir(folder_path) and path.exists(folder_path)
        if not raw_images_exist:
            logger.critical("Cannot find the raw images folder. Please ensure they are located inside the log folder as"
                            " Raw_Images. Cannot proceed geotagging. Aborting!")
            exit()
        else:
            return True

    @staticmethod
    def verify_cam_file_exists(cam_file_path):
        """Verify existence of CAM msgs file

        Args:
            :param cam_file_path: Absolute path of CAM msgs log file (str)
        """
        cam_file_exists = path.exists(cam_file_path)
        logger.debug("Verifying existence of CAM msgs file")
        if not cam_file_exists:
            logger.critical("Cannot find the CAM msgs file. Cannot proceed geotagging. Aborting!")
            exit()
        else:
            return True

    @staticmethod
    def check_one_to_one_count(cam_file_path, images):
        """Check if the no of CAM msgs and no of raw images match

        Args:
            :param cam_file_path: Absolute path of CAM msgs log file (str)
            :param images: Filtered images list (list)

        Returns:
            bool: True if no of cam msgs and no of images are the same, False otherwise
        """
        try:
            logger.debug("Reading CAM file: {}".format(cam_file_path))
            cam_file = open(cam_file_path, 'r')
            no_of_cams = -1  # This is -1 to account for the CAM file header line which is removed
            for line in cam_file:
                no_of_cams += 1
            cam_file.close()
        except IOError:
            logger.critical("Unable to open CAM msgs file required for geotagging. Please check the readability of the "
                            "file. Aborting!")
            exit()

        logger.debug("CAM msgs count: {}, Images count: {}".format(no_of_cams, len(images)))
        return no_of_cams == len(images)

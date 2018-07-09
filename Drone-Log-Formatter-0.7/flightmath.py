"""
Copyright (C) 2016 Skylark Drones
Utility class FlightMath which provides different functionalities like converting GPS time to local Time, converting
milliseconds to time, calculating max wind speed etc.
"""

import logging
from os import stat
from math import fabs
from operator import sub
from datetime import (datetime, timedelta)
import dateutil.tz

if __name__ == '__main__':
    logger = logging.getLogger("DroneLogFormatter")
else:
    logging.basicConfig(format='[%(levelname)s]: %(message)s')
    logger = logging.getLogger("FlightMath")
    logger.setLevel(logging.INFO)


class FlightMath(object):

    @staticmethod
    def convert_ms_to_duration(total_ms):
        """Convert milliseconds to duration

        Args:
            :param total_ms: Total time in milliseconds (int)

        Returns:
            dict: hours, minutes and seconds.
            Example: { 'hours': 13, 'minutes': 40, 'seconds': 10 }
        """
        return {
            'hours': (total_ms // (1000 * 60 * 60)) % 24,
            'minutes': (total_ms // (1000 * 60)) % 60,
            'seconds': (total_ms // 1000) % 60
        }

    @staticmethod
    def calculate_wind_speed(ground_speed, air_speed):
        """Calculate wind speed from given air speed and ground speed

        Args:
            :param ground_speed: Ground speed of aircraft (float)
            :param air_speed: Air speed of aircraft (float)

        Returns:
            float: Wind speed magnitude (scalar quantity)
        """
        wind_speed = list(map(sub, air_speed, ground_speed))
        wind_speed = [round(fabs(s), 2) for s in wind_speed]
        return wind_speed

    @staticmethod
    def calculate_average(values_list):
        """Calculate the average of a list

        Args:
            :param values_list: int/float list (list)

        Returns:
            float: average value
        """
        try:
            return round(float(sum(values_list) / len(values_list)), 2)
        except ZeroDivisionError:
            logger.error("Divide by zero error. There were no current values stored in the array "
                         "to calculate the average.")

    @staticmethod
    def calculate_truncation_percentage(input_file, output_file):
        """Calculate file truncation percentage

        Args:
            :param input_file: Absolute path of input file (str)
            :param output_file: Absolute path of output file (str)

        Returns:
            float: Percentage difference in file size between output and input file
        """
        input_file_size = round(float(stat(input_file)[6] / 1048576), 2)
        output_file_size = round(float(stat(output_file)[6] / 1048576), 2)
        diff = input_file_size - output_file_size
        truncation_percent = round(diff / input_file_size * 100.0, 2)
        return truncation_percent

    @staticmethod
    def leap(date):
        """
        NOTE: Method imported from http://stackoverflow.com/a/35772372
        Return the number of leap seconds since 6/Jan/1980

        Args:
            :param date: datetime instance

        Returns:
            int: leap seconds for the date
        """
        if date < datetime(1981, 6, 30, 23, 59, 59):
            return 0
        leap_list = [(1981, 6, 30), (1982, 6, 30), (1983, 6, 30),
                     (1985, 6, 30), (1987, 12, 31), (1989, 12, 31),
                     (1990, 12, 31), (1992, 6, 30), (1993, 6, 30),
                     (1994, 6, 30), (1995, 12, 31), (1997, 6, 30),
                     (1998, 12, 31), (2005, 12, 31), (2008, 12, 31),
                     (2012, 6, 30), (2015, 6, 30)]
        leap_dates = list(map(lambda x: datetime(x[0], x[1], x[2], 23, 59, 59), leap_list))
        for j in range(len(leap_dates[:-1])):
            if leap_dates[j] < date < leap_dates[j + 1]:
                return j + 1
        return len(leap_dates)

    @staticmethod
    def gps2utc(week, secs):
        """
        Convert GPS Time & Week to UTC Time
        NOTE: Method imported from http://stackoverflow.com/a/35772372

        Args:
            :param week: GPS week number, i.e. 1866 (int)
            :param secs: number of seconds since the beginning of `week` (int)

        Returns:
            datetime: UTC Time
        """
        secs_in_week = 604800
        gps_epoch = datetime(1980, 1, 6, 0, 0, 0)
        date_before_leaps = gps_epoch + timedelta(seconds=week * secs_in_week + secs)
        return date_before_leaps - timedelta(seconds=FlightMath.leap(date_before_leaps))

    @staticmethod
    def gps_to_local(week, secs):
        """Convert GPS Time & Week to Local Time

        Args:
            :param secs: number of seconds since the beginning of the week (int)
            :param week: GPS week number, i.e. 1900 (int)

        Returns:
            datetime: Local Time
        """
        from_zone = dateutil.tz.tzutc()
        to_zone = dateutil.tz.tzlocal()
        utc = FlightMath.gps2utc(week, secs)
        utc = utc.replace(tzinfo=from_zone)
        return utc.astimezone(to_zone)

    @staticmethod
    def generate_csv_file(filepath, data):
        """Generate csv file"""
        logger.debug("Generating {} csv file".format(filepath))
        try:
            with open(filepath, 'w') as csv_file:
                for line in data:
                    csv_file.write(line)
                    csv_file.write('\n')
            csv_file.close()
        except IOError:
            logger.critical("Unable to create {} csv file. Please close other applications that may be using this "
                            "file and locking it.".format(filepath))

"""
Copyright (C) 2016 Skylark Drones
Dict class provides flight variable permutations and flight log file definitions which allows DroneLogFormatter app to
be resilient against different log file formats and definitions. It indexes the log file and returns the location of
each flight variable.
"""

import logging

logger = logging.getLogger("DroneLogFormatter")


class Dict(object):

    @staticmethod
    def get_flight_variable_dicts():
        """Returns the flight variable permutations as a dict"""
        return {
            'Rel_Alt': ['RelAlt', 'RAlt'],  # altitude measured above sea level
            'Abs_Alt': ['Alt'],  # absolute ground level altitude
            'Time': ['TimeUS', 'TimeMS'],  # ATTENTION! TimeMS in GPS line refers to GPS Time and not relative time in ms!
            'T': ['T'],  # ATTENTION! T is only used in the GPS line where it represents time in ms!
            'Volt': ['Volt'],
            'Curr': ['Curr'],
            'NSat': ['NSats'],
            'Lat': ['Lat'],
            'Lng': ['Lng'],
            'GSpeed': ['Spd', 'GSpdCM'],
            'ASpeed': ['Arspd'],
            'GPSTime': ['GPSTime', 'TimeMS', 'GMS'],
            'GPSWeek': ['GPSWeek', 'Week', 'GWk'],
            'Mode': ['Mode'],
            'Pitch': ['Pitch'],
            'Roll': ['Roll'],
            'Yaw': ['Yaw'],
            'AccX': ['AccX']
        }

    @staticmethod
    def get_flight_columns():
        """Returns the flight log line definitions"""
        return {
            'GPS': {
                'Time': {'Index': None, 'Value': None},
                'Rel_Alt': {'Index': None, 'Value': None},
                'NSat': {'Index': None, 'Value': None},
                'GPSTime': {'Index': None, 'Value': None},
                'GPSWeek': {'Index': None, 'Value': None},
                'Lat': {'Index': None, 'Value': None},
                'Lng': {'Index': None, 'Value': None},
                'GSpeed': {'Index': None, 'Value': None},
                'T': {'Index': None, 'Value': None},
            },

            'CURR': {
                'Time': {'Index': None, 'Value': None},
                'Volt': {'Index': None, 'Value': None},
                'Curr': {'Index': None, 'Value': None},
            },

            'NTUN': {
                'Time': {'Index': None, 'Value': None},
                'ASpeed': {'Index': None, 'Value': None},
                'GSpeed': {'Index': None, 'Value': None}
            },

            'CAM': {
                'Time': {'Index': None, 'Value': None},
                'GPSTime': {'Index': None, 'Value': None},
                'GPSWeek': {'Index': None, 'Value': None},
                'Lat': {'Index': None, 'Value': None},
                'Lng': {'Index': None, 'Value': None},
                'Rel_Alt': {'Index': None, 'Value': None},
                'Abs_Alt': {'Index': None, 'Value': None},
                'Roll': {'Index': None, 'Value': None},
                'Pitch': {'Index': None, 'Value': None},
                'Yaw': {'Index': None, 'Value': None},
            },

            'MODE': {
                'Time': {'Index': None, 'Value': None},
                'Mode': {'Index': None, 'Value': None},
            },

            'ATT': {
                'Time': {'Index': None, 'Value': None},
                'Pitch': {'Index': None, 'Value': None},
                'Roll': {'Index': None, 'Value': None},
                'Yaw': {'Index': None, 'Value': None},
            },

            'IMU': {
                'Time': {'Index': None, 'Value': None},
                'AccX': {'Index': None, 'Value': None}
            }
        }

    @staticmethod
    def get_column_header(column_key, line_parts, flight_columns, skip_parameter=4):
        """Get the indexes and values of the column headers in a line

        Args:
            :param column_key: Column header key i.e. 'GPS', 'Alt', 'NTUN' (str)
            :param line_parts: Log file line split in parts (should be devoid of spaces and special characters) (str)
            :param flight_columns: Flight columns list to store the indexes found in this function (list)
            :param skip_parameter: Argument to skip columns in a log file (int)
        """
        logger.debug("Grabbing column header indexes & values for {}".format(column_key))
        for column_header in flight_columns[column_key]:
            for column_header_value in Dict.get_flight_variable_dicts()[column_header]:
                try:
                    index = line_parts.index(column_header_value)
                    flight_columns[column_key][column_header]['Index'] = index - skip_parameter
                    flight_columns[column_key][column_header]['Value'] = line_parts[index]
                except ValueError:
                    pass
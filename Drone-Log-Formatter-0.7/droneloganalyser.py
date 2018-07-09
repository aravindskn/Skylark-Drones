"""
Copyright (C) 2016 Skylark Drones
Drone Log Formatter main class.
"""

from os import path, sep, remove
import logging
import simplekml
import flightmath
import geotagger
import flightcolumndict as FCD

logger = logging.getLogger("DroneLogFormatter")
logger.setLevel(logging.INFO)
logging.basicConfig(format='[%(levelname)s]: %(message)s')


class DroneLogImporter(object):
    # CONFIGURATION VARIABLES

    # Default input and output file paths
    LOG_NO = '129'

    # TODO Remove hardcoded 'Documents' folder to make it OS independent
    # Base file path (OS Independent) (e.g. on Windows C:\\user-name\\Documents\\229\\)
    #BASE_PATH = path.expanduser('~') + sep + "Documents" + sep + LOG_NO + sep
    BASE_PATH = path.expanduser('~') + sep + "Documents" + sep + LOG_NO + sep
    INPUT_FILE_NAME = "{}{}.log".format(BASE_PATH, LOG_NO)
    OUTPUT_FILE_NAME = "{}{}-FORMAT.log".format(BASE_PATH, LOG_NO)
    OUTPUT_CAM_CSV_FILE_NAME = "{}{}-CAM.csv".format(BASE_PATH, LOG_NO)

    OUTPUT_CAM_KML_FILE_NAME = "{}{}-CAM.kml".format(BASE_PATH, LOG_NO)
    RAW_IMAGES_FOLDER = "{}Raw_Images{}".format(BASE_PATH, sep)
    GEOTAGGED_IMAGES_FOLDER = "{}Geotagged_Images_Test{}".format(BASE_PATH, sep)

    # Flag to toggle on/off functionalities
    GEOTAG_IMAGES = True
    GENERATE_KML = True
    GENERATE_CAM_LOG = True
    GENERATE_MODE_SWITCH_LOGS = True

    # Flight parameters - CAREFUL! Affects the data extraction process!
    FLIGHT_START = FLIGHT_END = False
    ABORT_TRUNCATION_THRESHOLD = 40.0  # Threshold percent above which the flight data extraction is malfunctioning
    GEOTAG_TOLERANCE = 1.0  # Geotagging time-offset tolerance in seconds
    FLIGHT_COLUMN_DICTS = FCD.Dict().get_flight_variable_dicts()
    FLIGHT_COLUMNS = FCD.Dict().get_flight_columns()

    def __init__(self):
        # Instantiate FlightMath Class (Library)
        self.FM = flightmath.FlightMath()

        # Instantiate Geotagger Class (Library
        self.GT = geotagger.Geotagger()

        self.version = "v0.7"
        self.applicationName = "Dronecubator Mission Control"

        # Output data variables
        self.home_lat = self.home_lng = None
        self.local_start_time = self.local_end_time = None
        self.start_voltage = self.end_voltage = None
        self.previous_mode = self.current_mode = None

        self.avg_current = None
        self.max_current = 0.0
        self.current = []

        self.accX = []
        self.max_accX = self.min_accX = None

        self.altitude = []

        self.endurance = None

        self.ground_speed = []
        self.air_speed = []
        self.wind_speed = []
        self.max_wind_speed = 0.0

        self.cam_log = []
        self.kml_log = []
        self.full_log = []
        self.mode_split_log = []

        self.log_file_path = None

    def analyse(self):
        # Request user for log file. If not provided or invalid, use default
        self.log_file_path = self.get_file()
        logger.debug("Input .log file path: {}".format(self.log_file_path))

        # Verify validity of input file
        if path.isfile(self.log_file_path):
            self.grab_flight_column_indexes(self.log_file_path)
            self.dry_run(self.log_file_path)
            self.process_file(self.log_file_path)
            self.generate_log_file()
            self.flight_data_valid = self.verify_log_validity(self.log_file_path, self.OUTPUT_FILE_NAME)

            if self.flight_data_valid is True:
                self.set_flight_results()
                self.print_to_console_flight_data()

                if self.GEOTAG_IMAGES or self.GENERATE_CAM_LOG:
                    self.FM.generate_csv_file(self.OUTPUT_CAM_CSV_FILE_NAME, self.cam_log)

                if self.GENERATE_KML:
                    self.generate_kml_file()

                if self.GENERATE_MODE_SWITCH_LOGS:
                    self.generate_mode_switch_data()

                if self.GEOTAG_IMAGES:
                    self.GT.geotag_images(self.OUTPUT_CAM_CSV_FILE_NAME, self.RAW_IMAGES_FOLDER,
                                          self.GEOTAGGED_IMAGES_FOLDER, self.GEOTAG_TOLERANCE,
                                          self.local_start_time, self.local_end_time)
        else:
            logger.critical("Input .log file path not found! ABORTING!")

    def generate_mode_switch_data(self):
        index = 1
        for element in self.mode_split_log:
            element['Altitude'].insert(0, 'Altitude')
            element['Alt_TimeMS'].insert(0, 'Time')
            element['Current'].insert(0, 'Current')
            element['Curr_TimeMS'].insert(0, 'Time')
            element['Airspeed'].insert(0, 'Airspeed')
            element['Arsp_TimeMS'].insert(0, 'Time')
            element['Pitch'].insert(0, 'Pitch')
            element['Pitch_TimeMS'].insert(0, 'Time')
            data = [', '.join(str(e) for e in element['Altitude']), ', '.join(str(e) for e in element['Alt_TimeMS']),
                    ', '.join(str(f) for f in element['Current']), ', '.join(str(e) for e in element['Curr_TimeMS']),
                    ', '.join(str(g) for g in element['Airspeed']), ', '.join(str(e) for e in element['Arsp_TimeMS']),
                    ', '.join(str(h) for h in element['Pitch']), ', '.join(str(e) for e in element['Pitch_TimeMS'])]
            filepath = "{}{}-{}-{}.csv".format(self.BASE_PATH, index, element['PREVIOUS_MODE'], element['CURRENT_MODE'])
            self.FM.generate_csv_file(filepath, data)
            index += 1

    def get_file(self):
        """Grab input log file from the user"""
        # For debugging purposes just use the default log file. In production mode, prompt user for
        # input log file.
        if logger.getEffectiveLevel() > logging.DEBUG:
            file_path = input("Enter file path [leave empty to use default]: ")
        else:
            file_path = None

        if file_path and not file_path.isspace():
            logger.debug("Using user entered input log file.")
            return file_path
        else:
            logger.debug("User entered input log file invalid. Defaulting to set log file.")
            return self.INPUT_FILE_NAME

    def process_file(self, input_log_file_path):
        """Process given file line by line"""
        logger.debug("Reading log file {}".format(input_log_file_path))
        log_file = open(input_log_file_path, 'r')

        for line in log_file:
            self.process_line(line)

        log_file.close()

    def grab_flight_column_indexes(self, input_log_file_path):
        """Process log file and grab flight column indexes from FMT definitions"""
        logger.debug("Processing log file {} and grabbing flight column indexes from FMT definitions".format(input_log_file_path))
        log_file = open(input_log_file_path, 'r')

        for line in log_file:
            line = line.rstrip()
            line_parts = line.split(',')
            line_parts = [s.strip() for s in line_parts]

            category = line_parts[0]

            if category == 'FMT':
                subcategory = line_parts[3]
                if subcategory == 'GPS' or subcategory == 'CURR' or subcategory == 'NTUN' or subcategory == 'MODE' \
                        or subcategory == 'ATT' or subcategory == 'IMU':
                    FCD.Dict().get_column_header(subcategory, line_parts, self.FLIGHT_COLUMNS)

                if subcategory == 'CAM':
                    FCD.Dict().get_column_header(subcategory, line_parts, self.FLIGHT_COLUMNS)
                    cam_file_header = ''
                    for column_header in self.FLIGHT_COLUMNS[subcategory]:
                        if self.FLIGHT_COLUMNS[subcategory][column_header]['Value'] is not None:
                            cam_file_header += self.FLIGHT_COLUMNS[subcategory][column_header]['Value'] + ', '
                    cam_file_header += 'LocalTime'
                    cam_file_header = cam_file_header.rstrip(' ')[:-1]
                    self.cam_log.append(cam_file_header)

            if category == 'PARM':
                break

        logger.debug("Grabbed all flight column indexes")

    def dry_run(self, input_log_file_path):
        """Process log file and capture global log data which are later used"""
        logger.debug(("Perform a dry run of log file {}".format(input_log_file_path)))
        log_file = open(input_log_file_path, 'r')

        for line in log_file:
            line = line.rstrip()
            line_parts = line.split(',')
            line_parts = [s.strip() for s in line_parts]

            category = line_parts[0]

            if category == 'FMT':
                pass

            elif category == 'PARM':
                pass

            else:
                if category == 'IMU':
                    self.accX.append(float(line_parts[self.FLIGHT_COLUMNS[category]['AccX']['Index']]))

        self.max_accX = max(self.accX)
        self.min_accX = min(self.accX)

        log_file.close()

    def process_line(self, line):
        """Process line and extract useful flight data"""
        line = line.rstrip()  # Remove trailing character '\n' from the line
        line_parts = line.split(',')
        line_parts = [s.strip() for s in line_parts]

        # Grab category (FMT, PARAMS, DATA) from the passed line
        category = line_parts[0]

        if category == 'FMT':
            self.full_log.append(line)

        elif category == 'PARM':
            self.full_log.append(line)

        else:
            if category == 'IMU':
                acc_x = float(line_parts[self.FLIGHT_COLUMNS[category]['AccX']['Index']])

                if not self.FLIGHT_START and acc_x == self.max_accX:
                    self.FLIGHT_START = True

                if self.FLIGHT_START and not self.FLIGHT_END and acc_x == self.min_accX:
                    self.FLIGHT_END = True

            if category == 'GPS':
                flight_alt = float(line_parts[self.FLIGHT_COLUMNS[category]['Rel_Alt']['Index']])
                nsats = int(line_parts[self.FLIGHT_COLUMNS[category]['NSat']['Index']])

                # Record END_TIME always as logs could end abruptly even before achieving minimum flight alt conditions
                # there by resulting in the END_TIME not set.
                self.local_end_time = self.FM.gps_to_local(
                    int(line_parts[self.FLIGHT_COLUMNS[category]['GPSWeek']['Index']]),
                    int(line_parts[self.FLIGHT_COLUMNS[category]['GPSTime']['Index']])/1000
                )

                # Record home lat and lng
                if self.home_lat is None and self.home_lng is None and flight_alt == 0.0 and nsats >= 6:
                    self.home_lat = float(line_parts[self.FLIGHT_COLUMNS[category]['Lat']['Index']])
                    self.home_lng = float(line_parts[self.FLIGHT_COLUMNS[category]['Lng']['Index']])
                    logger.info("Home location coordinates: {},{}".format(self.home_lat, self.home_lng))

                # Record flight start time
                if self.FLIGHT_START and self.local_start_time is None:
                    self.local_start_time = self.FM.gps_to_local(
                        int(line_parts[self.FLIGHT_COLUMNS[category]['GPSWeek']['Index']]),
                        int(line_parts[self.FLIGHT_COLUMNS[category]['GPSTime']['Index']]) / 1000
                    )

                # Record flight end time and exit
                if self.FLIGHT_END:
                    self.local_end_time = self.FM.gps_to_local(
                        int(line_parts[self.FLIGHT_COLUMNS[category]['GPSWeek']['Index']]),
                        int(line_parts[self.FLIGHT_COLUMNS[category]['GPSTime']['Index']]) / 1000
                    )

            if category == 'CURR':
                current = float(line_parts[self.FLIGHT_COLUMNS[category]['Curr']['Index']]) / 100.0
                if self.start_voltage is None:
                    # Record begin voltage measured during pre-flight check
                    if current <= 5:
                        self.start_voltage = float(line_parts[self.FLIGHT_COLUMNS[category]['Volt']['Index']]) / 100.0

                if self.FLIGHT_END:
                    # Record end voltage after flight has landed and current usage is minimum
                    if current <= 5:
                        self.end_voltage = float(line_parts[self.FLIGHT_COLUMNS[category]['Volt']['Index']]) / 100.0
                    return

            # Record data only AFTER flight start and BEFORE flight end
            if self.FLIGHT_START and not self.FLIGHT_END:
                self.full_log.append(line)

                if category == 'MODE':
                    # Record Mode (Manual, Auto, FBWA, Stabilize etc.)
                    self.previous_mode = self.current_mode
                    self.current_mode = line_parts[self.FLIGHT_COLUMNS[category]['Mode']['Index']]
                    self.mode_split_log.append({'PREVIOUS_MODE': self.previous_mode,
                                                'CURRENT_MODE': self.current_mode,
                                                'Altitude': [],
                                                'Alt_TimeMS': [],
                                                'Current': [],
                                                'Curr_TimeMS': [],
                                                'Airspeed': [],
                                                'Arsp_TimeMS': [],
                                                'Pitch': [],
                                                'Pitch_TimeMS': []})

                if category == 'CAM':
                    cam_file_line = ''
                    for column_header in self.FLIGHT_COLUMNS[category]:
                        if self.FLIGHT_COLUMNS[category][column_header]['Value'] is not None:
                            cam_file_line += line_parts[self.FLIGHT_COLUMNS[category][column_header]['Index']] + ', '

                    cam_file_line += self.FM.gps_to_local(
                        int(line_parts[self.FLIGHT_COLUMNS[category]['GPSWeek']['Index']]),
                        int(line_parts[self.FLIGHT_COLUMNS[category]['GPSTime']['Index']]) / 1000
                    ).strftime("%H:%M:%S")

                    lat_cord = float(line_parts[self.FLIGHT_COLUMNS[category]['Lat']['Index']])
                    lng_cord = float(line_parts[self.FLIGHT_COLUMNS[category]['Lng']['Index']])
                    cam_file_line = cam_file_line.rstrip(' ')[:-1]
                    self.cam_log.append(cam_file_line)
                    self.kml_log.append([lng_cord, lat_cord])

                if category == 'ATT':
                    # Record Pitch
                    pitch = float(line_parts[self.FLIGHT_COLUMNS[category]['Pitch']['Index']])
                    time = int(line_parts[self.FLIGHT_COLUMNS[category]['Time']['Index']])
                    if not len(self.mode_split_log) == 0:
                        self.mode_split_log[len(self.mode_split_log) - 1]['Pitch'].append(pitch)
                        self.mode_split_log[len(self.mode_split_log) - 1]['Pitch_TimeMS'].append(time)

                if category == 'GPS':
                    # Record altitude
                    flight_alt = float(line_parts[self.FLIGHT_COLUMNS[category]['Rel_Alt']['Index']])
                    if self.FLIGHT_COLUMNS[category]['T']['Index'] is not None:
                        time = int(line_parts[self.FLIGHT_COLUMNS[category]['T']['Index']])
                    self.altitude.append(flight_alt)
                    if not len(self.mode_split_log) == 0:
                        self.mode_split_log[len(self.mode_split_log) - 1]['Altitude'].append(flight_alt)
                        if self.FLIGHT_COLUMNS[category]['T']['Index'] is not None:
                            self.mode_split_log[len(self.mode_split_log) - 1]['Alt_TimeMS'].append(time)

                if category == 'NTUN':
                    # Record air speed
                    air_speed = float(line_parts[self.FLIGHT_COLUMNS[category]['ASpeed']['Index']])

                    # Record ground velocity
                    self.ground_speed.append(float(line_parts[self.FLIGHT_COLUMNS[category]['GSpeed']['Index']]) / 100.0)

                    time = int(line_parts[self.FLIGHT_COLUMNS[category]['Time']['Index']])
                    self.air_speed.append(air_speed)
                    if not len(self.mode_split_log) == 0:
                        self.mode_split_log[len(self.mode_split_log) - 1]['Airspeed'].append(air_speed)
                        self.mode_split_log[len(self.mode_split_log) - 1]['Arsp_TimeMS'].append(time)

                if category == 'CURR':
                    # Record end voltage during flight as well to ensure that end voltage is still recorded in case
                    # pixhawk stops logging data in the middle of a flight due to crash.
                    self.end_voltage = float(line_parts[self.FLIGHT_COLUMNS[category]['Volt']['Index']]) / 100.0

                    # Record current and max current
                    current = float(line_parts[self.FLIGHT_COLUMNS[category]['Curr']['Index']]) / 100.0
                    time = int(line_parts[self.FLIGHT_COLUMNS[category]['Time']['Index']])
                    self.current.append(current)
                    if current > self.max_current:
                        self.max_current = current

                    if not len(self.mode_split_log) == 0:
                        self.mode_split_log[len(self.mode_split_log) - 1]['Current'].append(current)
                        self.mode_split_log[len(self.mode_split_log) - 1]['Curr_TimeMS'].append(time)

    def verify_log_validity(self, input_file, output_file):
        """Validate Log File"""
        logger.debug("Verifying validity of log file by analyzing flight data truncation")

        truncation_percent = self.FM.calculate_truncation_percentage(input_file, output_file)

        if truncation_percent <= self.ABORT_TRUNCATION_THRESHOLD:
            logger.debug("{}% invalid flight data has been truncated.".format(truncation_percent))
            return True
        else:
            logger.error("{}% invalid flight data has been truncated!".format(truncation_percent))
            logger.error("Flight data truncation is too high to calculate useful flight data such as endurance, "
                         "avg. wind speed etc. Check log file for discrepancies. ABORTING!")
            logger.error("Removing output files...")
            remove(self.OUTPUT_FILE_NAME)
            return False

    def set_flight_results(self):
        try:
            logger.debug("Saving endurance value")
            total_ms = int((self.local_end_time - self.local_start_time).total_seconds() * 1000)
            self.endurance = self.FM.convert_ms_to_duration(total_ms)
        except TypeError:
            logger.error("Flight start or end time is invalid! Unable to calculate endurance")
            logger.error("Flight Start Time: {}, Flight End Time: {}".format(self.local_start_time,
                                                                             self.local_end_time))
            if not self.FLIGHT_START:
                logger.error("Flight did not go above minimum base flight altitude resulting in "
                             "invalid flight start time!")
        self.avg_current = self.FM.calculate_average(self.current)
        self.wind_speed = self.FM.calculate_wind_speed(self.ground_speed, self.air_speed)
        self.max_wind_speed = max(self.wind_speed)

    def generate_log_file(self):
        """Generate formatted log file"""
        logger.debug("Generating log file")
        out_log_file = open(self.OUTPUT_FILE_NAME, 'w')
        for line in self.full_log:
            out_log_file.write(line)
            out_log_file.write('\n')
        out_log_file.close()

    def generate_kml_file(self):
        """Generate CAM kml file for Google Earth"""
        logger.debug("Generating CAM kml file")
        kml = simplekml.Kml()
        index = 1
        for lng_cord, lat_cord in self.kml_log:
            kml.newpoint(name="CAM #{}".format(index), coords=[(lng_cord, lat_cord)])
            index += 1
        kml.save(self.OUTPUT_CAM_KML_FILE_NAME)

    def print_to_console_flight_data(self):
        """Print essential flight data to the console"""
        logger.info("Begin voltage: {}v (Pixhawk error could be around 0.2v-0.3v!)".format(self.start_voltage))
        logger.info("End voltage: {}v (Pixhawk error could be around 0.2v-0.3v!)".format(self.end_voltage))
        logger.info("Flight Start Time: {}".format(self.local_start_time.strftime("%b %d, %Y at %I:%M:%S %p")))
        logger.info("Flight End Time: {}".format(self.local_end_time.strftime("%b %d, %Y at %I:%M:%S %p")))
        logger.info(self.get_duration_string(self.endurance))
        logger.info("Max. current: {}A".format(self.max_current))
        logger.info("Avg. current: {}A".format(self.avg_current))
        logger.info("Ground speed: {}".format(self.ground_speed))
        logger.info("Max. ground speed: {}m/s".format(max(self.ground_speed)))
        logger.info("Air speed: {}".format(self.air_speed))
        logger.info("Max. air speed: {}m/s".format(max(self.air_speed)))
        logger.info("Wind speed: {}".format(self.wind_speed))
        logger.info("Max. wind speed: {}m/s".format(self.max_wind_speed))
        logger.info("Altitude: {}".format(self.altitude))

    @staticmethod
    def get_duration_string(endurance):
        if endurance['hours'] > 0:
            return("Endurance: {} hrs, {} mins, {} secs".format(endurance['hours'],
                                                                endurance['minutes'],
                                                                endurance['seconds']))
        else:
            return "Endurance: {} mins, {} secs".format(endurance['minutes'], endurance['seconds'])

    @staticmethod
    def calculate_percent(value, total):
        return (value / total) * 100

if __name__ == '__main__':
    DLF = DroneLogImporter()
    DLF.analyse()

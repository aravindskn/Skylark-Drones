from PyQt5.QtCore import pyqtProperty, pyqtSignal, QObject, pyqtSlot
from os import listdir
from fnmatch import filter
import droneloganalyser as DroneLogAnalyser
import flightmath as FlightMath
import geotagger as Geotagger


class MockDroneLogAnalyser(QObject):

    progressUpdated = pyqtSignal(int, arguments=['progress'])
    invalidLog = pyqtSignal()

    def __init__(self):
        super(MockDroneLogAnalyser, self).__init__()
        self.DLA = DroneLogAnalyser.DroneLogImporter()
        self.FM = FlightMath.FlightMath()
        self.GT = Geotagger.Geotagger()

        # Application Details
        self._version = self.DLA.version
        self._applicationName = self.DLA.applicationName

        # File Paths
        self._input_file_name = None
        self._raw_images_folder = None
        self._output_folder_name = None

        # Progress Indicators
        self.no_of_images = 0
        self.image_weight = 1
        self.weight = {'GrabFlightColumn': 1, 'DryRun': 2, 'ProcessLog': 5, 'GenerateLog': 3, 'SetFlightResult': 1,
                       'GenerateCAM': 2, 'GenerateKML': 2, 'GenerateMode': 3, 'GeotagImage': self.no_of_images * self.image_weight}
        self.total_tasks = self.weight['GrabFlightColumn'] + self.weight['DryRun'] + self.weight['ProcessLog'] + \
                               self.weight['SetFlightResult'] + self.weight['GenerateLog']
        self.tasks_done = 0

        # Flight Output
        self._local_start_time = self._local_end_time = None
        self._start_voltage = self._end_voltage = None
        self._max_current = self._avg_current = None
        self._home_lat = self._home_lng = None
        self._max_wind_speed = None
        self._endurance = None

        # Output Parameters
        self._geotag_images = self.DLA.GEOTAG_IMAGES
        self._generate_kml = self.DLA.GENERATE_KML
        self._generate_cam_log = self.DLA.GENERATE_CAM_LOG
        self._generate_mode_switch_log = self.DLA.GENERATE_MODE_SWITCH_LOGS

    @pyqtProperty('QString')
    def version(self):
        return self._version

    @pyqtProperty('QString')
    def applicationName(self):
        return self._applicationName

    @pyqtProperty('QString')
    def inputFilePath(self):
        return self._input_file_name

    @inputFilePath.setter
    def inputFilePath(self, value):
        self._input_file_name = value
        self.DLA.INPUT_FILE_NAME = self._input_file_name
        self.DLA.log_file_path = self._input_file_name

    @pyqtProperty('QString')
    def rawImagesFolder(self):
        return self._raw_images_folder

    @rawImagesFolder.setter
    def rawImagesFolder(self, value):
        self._raw_images_folder = value
        self.DLA.RAW_IMAGES_FOLDER = self._raw_images_folder

    @pyqtProperty('QString')
    def outputFolderPath(self):
        return self._output_folder_name

    @outputFolderPath.setter
    def outputFolderPath(self, value):
        self._output_folder_name = value
        self.DLA.BASE_PATH = self._output_folder_name

    @pyqtProperty('QString')
    def startFlightTime(self):
        return self._local_start_time

    @pyqtProperty('QString')
    def endFlightTime(self):
        return self._local_end_time

    @pyqtProperty('QString')
    def beginVoltage(self):
        return self._start_voltage

    @pyqtProperty('QString')
    def endVoltage(self):
        return self._end_voltage

    @pyqtProperty('QString')
    def maxCurrent(self):
        return self._max_current

    @pyqtProperty('QString')
    def avgCurrent(self):
        return self._avg_current

    @pyqtProperty('QString')
    def homeLat(self):
        return self._home_lat

    @pyqtProperty('QString')
    def homeLng(self):
        return self._home_lng

    @pyqtProperty('QString')
    def endurance(self):
        return self._endurance

    @pyqtProperty('QString')
    def maxWindSpeed(self):
        return self._max_wind_speed

    @pyqtProperty(bool)
    def generateKml(self):
        return self._generate_kml

    @generateKml.setter
    def generateKml(self, value):
        self._generate_kml = value
        self.DLA.GENERATE_KML = self._generate_kml

    @pyqtProperty(bool)
    def geotagImage(self):
        return self._geotag_images

    @geotagImage.setter
    def geotagImage(self, value):
        self._geotag_images = value
        self.DLA.GEOTAG_IMAGES = self._geotag_images

    @pyqtProperty(bool)
    def generateCamLog(self):
        return self._generate_cam_log

    @generateCamLog.setter
    def generateCamLog(self, value):
        self._generate_cam_log = value
        self.DLA.GENERATE_CAM_LOG = self._generate_cam_log

    @pyqtProperty(bool)
    def generateModeLog(self):
        return self._generate_mode_switch_log

    @generateModeLog.setter
    def generateModeLog(self, value):
        self._generate_mode_switch_log = value
        self.DLA.GENERATE_MODE_SWITCH_LOGS = self._generate_mode_switch_log

    @pyqtSlot()
    def process_log(self):
        if self._generate_cam_log:
            self.total_tasks += self.weight['GenerateCAM']

        if self._generate_kml:
            self.total_tasks += self.weight['GenerateKML']

        if self._geotag_images:
            self.no_of_images = len(filter(listdir(self._raw_images_folder), '*.jpg'))
            self.weight['GeotagImage'] = self.no_of_images * self.image_weight
            self.total_tasks += self.weight['GeotagImage']

        if self._generate_mode_switch_log:
            self.total_tasks += self.weight['GenerateMode']

        self.DLA.grab_flight_column_indexes(self._input_file_name)
        self.tasks_done += self.weight['GrabFlightColumn']
        self.progressUpdated.emit(self.DLA.calculate_percent(self.tasks_done, self.total_tasks))

        self.DLA.dry_run(self._input_file_name)
        self.tasks_done += self.weight['DryRun']
        self.progressUpdated.emit(self.DLA.calculate_percent(self.tasks_done, self.total_tasks))

        self.DLA.process_file(self._input_file_name)
        self.tasks_done += self.weight['ProcessLog']
        self.progressUpdated.emit(self.DLA.calculate_percent(self.tasks_done, self.total_tasks))

        self.DLA.OUTPUT_FILE_NAME = "{}FORMATTED_LOG.log".format(self._output_folder_name)
        self.DLA.generate_log_file()
        self.tasks_done += self.weight['GenerateLog']
        self.progressUpdated.emit(self.DLA.calculate_percent(self.tasks_done, self.total_tasks))

        self.flight_data_valid = self.DLA.verify_log_validity(self._input_file_name, self.DLA.OUTPUT_FILE_NAME)

        if not self.flight_data_valid:
            self.invalidLog.emit()
            return False

        self.DLA.set_flight_results()
        self.tasks_done += self.weight['SetFlightResult']
        self.progressUpdated.emit(self.DLA.calculate_percent(self.tasks_done, self.total_tasks))

        self._local_start_time = self.DLA.local_start_time.strftime("%b %d, %Y at %I:%M:%S %p")
        self._local_end_time = self.DLA.local_end_time.strftime("%b %d, %Y at %I:%M:%S %p")
        self._home_lat = self.DLA.home_lat
        self._home_lng = self.DLA.home_lng
        self._max_wind_speed = self.DLA.max_wind_speed
        self._avg_current = self.DLA.avg_current
        self._max_current = self.DLA.max_current
        self._start_voltage = self.DLA.start_voltage
        self._end_voltage = self.DLA.end_voltage
        self._endurance = self.DLA.get_duration_string(self.DLA.endurance)

        if self._generate_cam_log:
            self.DLA.OUTPUT_CAM_CSV_FILE_NAME = "{}CAM_CSV.csv".format(self._output_folder_name)
            self.FM.generate_csv_file(self.DLA.OUTPUT_CAM_CSV_FILE_NAME, self.DLA.cam_log)
            self.tasks_done += self.weight['GenerateCAM']
            self.progressUpdated.emit(self.DLA.calculate_percent(self.tasks_done, self.total_tasks))

        if self._generate_kml:
            self.DLA.OUTPUT_CAM_KML_FILE_NAME = "{}CAM_KML.kml".format(self._output_folder_name)
            self.DLA.generate_kml_file()
            self.tasks_done += self.weight['GenerateKML']
            self.progressUpdated.emit(self.DLA.calculate_percent(self.tasks_done, self.total_tasks))

        if self._generate_mode_switch_log:
            self.DLA.generate_mode_switch_data()
            self.tasks_done += self.weight['GenerateMode']
            self.progressUpdated.emit(self.DLA.calculate_percent(self.tasks_done, self.total_tasks))

        return True

    def gui_geotag_images(self):
        self.GT.create_geotag_folder(self.DLA.GEOTAGGED_IMAGES_FOLDER)
        self.GT.get_cam_msgs(self.DLA.OUTPUT_CAM_CSV_FILE_NAME)
        filtered_images = self.GT.filter_images(self._raw_images_folder, self.DLA.local_start_time.replace(tzinfo=None), self.DLA.local_end_time.replace(tzinfo=None))
        same_image_cam_count = self.GT.check_one_to_one_count(self.DLA.OUTPUT_CAM_CSV_FILE_NAME, filtered_images)
        if same_image_cam_count:
            self.GT.cam_msg_geotag(self._raw_images_folder, self.DLA.GEOTAGGED_IMAGES_FOLDER, filtered_images, self.update_geotag_progress)
        else:
            self.GT.time_offset_geotag(self._raw_images_folder, self.DLA.GEOTAGGED_IMAGES_FOLDER, self.DLA.GEOTAG_TOLERANCE, filtered_images, self.update_geotag_progress)

    def update_geotag_progress(self):
        self.tasks_done += self.image_weight
        self.progressUpdated.emit(self.DLA.calculate_percent(self.tasks_done, self.total_tasks))
from PyQt5.QtWidgets import (QHBoxLayout, QPushButton, QWidget, QLabel, QLineEdit, QGridLayout, QSpacerItem,
                             QSizePolicy, QCheckBox, QFileDialog, QProgressBar, QTextEdit, QMessageBox)
from PyQt5.QtCore import QDir
from os.path import expanduser, dirname, sep, isfile


class AnalysePage(QWidget):
    def __init__(self, MDLA, stack, statusBar):
        super().__init__()

        self.minHeight = 30

        MDLA.invalidLog.connect(lambda: self.showTruncationErrorDialog(MDLA))

        self.logFileHeader = QLabel("Log File Path")
        self.logFileField = QLineEdit(self)
        self.logFileField.setMinimumHeight(self.minHeight)
        self.logFileField.textChanged.connect(lambda: self.verifyInputFile(self.logFileField.text()))
        self.browseLogButton = self.create_button("Browse Log", tool_tip="Browse for Pixhawk log files", min_height=self.minHeight)
        self.browseLogButton.clicked.connect(lambda: self.get_log_file(MDLA, statusBar))

        self.rawImagesHeader = QLabel("Raw Images Folder")
        self.rawImagesField = QLineEdit(self)
        self.rawImagesField.setMinimumHeight(self.minHeight)
        self.browseImagesButton = self.create_button("Browse Raw Images", tool_tip="Browse for the folder containing the raw images", min_height=self.minHeight)
        self.browseImagesButton.clicked.connect(lambda: self.get_raw_images_folder(MDLA, statusBar))

        self.kmlCheckbox = QCheckBox("Generate KML")
        self.kmlCheckbox.setMinimumHeight(self.minHeight)
        self.kmlCheckbox.setChecked(MDLA.generateKml)
        self.kmlCheckbox.stateChanged.connect(lambda: self.updateKmlBackendToggle(MDLA))
        self.kmlCheckbox.setToolTip("Generate a Google Earth compatible KML file containing all CAM points")

        self.camCheckbox = QCheckBox("Generate CAM Log")
        self.camCheckbox.setMinimumHeight(self.minHeight)
        self.camCheckbox.setChecked(MDLA.generateCamLog)
        self.camCheckbox.stateChanged.connect(lambda: self.updateCamBackendToggle(MDLA))

        self.modeCheckbox = QCheckBox("Generate Mode Switch Log")
        self.modeCheckbox.setMinimumHeight(self.minHeight)
        self.modeCheckbox.setChecked(MDLA.generateModeLog)
        self.modeCheckbox.stateChanged.connect(lambda: self.updateModeBackendToggle(MDLA))

        self.geotagCheckbox = QCheckBox("Geotag Images")
        self.geotagCheckbox.setMinimumHeight(self.minHeight)
        self.geotagCheckbox.setChecked(MDLA.geotagImage)
        self.geotagCheckbox.stateChanged.connect(lambda: self.updateGeotagBackendToggle(MDLA))

        self.analyseProgressBar = QProgressBar()
        self.analyseProgressBar.setTextVisible(False)
        self.analyseProgressBar.setMinimumWidth(self.width() + 56)
        MDLA.progressUpdated.connect(self.show_progress)

        self.grid = QGridLayout()
        self.grid.setHorizontalSpacing(5)
        self.grid.setVerticalSpacing(5)
        self.grid.setContentsMargins(40, 40, 40, 40)

        self.grid.addWidget(self.logFileHeader, 0, 0)
        self.grid.addWidget(self.logFileField, 1, 0, 1, 2)
        self.grid.addWidget(self.browseLogButton, 1, 2, 1, 1)

        # Add vertical gap between first and second form entry
        self.logEntrySpacer = QSpacerItem(0, 20, QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.grid.addItem(self.logEntrySpacer, 2, 0)

        self.grid.addWidget(self.rawImagesHeader, 3, 0)
        self.grid.addWidget(self.rawImagesField, 4, 0, 1, 2)
        self.grid.addWidget(self.browseImagesButton, 4, 2, 1, 1)

        self.rawImagesSpacer = QSpacerItem(0, 20, QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.grid.addItem(self.rawImagesSpacer, 5, 0)

        self.grid.addWidget(self.kmlCheckbox, 6, 0)
        self.grid.addWidget(self.camCheckbox, 6, 1)
        self.grid.addWidget(self.modeCheckbox, 6, 2)
        self.grid.addWidget(self.geotagCheckbox, 7,0)

        self.optionsSpacer = QSpacerItem(0, 20, QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.grid.addItem(self.optionsSpacer, 8, 0)

        self.flightOutput = QTextEdit()
        self.flightOutput.setReadOnly(True)
        self.flightOutput.setVisible(False)
        self.grid.addWidget(self.flightOutput, 9, 0, 5, 3)

        self.flightOutputSpacer = QSpacerItem(0, 20, QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.grid.addItem(self.flightOutputSpacer, 15, 0)

        self.bottomSpacer = QSpacerItem(0, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.grid.addItem(self.bottomSpacer, 16, 0)

        self.mainButtonsHBox = QHBoxLayout()
        self.mainButtonsHBox.setSpacing(10)

        self.proceedButton = self.create_button("Process", tool_tip="Analyse log", min_height=self.minHeight)
        self.proceedButton.setEnabled(False)
        self.proceedButton.clicked.connect(lambda: self.process_log(statusBar, MDLA))

        self.backButton = self.create_button("Back", tool_tip="Go back to main page", min_height=self.minHeight)
        self.backButton.clicked.connect(lambda: self.go_home(stack))

        self.clearButton = self.create_button("Clear", tool_tip="Reset page to default state", min_height=self.minHeight)
        self.clearButton.setVisible(False)
        self.clearButton.clicked.connect(lambda: self.reset_page(statusBar))

        self.mainButtonsHBox.addWidget(self.proceedButton)
        self.mainButtonsHBox.addWidget(self.backButton)
        self.mainButtonsHBox.addWidget(self.clearButton)

        self.grid.addItem(self.mainButtonsHBox, 17, 0, 1, 3)

        self.setLayout(self.grid)

    @staticmethod
    def go_home(stack):
        stack.setCurrentIndex(0)

    @staticmethod
    def create_button(name, tool_tip=None, status_tip=None, min_height=None):
        button = QPushButton(name)
        button.setToolTip(tool_tip)
        button.setStatusTip(status_tip)
        button.setMinimumHeight(min_height)
        return button

    def verifyInputFile(self, file_path):
        if isfile(file_path):
            self.proceedButton.setEnabled(True)
        else:
            self.proceedButton.setEnabled(False)

    def updateModeBackendToggle(self, MDLA):
        MDLA.generateModeLog = self.modeCheckbox.isChecked()

    def updateCamBackendToggle(self, MDLA):
        MDLA.generateCamLog = self.camCheckbox.isChecked()

    def updateKmlBackendToggle(self, MDLA):
        MDLA.generateKml = self.kmlCheckbox.isChecked()
        if self.kmlCheckbox.isChecked() and not self.camCheckbox.isChecked():
            self.camCheckbox.setChecked(True)

    def updateGeotagBackendToggle(self, MDLA):
        MDLA.geotagImage = self.geotagCheckbox.isChecked()
        if self.geotagCheckbox.isChecked() and not self.camCheckbox.isChecked():
            self.camCheckbox.setChecked(True)

    def get_log_file(self, MDLA, statusBar):
        file_name = QFileDialog.getOpenFileName(
            self,
            'Select log file',
            expanduser("~") + "/Documents",  # TODO Remove the hardcoded path separator
            "Log files (*.log)"
        )

        if file_name[0]:
            self.logFileField.setText(QDir.toNativeSeparators(file_name[0]))
            MDLA.inputFilePath = QDir.toNativeSeparators(file_name[0])
            MDLA.outputFolderPath = QDir.toNativeSeparators(dirname(MDLA.inputFilePath)) + sep
            statusBar.showMessage("Input log file path set", 2000)

    def get_raw_images_folder(self, MDLA, statusBar):
        # TODO Remove the hardcoded path separator
        log_folder = MDLA.outputFolderPath if MDLA.outputFolderPath else expanduser("~") + "/Documents"

        folder_name = QFileDialog.getExistingDirectory(self, 'Select raw images folder', log_folder,)

        if folder_name:
            self.rawImagesField.setText(QDir.toNativeSeparators(folder_name) + sep)
            MDLA.rawImagesFolder = QDir.toNativeSeparators(folder_name) + sep
            statusBar.showMessage("Raw images folder set", 2000)

    def show_progress(self, progress):
        self.analyseProgressBar.setVisible(True)
        self.analyseProgressBar.setValue(progress)

    def process_log(self, statusBar, MDLA):
        statusBar.addWidget(self.analyseProgressBar)
        self.flightOutput.setVisible(True)
        self.flightOutput.append("Analysing log file....")
        self.grid.removeItem(self.bottomSpacer)
        self.valid_flight_log = MDLA.process_log()

        if not self.valid_flight_log:
            statusBar.removeWidget(self.analyseProgressBar)
            self.reset_page(statusBar)
            statusBar.showMessage("Error! Log file could not be analysed", 3000)
            return

        self.flightOutput.append("Flight start time: {}".format(MDLA.startFlightTime))
        self.flightOutput.append("Flight end time: {}".format(MDLA.endFlightTime))
        self.flightOutput.append(MDLA.endurance)
        self.flightOutput.append("Home Coordinates: {}, {}".format(MDLA.homeLat, MDLA.homeLng))
        self.flightOutput.append("Begin voltage: {}v".format(MDLA.beginVoltage))
        self.flightOutput.append("End voltage: {}v".format(MDLA.endVoltage))
        self.flightOutput.append("Max wind speed: {}m/s".format(MDLA.maxWindSpeed))
        self.flightOutput.append("Max current: {}A".format(MDLA.maxCurrent))
        self.flightOutput.append("Average current: {}A".format(MDLA.avgCurrent))

        if self.geotagCheckbox.isChecked():
            self.flightOutput.append("Geotagging images....")
            MDLA.gui_geotag_images()

        statusBar.removeWidget(self.analyseProgressBar)
        statusBar.showMessage("Log file analysed", 3000)
        self.clearButton.setVisible(True)

    def reset_page(self, statusBar):
        self.flightOutput.clear()
        self.flightOutput.setVisible(False)
        self.analyseProgressBar.reset()
        self.grid.addItem(self.bottomSpacer, 16, 0)
        self.clearButton.setVisible(False)
        statusBar.showMessage("Flight log cleared", 3000)

    def showTruncationErrorDialog(self, MDLA):
        QMessageBox.critical(self, "Unable to extract flight data",
                             """
                             <p>{} is unable to extract useful flight data from the input log file. This can occur due to
                             several reasons which include invalid flight log, multiple launch attempts resulting in {}
                             ending prematurely.

                             <p> If you are sure that the flight log is valid, please file a bug on the Github project page.
                             """.format(MDLA.applicationName, MDLA.applicationName),
                             QMessageBox.Abort | QMessageBox.Default)

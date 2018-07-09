import sys
from PyQt5.QtWidgets import (QWidget, QGridLayout, QPushButton, QApplication, QDesktopWidget, QFileDialog,
                             QInputDialog, QMessageBox, QMainWindow)
import csv
import utm
import string


class MyMainWindow(QMainWindow):

    def __init__(self, parent=None):

        super(MyMainWindow, self).__init__(parent)
        self.form_widget = UTMToLatLongGUI()
        self.setCentralWidget(self.form_widget)
        self.statusBar().showMessage('ready')
        self.setGeometry(300, 300, 500, 100)
        self.center()

        self.show()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Message',
                                     "Are you sure to quit?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()


class UTMToLatLongGUI(QWidget):

    def __init__(self):

        super().__init__()

        self.file_path = ""
        self.folder_path = ""
        self.zone_no = 43
        self.zone_letter = 'P'

        self.initUI()

    def initUI(self):

        grid = QGridLayout()
        self.setLayout(grid)

        button1 = QPushButton('Csv Upload')
        grid.addWidget(button1, 1, 0)
        button1.clicked.connect(self.getFilePath)

        button2a = QPushButton('Enter Zone No')
        grid.addWidget(button2a, 0, 0)
        button2a.clicked.connect(self.getZoneNumber)

        button2b = QPushButton('Enter Zone Letter')
        grid.addWidget(button2b, 0, 1)
        button2b.clicked.connect(self.getZoneLetter)

        button3 = QPushButton('Convert and Save')
        grid.addWidget(button3, 1, 1)
        button3.clicked.connect(self.getFolderPath)

        self.setWindowTitle('UTM to Lat Long Converter')

        self.show()

    def getZoneNumber(self):
        num, ok = QInputDialog.getInt(self, "Zone Number", "Enter zone number(1-60)")
        if ok:
            if not int(num) in range(1, 61):
                QMessageBox.about(self, 'Error', 'Input can only be a number b/w 1-60')
            else:
                self.zone_no = int(num)
        else:
            self.getZoneNumber()

    def getZoneLetter(self):
        letter, ok = QInputDialog.getText(self, "Zone Letter", "Enter zone letter(C-X)")
        if ok:
            if not letter in string.ascii_uppercase[2:24] + string.ascii_lowercase[2:24]:
                QMessageBox.about(self, 'Error', 'Enter letter in range C-X.')
            else:
                self.zone_letter = letter.upper()
        else:
            self.getZoneLetter()

    def getFilePath(self):
        self.file_path = QFileDialog.getOpenFileName(self, 'Open file', '/home')[0]
        print(self.file_path)

    def getFolderPath(self):
        self.convert_utm_to_lat_long()

    def convert_utm_to_lat_long(self):
        u = UTMToLatLong()
        u.convert(self.file_path, self.zone_no, self.zone_letter)
        assert isinstance(converter.statusBar().showMessage, object)
        converter.statusBar().showMessage('Done')


class UTMToLatLong:

    data = []

    def convert(self, file_path, zone_no, zone_letter):
        try:
            f1 = open(file_path, 'r')
            reader = csv.reader(f1)
        except:
            converter.statusBar().showMessage('Please select a file first')
        new_file_name = file_path.split('.')[0] + "InLatLong.csv"
        f2 = open(new_file_name, 'w')
        writer = csv.writer(f2)
        for row in reader:
            #do calc here
            lat_long = list(utm.to_latlon(float(row[1]), float(row[2]), zone_no, zone_letter))
            writer.writerow(row + lat_long)
        f1.close()
        f2.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    converter = MyMainWindow()
    sys.exit(app.exec_())

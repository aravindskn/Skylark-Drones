import sys
from os import path

from PyQt5.QtGui import QIcon, QPalette, QColor
from PyQt5.QtWidgets import QMainWindow, QApplication, QStackedWidget, QAction

from dlamock import MockDroneLogAnalyser
from ui.AnalysePage import AnalysePage
from ui.HomePage import Home
import images


class DroneCubatorMissionControl(QMainWindow):

    def __init__(self):
        super().__init__()
        self.MDLA = MockDroneLogAnalyser()
        self.initUI()

    def initUI(self):
        # Set window parameters like minimum size, icon and title
        self.setMinimumSize(700, 600)
        self.setWindowIcon(QIcon(':images/icon.png'))
        self.setWindowTitle(self.MDLA.applicationName)

        # Instantiate a status bar
        self.statusBar = self.statusBar()
        self.statusBar.setSizeGripEnabled(False)

        # Set application background color
        pal = QPalette()
        pal.setColor(QPalette.Background, QColor(255, 255, 255))
        self.setPalette(pal)

        # Exit action
        self.exitAction = QAction('&Exit', self)
        self.exitAction.setShortcut('Ctrl+Q')
        self.exitAction.setStatusTip('Quit application')
        self.exitAction.triggered.connect(QApplication.quit)

        # Instantiate menu bar
        self.menubar = self.menuBar()

        # Add file menu
        self.fileMenu = self.menubar.addMenu('&File')
        self.fileMenu.addAction(self.exitAction)

        # Create a stacked widget
        self.stack = QStackedWidget(self)

        # Create 2 pages
        self.stack1 = Home(self.MDLA, self.stack, self.menubar)
        self.stack2 = AnalysePage(self.MDLA, self.stack, self.statusBar)

        # Add the pages to the stack
        self.stack.addWidget(self.stack1)
        self.stack.addWidget(self.stack2)

        self.setCentralWidget(self.stack)

        self.show()

        self.statusBar.showMessage("Ready", 2000)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setOrganizationName("Skylark Drones")
    app.setOrganizationDomain("skylarkdrones.com")
    app.setApplicationName(MockDroneLogAnalyser().applicationName)
    DCMC = DroneCubatorMissionControl()
    sys.exit(app.exec_())
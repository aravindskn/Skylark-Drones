from PyQt5.QtWidgets import QVBoxLayout, QPushButton, QWidget, QMessageBox, QAction

class Home(QWidget):

    def __init__(self, MDLA, Stack, MenuBar):
        super().__init__()

        # About action
        self.aboutAction = QAction('About {}'.format(MDLA.applicationName), self)
        self.aboutAction.setStatusTip("Show information about {}".format(MDLA.applicationName))
        self.aboutAction.triggered.connect(lambda: self.helpAbout(MDLA))

        # Add help menu
        self.helpMenu = MenuBar.addMenu('&Help')
        self.helpMenu.addAction(self.aboutAction)

        preFlightButton = QPushButton("Pre-Flight Check")
        preFlightButton.setMinimumHeight(60)
        preFlightButton.setEnabled(False)

        inFlightButton = QPushButton("In-Flight Check")
        inFlightButton.setMinimumHeight(60)
        inFlightButton.setEnabled(False)

        analyseLogButton = QPushButton("Analyse Log")
        analyseLogButton.setMinimumHeight(60)
        analyseLogButton.clicked.connect(lambda: self.open_analyse_page(Stack))

        vbox = QVBoxLayout()
        vbox.addStretch()
        vbox.addWidget(preFlightButton)
        vbox.addWidget(inFlightButton)
        vbox.addWidget(analyseLogButton)
        vbox.addStretch()
        vbox.setSpacing(20)
        vbox.setContentsMargins(60, 40, 60, 40)

        self.setLayout(vbox)

    def open_analyse_page(self, Stack):
        Stack.setCurrentIndex(1)

    def help_try(self):
        print("test")

    def helpAbout(self, MDLA):
        QMessageBox.about(self, "About {}".format(MDLA.applicationName),
                          """
                          <b>{} {} </b>
                          <p>Application used in all phases of a drone operation
                          starting from the pre-flight check to post-flight data processing.
                          <p>Copyright &copy; 20016 Skylark Drones Ltd. All rights reserved.
                          """.format(MDLA.applicationName, MDLA.version))

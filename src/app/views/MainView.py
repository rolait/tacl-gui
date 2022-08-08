from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *

from app.Database import Database
from app.views.components.MainMenuBar import MainMenuBar
from app.views.components.NoDatabaseBox import NoDatabaseBox
from app.views.components.DatabaseInfoGroupBox import DatabaseInfoGroupBox
from app.views.components.SelectOrGenerateDatabaseBox import SelectOrGenerateDatabaseBox


class MainView(QMainWindow):

    def __init__(self, desktop: QDesktopWidget):
        super().__init__()

        self._desktop = desktop

        self._noDatabaseBox = NoDatabaseBox()
        self._selectOrGenerateDatabaseBox = SelectOrGenerateDatabaseBox()

        self._pleaseSelectDatabaseLabel = QLabel()
        self._pleaseSelectDatabaseLabel.setAlignment(Qt.AlignCenter)

        self._whatDoYouWantToDoLabel = QLabel()
        self._whatDoYouWantToDoLabel.setAlignment(Qt.AlignCenter)

        self._differenceIntersectButton = QPushButton()
        self._differenceIntersectButton.setFixedWidth(200)

        self._searchButton = QPushButton()
        self._searchButton.setFixedWidth(200)

        self._suppliedIntersectButton = QPushButton()
        self._suppliedIntersectButton.setFixedWidth(200)

        self._filterRationaliseButton = QPushButton()
        self._filterRationaliseButton.setFixedWidth(200)

        self._actionsVBox = QVBoxLayout()
        self._actionsVBox.setSpacing(15)
        self._actionsVBox.setAlignment(Qt.AlignCenter)

        self._actionsVBox.addWidget(self._whatDoYouWantToDoLabel)
        self._actionsVBox.addWidget(self._differenceIntersectButton)
        self._actionsVBox.addWidget(self._searchButton)
        self._actionsVBox.addWidget(self._suppliedIntersectButton)
        self._actionsVBox.addWidget(self._filterRationaliseButton)

        self._commandsGroupBox = QGroupBox()
        self._commandsGroupBox.setLayout(self._actionsVBox)

        self._databaseInfoGroupBox = DatabaseInfoGroupBox()

        self._menuBar = MainMenuBar()
        self.setMenuBar(self._menuBar)

        mainVBox = QVBoxLayout()
        mainVBox.addStretch(1)
        mainVBox.addWidget(self._noDatabaseBox)
        mainVBox.addWidget(self._selectOrGenerateDatabaseBox)
        mainVBox.addWidget(self._databaseInfoGroupBox)
        mainVBox.addWidget(self._commandsGroupBox)

        centralWidget = QWidget()
        centralWidget.setLayout(mainVBox)
        self.setCentralWidget(centralWidget)

        self.setMaximumWidth(self.width())
        self.updateTranslations()
        self.layout().setSizeConstraint(QLayout.SetFixedSize)

        self._noDatabaseBox.setVisible(False)
        self._databaseInfoGroupBox.setVisible(False)
        self._commandsGroupBox.setVisible(False)

    def updateTranslations(self) -> None:
        self.setWindowTitle(self.tr("TACL-GUI 鬼"))
        self._menuBar.updateTranslations()

        self._whatDoYouWantToDoLabel.setText(self.tr("What do you want to do?"))
        self._differenceIntersectButton.setText(self.tr("Difference/Intersect"))
        self._searchButton.setText(self.tr("Search"))
        self._suppliedIntersectButton.setText(self.tr("Supplied Intersect"))
        self._filterRationaliseButton.setText(self.tr("Filter/Rationalise"))

        self._commandsGroupBox.setTitle(self.tr("Commands"))
        self._pleaseSelectDatabaseLabel.setText(self.tr("Please select a database."))

        self._databaseInfoGroupBox.updateTranslations()

        self._noDatabaseBox.updateTranslations()
        self._selectOrGenerateDatabaseBox.updateTranslations()

    def getMenuBar(self) -> MainMenuBar:
        return self._menuBar

    def getNoDatabaseBox(self) -> NoDatabaseBox:
        return self._noDatabaseBox

    def getSelectOrGenerateDatabaseBox(self) -> SelectOrGenerateDatabaseBox:
        return self._selectOrGenerateDatabaseBox

    def getDifferenceIntersectButton(self) -> QPushButton:
        return self._differenceIntersectButton

    def getSearchButton(self) -> QPushButton:
        return self._searchButton

    def getSuppliedIntersectButton(self) -> QPushButton:
        return self._suppliedIntersectButton

    def getFilterRationaliseButton(self) -> QPushButton:
        return self._filterRationaliseButton

    def getDatabaseInfoBox(self) -> DatabaseInfoGroupBox:
        return self._databaseInfoGroupBox

    def showNoDatabasesBox(self) -> None:
        self._noDatabaseBox.setVisible(True)
        self._selectOrGenerateDatabaseBox.setVisible(False)
        self._databaseInfoGroupBox.setVisible(False)
        self._commandsGroupBox.setVisible(False)

    def showSelectOrGenerateBox(self) -> None:
        self._selectOrGenerateDatabaseBox.setVisible(True)
        self._noDatabaseBox.setVisible(False)
        self._databaseInfoGroupBox.setVisible(False)
        self._commandsGroupBox.setVisible(False)

    def showDatabase(self, database: Database) -> None:
        self._databaseInfoGroupBox.updateDatabaseInfo(database)

        self._noDatabaseBox.setVisible(False)
        self._selectOrGenerateDatabaseBox.setVisible(False)
        self._databaseInfoGroupBox.setVisible(True)
        self._commandsGroupBox.setVisible(True)

    def center(self) -> None:
        frameGeometry = self.frameGeometry()
        centerPoint = self._desktop.availableGeometry().center()

        frameGeometry.moveCenter(centerPoint)
        self.move(frameGeometry.topLeft())
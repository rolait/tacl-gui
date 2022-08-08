from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *

from app.Database import Database


class DatabaseInfoGroupBox(QGroupBox):

    def __init__(self):
        super().__init__()

        self._corpusPathLabel = QLabel()
        self._corpusPathValueLabel = self._createValueLabel()
        self._corpusPathLabel = QLabel()

        self._databaseNameLabel = QLabel()
        self._databaseNameValueLabel = self._createValueLabel()
        self._databasePathLabel = QLabel()
        self._databasePathValueLabel = self._createValueLabel()
        self._ngramsLengthLabel = QLabel()
        self._ngramsLengthValueLabel = self._createValueLabel()

        grid = QGridLayout()
        grid.setColumnStretch(1, 1)
        grid.setHorizontalSpacing(10)
        row: int = 0
        grid.addWidget(self._databaseNameLabel, row, 0)
        grid.addWidget(self._databaseNameValueLabel, row, 1)
        row += 1
        grid.addWidget(self._databasePathLabel, row, 0)
        grid.addWidget(self._databasePathValueLabel, row, 1)
        row += 1
        grid.addWidget(self._corpusPathLabel, row, 0)
        grid.addWidget(self._corpusPathValueLabel, row, 1)
        row += 1
        grid.addWidget(self._ngramsLengthLabel, row, 0)
        grid.addWidget(self._ngramsLengthValueLabel, row, 1)

        buttonsHBox = QHBoxLayout()
        self._updateButton = QPushButton()
        self._deleteButton = QPushButton()

        buttonsHBox.addWidget(self._updateButton)
        buttonsHBox.addWidget(self._deleteButton)
        buttonsHBox.addStretch(1)

        mainBox = QVBoxLayout()
        mainBox.addLayout(grid)
        mainBox.addLayout(buttonsHBox)

        self.setLayout(mainBox)

    def _createValueLabel(self) -> QLabel:
        label = QLabel()
        label.setStyleSheet("background-color: #ffffff; padding: 5px;")
        label.setTextInteractionFlags(Qt.TextSelectableByMouse )

        return label

    def updateTranslations(self) -> None:
        self.setTitle(self.tr("Database Info"))
        self._databaseNameLabel.setText(self.tr("Name") + ":")
        self._databasePathLabel.setText(self.tr("Database Path") + ":")
        self._corpusPathLabel.setText(self.tr("Corpus Path") + ":")
        self._ngramsLengthLabel.setText(self.tr("n-grams (min/max)") + ":")

        self._updateButton.setText(self.tr("Update"))
        self._deleteButton.setText(self.tr("Delete"))

    def updateDatabaseInfo(self, database: Database):
        self._databaseNameValueLabel.setText(str(database.getName()))
        self._databasePathValueLabel.setText(database.getPath().truncate(50))
        self._corpusPathValueLabel.setText(database.getCorpusPath().truncate(50))

        ngramsLength = "{}/{}".format(database.getNGramMinLength(), database.getNGramMaxLength())
        self._ngramsLengthValueLabel.setText(ngramsLength)

    def getDeleteButton(self) -> QPushButton:
        return self._deleteButton

    def getUpdateButton(self) -> QPushButton:
        return self._updateButton

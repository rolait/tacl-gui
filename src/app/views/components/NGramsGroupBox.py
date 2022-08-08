from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QGroupBox, QFormLayout, QLabel, QSpinBox

from app.validatable.DatabaseNGramLengths import DatabaseNGramLengths


class NGramsGroupBox(QGroupBox):

    def __init__(self):
        super().__init__()

        formGrid = QFormLayout()
        self.setLayout(formGrid)

        # ------------------------------
        # N-grams Min Length
        # -----------------------------
        self._minLengthLabel = QLabel()
        self._minLengthSpinBox = QSpinBox()
        self._minLengthSpinBox.setFixedWidth(50)

        formGrid.addRow(self._minLengthLabel, self._minLengthSpinBox)

        # ------------------------------
        # N-grams Max Length
        # -----------------------------
        self._maxLengthLabel = QLabel()
        self._maxLengthSpinBox = QSpinBox()
        self._maxLengthSpinBox.setFixedWidth(50)

        self._minLengthSpinBox.valueChanged.connect(self._minLengthSpinBoxChanged)
        self._maxLengthSpinBox.valueChanged.connect(self._maxLengthSpinBoxChanged)

        formGrid.addRow(self._maxLengthLabel, self._maxLengthSpinBox)

    @pyqtSlot(int)
    def _minLengthSpinBoxChanged(self, minLength: int) -> None:
        """
        In case min > max, adapt max.
        """
        if minLength > self._maxLengthSpinBox.value():
            self._maxLengthSpinBox.setValue(minLength)

    @pyqtSlot(int)
    def _maxLengthSpinBoxChanged(self, maxLength: int) -> None:
        """
        In case max < min, adapt min.
        """
        if maxLength < self._minLengthSpinBox.value():
            self._minLengthSpinBox.setValue(maxLength)

    def updateTranslations(self) -> None:
        self.setTitle(self.tr("n-grams"))
        self._minLengthLabel.setText(self.tr("Min. Length") + ":")
        self._maxLengthLabel.setText(self.tr("Max. Length") + ":")

    def setValues(self, min: int, max: int) -> None:
        self._minLengthSpinBox.setValue(min)
        self._maxLengthSpinBox.setValue(max)

    def setMinMaxValues(self,
        minSpinBoxMin: int, minSpinBoxMax: int,
        maxSpinBoxMin: int, maxSpinBoxMax: int,
    ) -> None:
        self._minLengthSpinBox.setMinimum(minSpinBoxMin)
        self._minLengthSpinBox.setMaximum(minSpinBoxMax)
        self._maxLengthSpinBox.setMinimum(maxSpinBoxMin)
        self._maxLengthSpinBox.setMaximum(maxSpinBoxMax)

        self._minLengthSpinBox.setDisabled(minSpinBoxMin == minSpinBoxMax)
        self._maxLengthSpinBox.setDisabled(maxSpinBoxMin == maxSpinBoxMax)


    def getInput(self) -> DatabaseNGramLengths:
        minLength: int = self._minLengthSpinBox.value()
        maxLength: int = self._maxLengthSpinBox.value()

        return DatabaseNGramLengths(minLength, maxLength)



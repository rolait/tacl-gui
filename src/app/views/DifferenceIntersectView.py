from PyQt5.QtCore import Qt
from PyQt5.QtGui import QGuiApplication
from PyQt5.QtWidgets import *

from app.views.DialogFactory import DialogFactory
from app.views.DialogView import DialogView
from app.views.components.CheckboxWithTextFieldWidget import CheckboxWithTextFieldWidget
from app.views.components.FileSelectionWidget import FileSelectionWidget
from app.views.components.LabelWithTooltipWidget import LabelWithTooltipWidget


class DifferenceIntersectView(DialogView):

    def __init__(
        self,
        dialogFactory: DialogFactory
    ):
        super().__init__()

        formGrid = QGridLayout()
        formGrid.setSpacing(10)

        # -----------------------------
        # Command
        # -----------------------------
        row: int = 0
        self._commandLabel = QLabel()
        QGuiApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)

        self._differenceRadioButton = QRadioButton()
        self._differenceRadioButton.setChecked(True)
        self._intersectRadioButton = QRadioButton()

        radioButtonHBox = QHBoxLayout()
        radioButtonHBox.addWidget(self._differenceRadioButton)
        radioButtonHBox.addWidget(self._intersectRadioButton)
        radioButtonHBox.addStretch(1)

        formGrid.addWidget(self._commandLabel, row, 0)
        formGrid.addLayout(radioButtonHBox, row, 1)

        # -----------------------------
        # Catalogue File
        # -----------------------------
        row += 1
        self._catalogueFileLabel = LabelWithTooltipWidget()
        self._catalogueFileSelection = FileSelectionWidget(
            self,
            lambda dir: dialogFactory.showOpenExistingFileDialog(self, dir)
        )

        formGrid.addWidget(self._catalogueFileLabel , row, 0)
        formGrid.addWidget(self._catalogueFileSelection, row, 1)

        # -----------------------------
        # Output File
        # -----------------------------
        row += 1
        self._outputFileLabel = LabelWithTooltipWidget()
        self._outputPathFileSelection = FileSelectionWidget(
            self,
            lambda dir: dialogFactory.showSaveFileDialog(self, dir)
        )
        formGrid.addWidget(self._outputFileLabel, row, 0)
        formGrid.addWidget(self._outputPathFileSelection, row, 1)

        # -----------------------------
        # Asymmetric
        # -----------------------------
        row += 1
        self._asymmetricLabel = LabelWithTooltipWidget()
        self._asymmetricText = CheckboxWithTextFieldWidget('Label')

        formGrid.addWidget(self._asymmetricLabel, row, 0)
        formGrid.addWidget(self._asymmetricText, row, 1)


        # -----------------------------
        # Buttons
        # -----------------------------
        row += 1
        self._runTestButton = QPushButton()
        self._cancelButton = QPushButton()

        buttonsHBox = QHBoxLayout()
        buttonsHBox.addWidget(self._runTestButton)
        buttonsHBox.addWidget(self._cancelButton)
        buttonsHBox.setAlignment(Qt.AlignLeft)

        self._runTestButton.setDefault(True)

        mainVBox = QVBoxLayout()
        mainVBox.addLayout(formGrid)
        mainVBox.addLayout(buttonsHBox)

        self.updateTranslations()
        self._fixLayout(mainVBox)

        self._differenceRadioButton.toggled.connect(self._toggleAdditionalOptions)
        self._intersectRadioButton.toggled.connect(self._toggleAdditionalOptions)

    def updateTranslations(self) -> None:
        self.setWindowTitle(self.tr("Difference/Intersect"))

        self._commandLabel.setText(self.tr("Command") + ":")
        self._differenceRadioButton.setText(self.tr("Difference"))
        self._intersectRadioButton.setText(self.tr("Intersect"))

        self._asymmetricLabel.setText(self.tr("Asymmetric") + ":")
        self._asymmetricLabel.setTooltipText(self.tr(
            "Restricts the results to strings found in the text with the supplied label only."
        ))

        self._catalogueFileLabel.setText(self.tr("Catalogue Path") + ":")
        self._catalogueFileLabel.setTooltipText(self.tr("Select a catalogue file."))
        self._catalogueFileSelection.setButtonText(self.tr("Select"))

        self._outputFileLabel.setText(self.tr("Output CSV File") + ":")
        self._outputFileLabel.setTooltipText(self.tr("Specify a location and name for your results."))
        self._outputPathFileSelection.setButtonText(self.tr("Select"))

        self._runTestButton.setText(self.tr("Run Test"))
        self._cancelButton.setText(self.tr("Cancel"))

    def getCancelButton(self) -> QPushButton:
        return self._cancelButton

    def getRunTestButton(self) -> QPushButton:
        return self._runTestButton

    def isDifferenceChecked(self) -> bool:
        return self._differenceRadioButton.isChecked()

    def getCataloguePath(self) -> str:
        return self._catalogueFileSelection.getPathTextField().text()

    def getOutputPath(self) -> str:
        return self._outputPathFileSelection.getPathTextField().text()

    def getAsymmetricLabel(self) -> str:
        return self._asymmetricText.getValue()

    def clearInput(self):
        self._differenceRadioButton.setChecked(True)
        self._catalogueFileSelection.getPathTextField().setText("")
        self._outputPathFileSelection.getPathTextField().setText("")
        self._asymmetricText.clear()

    def _toggleAdditionalOptions(self):
        differenceSelected = self.isDifferenceChecked();

        self._asymmetricLabel.setVisible(differenceSelected)
        self._asymmetricText.setVisible(differenceSelected)


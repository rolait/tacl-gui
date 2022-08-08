from typing import Optional

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *

from app.views.DialogFactory import DialogFactory
from app.views.DialogView import DialogView
from app.views.components.FileSelectionWidget import FileSelectionWidget
from app.views.components.LabelWithTooltipWidget import LabelWithTooltipWidget
from app.validatable.ResultPath import ResultPath
from app.views.components.HorizontalPositiveSpinBox import HorizontalPositiveSpinBox


class FilterRationaliseView(DialogView):

    def __init__(self, dialogFactory: DialogFactory):
        super().__init__()

        self._mainVBox = QVBoxLayout()
        self._initResultAndOutputGroup(dialogFactory)
        self._initOptionsGroup()
        self._initButtons()

        self._runFiltersButton.setDefault(True)

        self.updateTranslations()
        self._fixLayout(self._mainVBox)

    def _initResultAndOutputGroup(self, dialogFactory: DialogFactory):
        formGrid = QGridLayout()
        formGrid.setSpacing(10)

        row: int = 0
        self._resultFileLabel = QLabel()
        self._resultFileSelection = FileSelectionWidget(
            self, lambda dir: dialogFactory.showOpenExistingFileDialog(self, dir)
        )
        formGrid.addWidget(self._resultFileLabel, row, 0)
        formGrid.addWidget(self._resultFileSelection, row, 1)

        row += 1
        self._outputFileLabel = LabelWithTooltipWidget()
        self._outputPathFileSelection = FileSelectionWidget(
            self,
            lambda dir: dialogFactory.showSaveFileDialog(self, dir)
        )
        formGrid.addWidget(self._outputFileLabel, row, 0)
        formGrid.addWidget(self._outputPathFileSelection, row, 1)

        self._resultAndOutputGroup = QGroupBox()
        self._resultAndOutputGroup.setLayout(formGrid)
        self._mainVBox.addWidget(self._resultAndOutputGroup)


    def _initOptionsGroup(self):
        formGrid = QGridLayout()
        formGrid.setSpacing(10)

        row: int = 0
        self._minCountLabel = LabelWithTooltipWidget()
        self._minCountSpinBox = HorizontalPositiveSpinBox(1)

        hbox = QHBoxLayout()
        hbox.addWidget(self._minCountSpinBox)
        hbox.setContentsMargins(0, 0, 0, 0)
        hbox.addStretch(1)
        hbox.setAlignment(Qt.AlignLeft)

        formGrid.addWidget(self._minCountLabel, row, 0)
        formGrid.addLayout(hbox, row, 1, Qt.AlignLeft)

        self._maxCountLabel = LabelWithTooltipWidget()
        self._maxCountSpinBox = HorizontalPositiveSpinBox()
        formGrid.addWidget(self._maxCountLabel, row, 2)
        formGrid.addWidget(self._maxCountSpinBox, row, 3, Qt.AlignLeft)

        row += 1
        self._minSizeLabel = LabelWithTooltipWidget()
        self._minSizeSpinBox = HorizontalPositiveSpinBox(1)
        formGrid.addWidget(self._minSizeLabel, row, 0)
        formGrid.addWidget(self._minSizeSpinBox, row, 1, Qt.AlignLeft)

        self._maxSizeLabel = LabelWithTooltipWidget()
        self._maxSizeSpinBox = HorizontalPositiveSpinBox()
        formGrid.addWidget(self._maxSizeLabel, row, 2)
        formGrid.addWidget(self._maxSizeSpinBox, row, 3, Qt.AlignLeft)

        row += 1
        self._minCountWorkLabel = LabelWithTooltipWidget()
        self._minCountWorkSpinBox = HorizontalPositiveSpinBox(1)
        formGrid.addWidget(self._minCountWorkLabel, row, 0)
        formGrid.addWidget(self._minCountWorkSpinBox, row, 1, Qt.AlignLeft)

        self._maxCountWorkLabel = LabelWithTooltipWidget()
        self._maxCountWorkSpinBox = HorizontalPositiveSpinBox()
        formGrid.addWidget(self._maxCountWorkLabel, row, 2)
        formGrid.addWidget(self._maxCountWorkSpinBox, row, 3, Qt.AlignLeft)

        row += 1
        self._minWorksLabel = LabelWithTooltipWidget()
        self._minWorksSpinBox = HorizontalPositiveSpinBox(1)
        formGrid.addWidget(self._minWorksLabel, row, 0)
        formGrid.addWidget(self._minWorksSpinBox, row, 1, Qt.AlignLeft)

        self._maxWorksLabel = LabelWithTooltipWidget()
        self._maxWorksSpinBox = HorizontalPositiveSpinBox()
        formGrid.addWidget(self._maxWorksLabel, row, 2)
        formGrid.addWidget(self._maxWorksSpinBox, row, 3, Qt.AlignLeft)

        self._optionsGroup = QGroupBox()
        self._optionsGroup.setLayout(formGrid)
        self._mainVBox.addWidget(self._optionsGroup)

    def _initButtons(self):
        self._runFiltersButton = QPushButton()
        self._cancelButton = QPushButton()

        buttonHBox = QHBoxLayout()
        buttonHBox.addWidget(self._runFiltersButton)
        buttonHBox.addWidget(self._cancelButton)
        buttonHBox.setAlignment(Qt.AlignLeft)

        self._mainVBox.addLayout(buttonHBox)

    def updateTranslations(self) -> None:
        self.setWindowTitle(self.tr("Filter, Rationalise and Tidy Results"))
        self._resultAndOutputGroup.setTitle(self.tr("Result && Output Files"))
        self._optionsGroup.setTitle(self.tr("Options"))

        self._resultFileLabel.setText(self.tr("Result File") + ":")
        self._minCountLabel.setText(self.tr("Min. Count") + ":")
        self._maxCountLabel.setText(self.tr("Max. Count") + ":")
        self._minSizeLabel.setText(self.tr("Min. Size") + ":")
        self._maxSizeLabel.setText(self.tr("Max. Size") + ":")
        self._minCountWorkLabel.setText(self.tr("Min. Count/Work") + ":")
        self._maxCountWorkLabel.setText(self.tr("Max. Count/Work") + ":")
        self._minWorksLabel.setText(self.tr("Min. Works") + ":")
        self._maxWorksLabel.setText(self.tr("Max. Works") + ":")

        self._minCountLabel.setTooltipText(self.tr("Minimum total count per n-gram to include."))
        self._maxCountLabel.setTooltipText(self.tr("Maximum total count per n-gram to include."))
        self._minSizeLabel.setTooltipText(self.tr("Minimum size of n-grams to include."))
        self._maxSizeLabel.setTooltipText(self.tr("Maximum size of n-grams to include."))
        self._minCountWorkLabel.setTooltipText(self.tr(
            "Minimum count per n-gram per work to include; if a single witness meets this criterion for an n-gram, all "
            "instances of that n-gram are kept. (default: None)"
        ))
        self._maxCountWorkLabel.setTooltipText(self.tr(
            "Maximum count per n-gram per work to include; if a single witness meets this criterion for an n-gram, all"
            "instances of that n-gram are kept. (default: None)"
        ))
        self._minWorksLabel.setTooltipText(self.tr(
            "Minimum count of works containing n-gram to include. (default: None)"
        ))
        self._maxWorksLabel.setTooltipText(self.tr(
            "Maximum count of works containing n-gram to include. (default: None)"
        ))

        self._outputFileLabel.setText(self.tr("Ouput CSV File") + ":")
        self._outputFileLabel.setTooltipText("Specify a location and name for your results.")
        self._outputPathFileSelection.setButtonText(self.tr("Select"))
        self._resultFileSelection.setButtonText(self.tr("Select"))

        self._runFiltersButton.setText(self.tr("Run Filters"))
        self._cancelButton.setText(self.tr("Cancel"))

    def clearInput(self):
        self._resultFileSelection.getPathTextField().clear()
        self._outputPathFileSelection.getPathTextField().clear()

    def getRunFiltersButton(self) -> QPushButton:
        return self._runFiltersButton

    def setResultPath(self, resultPath: ResultPath) -> None:
        self._resultFileSelection.getPathTextField().setText(str(resultPath))

    def getCancelButton(self) -> QPushButton:
        return self._cancelButton

    def getResultFile(self) -> str:
        return self._resultFileSelection.getPathTextField().text()

    def getOutputPath(self) -> str:
        return self._outputPathFileSelection.getPathTextField().text()

    def getMinCount(self) -> Optional[int]:
        return self._minCountSpinBox.getValue()

    def getMaxCount(self) -> Optional[int]:
        return self._maxCountSpinBox.getValue()

    def getMinSize(self) -> Optional[int]:
        return self._minSizeSpinBox.getValue()

    def getMaxSize(self) -> Optional[int]:
        return self._maxSizeSpinBox.getValue()

    def getMinCountWorks(self) -> Optional[int]:
        return self._minCountWorkSpinBox.getValue()

    def getMaxCountWorks(self) -> Optional[int]:
        return self._maxCountWorkSpinBox.getValue()

    def getMinWorks(self) -> Optional[int]:
        return self._minWorksSpinBox.getValue()

    def getMaxWorks(self) -> Optional[int]:
        return self._maxWorksSpinBox.getValue()
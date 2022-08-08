from pathlib import Path
from traceback import format_exception
from typing import List, Tuple, Optional, Union, Callable

from PyQt5.QtCore import Qt, QObject
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QProgressDialog, QMessageBox, QWidget, QFileDialog

from app.Runnable import Runnable
from app.repositories.SettingsRepository import SettingsRepository
from app.utils import tr
from app.validatable.Id import Id
from app.validatable.WritableFilePath import WritableFilePath


class DialogFactory(QObject):

    def __init__(self, settingsRepository: SettingsRepository):
        super().__init__()
        self._settingsRepository = settingsRepository
        self._settings = self._settingsRepository.find()

    def showOpenExistingDirectoryDialog(self, parent: QWidget, currentDir: str) -> Optional[str]:
        result = QFileDialog.getExistingDirectory(
            parent,
            self.tr("Please select a directory"),
            self._getStartOpenPath(currentDir)
        )

        if not result or len(result.strip()) == 0:
            return None

        return self._updateLastOpenedPath(result)

    def showOpenExistingFileDialog(self, parent: QWidget, currentDir: str) -> Optional[str]:
        result =  QFileDialog.getOpenFileName(
            parent,
            self.tr("Please select a file"),
            self._getStartOpenPath(currentDir)
        )

        if not isinstance(result, Tuple) or not result[0]:
            return None

        return self._updateLastOpenedPath(result[0])

    def showOpenExistingFilesDialog(self, parent: QWidget, currentDir: str) -> Optional[List[str]]:
        result = QFileDialog.getOpenFileNames(
            parent,
            self.tr("Please select one or several files"),
            self._getStartOpenPath(currentDir)
        )

        if not isinstance(result, Tuple) or not isinstance(result[0], List):
            return None

        list = result[0]
        if len(list) > 0:
            self._updateLastOpenedPath(list[0])

        return list

    def _getStartOpenPath(self, currentDir: str) -> str:
        if len(currentDir) > 0:
            return currentDir

        return self._settings.getLastOpenPath()

    def _updateLastOpenedPath(self, result: str):
        openedPath = str(Path(result).parent.absolute())
        self._settings.setLastOpenPath(openedPath)
        self._settingsRepository.save(self._settings)

        return result

    def showSaveFileDialog(self, parent: QWidget, currentDir: str) -> Optional[str]:
        result = QFileDialog.getSaveFileName(
            parent,
            self.tr("Please choose a location to save the file"),
            self._getStartSavePath(currentDir),
            "", "",
            QFileDialog.DontConfirmOverwrite
        )

        if not isinstance(result, Tuple) or not result[0]:
            return None

        savePath = str(Path(result[0]).parent.absolute())
        self._settings.setLastSavePath(savePath)
        self._settingsRepository.save(self._settings)

        return str(result[0])

    def _getStartSavePath(self, currentDir: str) -> str:
        if len(currentDir) > 0:
            return currentDir

        return self._settings.getLastSavePath()

    def showOverwriteDialogIfFileExistent(self, file: WritableFilePath, parent: QWidget) -> bool:
        if not file.asPath().exists():
            return True

        return self.showConfirmationDialog(
            tr("Please Confirm"),
            tr("The file '{}' does already exist. Do you want to overwrite it?").format(file),
            parent,
            tr("Yes"), tr("No")
        )

    def showConfirmationDialog(
        self,
        title: str,
        text: str,
        parent: QWidget,
        okButtonText: str ,
        cancelButtonText: str,
        defaultButton: int = QMessageBox.Cancel,
        icon: int = QMessageBox.Question,
        details: str = None
    ) -> bool:
        dialog = QMessageBox(parent)
        dialog.setIcon(icon)
        dialog.setFixedWidth(550)
        dialog.setWindowTitle(title)
        dialog.setText(text)
        dialog.setStandardButtons(QMessageBox.Cancel | QMessageBox.Ok)
        dialog.setDefaultButton(defaultButton)

        self._prepareDialogButton(dialog, QMessageBox.Ok, okButtonText)
        self._prepareDialogButton(dialog, QMessageBox.Cancel, cancelButtonText)

        if details is not None:
            dialog.setDetailedText(details)

        if dialog.exec_() == QMessageBox.Ok:
            return True

        return False

    def _prepareDialogButton(self, dialog: QMessageBox, type: int, text: str):
        button = dialog.button(type)
        button.setText(text)
        button.setIcon(QIcon())

    def showInfoBox(self, title: str, text):
        box = QMessageBox()
        box.setIcon(QMessageBox.Information)
        box.setFixedWidth(550)
        box.setWindowTitle(title)
        box.setText(text)
        box.exec_()

    def showProgressDialog(
            self,
            parent: QWidget,
            windowTitle: str,
            maxValue: int,
            labelText: str,
            runnable: Runnable
    ) -> QProgressDialog:
        dialog = QProgressDialog(
            labelText,
            self.tr("Cancel"),
            0,
            maxValue,
            parent
        )
        dialog.setWindowModality(Qt.WindowModal)
        dialog.setWindowTitle(windowTitle)
        dialog.setFixedWidth(400)
        dialog.show()

        signals = runnable.getSignals()
        signals.getProgressSignal().connect(dialog.setLabelText)

        return dialog

    def showTaclError(self, exception: Exception):
        self.showErrorMessage(
            self.tr("TACL Error"),
            self.tr("TACL reports the following error") + ":\n\n" + str(exception),
            ''.join(format_exception(type(exception), exception, exception.__traceback__))

        )

    def showInputError(self, text: str, details: str = None):
        self.showErrorMessage(
            self.tr("Invalid Data"),
            self.tr("The entered data is invalid") + "\n\n" + text,
            details
        )

    def showErrorMessage(self, title: str, text: str, details: str = None):
        errorBox = QMessageBox()
        errorBox.setIcon(QMessageBox.Warning)
        errorBox.setFixedWidth(850)
        errorBox.setWindowTitle(title)
        errorBox.setText(text)

        if details is not None:
            errorBox.setDetailedText(details)
        errorBox.exec_()

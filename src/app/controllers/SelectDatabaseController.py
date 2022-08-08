from logging import Logger
from typing import Optional

from PyQt5.QtGui import QCloseEvent

from app.Database import Database
from app.repositories.DatabaseRepository import DatabaseRepository
from app.validatable.Id import Id
from app.views.SelectDatabaseView import SelectDatabaseView


class SelectDatabaseController:
    _currentDatabaseId: Id = None

    def __init__(self, view: SelectDatabaseView, databaseRepository: DatabaseRepository, logger: Logger):
        self._view = view
        self._databaseRepository = databaseRepository
        self._logger = logger

        # actions
        self._view.getSelectButton().clicked.connect(lambda: self._select())
        self._view.getCancelButton().clicked.connect(lambda: self._cancel())
        self._view.closeEvent = lambda e: self._cancel()

    def run(self, currentDatabaseId: Optional[Id]) -> Id:
        self._currentDatabaseId = currentDatabaseId
        self._updateDatabasesComboBox()

        self._view.showAsApplicationModal()

        return self._currentDatabaseId

    def _cancel(self) -> None:
        self._currentDatabaseId = None
        self._view.hide()

    def _select(self) -> None:
        self._currentDatabaseId = Id(self._view.getDatabaseComboBox().currentData())
        self._view.hide()

    def _updateDatabasesComboBox(self) -> None:
        databases = self._databaseRepository.findAllNames()
        comboBox = self._view.getDatabaseComboBox()
        comboBox.clear()

        # Update the combo box.
        comboBox.setDisabled(False)
        for id, name in databases.items():
            comboBox.addItem(str(name), id.asInt())

        # select the database.
        index = -1
        if self._currentDatabaseId is not None:
            index = comboBox.findData(self._currentDatabaseId.asInt())

            if index == -1:
                self._logger.error(
                    "There should be an item with the database id {} in the combo box.".format(
                        self._currentDatabaseId.asInt())
                )

        if index != -1:
            comboBox.setCurrentIndex(index)

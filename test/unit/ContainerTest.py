import sys
from collections import Callable
from logging import Logger
from sqlite3 import Connection
from typing import Type
from unittest.mock import Mock

import pytest
from PyQt5.QtCore import QThreadPool
from PyQt5.QtWidgets import QApplication, QDesktopWidget

from app.Container import Container
from app.LoggerHandlerFactory import LoggerHandlerFactory
from app.Settings import Settings
from app.controllers.DifferenceIntersectController import DifferenceIntersectController
from app.controllers.FilterRationaliseController import FilterRationaliseController
from app.controllers.GenerateDatabaseController import GenerateDatabaseController
from app.controllers.ImportDatabaseController import ImportDatabaseController
from app.controllers.MainController import MainController
from app.controllers.SearchController import SearchController
from app.controllers.SelectDatabaseController import SelectDatabaseController
from app.controllers.SuppliedIntersectController import SuppliedIntersectController
from app.controllers.UpdateDatabaseController import UpdateDatabaseController
from app.inputValidator.InputValidatorFactory import InputValidatorFactory
from app.repositories.DatabaseRepository import DatabaseRepository
from app.repositories.ResultRepository import ResultRepository
from app.repositories.SettingsRepository import SettingsRepository
from app.tacl.Tacl import Tacl
from app.tacl.TaclRunner import TaclRunner
from app.views.DialogFactory import DialogFactory
from app.views.DifferenceIntersectView import DifferenceIntersectView
from app.views.FilterRationaliseView import FilterRationaliseView
from app.views.GenerateDatabaseView import GenerateDatabaseView
from app.views.MainView import MainView
from app.views.SearchView import SearchView
from app.views.SelectDatabaseView import SelectDatabaseView
from app.views.SuppliedIntersectView import SuppliedIntersectView
from app.views.UpdateDatabaseView import UpdateDatabaseView
from test.TaclGuiTestCase import TaclGuiTestCase

application: QApplication = Mock(spec=QApplication)
connection: QApplication = Mock(spec=Connection)
container = Container(application, connection)
app = QApplication(sys.argv)


class ContainerTest:

    @pytest.mark.parametrize(
        "containerMethod, expectedType",
        [
            [container.logger, Logger],
            [container.tacl, Tacl],
            [container.loggerHandlerFactory, LoggerHandlerFactory],
            [container.databaseRepository, DatabaseRepository],
            [container.resultRepository, ResultRepository],
            [container.settingsRepository, SettingsRepository],
            [container.mainController, MainController],
        ]
    )
    def test_alwaysReturnsSameInstance(self, containerMethod: Callable, expectedType: Type):
        if expectedType is not SettingsRepository:
            container.settingsRepository = Mock(spec=SettingsRepository)

        instance1 = containerMethod()
        instance2 = containerMethod()

        assert instance1 == instance2
        assert type(instance1) == expectedType

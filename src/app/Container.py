import logging
from logging import Logger
from sqlite3 import Connection
from typing import Callable, Type

from PyQt5.QtCore import QThreadPool
from PyQt5.QtWidgets import QDesktopWidget, QApplication

from app.LoggerHandlerFactory import LoggerHandlerFactory
from app.controllers.ImportDatabaseController import ImportDatabaseController
from app.controllers.UpdateDatabaseController import UpdateDatabaseController
from app.tacl.Tacl import Tacl
from app.tacl.TaclRunner import TaclRunner
from app.controllers.GenerateDatabaseController import GenerateDatabaseController
from app.controllers.DifferenceIntersectController import DifferenceIntersectController
from app.controllers.FilterRationaliseController import FilterRationaliseController
from app.controllers.MainController import MainController
from app.controllers.SearchController import SearchController
from app.controllers.SelectDatabaseController import SelectDatabaseController
from app.controllers.SuppliedIntersectController import SuppliedIntersectController
from app.inputValidator.InputValidatorFactory import InputValidatorFactory
from app.repositories.DatabaseRepository import DatabaseRepository
from app.repositories.ResultRepository import ResultRepository
from app.repositories.SettingsRepository import SettingsRepository
from app.views.GenerateDatabaseView import GenerateDatabaseView
from app.views.DialogFactory import DialogFactory
from app.views.DifferenceIntersectView import DifferenceIntersectView
from app.views.FilterRationaliseView import FilterRationaliseView
from app.views.ImportDatabaseView import ImportDatabaseView
from app.views.MainView import MainView
from app.views.SearchView import SearchView
from app.views.SelectDatabaseView import SelectDatabaseView
from app.views.SuppliedIntersectView import SuppliedIntersectView
from app.views.UpdateDatabaseView import UpdateDatabaseView


class Container:
    """
    IoC Container implementation for dependency injection.
    """

    def __init__(self, application: QApplication, connection: Connection):
        self._application = application
        self._connection = connection

        self._instances = {}

    def _get(self, classType: Type, instantiateFunction: Callable):
        """
        Ensures that always the same instance of a given class type is returned.

        :param classType: The class to be instantiated
        :param instantiateFunction:  The function which instantiates the class
        :return: The instantiated class
        """

        className: str = classType.__qualname__
        if className not in self._instances:
            self._instances[className] = instantiateFunction()

        return self._instances[className]

    def logger(self) -> Logger:
        return logging.getLogger("tacl-gui")

    def tacl(self) -> Tacl:
        return self._get(Tacl, lambda: Tacl(
            self.loggerHandlerFactory()
        ))

    def generateDatabaseController(self) -> GenerateDatabaseController:
        return self._get(GenerateDatabaseController, lambda: GenerateDatabaseController(
            self.generateDatabaseView(),
            self.dialogFactory(),
            self.inputValidatorFactory(),
            self.databaseRepository(),
            self.taclRunner()
        ))

    def importDatabaseController(self) -> ImportDatabaseController:
        return self._get(ImportDatabaseController, lambda: ImportDatabaseController(
            self.importDatabaseView(),
            self.dialogFactory(),
            self.inputValidatorFactory(),
            self.databaseRepository()
        ))

    def updateDatabaseController(self) -> UpdateDatabaseController:
        return self._get(UpdateDatabaseController, lambda: UpdateDatabaseController(
            self.updateDatabaseView(),
            self.dialogFactory(),
            self.inputValidatorFactory(),
            self.databaseRepository(),
            self.taclRunner()
        ))

    def generateDatabaseView(self) -> GenerateDatabaseView:
        return self._get(GenerateDatabaseView, lambda: GenerateDatabaseView(
            self.dialogFactory()
        ))

    def importDatabaseView(self) -> ImportDatabaseView:
        return self._get(ImportDatabaseView, lambda: ImportDatabaseView(
            self.dialogFactory()
        ))

    def updateDatabaseView(self) -> UpdateDatabaseView:
        return self._get(UpdateDatabaseView, lambda: UpdateDatabaseView())

    def desktop(self) -> QDesktopWidget:
        return QApplication.desktop()

    def loggerHandlerFactory(self) -> LoggerHandlerFactory:
        return self._get(LoggerHandlerFactory, lambda: LoggerHandlerFactory())

    def dialogFactory(self) -> DialogFactory:
        return self._get(DialogFactory, lambda: DialogFactory(
            self.settingsRepository()
        ))

    def inputValidatorFactory(self) -> InputValidatorFactory:
        return self._get(InputValidatorFactory, lambda: InputValidatorFactory(self.dialogFactory()))

    def qThreadPool(self) -> QThreadPool:
        return QThreadPool.globalInstance()

    def connection(self) -> Connection:
        return self._connection

    def databaseRepository(self) -> DatabaseRepository:
        return self._get(DatabaseRepository, lambda: DatabaseRepository(
            self._connection
        ))

    def mainView(self) -> MainView:
        return self._get(MainView, lambda: MainView(self.desktop()))

    def mainController(self) -> MainController:
        return self._get(MainController, lambda: MainController(
            self.mainView(),
            self.databaseRepository(),
            self.generateDatabaseController(),
            self.importDatabaseController(),
            self.updateDatabaseController(),
            self.differenceIntersectController(),
            self.searchController(),
            self.logger(),
            self.settingsRepository(),
            self.dialogFactory(),
            self.selectDatabaseController(),
            self.suppliedIntersectController(),
            self.filterRationaliseController(),
            self.taclRunner(),
            self.qThreadPool()
        ))

    def settingsRepository(self) -> SettingsRepository:
        return self._get(SettingsRepository, lambda:  SettingsRepository(self._connection))

    def differenceIntersectView(self) -> DifferenceIntersectView:
        return self._get(DifferenceIntersectView, lambda: DifferenceIntersectView(self.dialogFactory()))

    def differenceIntersectController(self) -> DifferenceIntersectController:
        return self._get(DifferenceIntersectController, lambda: DifferenceIntersectController(
            self.differenceIntersectView(),
            self.taclRunner(),
            self.inputValidatorFactory(),
            self.resultRepository(),
            self.dialogFactory()
        ))

    def searchView(self) -> SearchView:
        return self._get(SearchView, lambda: SearchView(self.dialogFactory()))

    def searchController(self) -> SearchController:
        return self._get(SearchController, lambda: SearchController(
            self.searchView(), self.inputValidatorFactory(), self.taclRunner(), self.dialogFactory()
        ))

    def taclRunner(self) -> TaclRunner:
        return self._get(TaclRunner, lambda: TaclRunner(
            self.tacl(),
            self.dialogFactory(),
            self.qThreadPool()
        ))

    def resultRepository(self) -> ResultRepository:
        return self._get(ResultRepository, lambda: ResultRepository(
            self.connection()
        ))

    def selectDatabaseView(self) -> SelectDatabaseView:
        return self._get(SelectDatabaseView, lambda: SelectDatabaseView())

    def selectDatabaseController(self) -> SelectDatabaseController:
        return self._get(SelectDatabaseController, lambda: SelectDatabaseController(
            self.selectDatabaseView(),
            self.databaseRepository(),
            self.logger()
        ))

    def suppliedIntersectView(self) -> SuppliedIntersectView:
        return self._get(SuppliedIntersectView, lambda: SuppliedIntersectView(self.dialogFactory()))

    def suppliedIntersectController(self) -> SuppliedIntersectController:
        return self._get(SuppliedIntersectController, lambda: SuppliedIntersectController(
            self.suppliedIntersectView(),
            self.taclRunner(),
            self.resultRepository(),
            self.dialogFactory(),
            self.differenceIntersectController(),
            self.filterRationaliseController(),
            self.inputValidatorFactory()
        ))

    def filterRationaliseView(self) -> FilterRationaliseView:
        return self._get(FilterRationaliseView, lambda: FilterRationaliseView(self.dialogFactory()))

    def filterRationaliseController(self) -> FilterRationaliseController:
        return self._get(FilterRationaliseController, lambda: FilterRationaliseController(
            self.filterRationaliseView(),
            self.inputValidatorFactory(),
            self.resultRepository(),
            self.taclRunner(),
            self.dialogFactory()
        ))

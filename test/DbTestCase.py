import os
import sqlite3
from collections import Iterable
from sqlite3 import Connection

from test.TaclGuiTestCase import TaclGuiTestCase


class DbTestCase(TaclGuiTestCase):

    def setUp(self, path: str) -> None:
        self._connection = sqlite3.connect(":memory:")
        self._connection.row_factory = sqlite3.Row

        sqlPath = os.path.dirname(os.path.realpath(__file__)) + path
        with open(sqlPath, "r") as databaseSqlFile:
            self._connection.executescript(databaseSqlFile.read())

    def tearDown(self) -> None:
        self._connection.close()

    def getConnection(self) -> Connection:
        return self._connection

    def executeUpdate(self, sql: str, parameters: Iterable = ()):
        cursor = self._connection.cursor()
        cursor.execute(sql, parameters)
        self._connection.commit()
        cursor.close()
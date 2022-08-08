import os
import sqlite3
from collections import Iterable
from sqlite3 import Connection

from test.DbTestCase import DbTestCase
from test.TaclGuiTestCase import TaclGuiTestCase


class TaclDbTestCase(DbTestCase):

    def setUp(self) -> None:
        super().setUp("/../resources/tacl.db.structure.sql")

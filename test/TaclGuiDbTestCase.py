import os
import sqlite3
from collections import Iterable
from sqlite3 import Connection

from test.DbTestCase import DbTestCase
from test.TaclGuiTestCase import TaclGuiTestCase


class TaclGuiDbTestCase(DbTestCase):

    def setUp(self) -> None:
        super(TaclGuiDbTestCase, self).setUp("/../resources/tacl-gui.db.structure.sql")

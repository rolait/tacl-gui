from unittest.mock import Mock

from app.Database import Database
from app.repositories.DatabaseRepository import DatabaseRepository
from app.validatable.CorpusPath import CorpusPath
from app.validatable.DatabaseNGramLengths import DatabaseNGramLengths
from app.validatable.DatabaseName import DatabaseName
from app.validatable.DatabasePath import DatabasePath
from app.validatable.Id import Id
from app.views.DialogFactory import DialogFactory
from test.TaclGuiDbTestCase import TaclGuiDbTestCase


class DatabaseRepositoryTest(TaclGuiDbTestCase):

    def setUp(self) -> None:
        super().setUp()
        self._repo = DatabaseRepository(self.getConnection())

    def test_save_insertsNewDatabase(self):
        db = Database(
            None,
            DatabaseName("Test Database"),
            DatabasePath(self.RESOURCE_DIR + "db/test.db"),
            CorpusPath(self.RESOURCE_DIR + "db/corpus"),
            DatabaseNGramLengths(2, 3)
        )

        id = self._repo.save(db)

        retrievedDb = self._repo.findById(id)
        self._assertDatabasesAreEqual(db, retrievedDb)

    def test_save_updatesExistingDatabase(self):
        self._populateTestDatabases()
        updatedDb = Database(
            Id(1),
            DatabaseName("Updated Test Database"),
            DatabasePath(self.resource("db/test2.db")),
            CorpusPath(self.resource("db/corpus2")),
            DatabaseNGramLengths(3, 4)
        )
        self._repo.save(updatedDb)

        retrievedDb = self._repo.findById(Id(1))
        self.assertEqual(updatedDb.getId().asInt(), retrievedDb.getId().asInt())
        self._assertDatabasesAreEqual(updatedDb, retrievedDb)

    def _assertDatabasesAreEqual(self, db: Database, retrievedDb: Database):
        self.assertEqual(str(db.getName()), str(retrievedDb.getName()))
        self.assertEqual(str(db.getPath()), str(retrievedDb.getPath()))
        self.assertEqual(str(db.getCorpusPath()), str(retrievedDb.getCorpusPath()))
        self.assertEqual(db.getNGramMinLength(), retrievedDb.getNGramMinLength())
        self.assertEqual(db.getNGramMaxLength(), retrievedDb.getNGramMaxLength())

    def test_findAllNames_returnsAllDbsOrderedByName(self):
        self.executeUpdate(
            """
            INSERT INTO databases VALUES
                (1, 'C', '', '', 2, 3),
                (2, 'A', '', '', 2, 4),
                (3, 'B', '', '', 2, 4)
            ;
            """
        )

        dbs = list(self._repo.findAllNames().values())

        self.assertEqual(3, len(dbs))
        self.assertEqual("A", str(dbs[0]))
        self.assertEqual("B", str(dbs[1]))
        self.assertEqual("C", str(dbs[2]))

    def test_findById_findsCorrectDatabaseForGivenId(self):
        self._populateTestDatabases()
        retrievedDb = self._repo.findById(Id(1))
        self.assertEqual(1, retrievedDb.getId().asInt())

    def test_findById_returnsNoneForNotExistingId(self):
        self._populateTestDatabases()
        retrievedDb = self._repo.findById(Id(3))
        self.assertIsNone(retrievedDb)

    def test_existsByName_returnsTrueWhenNameExists(self):
        self._populateTestDatabases()
        result = self._repo.existsByName(DatabaseName("Test Database"))
        self.assertTrue(result)

    def test_existsByName_returnsFalseWhenNameDoesntExists(self):
        self._populateTestDatabases()
        result = self._repo.existsByName(DatabaseName("Not Existing Db"))
        self.assertFalse(result)

    def test_deleteById_deletesSuccesfullyFromDatabase(self):
        self._populateTestDatabases()
        self._repo.deleteById(Id(2))

        self.assertIsNone(self._repo.findById(Id(2)))
        self.assertIsNotNone(self._repo.findById(Id(1)))

    def test_deleteByDatabasePath_deletesSuccesfullyFromDatabase(self):
        self._populateTestDatabases()
        self._repo.deleteByDatabasePath(DatabasePath(self.resource("db/test2.db")))

        self.assertIsNone(self._repo.findById(Id(2)))
        self.assertIsNotNone(self._repo.findById(Id(1)))

    def test_findNameByDatabasePath_findsExistingDatabase(self):
        self._populateTestDatabases()
        existingName = self._repo.findNameByDatabasePath(DatabasePath(self.resource("db/test.db")))
        self.assertEqual("Test Database", existingName)

    def test_findNameByDatabasePath_returnsNoneForNonExistentDatabase(self):
        self._populateTestDatabases()
        nonExistentName = self._repo.findNameByDatabasePath(DatabasePath(self.resource("db/test3.db")))
        self.assertIsNone(nonExistentName)

    def _populateTestDatabases(self):
        self.executeUpdate(
            """
            INSERT INTO databases VALUES
                (1, 'Test Database', ?, ?, 2, 3),
                (2, 'Test Database 2', ?, ?, 2, 4)
            ;
            """,
            (
                self.resource("db/test.db"), self.resource("db/corpus"),
                self.resource("db/test2.db"), self.resource("db/corpus")
            )
        )
from unittest.mock import Mock, MagicMock

from app.Database import Database
from app.ResultType import ResultType
from app.repositories.ResultRepository import ResultRepository
from app.validatable.Id import Id
from app.validatable.ResultPath import ResultPath
from test.TaclGuiDbTestCase import TaclGuiDbTestCase


class ResultRepositoryTest(TaclGuiDbTestCase):

    def setUp(self) -> None:
        super().setUp()
        self._repo = ResultRepository(self.getConnection())

    def test_save_insertsTheResultForNonExistingPath(self):
        database = Mock(spec=Database)
        database.getId = MagicMock(return_value=Id(1))

        resultPath1 = ResultPath(self.resource("db/result1.csv"))
        resultPath2 = ResultPath(self.resource("db/result2.csv"))

        self._repo.save(database, resultPath1, ResultType.DIFFERENCE)
        self._repo.save(database, resultPath2, ResultType.INTERSECT)

        results = self._repo.findTwoMostRecentForSuppliedIntersect(database)

        self.assertEqual(2, len(results))
        self.assertEqual(str(resultPath1), str(results[0]))
        self.assertEqual(str(resultPath2), str(results[1]))

    def test_save_updatesResultIfPathAlreadyExists(self):
        database = Mock(spec=Database)
        database.getId = MagicMock(return_value=Id(1))

        resultPath1 = ResultPath(self.resource("db/result1.csv"))

        self._repo.save(database, resultPath1, ResultType.DIFFERENCE)
        self.assertEqual(1, len(self._repo.findTwoMostRecentForSuppliedIntersect(database)))

        self._repo.save(database, resultPath1, ResultType.INTERSECT)
        self.assertEqual(1, len(self._repo.findTwoMostRecentForSuppliedIntersect(database)))

    def test_findTwoMostRecentForSuppliedIntersect_returnsTwoMostRecentResultsForDatabase(self):
        self._populateData()

        database = Mock(spec=Database)
        database.getId = MagicMock(return_value=Id(1))
        results = self._repo.findTwoMostRecentForSuppliedIntersect(database)

        self.assertEqual(2, len(results))
        self.assertEqual(self.resource("db/result3.csv"), str(results[0]))
        self.assertEqual(self.resource("db/result4.csv"), str(results[1]))

    def test_findTwoMostRecentForSuppliedIntersect_returnsOneResultIfOnlyOneResultExistent(self):
        self._populateData()

        database = Mock(spec=Database)
        database.getId = MagicMock(return_value=Id(2))
        results = self._repo.findTwoMostRecentForSuppliedIntersect(database)

        self.assertEqual(1, len(results))
        self.assertEqual(self.resource("db/result5.csv"), str(results[0]))

    def _populateData(self) -> None:
        self.executeUpdate(
            """
            INSERT INTO results VALUES 
                (1,  1, ?, 'difference', '2020-09-21 00:00:00'),
                (2,  1, '/some/notExistentPath.csv', 'difference', '2020-09-22 00:00:00'),
                (3,  1, ?, 'intersect', '2020-09-23 00:00:00'),
                (4,  1, ?, 'intersect', '2020-09-22 00:00:00'),
                (5,  2, ?, 'difference', '2020-09-21 00:00:00'),
                (6,  2, '/some/other/notExistentPath.csv', 'intersect', '2020-09-22 00:00:00')
            ;
            """,
            (
                self.resource("db/result1.csv"),
                self.resource("db/result3.csv"),
                self.resource("db/result4.csv"),
                self.resource("db/result5.csv"),
            )
        )
from unittest.mock import Mock, MagicMock, patch

from app.Database import Database
from app.tacl.TaclDatabase import TaclDatabase
from app.validatable.CorpusPath import CorpusPath
from app.validatable.DatabasePath import DatabasePath
from test.TaclDbTestCase import TaclDbTestCase


# noinspection SpellCheckingInspection
@patch("app.validatable.WritableFilePath.tr", side_effect=lambda text: text)
class TaclDatabaseTest(TaclDbTestCase):

    def setUp(self) -> None:
        super().setUp()
        databasePath = Mock(spec=DatabasePath)
        self._corpusPath = CorpusPath(self.RESOURCE_DIR + 'DatabaseTest/corpus')
        self._corpusPath2 = CorpusPath(self.RESOURCE_DIR + 'DatabaseTest/corpus2')
        self._database = TaclDatabase(databasePath)
        self._database.connect = MagicMock(return_value=self._connection)

    def test_extractNgramLengths_returnsCorrectNgramsLength(self, tr):
        self.executeUpdate(
            """
            INSERT INTO Text VALUES  (1, 'work1', 'witness1', 'ac6c8a90da885e84d0fd3bf72078ede3', 1, '');
            """
        )
        self.executeUpdate(
            """
            INSERT INTO TextHasNGram VALUES 
                (1, 2, 1),
                (1, 2, 1),
                (1, 3, 1),
                (1, 3, 1),
                (1, 4, 1),
                (1, 4, 1)
            ;
            """
        )

        ngrams = self._database.extractNgramLengths()
        self.assertEqual(2, ngrams.getMinLength())
        self.assertEqual(4, ngrams.getMaxLength())

    def test_createWitnessReport_returnsEmptyReport(self, tr):
        self._insertWitnesses()
        report = self._database.createWitnessReport(self._corpusPath)
        self.assertFalse(report.hasMissingWitnesses())
        self.assertFalse(report.hasChangedOrAddedWitnesses())

    def test_createWitnessReport_returnReportOfNewlyAddedWorkAndWittness(self, tr):
        self._insertWitnesses()
        report = self._database.createWitnessReport(self._corpusPath2)
        self.assertFalse(report.hasMissingWitnesses())
        self.assertTrue(report.hasChangedOrAddedWitnesses())

        self.assertEqual(
            "=== New Witnesses (1)===\n"
            "work3/witness5",

            report.createReportText()
        )

    def _insertWitnesses(self):
        self.executeUpdate(
            """
            INSERT INTO Text VALUES 
                (1, 'work1', 'witness1', 'ac6c8a90da885e84d0fd3bf72078ede3', 1, ''),
                (2, 'work1', 'witness2', 'd41d8cd98f00b204e9800998ecf8427e', 1, ''),
                (3, 'work2', 'witness3', '11c3af454e0818487eca60812fdf60ff', 1, ''),
                (4, 'work2', 'witness4', 'e2216d95bc2d3ffe2b766e48067b7699', 1, '')
            ;
            """
        )

    def test_createWitnessReport_returnsMissingAndChangedWorkList(self, tr):
        self.executeUpdate(
            """
            INSERT INTO Text VALUES 
                (1, 'work1', 'witness1', 'ac6c8a90da885e84d0fd3bf72078ede3', 1, ''),
                (2, 'work1', 'witness2', 'witness2', 1, ''),
                (4, 'work2', 'witness4', 'witness4', 1, ''),
                
                (5, 'work1', 'witness5', 'witness5', 1, ''),
                (6, 'work3', 'witness6', 'witness6', 1, '')
            ;
            """
        )

        report = self._database.createWitnessReport(self._corpusPath)
        self.assertTrue(report.hasMissingWitnesses())
        self.assertTrue(report.hasChangedOrAddedWitnesses())

        self.assertEqual(
            "=== Missing Witnesses (2)===\n"
            "work1/witness5\n"
            "work3/witness6\n"
            "\n"
            "=== Changed Witnesses (2)===\n"
            "work1/witness2\n"
            "work2/witness4\n"
            "\n"
            "=== New Witnesses (1)===\n"
            "work2/witness3",

            report.createReportText()
        )

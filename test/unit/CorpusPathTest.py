import os
from unittest.mock import patch

from app.inputValidator.ValidationError import ValidationError
from app.validatable.CorpusPath import CorpusPath
from test.TaclGuiTestCase import TaclGuiTestCase


@patch("app.validatable.CataloguePath.tr", side_effect = lambda text: text)
class CorpusPathTest(TaclGuiTestCase):

    def test_init_throwsValidationErrorWhenCorpusPathIsEmpty(self, tr):
        self.assertRaises(ValidationError, lambda: CorpusPath(self.RESOURCE_DIR + "CorpusPath/emptyDir"))

    def test_init_returnsObjectWhenCorpusPathIsValid(self, tr):
        path = os.path.abspath(self.RESOURCE_DIR + "CorpusPathTest/corpus")
        corpusPath = CorpusPath(path)

        self.assertEqual(path, str(corpusPath))
        self.assertEqual(2, corpusPath.getWorkCount())

    def test_createBaseCatalogueFile_returnsValidBaseCatalogueFile(self, tr):
        path = os.path.abspath(self.RESOURCE_DIR + "CorpusPathTest/corpus")
        object = CorpusPath(path)

        with object.createBaseCatalogueFile() as file:
            lines = open(file.name).readlines()

        self.assertEqual(2, len(lines))
        self.assertEqual('work1 ' + CorpusPath.DEFAULT_LABEL + '\n', lines[0])
        self.assertEqual('work2 ' + CorpusPath.DEFAULT_LABEL + '\n', lines[1])




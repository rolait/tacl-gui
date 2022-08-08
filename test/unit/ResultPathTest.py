import os
from unittest.mock import patch

from app.inputValidator.ValidationError import ValidationError
from app.validatable.CorpusPath import CorpusPath
from app.validatable.ResultPath import ResultPath
from test.TaclGuiTestCase import TaclGuiTestCase


@patch("app.validatable.CataloguePath.tr", side_effect = lambda text: text)
class CorpusPathTest(TaclGuiTestCase):

    def test_toDataFrame_createsDataFrameObject(self, tr):
        resulPath = ResultPath(self.resource("ResultPathTest/intersect.csv"))
        dataFrame = resulPath.toDataFrame()
        sample = dataFrame.iloc[0]

        self.assertEqual(sample["ngram"], "一三")
        self.assertEqual(sample["label"], "test1")





from app.validatable.OutputCSVPath import OutputCSVPath
from test.TaclGuiTestCase import TaclGuiTestCase


class OutputCSVPathTest(TaclGuiTestCase):

    def test_init_keepsPathIfCsvEndingExists(self):
        self.assertEqual("/test/file.csv", str(OutputCSVPath("/test/file.csv")))
        self.assertEqual("/test/file.CsV", str(OutputCSVPath("/test/file.CsV")))

    def test_init_addsCSVToFileEndIfNotExistent(self):
        self.assertEqual("/test/file.csv", str(OutputCSVPath("/test/file")))

import os
from unittest import TestCase


class TaclGuiTestCase(TestCase):
    RESOURCE_DIR = os.path.dirname(os.path.realpath(__file__)) + "/resources/"

    def resource(self, resource: str) -> str:
        return self.RESOURCE_DIR + resource
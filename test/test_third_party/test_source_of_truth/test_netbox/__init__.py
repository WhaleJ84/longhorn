from src.longhorn.third_party.source_of_truth.netbox.netbox_functions import Netbox
from test import LonghornTestCase


class NetboxTestCase(LonghornTestCase):
    def setUp(self) -> None:
        self.netbox = Netbox()

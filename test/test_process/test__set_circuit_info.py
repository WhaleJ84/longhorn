from . import ProcessFunctionsTestCase


class SetCircuitInfoTestCase(ProcessFunctionsTestCase):
    def test_set_circuit_info_sets_link_type_correctly(self):
        self.process._set_circuit_info()
        self.assertEqual(
            self.process.link_type,
            "TRANSIT",
        )

    def test_set_circuit_info_sets_side_a_correctly(self):
        self.process._set_circuit_info()
        self.assertEqual(
            self.process.side_a,
            "LON",
        )

    def test_set_circuit_info_sets_side_z_correctly(self):
        self.process._set_circuit_info()
        self.assertEqual(
            self.process.side_z,
            "CAR",
        )

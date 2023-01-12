import unittest

from database.test_db import TestDB
from io_tools.load import load_patient_folder
from omics.omic_generator import OmicsGenerator


class TestOmicsGenerator(unittest.TestCase):
    def setUp(self) -> None:
        self.db_tests = TestDB()
        self.db_tests.setUp()
        self.db = self.db_tests.db
        self.omics_generator = OmicsGenerator(self.db)

    def tearDown(self) -> None:
        self.db_tests.tearDown()

    def test_generate_pyradiomics(self):
        load_patient_folder(self.db, "input")
        self.omics_generator.run_pyradiomics()

    def test_z_boundaries(self):
        load_patient_folder(self.db, "input")
        self.omics_generator.run_z_boundaries()

    def test_avoid_redundant_omic_run(self):
        load_patient_folder(self.db, "input")

        # Now all should run (len != 0)
        self.assertNotEqual(0, len(list(self.omics_generator.run_pyradiomics())))
        self.assertNotEqual(0, len(list(self.omics_generator.run_z_boundaries())))

        # Upon rerun none should run (len == 0)
        self.assertEqual(0, len(list(self.omics_generator.run_pyradiomics())))
        self.assertEqual(0, len(list(self.omics_generator.run_z_boundaries())))

if __name__ == '__main__':
    unittest.main()

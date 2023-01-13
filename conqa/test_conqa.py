import logging
import unittest

from conqa.client import Conqa

logging.basicConfig(encoding='utf-8', level=logging.DEBUG)

class TestConQAClient(unittest.TestCase):
    def setUp(self) -> None:
        self.client = Conqa(database_path=None, threads=8)

    def test_generate_pyradiomics(self):
        self.client.load_nifti_folder_to_db("input")
        self.client.run_pyradiomics()

    def test_z_boundaries(self):
        self.client.load_nifti_folder_to_db("input")
        self.client.run_z_boundaries()

    def test_avoid_redundant_omic_run(self):
        self.client.load_nifti_folder_to_db("input")
        # Now all should run (len != 0)
        self.assertNotEqual(0, len(list(self.client.run_pyradiomics())))
        self.assertNotEqual(0, len(list(self.client.run_z_boundaries())))

        # Upon rerun none should run (len == 0)
        self.assertEqual(0, len(list(self.client.run_pyradiomics())))
        self.assertEqual(0, len(list(self.client.run_z_boundaries())))


if __name__ == '__main__':
    unittest.main()

import unittest

from database.db_models import NiftiImage, NiftiStructure
from database.test_db import TestDB
from omics.functions.pyradiomics import generate_pyradiomics


class TestPyradiomics(unittest.TestCase):
    def setUp(self) -> None:
        self.db_tests = TestDB()
        self.db_tests.setUp()
        self.db = self.db_tests.db
        
    def tearDown(self) -> None:
        self.db_tests.tearDown()
        
    def test_generate_pyradiomics(self):
        img = self.db.add_nifti_image("input/0Zvl0Wg21eEl7An70zvMLrKST&20190214&CT.nii.gz")
        structure = self.db.add_nifti_structure(path="input/0Zvl0Wg21eEl7An70zvMLrKST&20190214&Brain.nii.gz",
                                                nifti_image_id=img.id,
                                                label_int=255,
                                                name="Brain")

        omics = generate_pyradiomics(structure)
        [print(omic) for omic in omics]
        for omic in omics:
            self.assertListEqual(["nifti_structure_id", "name", "value", "omic_package"], list(omic.keys()))
            print(omic)



if __name__ == '__main__':
    unittest.main()

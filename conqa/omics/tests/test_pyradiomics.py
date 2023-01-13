import logging
import unittest

from conqa.omics.pyradiomics import batch_generate_pyradiomics
from database.db import DB

logging.basicConfig(encoding='utf-8', level=logging.DEBUG)


class TestPyradiomics(unittest.TestCase):
    def setUp(self, db=None) -> None:
        self.db = DB()

    def test_generate_pyradiomics(self):
        img = self.db.add_nifti_image("input/1koskEvGaSUB9v2z8D6JZYALM/20190227/image.nii.gz")
        structure = self.db.add_nifti_structure(path="input/1koskEvGaSUB9v2z8D6JZYALM/20190227/mask_PCM_Mid.nii.gz",
                                                nifti_image_id=img.id,
                                                label_int=255,
                                                name="PCM_Mid")

        omics = batch_generate_pyradiomics(db=self.db, structures_iterable=[structure], threads=8)
        for omic in omics:
            self.assertIn("nifti_structure_id", list(omic.__dict__.keys()))
            self.assertIn("name", list(omic.__dict__.keys()))
            self.assertIn("_value", list(omic.__dict__.keys()))
            self.assertIn("omic_package", list(omic.__dict__.keys()))

if __name__ == '__main__':
    unittest.main()

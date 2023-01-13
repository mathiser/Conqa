import logging
import unittest

from conqa.omics.z_boundaries import batch_find_contour_z_boundaries
from database.db import DB

logging.basicConfig(encoding='utf-8', level=logging.DEBUG)


class TestZBoundaries(unittest.TestCase):
    def setUp(self) -> None:
        self.db = DB()

    def test_find_contour_z_boundaries(self):
        image = self.db.add_nifti_image(path="input/1koskEvGaSUB9v2z8D6JZYALM/20190227/image.nii.gz")
        structure = self.db.add_nifti_structure(
                                   nifti_image_id=image.id,
                                   path="input/1koskEvGaSUB9v2z8D6JZYALM/20190227/mask_PCM_Mid.nii.gz",
                                   name="PCM_Mid")

        omics = batch_find_contour_z_boundaries(db=self.db, structures_iterable=[structure], threads=8)
        for omic in omics:
            self.assertIn("nifti_structure_id", list(omic.__dict__.keys()))
            self.assertIn("name", list(omic.__dict__.keys()))
            self.assertIn("_value", list(omic.__dict__.keys()))
            self.assertIn("omic_package", list(omic.__dict__.keys()))

if __name__ == '__main__':
    unittest.main()

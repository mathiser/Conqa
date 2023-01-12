import secrets
import unittest

from database.db_models import NiftiStructure, NiftiImage
from omics.functions.z_boundaries import find_contour_z_boundaries


class TestPyradiomics(unittest.TestCase):
    def test_find_contour_z_boundaries(self):
        image = NiftiImage(id=1, path="input/0Zvl0Wg21eEl7An70zvMLrKST&20190214&CT.nii.gz")
        structure = NiftiStructure(id=1,
                                   nifti_image=image,
                                   path="input/0Zvl0Wg21eEl7An70zvMLrKST&20190214&Submandibular_L.nii.gz",
                                   name="Submandibular_L")

        omics = find_contour_z_boundaries(structure=structure)
        for omic in omics:
            self.assertListEqual(["nifti_structure_id", "name", "value", "omic_package"], list(omic.keys()))


if __name__ == '__main__':
    unittest.main()

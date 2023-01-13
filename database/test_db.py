import logging
import random
import secrets
import unittest

import numpy as np

from database.db import DB
from database.db_models import NiftiStructure

logging.basicConfig(encoding='utf-8', level=logging.DEBUG)

def get_dummy_nifti_image_kwargs():
    return {"path": "/some/path/to/an/image"}


def get_dummy_nifti_structure_kwargs(nifti_image_id):
    return {"path": secrets.token_urlsafe(4),
            "name": secrets.token_urlsafe(4),
            "nifti_image_id": nifti_image_id}


def get_dummy_omic_kwarg_int(nifti_structure_id):
    return {
        "name": secrets.token_urlsafe(4),
        "value": random.randint(1, 100000),
        "nifti_structure_id": nifti_structure_id,
        "omic_package": "test_package"}


def get_dummy_omic_kwarg_float(nifti_structure_id):
    return {
        "name": secrets.token_urlsafe(4),
        "value": random.randint(1, 100000) / 666,
        "nifti_structure_id": nifti_structure_id,
        "omic_package": "test_package"}


def get_dummy_omic_kwarg_string(nifti_structure_id):
    return {
        "name": secrets.token_urlsafe(4),
        "value": str(random.randint(1, 100000)),
        "nifti_structure_id": nifti_structure_id,
        "omic_package": "test_package"}


def get_dummy_omic_kwarg_list(nifti_structure_id):
    return {
        "name": secrets.token_urlsafe(4),
        "value": list([random.randint(1, 100000) for n in range(random.randint(1, 10000))]),
        "nifti_structure_id": nifti_structure_id,
        "omic_package": "test_package"}


def get_dummy_omic_kwarg_array(nifti_structure_id):
    return {
        "name": secrets.token_urlsafe(4),
        "value": np.arange(random.randint(1, 10000)),
        "nifti_structure_id": nifti_structure_id,
        "omic_package": "test_package"}


class TestDB(unittest.TestCase):
    def setUp(self) -> None:
        self.db = DB()

    def test_add_nifti_image(self):
        img = self.db.add_nifti_image(**get_dummy_nifti_image_kwargs())
        echo_img = self.db.get_nifti_image_by_kwargs({"id": img.id})
        self.assertEqual(img.id, echo_img.id)

    def test_get_nifti_images(self):
        img0 = self.db.add_nifti_image(**get_dummy_nifti_image_kwargs())
        img1 = self.db.add_nifti_image(**get_dummy_nifti_image_kwargs())
        imgs = self.db.get_nifti_images()
        self.assertEqual(img0.id, imgs[0].id)
        self.assertEqual(img1.id, imgs[1].id)

    def test_add_nifti_structure(self):
        img = self.db.add_nifti_image(**get_dummy_nifti_image_kwargs())
        structure = self.db.add_nifti_structure(**get_dummy_nifti_structure_kwargs(img.id))
        self.assertEqual(img.id, structure.nifti_image_id)

    def test_add_multiple_nifti_structures(self):
        img = self.db.add_nifti_image(**get_dummy_nifti_image_kwargs())
        structures = list([self.db.add_nifti_structure(**get_dummy_nifti_structure_kwargs(img.id)) for i in range(10)])
        echo_structures = self.db.get_nifti_structures()
        for i, echo_struct in enumerate(echo_structures):
            self.assertEqual(structures[i].id, echo_struct.id)

        echo_img = self.db.get_nifti_image_by_kwargs({"id": img.id})
        for i, echo_struct in enumerate(echo_img.nifti_structures):
            self.assertEqual(structures[i].id, echo_struct.id)

    def test_get_nifti_structure_by_kwargs(self):
        img = self.db.add_nifti_image(**get_dummy_nifti_image_kwargs())
        structures = list([self.db.add_nifti_structure(**get_dummy_nifti_structure_kwargs(img.id)) for i in range(10)])
        echo_structures = self.db.get_nifti_structures_by_kwargs({"nifti_image_id": img.id})

        for i, echo_struct in enumerate(structures):
            self.assertEqual(echo_structures[i].id, echo_struct.id)

    def test_add_omic_int(self):
        img = self.db.add_nifti_image(**get_dummy_nifti_image_kwargs())
        structure = self.db.add_nifti_structure(**get_dummy_nifti_structure_kwargs(img.id))
        for u in range(10):
            self.db.add_omic(**get_dummy_omic_kwarg_int(nifti_structure_id=structure.id))

        echo_structure = self.db.get_nifti_structures_by_kwargs({"id": structure.id})[0]
        for omic in echo_structure.omics:
            self.assertIsInstance(omic.value, int)

    def test_add_omic_float(self):
        img = self.db.add_nifti_image(**get_dummy_nifti_image_kwargs())
        structure = self.db.add_nifti_structure(**get_dummy_nifti_structure_kwargs(img.id))
        for u in range(10):
            self.db.add_omic(**get_dummy_omic_kwarg_float(nifti_structure_id=structure.id))

        echo_structure = self.db.get_nifti_structures_by_kwargs({"id": structure.id})[0]
        for omic in echo_structure.omics:
            self.assertIsInstance(omic.value, float)

    def test_add_omic_list(self):
        img = self.db.add_nifti_image(**get_dummy_nifti_image_kwargs())
        structure = self.db.add_nifti_structure(**get_dummy_nifti_structure_kwargs(img.id))
        for u in range(10):
            self.db.add_omic(**get_dummy_omic_kwarg_list(nifti_structure_id=structure.id))

        echo_structure = self.db.get_nifti_structures_by_kwargs({"id": structure.id})[0]
        for omic in echo_structure.omics:
            self.assertIsInstance(omic.value, list)

    def test_add_omic_array(self):
        img = self.db.add_nifti_image(**get_dummy_nifti_image_kwargs())
        structure = self.db.add_nifti_structure(**get_dummy_nifti_structure_kwargs(img.id))
        for u in range(10):
            self.db.add_omic(**get_dummy_omic_kwarg_array(nifti_structure_id=structure.id))

        echo_structure = self.db.get_nifti_structures_by_kwargs({"id": structure.id})[0]
        for omic in echo_structure.omics:
            self.assertIsInstance(omic.value, list)

    def test_load_default_base_names(self):
        self.db = DB(database_path=None, default_base_names_json=True)
        for i in self.db.get_structure_base_names():
            self.assertIsNotNone(i)

    def test_try_add_structure_base_name_association(self):
        self.db = DB(database_path=None, default_base_names_json=False)

        img = self.db.add_nifti_image("/some/path")
        bn = self.db.add_structure_base_name("GTVt")
        synonyms = ["gtvt", "gtv-t", "gtv_t", "GTV_t"]
        for s in synonyms:
            self.db.add_structure_synonym_name(bn.id, s)

        for s in synonyms:
            structure = self.db.add_nifti_structure(path="/some/path/",
                                                    name=s,
                                                    nifti_image_id=img.id)

            structure = self.db.get_nifti_structures_by_kwargs({"id": structure.id})[0]
            print(structure.__dict__)
            self.assertEqual("GTVt", structure.structure_base_name.name)

if __name__ == '__main__':
    unittest.main()

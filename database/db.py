import json
from typing import Union, Any, List

import numpy as np
import pandas as pd
import sqlalchemy
from sqlalchemy.orm import sessionmaker, scoped_session

from database.db_interface import DBInterface
from database.db_models import Base, NiftiImage, NiftiStructure, Omic


class DB(DBInterface):
    def __init__(self, database_url=None):
        if not database_url:
            database_url = f'sqlite://'  ## Make an in memory DB

        engine = sqlalchemy.create_engine(database_url, future=True)
        Base.metadata.create_all(engine)

        session_maker = sessionmaker(bind=engine, expire_on_commit=False)
        self.Session = scoped_session(session_factory=session_maker)

    def get_nifti_images(self) -> List[NiftiImage]:
        with self.Session() as session:
            return session.query(NiftiImage).all()

    def get_nifti_image_by_kwargs(self, kwargs) -> NiftiImage:
        with self.Session() as session:
            return session.query(NiftiImage).filter_by(**kwargs).first()

    def get_nifti_structures(self) -> List[NiftiStructure]:
        with self.Session() as session:
            return session.query(NiftiStructure).all()

    def get_nifti_structures_by_kwargs(self, kwargs) -> NiftiStructure:
        with self.Session() as session:
            return session.query(NiftiStructure).filter_by(**kwargs).all()

    def add_nifti_image(self,
                        path) -> NiftiImage:
        img = NiftiImage(path=path)
        return self.add_generic(img)

    def add_nifti_structure(self,
                            path: str,
                            name: str,
                            nifti_image_id: int,
                            label_int: Union[int, None] = None) -> NiftiStructure:
        struct = NiftiStructure(path=path,
                                name=name,
                                nifti_image_id=nifti_image_id,
                                label_int=label_int)
        return self.add_generic(struct)

    def add_omic(self,
                 nifti_structure_id: int,
                 name: str,
                 value: Any,
                 omic_package: str) -> Omic:

        assert type(value) in [int, float, str, np.ndarray, tuple, list]

        if isinstance(value, np.ndarray):
            value = list([int(i) for i in value])

        try:  # Check if json serializable
            value = json.dumps(value)
        except TypeError as e:
            print(f"{value}: {e}")
            raise e

        o = Omic(name=name,
                 nifti_structure_id=nifti_structure_id,
                 _value=value,
                 omic_package=omic_package)

        return self.add_generic(o)

    def add_generic(self, obj):
        with self.Session() as session:
            session.add(obj)
            session.commit()
            session.refresh(obj)
            return obj

    def generate_omics_report(self):
        structures = self.get_nifti_structures()
        d = {}
        for structure in structures:
            d[structure.id] = {
                "image_path": structure.nifti_image.path,
                "structure_path": structure.path,
                "structure_name": structure.name
            }
            for omic in structure.omics:
                d[omic.name] = omic.value
        return pd.DataFrame


    def get_label_names(self):
        return {"image",
                "brain",
                "brainstem",
                "mandible",
                "parotid_l",
                "parotid_r",
                "submandibular_l",
                "submandibular_r",
                "pcm_up",
                "pcm_mid",
                "pcm_low",
                "thyroid"
                "spinalcord"
                "esophagus"
                }

    def get_synonym_dictionary(self):
        return {
            "CT.nii.gz": "image",
            "Brain.nii.gz": "brain",
            "Brainstem.nii.gz": "brainstem",
            "SpinalCord.nii.gz": "spinalcord",
            "Mandible.nii.gz": "mandible",
            "Parotid_L.nii.gz": "parotid_l",
            "Parotid_R.nii.gz": "parotid_r",
            "Submandibular_L.nii.gz": "submandibular_l",
            "Submandibular_R.nii.gz": "submandibular_r",
            "PCM_Up.nii.gz": "pcm_up",
            "PCM_Mid.nii.gz": "pcm_mid",
            "PCM_Low.nii.gz": "pcm_low",
            "Thyroid.nii.gz": "thyroid",
            "Esophagus.nii.gz": "esophagus"
        }

    def get_volume_number_constraint(self):
        return {
            "brain": 1,
            "brainstem": 1,
            "spinalcord": 1,
            "mandible": 1,
            "parotid_l": 1,
            "parotid_r": 1,
            "submandibular_l": 1,
            "submandibular_r": 1,
            "pcm_up": 1,
            "pcm_mid": 1,
            "pcm_low": 1,
            "thyroid": 2,
            "esophagus": 1
        }

    def get_adjacency_constraint(self):
        return [
            ("esophagus", "pcm_low"),
            ("pcm_low", "pcm_mid"),
            ("pcm_mid", "pcm_up"),
            ("spinalcord", "brainstem"),
            ("larynx_g", "larynx_sg")
        ]

    def get_paired_structures(self):
        return [
            ("parotid_r", "parotid_l"),
            ("submandibular_r", "submandibular_l")
        ]

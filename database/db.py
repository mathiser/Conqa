import datetime
import json
from typing import Union, Any, List

import numpy as np
import sqlalchemy
from sqlalchemy.orm import sessionmaker, scoped_session

from database.db_interface import DBInterface
from database.db_models import Base, NiftiImage, NiftiStructure, Omic, StructureBaseName, StructureSynonymName, \
    StructureBaseNameAssociation


class DB(DBInterface):
    def __init__(self, database_path=None, default_base_names_json=True):
        if database_path:
            self.database_path = f'sqlite:///' + database_path
        else:
            self.database_path = f'sqlite://'  # Make an in memory DB

        engine = sqlalchemy.create_engine(self.database_path, future=True)
        Base.metadata.create_all(engine)

        session_maker = sessionmaker(bind=engine, expire_on_commit=False)
        self.Session = scoped_session(session_factory=session_maker)

        if isinstance(default_base_names_json, str):
            self.load_default_base_names(default_base_names_json)
        elif isinstance(default_base_names_json, bool):
            if default_base_names_json:
                self.load_default_base_names("resources/default_base_names.json")

    def load_default_base_names(self, default_base_names_json):
        with open(default_base_names_json, "r") as r:
            base_names = json.loads(r.read())
        for base_name in base_names:
            try:
                self.add_structure_base_name(base_name)
            except Exception as e:
                print(e)

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
                        path: str,
                        scan_date: Union[datetime.datetime, None] = None,
                        patient_id: Union[str, None] = None) -> NiftiImage:
        img = NiftiImage(path=path,
                         scan_date=scan_date,
                         patient_id=patient_id)
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
        struct = self.add_generic(struct)

        self.try_add_structure_base_name_association(struct)

        return struct

    def add_omic(self,
                 nifti_structure_id: int,
                 name: str,
                 value: Any,
                 omic_package: str) -> Omic:

        if isinstance(value, np.ndarray):
            if value.shape == ():
                value = ""
            else:
                try:
                    value = list([float(i) for i in value])
                except Exception as e:
                    print(type(value), value)
                    print(e)

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

    def get_structure_base_names(self):
        with self.Session() as session:
            return session.query(StructureBaseName).all()

    def get_structure_synonym_names(self):
        with self.Session() as session:
            return session.query(StructureSynonymName).all()

    def add_structure_synonym_name(self,
                                   structure_base_name_id: id,
                                   name: str):
        with self.Session() as session:
            if not session.query(StructureSynonymName).filter_by(name=name).first():
                sn = StructureSynonymName(structure_base_name_id=structure_base_name_id,
                                          name=name)

                return self.add_generic(sn)

    def add_structure_base_name(self, name: str):
        with self.Session() as session:
            if not session.query(StructureBaseName).filter_by(name=name).first():
                bn = StructureBaseName(name=name)
                bn = self.add_generic(bn)
            else:
                return None
            if not session.query(StructureSynonymName).filter_by(name=name).first():

                sn = StructureSynonymName(structure_base_name_id=bn.id,
                                          name=name)
                sn = self.add_generic(sn)
        return bn

    def add_structure_base_name_association(self,
                                            structure_base_name_id: int,
                                            nifti_structure_id: int):
        with self.Session() as session:
            if not session.query(StructureBaseNameAssociation).filter_by(nifti_structure_id=nifti_structure_id).first():
                bn = StructureBaseNameAssociation(structure_base_name_id=structure_base_name_id,
                                                  nifti_structure_id=nifti_structure_id)
                return self.add_generic(bn)

    def try_add_structure_base_name_association(self, structure: NiftiStructure):
        synonyms = self.get_structure_synonym_names()
        for synonym in synonyms:
            # Match synonym directly
            if structure.name == synonym.name:
                return self.add_structure_base_name_association(nifti_structure_id=structure.id,
                                                                structure_base_name_id=synonym.structure_base_name_id)

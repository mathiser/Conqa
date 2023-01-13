import datetime
import json

import SimpleITK as sitk
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class NiftiImage(Base):
    __tablename__ = "nifti_images"
    id = Column(Integer, unique=True, primary_key=True, autoincrement=True)
    path = Column(String)

    nifti_structures = relationship("NiftiStructure", lazy="subquery", back_populates="nifti_image")

    scan_date = Column(DateTime, default=datetime.datetime.now)
    patient_id = Column(String, default="111111-1111")

    _image = None
    _array = None

    def as_image(self):
        if not self._image:
            self._image = sitk.ReadImage(self.path)
        return self._image

    def as_array(self):
        if not self._array:
            self._array = sitk.GetArrayFromImage(self.as_image())
        return self._array


class NiftiStructure(Base):
    __tablename__ = "nifti_structures"

    id = Column(Integer, unique=True, primary_key=True, autoincrement=True)

    # Base name
    _structure_base_name_association = relationship("StructureBaseNameAssociation", lazy="subquery", uselist=False)

    nifti_image_id = Column(Integer, ForeignKey('nifti_images.id'))
    nifti_image = relationship("NiftiImage", lazy="joined", back_populates="nifti_structures", uselist=False)
    omics = relationship("Omic", lazy="joined")

    path = Column(String)
    name = Column(String)
    label_int = Column(Integer, default=255)

    _image = None
    _array = None

    def as_image(self):
        if not self._image:
            self._image = sitk.ReadImage(self.path)
        return self._image

    def as_array(self):
        if not self._array:
            self._array = sitk.GetArrayFromImage(self.as_image())
        return self._array

    @property
    def structure_base_name(self):
        if self._structure_base_name_association:
            return self._structure_base_name_association.structure_base_name

    @property
    def omic_features(self):
        return list([omic.name for omic in self.omics])

    @property
    def executed_omic_packages(self):
        return [omic.omic_package for omic in self.omics]


class Omic(Base):
    __tablename__ = "omics"
    id = Column(Integer, unique=True, primary_key=True, autoincrement=True)
    nifti_structure_id = Column(Integer, ForeignKey('nifti_structures.id'))
    name = Column(String)
    _value = Column(String)
    omic_package = Column(String)

    @property
    def value(self):
        return json.loads(self._value)


class StructureBaseName(Base):
    __tablename__ = "structure_base_names"
    id = Column(Integer, unique=True, primary_key=True, autoincrement=True)
    name = Column(String, unique=True)
    structure_synonym_names = relationship("StructureSynonymName", lazy="subquery",
                                           back_populates="structure_base_name")


class StructureSynonymName(Base):
    __tablename__ = "structure_synonym_names"
    id = Column(Integer, unique=True, primary_key=True, autoincrement=True)
    structure_base_name_id = Column(Integer, ForeignKey("structure_base_names.id"))
    structure_base_name = relationship("StructureBaseName", lazy="joined", back_populates="structure_synonym_names",
                                       uselist=False)
    name = Column(String, unique=True)


class StructureBaseNameAssociation(Base):
    __tablename__ = "structure_synonym_names_associations"
    id = Column(Integer, unique=True, primary_key=True, autoincrement=True)
    structure_base_name_id = Column(Integer, ForeignKey("structure_base_names.id"))
    structure_base_name = relationship("StructureBaseName", lazy="subquery", uselist=False)

    nifti_structure_id = Column(Integer, ForeignKey("nifti_structures.id"), unique=True)

from abc import abstractmethod
from datetime import datetime
from typing import Any, Union, List

from database.db_models import NiftiImage, StructureBaseName, NiftiStructure, Omic


class DBInterface:
    @abstractmethod
    def get_synonym_dictionary(self):
        pass

    @abstractmethod
    def get_volume_number_constraint(self):
        pass

    @abstractmethod
    def get_label_names(self):
        pass

    @abstractmethod
    def get_nifti_images(self) -> List[NiftiImage]:
        pass

    @abstractmethod
    def get_image_by_kwargs(self, kwargs):
        pass

    @abstractmethod
    def add_nifti_image(self,
                        path: str,
                        scan_date: Union[datetime, None] = None,
                        patient_id: Union[str, None] = None) -> NiftiImage:
        pass

    @abstractmethod
    def add_nifti_structure(self, name, path, nifti_image_id) -> NiftiStructure:
        pass

    @abstractmethod
    def add_omic(self,
                 nifti_structure_id: int,
                 name: str,
                 value: Any,
                 omic_package: str) -> Omic:
        pass

    @abstractmethod
    def get_nifti_structures(self) -> List[NiftiStructure]:
        pass

    @abstractmethod
    def get_structure_base_names(self) -> List[StructureBaseName]:
        pass

    @abstractmethod
    def get_structure_synonym_names(self):
        pass

    @abstractmethod
    def add_structure_base_name(self, name: str):
        pass

    @abstractmethod
    def add_structure_synonym_name(self,
                                   structure_base_name_id: id,
                                   name: str):
        pass

    @abstractmethod
    def add_structure_base_name_association(self,
                                            structure_base_name_id: int,
                                            nifti_structure_id: int):
        pass

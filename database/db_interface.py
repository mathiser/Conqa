from abc import abstractmethod
from typing import Any


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
    def get_nifti_images(self):
        pass

    @abstractmethod
    def get_image_by_kwargs(self, kwargs):
        pass

    @abstractmethod
    def add_nifti_image(self, img_path):
        pass

    @abstractmethod
    def add_nifti_structure(self, name, path, nifti_image_id):
        pass

    @abstractmethod
    def add_omic(self,
                 nifti_structure_id: int,
                 name: str,
                 value: Any,
                 omic_package: str):
        pass

    @abstractmethod
    def get_nifti_structures(self):
        pass

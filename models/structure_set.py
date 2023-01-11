from typing import Union, Dict

import SimpleITK as sitk


class StructureSet:
    def __init__(self,
                 image_path: str,
                 structure_paths: Dict[str, str]):
        self.image = NiftiStructure(path=image_path, name="image")
        self.structures = {}
        for name, path in structure_paths.items():
            self.structures[name] = NiftiStructure(path=path, name=name)


class NiftiStructure:
    def __init__(self, path, name, label_int=255):
        self.path = path
        self.name = name
        self.label_int = label_int
        self._image = None
        self._array = None

    @property
    def as_image(self):
        if not self._image:
            self._image = sitk.ReadImage(self.path)
        return self._image

    @property
    def as_array(self):
        if not self._array:
            self._array = sitk.GetArrayFromImage(self.as_image)
        return self._array


from radiomics import featureextractor

from models.structure_set import NiftiStructure
import numpy as np


def arg_yielder(structure_set):
    for label_name, nifti_structure in structure_set.structures.items():
        yield structure_set.image, label_name, nifti_structure


def generate_pyradiomics(image: NiftiStructure, label_name: str, nifti_structure: NiftiStructure):
    extractor = featureextractor.RadiomicsFeatureExtractor()
    featureVector = extractor.execute(image.path, nifti_structure.path,
                                      label=255)  # Label is hardcoded - should be handled eventually

    d = {"structure": label_name}
    for featureName in featureVector.keys():
        d[featureName] = featureVector[featureName]

    return d


def generate_firstorder_pyradiomics(image: NiftiStructure, label_name: str, nifti_structure: NiftiStructure):
    # Initialize feature extractor
    extractor = featureextractor.RadiomicsFeatureExtractor()

    # Disable all classes except firstorder
    extractor.disableAllFeatures()

    # Enable all features in firstorder
    extractor.enableFeatureClassByName('firstorder')

    featureVector = extractor.execute(image.path, nifti_structure.path, label=255)

    # Show output
    d = {"structure": label_name}
    for featureName in featureVector.keys():
        d[featureName] = featureVector[featureName]

    return d


def find_contour_z_boundaries(image: NiftiStructure, label_name: str, nifti_structure: NiftiStructure):
    arr = nifti_structure.as_array.astype(bool)

    contour_range = []
    for z in range(arr.shape[0]):
        if bool(np.count_nonzero(arr[z, :, :])):
            contour_range.append(z)

    d = {
        "structure": label_name,
        "z_contour_range": contour_range,
        "z_top": contour_range[-1],
        "z_bottom": contour_range[0]
    }

    return d

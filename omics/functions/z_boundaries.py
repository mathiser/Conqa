import numpy as np

from database.db_models import NiftiStructure


def find_contour_z_boundaries(structure: NiftiStructure):
    arr = structure.as_array().astype(bool)

    contour_range = []
    for z in range(arr.shape[0]):
        if bool(np.count_nonzero(arr[z, :, :])):
            contour_range.append(z)
    return_list = []

    return_list.append({"nifti_structure_id": structure.id,
                        "name": "z_top",
                        "value": str(contour_range[-1]),
                        "omic_package": "z_boundaries"})

    return_list.append({"nifti_structure_id": structure.id,
                        "name": "z_range",
                        "value": contour_range,
                        "omic_package": "z_boundaries"})

    return_list.append({"nifti_structure_id": structure.id,
                        "name": "z_bottom",
                        "value": str(contour_range[0]),
                        "omic_package": "z_boundaries"})
    return return_list

import logging
from multiprocessing.pool import ThreadPool

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


def batch_find_contour_z_boundaries(db, structures_iterable, threads):
    t = ThreadPool(threads)
    try:
        results = t.map(find_contour_z_boundaries, structures_iterable)
        for result in results:
            for feature in result:
                omic = db.add_omic(**feature)
                logging.info(f"Added omic: {omic.name} to nifti_structure: {omic.nifti_structure_id}")
                yield omic
    except Exception as e:
        print(e)
    finally:
        t.close()
        t.join()

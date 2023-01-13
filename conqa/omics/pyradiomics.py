import logging
from multiprocessing.pool import ThreadPool

from radiomics import featureextractor

from database.db_interface import DBInterface
from database.db_models import NiftiStructure


def generate_pyradiomics(nifti_structure: NiftiStructure, only_firstorder=False):
    extractor = featureextractor.RadiomicsFeatureExtractor()
    if only_firstorder:
        extractor.disableAllFeatures()
        extractor.enableFeatureClassByName('firstorder')

    featureVector = extractor.execute(nifti_structure.nifti_image.path,
                                      nifti_structure.path,
                                      nifti_structure.label_int)
    return_list = []
    for featureName in featureVector.keys():
        return_list.append({"nifti_structure_id": nifti_structure.id,
                            "name": featureName,
                            "value": featureVector[featureName],
                            "omic_package": "pyradiomics"})
    return return_list


def batch_generate_pyradiomics(db: DBInterface, structures_iterable, threads):
    t = ThreadPool(threads)
    try:
        results = t.map(generate_pyradiomics, structures_iterable)
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

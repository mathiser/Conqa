from radiomics import featureextractor

from database.db_models import NiftiStructure


def generate_pyradiomics(nifti_structure: NiftiStructure, only_firstorder=True):
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
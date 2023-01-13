import logging

import pandas as pd

from database.db_interface import DBInterface


class ReportGenerator:
    def __init__(self, db: DBInterface):
        self.db = db

    def generate_omics_report(self) -> pd.DataFrame:
        structures = self.db.get_nifti_structures()
        d = {}
        for structure in structures:
            d[structure.id] = {
                "image_path": structure.nifti_image.path,
                "image_id": structure.nifti_image.id,
                "image_date": structure.nifti_image.scan_date,
                "image_patient_id": structure.nifti_image.patient_id,
                "structure_path": structure.path,
                "structure_name": structure.name,
                "structure_id": structure.id

            }
            for omic in structure.omics:
                d[structure.id][omic.name] = omic.value

        df = pd.DataFrame(d).T
        return df
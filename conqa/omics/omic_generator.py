from typing import List

from conqa.omics.pyradiomics import batch_generate_pyradiomics
from conqa.omics.z_boundaries import batch_find_contour_z_boundaries
from database.db_interface import DBInterface
from database.db_models import Omic


class OmicGenerator:
    def __init__(self, db: DBInterface, threads: int):
        self.db = db
        self.threads = threads

    def run_all_omics(self):
        self.run_pyradiomics()
        self.run_z_boundaries()

    def run_pyradiomics(self) -> List[Omic]:
        return batch_generate_pyradiomics(db=self.db,
                                          structures_iterable=self.yield_structures("pyradiomics"),
                                          threads=self.threads)

    def run_z_boundaries(self) -> List[Omic]:
        return batch_find_contour_z_boundaries(db=self.db,
                                               structures_iterable=self.yield_structures("z_boundaries"),
                                               threads=self.threads)

    def yield_structures(self, omic_package: str):
        # This function yields all structures
        # that are does not have the given omic_package in nifti_structure.executed_omic_packages
        structures = self.db.get_nifti_structures()
        for structure in structures:
            if omic_package not in structure.executed_omic_packages:
                yield structure

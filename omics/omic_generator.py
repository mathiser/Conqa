from multiprocessing.pool import ThreadPool
from typing import List

from database.db_interface import DBInterface
from database.db_models import Omic
from omics.functions.pyradiomics import generate_pyradiomics
from omics.functions.z_boundaries import find_contour_z_boundaries


class OmicsGenerator:
    def __init__(self, db: DBInterface, threads=8):
        self.db = db
        self.threads = threads

    def run_all(self):
        self.run_pyradiomics()
        self.run_z_boundaries()

    def run_pyradiomics(self) -> List[Omic]:
        t = ThreadPool(self.threads)
        try:
            results = t.map(generate_pyradiomics, self.yield_structures("pyradiomics"))
            for result in results:
                for feature in result:
                    yield self.db.add_omic(**feature)

        except Exception as e:
            print(e)
        finally:
            t.close()
            t.join()


    def run_z_boundaries(self) -> List[Omic]:
        t = ThreadPool(self.threads)
        try:
            results = t.map(find_contour_z_boundaries, self.yield_structures("z_boundaries"))
            for result in results:
                for feature in result:
                    yield self.db.add_omic(**feature)
        except Exception as e:
            print(e)
        finally:
            t.close()
            t.join()


    def yield_structures(self, omic_package: str):
        # This function yields all structures
        # that are does not have the given omic_package in nifti_structure.executed_omic_packages
        structures = self.db.get_nifti_structures()
        for structure in structures:
            if omic_package not in structure.executed_omic_packages:
                yield structure

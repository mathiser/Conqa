from typing import List, Union

from conqa.io.io_handler import IOHandler
from conqa.omics import OmicGenerator
from conqa.qa.reports import ReportGenerator

from database.db import DB
from database.db_models import Omic


class Conqa:
    """
    This class serves as the application interface with "public functions" to Conqa
    """
    def __init__(self, database_path: Union[str, None] = None, threads: int = 8):
        self.db = DB(database_path=database_path)
        self.threads = threads
        self.omic_generator = OmicGenerator(db=self.db, threads=self.threads)
        self.io_handler = IOHandler(db=self.db)
        self.report_generator = ReportGenerator(db=self.db)

    def run_all_omics(self):
        self.omic_generator.run_pyradiomics()
        self.omic_generator.run_z_boundaries()

    def run_pyradiomics(self) -> List[Omic]:
        return self.omic_generator.run_pyradiomics()

    def run_z_boundaries(self) -> List[Omic]:
        return self.omic_generator.run_z_boundaries()

    def load_nifti_folder_to_db(self, folder: str):
        return self.io_handler.load_nifti_folder_to_db(folder=folder)

    def generate_omics_report(self):
        return self.report_generator.generate_omics_report()

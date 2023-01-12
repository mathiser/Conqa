from queue import Queue

from database.db import DB
from io_tools.load import load_patient_folder


class ConQA:
    def __init__(self, input_folder: str):
        self.db = DB()  # DB Mock
        self.reports_queue = Queue()
        load_patient_folder(self.db, input_folder)
        print(self.db.get_nifti_images())
        print(self.db.get_nifti_images()[0].nifti_structures[0].__dict__)


if __name__ == "__main__":
    ConQA(input_folder="./input/")



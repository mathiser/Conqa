import datetime
import logging
import os

from database.db_interface import DBInterface


class IOHandler:
    def __init__(self, db: DBInterface):
        self.db = db

    def load_nifti_folder_to_db(self, folder: str):
        # Must be a base folder o
        for pid in os.listdir(folder):
            logging.debug(pid)
            pid_path = os.path.join(folder, pid)
            for date in os.listdir(pid_path):
                logging.debug(date)
                date_path = os.path.join(pid_path, date)

                # assume image location
                img_path = os.path.join(date_path, "image.nii.gz")
                if not os.path.isfile(img_path):
                    logging.error(f"Image not found - check folder {date_path}")
                    continue

                img = self.db.add_nifti_image(path=img_path,
                                              scan_date=datetime.datetime.strptime(date, "%Y%m%d"),
                                              patient_id=pid)

                for file in os.listdir(date_path):
                    file_path = os.path.join(date_path, file)
                    if file.startswith("mask_"):
                        structure_name = file.replace("mask_", "").replace(".nii.gz", "")
                        self.db.add_nifti_structure(name=structure_name,
                                                    path=file_path,
                                                    nifti_image_id=img.id)

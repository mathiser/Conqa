import os

from database.db_interface import DBInterface


def load_patient_folder(db: DBInterface, folder: str):
    d = {}
    for fol, subs, files in os.walk(folder):
        for file in files:
            if file.endswith("CT.nii.gz"):
                img_path = os.path.join(fol, file)
                img = db.add_nifti_image(img_path)
                break
        else:
            raise Exception("Found no scan")

        for file in files:
            if not file.endswith("CT.nii.gz"):
                db.add_nifti_structure(name=file.split("&")[-1].replace(".nii.gz", ""),
                                       path=os.path.join(fol, file),
                                       nifti_image_id=img.id)
                return d
from database.db_interface import DBInterface


class DB(DBInterface):
    def get_label_names(self):
        return {"image",
                "brain",
                "brainstem",
                "mandible",
                "parotid_l",
                "parotid_r",
                "submandibular_l",
                "submandibular_r",
                "pcm_up",
                "pcm_mid",
                "pcm_low",
                "thyroid"
                "spinalcord"
                "esophagus"
                }

    def get_synonym_dictionary(self):
        return {
            "CT.nii.gz": "image",
            "Brain.nii.gz": "brain",
            "Brainstem.nii.gz": "brainstem",
            "SpinalCord.nii.gz": "spinalcord",
            "Mandible.nii.gz": "mandible",
            "Parotid_L.nii.gz": "parotid_l",
            "Parotid_R.nii.gz": "parotid_r",
            "Submandibular_L.nii.gz": "submandibular_l",
            "Submandibular_R.nii.gz": "submandibular_r",
            "PCM_Up.nii.gz": "pcm_up",
            "PCM_Mid.nii.gz": "pcm_mid",
            "PCM_Low.nii.gz": "pcm_low",
            "Thyroid.nii.gz": "thyroid",
            "Esophagus.nii.gz": "esophagus"
        }

    def get_volume_number_constraint(self):
        return {
            "brain": 1,
            "brainstem": 1,
            "spinalcord": 1,
            "mandible": 1,
            "parotid_l": 1,
            "parotid_r": 1,
            "submandibular_l": 1,
            "submandibular_r": 1,
            "pcm_up": 1,
            "pcm_mid": 1,
            "pcm_low": 1,
            "thyroid": 2,
            "esophagus": 1
        }

    def get_adjacency_constraint(self):
        return [
            ("esophagus", "pcm_low"),
            ("pcm_low", "pcm_mid"),
            ("pcm_mid", "pcm_up"),
            ("spinalcord", "brainstem"),
            ("larynx_g", "larynx_sg")
        ]

    def get_paired_structures(self):
        return [
            ("parotid_r", "parotid_l"),
            ("submandibular_r", "submandibular_l")
        ]

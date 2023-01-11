from queue import Queue

from monai.deploy.core import Application

from database.db import DB

from operators.io import NiftiLoader, ResultWriter
from operators.omics import OmicGenerator
from operators.qa import VolumeNoCheck, AdjacencyCheck


class ConQA(Application):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def compose(self):
        db = DB()  # DB Mock
        reports_queue = Queue()
        dataloader_op = NiftiLoader(db.get_synonym_dictionary())  # Load files according to synonym_dictionary
        omics_op = OmicGenerator()  # Omics generator (pyradiomics and maybe some self-made ones)

        # Generate Omics
        self.add_flow(dataloader_op, omics_op, {"structure_set": "structure_set"})

        ##### QA Check s#######
        # Vol no check
        volume_no_check = VolumeNoCheck(volume_no_contraints=db.get_volume_number_constraint())
        self.add_flow(omics_op, volume_no_check, {"omics": "omics"})

        # Adjacency check
        adjacency_check = AdjacencyCheck(adjacency_constraint=db.get_adjacency_constraint())
        self.add_flow(omics_op, adjacency_check, {"omics": "omics"})
        self.add_flow(volume_no_check, adjacency_check, {"reports": "reports"})

        # Write report
        writer_op = ResultWriter(reports_queue=reports_queue)  # Writing report to disk
        self.add_flow(adjacency_check, writer_op, {"reports": "reports"})
        self.add_flow(omics_op, writer_op, {"omics": "omics"})



if __name__ == "__main__":
    ConQA(do_run=True)

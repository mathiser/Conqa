import logging
from multiprocessing.pool import ThreadPool

import monai.deploy.core as md
import pandas as pd
import radiomics
from monai.deploy.core import ExecutionContext, InputContext, IOType, Operator, OutputContext

from models.structure_set import StructureSet
from operators.omics.omic_functions import arg_yielder, generate_firstorder_pyradiomics, find_contour_z_boundaries
logger = radiomics.logger
logger.setLevel(logging.ERROR)  # set level to DEBUG to include debug log messages in log file

@md.input("structure_set", StructureSet, IOType.IN_MEMORY)
@md.output("omics", pd.DataFrame, IOType.IN_MEMORY)
@md.env(pip_packages=[])
class OmicGenerator(Operator):

    def __init__(self, threads=8):
        self.logger = logging.getLogger("{}.{}".format(__name__, type(self).__name__))
        super().__init__()
        self.threads = threads

    def compute(self, op_input: InputContext, op_output: OutputContext, context: ExecutionContext):
        structure_set = op_input.get("structure_set")

        t = ThreadPool(self.threads)
        omics = t.starmap(generate_firstorder_pyradiomics, arg_yielder(structure_set))
        z_omics = t.starmap(find_contour_z_boundaries, arg_yielder(structure_set))

        t.close()
        t.join()
        omics_df = pd.DataFrame(omics)
        z_omics_df = pd.DataFrame(z_omics)
        merged_omics = pd.merge(omics_df, z_omics_df, on="structure")

        op_output.set(merged_omics, "omics")




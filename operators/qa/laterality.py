import logging
from queue import Queue
from typing import List

import monai.deploy.core as md
import numpy as np
import pandas as pd
import radiomics
from monai.deploy.core import ExecutionContext, InputContext, IOType, Operator, OutputContext

logger = radiomics.logger
logger.setLevel(logging.ERROR)  # set level to DEBUG to include debug log messages in log file


@md.input("omics", pd.DataFrame, IOType.IN_MEMORY)
@md.input("reports", List[pd.DataFrame], IOType.IN_MEMORY)
@md.output("reports", List[pd.DataFrame], IOType.IN_MEMORY)
@md.env(pip_packages=[])
class LateralityCheck(Operator):
    def __init__(self, adjacency_constraint: dict):
        self.logger = logging.getLogger("{}.{}".format(__name__, type(self).__name__))
        super().__init__()
        self.adjacency_constraint = adjacency_constraint

    def compute(self, op_input: InputContext, op_output: OutputContext, context: ExecutionContext):
        omics_df = op_input.get("omics")
        result_df = self.adjacency_check(omics_df=omics_df)

        reports = op_input.get("reports")
        reports.append(result_df)
        op_output.set(reports, label="reports")

    def adjacency_check(self, omics_df):
        assert "" in omics_df.columns
        assert "z_bottom" in omics_df.columns

        df = omics_df[["structure", "z_top", "z_bottom"]].copy()

        df["adjacency_check_top"] = None  # Change to True if pass
        df["adjacency_check_bottom"] = None  # Change to True if pass
        for adjacent_structures in self.adjacency_constraint:
            bottom_structure, top_structure = adjacent_structures

            check = (df[df["structure"] == bottom_structure]["z_top"].iloc[0] + 1 ==
                     df[df["structure"] == top_structure]["z_bottom"].iloc[0])

            # Write check to df
            df.loc[df["structure"] == bottom_structure, "adjacency_check_top"] = check
            df.loc[df["structure"] == top_structure, "adjacency_check_bottom"] = check
        return df

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
@md.output("reports", List[pd.DataFrame], IOType.IN_MEMORY)
@md.env(pip_packages=[])
class VolumeNoCheck(Operator):
    def __init__(self, volume_no_contraints: dict):
        self.logger = logging.getLogger("{}.{}".format(__name__, type(self).__name__))
        super().__init__()
        self.volume_no_contraints = volume_no_contraints

    def compute(self, op_input: InputContext, op_output: OutputContext, context: ExecutionContext):
        omics_df = op_input.get("omics")
        result_df = self.volume_no_check(omics_df=omics_df)
        op_output.set([result_df], "reports")

    def volume_no_check(self, omics_df):
        assert "diagnostics_Mask-original_VolumeNum" in omics_df.columns
        df = omics_df[["structure", "diagnostics_Mask-original_VolumeNum"]].copy()

        df["volume_no_check"] = False  # Change to True if pass
        for structure, allowed_sub_volumes in self.volume_no_contraints.items():
            # Add the constraint
            df.loc[df["structure"] == structure, "allowed_sub_volumes"] = allowed_sub_volumes

            # Do the check
            df.loc[((df["structure"] == structure) &
                   (df['diagnostics_Mask-original_VolumeNum'] <= allowed_sub_volumes)), "volume_no_check"] = True
        return df

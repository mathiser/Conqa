import logging
import os
from queue import Queue
from typing import List

import pandas as pd
import monai.deploy.core as md
from monai.deploy.core import ExecutionContext, InputContext, IOType, Operator, OutputContext, DataPath

@md.input("omics", pd.DataFrame, IOType.IN_MEMORY)
@md.input("reports", List[pd.DataFrame], IOType.IN_MEMORY)
@md.output("", DataPath, IOType.DISK)
@md.env(pip_packages=[])
class ResultWriter(Operator):
    def __init__(self, reports_queue: Queue):
        self.logger = logging.getLogger("{}.{}".format(__name__, type(self).__name__))
        super().__init__()
        self.reports_queue = reports_queue

    def compute(self, op_input: InputContext, op_output: OutputContext, context: ExecutionContext):
        reports = op_input.get("reports")
        base_df = reports[0]
        for df in reports[1:]:
            base_df = pd.merge(base_df, df, on="structure")

        output_folder = op_output.get().path
        base_df.to_csv(os.path.join(output_folder, "results.csv"))

        omics = op_input.get("omics")
        omics.to_csv(os.path.join(output_folder, "omics.csv"))

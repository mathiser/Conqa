import logging
import os
from multiprocessing.pool import ThreadPool
from typing import Dict, Tuple

import monai.deploy.core as md
import numpy as np
from monai.deploy.core import ExecutionContext, InputContext, IOType, Operator, OutputContext, DataPath

from models.structure_set import StructureSet


@md.input("", DataPath, IOType.DISK)
@md.output("structure_set", StructureSet, IOType.IN_MEMORY)
@md.env(pip_packages=[])
class NiftiLoader(Operator):
    def __init__(self, synonym_dictionary: Dict):
        self.logger = logging.getLogger("{}.{}".format(__name__, type(self).__name__))
        super().__init__()
        self.synonym_dictionary = synonym_dictionary

    def compute(self, op_input: InputContext, op_output: OutputContext, context: ExecutionContext):
        input_folder = op_input.get("").path
        print(input_folder)

        structure_dict = {}
        for fol, subs, files in os.walk(input_folder):
            for f in files:
                for k, v in self.synonym_dictionary.items():
                    if k in f:
                        structure_dict[v] = os.path.join(fol, f)

        image_path = structure_dict["image"]
        del structure_dict["image"]
        structure_set = StructureSet(image_path=image_path, structure_paths=structure_dict)
        op_output.set(structure_set, "structure_set")



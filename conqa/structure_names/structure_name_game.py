import datetime
import json
import logging
import sqlite3

from sqlalchemy.exc import IntegrityError

from database.db_interface import DBInterface
from database.db_models import NiftiStructure
import Levenshtein


class NameGame:
    def __init__(self, db: DBInterface):
        self.db = db

    def yield_nifti_structures_with_no_base_name(self):
        return_list = []
        for structure in self.db.get_nifti_structures():
            if not structure.structure_base_name:
                return_list.append(structure)

        return return_list

    def add_or_order_synonyms_by_levenshtein(self, structure: NiftiStructure):
        synonyms = self.db.get_structure_synonym_names()
        return_list = []
        if len(synonyms) == 0:
            print(return_list)
            return return_list
        for synonym in synonyms:
            l = Levenshtein.distance(structure.name, synonym.name)
            if l == 0:
                self.db.add_structure_base_name_association(nifti_structure_id=structure.id,
                                                            structure_base_name_id=synonym.structure_base_name.id)
                return False
            else:
                return_list.append({"leven": Levenshtein.distance(structure.name, synonym.structure_base_name.name),
                                    "structure": structure, "basename": synonym.structure_base_name})

        return_list.sort(key=lambda k: k["leven"])

        return return_list

    def game_loop(self):
        structures = self.yield_nifti_structures_with_no_base_name()
        while len(structures) != 0:
            structure = structures.pop()

            leven = self.add_or_order_synonyms_by_levenshtein(structure)
            while isinstance(leven, list):
                print(f"------------- {len(structures)} structures left ---------------")

                idx = 0
                if len(leven) < 4:
                    these = leven
                else:
                    these = leven[idx:idx + 4]

                print(f"THIS STRUCTURE: {structure.name}")
                for these_i, r in enumerate(these):
                    print(these_i + 1, r["basename"].name, r["leven"])
                print("Input number of the matching base name")
                print("r: Show next four")
                print("e: Show previous four")
                print("w: Add as new base name")
                print("s: Specify a new base name for this structure")
                print("q: quit")
                inp = input("Input: ")
                try:
                    inp = int(inp)
                    inp -= 1
                    if 0 <= inp < 4:
                        logging.info(self.db.add_structure_synonym_name(structure_base_name_id=these[inp]["basename"].id,
                                                           name=these[inp]["structure"].name))

                        self.db.add_structure_base_name_association(nifti_structure_id=these[inp]["structure"].id,
                                                                    structure_base_name_id=these[inp]["basename"].id)
                        break
                    else:
                        print("Input out of range")
                except IntegrityError as e:
                    pass
                except ValueError as e:
                    pass
                except Exception as e:
                    raise e
                if inp == "w":
                    self.db.add_structure_base_name(structure.name)
                    break
                elif inp == "s":
                    try:
                        bn = self.db.add_structure_base_name(input("New base name: "))
                        self.db.add_structure_base_name_association(nifti_structure_id=structure.id,
                                                                    structure_base_name_id=bn.id)
                        break
                    except Exception as e:
                        print(e)
                        print("invalid input")

                elif inp == "r":
                    idx += 4
                    if len(leven) < idx:
                        idx = len(leven)
                elif inp == "r":
                    idx -= 4
                    if idx < 0:
                        idx = 0
                elif inp == "q":
                    print("quitting...")
                    return
                else:
                    print("Invalid input - try again")

            structures = self.yield_nifti_structures_with_no_base_name()


        path = f"resources/{datetime.datetime.now()}_name_game_results.json"
        print(f"Dumping your work into {path}")
        d = {}
        for synonym in self.db.get_structure_synonym_names():
            d[synonym.name] = synonym.structure_base_name.name
        with open(path, "w") as f:
            f.write(json.dumps(d))

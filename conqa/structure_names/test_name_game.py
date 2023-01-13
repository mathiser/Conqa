import unittest

from conqa.io import IOHandler
from conqa.structure_names.structure_name_game import NameGame
from database.db import DB
from database.test_db import TestDB


class TestNameGame(unittest.TestCase):
    def setUp(self) -> None:
        self.db = DB(database_path="test_name_game.db")
        self.name_game = NameGame(db=self.db)

    def test_game_loop(self):
        #self.test_order_synonyms_by_levenshtein()
        self.io = IOHandler(self.db)
        self.io.load_nifti_folder_to_db("input")
        self.name_game.game_loop()

if __name__ == '__main__':
    unittest.main()

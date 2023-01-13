import logging
import sys

from conqa.client import Conqa

logging.basicConfig(encoding='utf-8', level=logging.INFO)
db_path = sys.argv[1]

if __name__ == "__main__":
    conqa = Conqa(database_path=db_path, threads=8)


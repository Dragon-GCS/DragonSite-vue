from pathlib import Path

# root directory is server folder
ROOT = Path(__file__).parent.parent.absolute()
PORT = 8888

DATABASE_URL = 'sqlite:///' + str(ROOT / 'db.sqlite')
FILE_DIR = ROOT / 'files'
DIST_DIR = ROOT / '../dist'

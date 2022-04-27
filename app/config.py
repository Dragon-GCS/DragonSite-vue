from pathlib import Path


class Config:
    ROOT = Path(__file__).parent.resolve()
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + str(ROOT / "db.sqlite")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TEMPLATE_DIR = ROOT.parent / "dist"


class DevConfig(Config):
    DEBUG = True
    PORT = "8000"


class ProdConfig(Config):
    PORT = "80"

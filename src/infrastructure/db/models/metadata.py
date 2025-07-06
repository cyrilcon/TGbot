from sqlalchemy import MetaData

from config import config

metadata = MetaData(naming_convention=config.db.naming_convention)

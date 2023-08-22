from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .confgi import setting





# SQLALCHEMY_DATABASE_URL = (
#     f"postgresql://{setting.database_username}:{setting.database_password}@"
#     f"{setting.database_hostname}:{setting.database_port}/{setting.database_name}"
# )
SQLALCHEMY_DATABASE_URL = ("postgresql://vlogs_user:HStNVutHb9fjCtqHpN7reCuxtFajyfuG@dpg-cji2ok8cfp5c73fh3na0-a.singapore-postgres.render.com/vlogs")
engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


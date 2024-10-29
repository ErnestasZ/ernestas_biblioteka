from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session, declarative_base
from dotenv import load_dotenv
import os
# from ernestas_biblioteka.orm.classes.consumer import Base as UserBase
# from ernestas_biblioteka.orm.classes.records import Base as UserRecordBase

load_dotenv()

DATABASE_URL = f"postgresql+psycopg2://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"


def db_connection():
    try:
        engine = create_engine(DATABASE_URL)
        # UserBase.metadata.create_all(engine)  # Create User table
        # UserRecordBase.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        # Base = declarative_base()

        # Return the session factory and engine if needed for table creation
        return Session, engine

    except Exception as e:
        print('Database connection failed:', e)
        return None

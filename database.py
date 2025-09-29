from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

db_url ="postgresql://postgres:%40%40shubha@localhost:5432/Product"

engine = create_engine(db_url)
session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
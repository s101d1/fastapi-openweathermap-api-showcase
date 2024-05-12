import os
from dotenv import load_dotenv

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

load_dotenv()

engine = create_engine(os.environ["DB_URL"], echo=True)
Session = sessionmaker(bind=engine)
session = Session()

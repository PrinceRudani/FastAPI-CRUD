from sqlalchemy import create_engine, MetaData
from base.db.database import DATABASE_URL  # Adjust this path based on your project

engine = create_engine(DATABASE_URL)
metadata = MetaData()
metadata.reflect(bind=engine)
metadata.drop_all(bind=engine)

print("All tables dropped successfully!")

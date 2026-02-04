from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
DATABASE_URL = "postgresql://undiyal_postgres_user:UCRM8e4QPI2PWpll9AdRK51AtRjHaZLC@dpg-d60sk8m3jp1c73aemgu0-a.virginia-postgres.render.com/undiyal_postgres?sslmode=require"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

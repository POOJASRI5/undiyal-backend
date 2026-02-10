from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
DATABASE_URL = "postgresql://undiyal_postgres_r73b_user:Ab9eKu0G8WpGwvuxZv9o3g3zeaKKHVY7@dpg-d6536pm3li6c7398bk30-a.virginia-postgres.render.com/undiyal_postgres_r73b"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

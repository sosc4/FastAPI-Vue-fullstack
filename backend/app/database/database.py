from pathlib import Path

from sqlmodel import create_engine

PATH = Path(__file__).parent.parent.parent
DATABASE_URL = f"sqlite:///{PATH}/database.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

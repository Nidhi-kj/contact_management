


import os
from pathlib import Path
from dotenv import load_dotenv

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Backend folder ka path
BASE_DIR = Path(__file__).resolve().parent.parent

# .env load karna
load_dotenv(BASE_DIR / ".env")

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL .env file mein nahi mila")

# CA certificate ka path
CA_CERT = BASE_DIR / "ca.pem"

engine = create_engine(
    DATABASE_URL,
    echo=True,
    connect_args={
        "ssl": {
            "ca": str(CA_CERT)
        }
    }
)

Base = declarative_base()

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

        # import os
# from pathlib import Path
# from dotenv import load_dotenv

# from sqlalchemy import create_engine
# from sqlalchemy.orm import declarative_base, sessionmaker

# # database.py jis folder mein hai, usi folder mein .env hai
# env_path = Path(__file__).resolve().parent.parent / ".env"

# load_dotenv(dotenv_path=env_path)

# DATABASE_URL = os.getenv("DATABASE_URL")

# # Debugging
# print("ENV FILE FOUND:", env_path.exists())
# print("DATABASE URL LOADED:", DATABASE_URL is not None)

# if not DATABASE_URL:
#     raise ValueError("DATABASE_URL .env file se load nahi ho raha!")

# engine = create_engine(
#     DATABASE_URL,
#     echo=True
# )

# Base = declarative_base()

# SessionLocal = sessionmaker(
#     bind=engine,
#     autoflush=False,
#     autocommit=False
# )

# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()
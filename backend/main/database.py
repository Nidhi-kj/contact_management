from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = "mysql+pymysql://root:root@localhost:3306/contact_management"

engine = create_engine(DATABASE_URL, echo=True)



Base = declarative_base()

# object create krne k lye template session bnta h
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
from sqlalchemy.orm import sessionmaker
from sqlmodel import create_engine
from sqlmodel import Session

DATABASE_URL = "postgresql://socialuser:socialuser123@ec2-13-51-157-83.eu-north-1.compute.amazonaws.com:5432/socialapp"
# eng = 'database.db'

# sqlite_url = f'sqlite:///{eng}'
# engine = create_engine(sqlite_url)


# postgres_url = DATABASE_URL
print("postgres", DATABASE_URL)
engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db = SessionLocal()


# session = Session(bind=engine)
def get_session():
    with Session(engine) as session:
        yield session

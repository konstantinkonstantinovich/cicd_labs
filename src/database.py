import os

from sqlmodel import Session, SQLModel, create_engine

DATABASE_URL = f'postgresql+psycopg2://{os.environ["POSTGRES_USER"]}:' \
               f'{os.environ["POSTGRES_PASSWORD"]}@{os.environ["POSTGRES_HOST"]}:5432/{os.environ["POSTGRES_NAME"]}'
engine = create_engine(DATABASE_URL)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
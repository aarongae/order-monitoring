import os

from sqlalchemy import create_engine, Table, MetaData, Column, Integer, String
from datetime import datetime

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import session, sessionmaker

user = os.getenv('POSTGRES_USER', 'user')
password = os.getenv('POSTGRES_PASSWORD', 'password')
host = os.getenv('POSTGRES_HOST', 'localhost')
database = os.getenv('POSTGRES_DB', 'lieferbot')
port = os.getenv('POSTGRES_PORT', 5432)

DB_CONNECTION_URI = f'postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}'
engine = create_engine(DB_CONNECTION_URI)

Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()


class Orders(Base):
    __tablename__ = 'orders'

    order_id = Column(String, primary_key=True)
    timestamp = Column(String)
    order_status = Column(String)

    def __repr__(self):
        return f'User {self.order_id}'


def init_db():
    Base.metadata.create_all(engine)


def insert_record(record):
    session.add(record)
    session.commit()


def bulk_insert(obj_list):
    session.bulk_save_objects(obj_list)
    session.commit()


def delete_record_by_id(id):
    session.query(Orders).filter(Orders.order_id==id).delete()
    session.commit()


if __name__ == "__main__":
    init_db()

    order_list = [
        Orders(order_id='order1', timestamp=datetime.now(), order_status='UNASSIGNED'),
        Orders(order_id='order2', timestamp=datetime.now(), order_status='UNASSIGNED'),
        Orders(order_id='order3', timestamp=datetime.now(), order_status='UNASSIGNED')
    ]

    #TODO: not safe for multiple runs
    bulk_insert(order_list)

    for order in session.query(Orders).all():
        print(order.order_id)


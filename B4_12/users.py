import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime, timedelta
import numpy as np

DB_PATH = "sqlite:///sochi_athletes.sqlite3"
Base = declarative_base()

class User(Base):
    __tablename__ = 'user'
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    first_name = sa.Column(sa.Text)
    last_name = sa.Column(sa.Text)
    gender = sa.Column(sa.Text)
    email = sa.Column(sa.Text)
    birthdate = sa.Column(sa.Text)
    height = sa.Column(sa.Float)
               
def connect_db():
    engine = sa.create_engine(DB_PATH)
    Base.metadata.create_all(engine)
    session = sessionmaker(engine)
    return session()

def request_data():
    print("Привет! Я запишу твои данные!")
    first_name = input("Введи своё имя: ")
    last_name = input("А теперь фамилию: ")
    gender = input("введите пол: ")
    email = input("Мне еще понадобится адрес твоей электронной почты: ")
    birthdate = input("введите дату рождения (формат: yyyy-mm-dd): ")
    height = float(input("введите рост в метрах (например 1.78): "))
        
    user = User(
        first_name = first_name,
        last_name = last_name,      
        gender = gender,
        email = email,
        birthdate = birthdate,
        height = height
    )
    return user

def main():
    session = connect_db()
    print("Ввести данные нового пользователя\n")
    user = request_data()
    session.add(user)
    session.commit()
    print("Спасибо, данные сохранены!")

if __name__ == "__main__":
    main()
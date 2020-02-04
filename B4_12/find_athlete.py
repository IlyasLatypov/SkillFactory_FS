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
        
class Athelete(Base):
    __tablename__ = 'athelete'
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    age = sa.Column(sa.Integer)
    birthdate = sa.Column(sa.Text)
    gender = sa.Column(sa.Text)
    height = sa.Column(sa.Float)    
    name = sa.Column(sa.Text)
    weight = sa.Column(sa.Integer)
    gold_medals = sa.Column(sa.Integer)
    silver_medals = sa.Column(sa.Integer)
    bronze_medals = sa.Column(sa.Integer)
    total_medals = sa.Column(sa.Integer)
    sport = sa.Column(sa.Text)
    country = sa.Column(sa.Text)

def connect_db():
    engine = sa.create_engine(DB_PATH)
    Base.metadata.create_all(engine)
    session = sessionmaker(engine)
    return session()

def find_user(id_, session):
    query = session.query(User).filter(User.id == id_)

    if query.count() == 0:
        print('Нет пользователя с идентификатором:', id_)
        return (-1, -1)
    else:
        dt = datetime.strptime(query[0].birthdate,'%Y-%m-%d')
        print('\nУ пользователя дата рождения (формат: dd.mm.yyyy):', dt.strftime('%d.%m.%Y'),' и рост: ' ,query[0].height)
        return (dt, query[0].height)

def find_athelete(bdate, h, session):
    query = session.query(Athelete).all()
    lpoisk = [(i.id, datetime.strptime(i.birthdate,'%Y-%m-%d'), i.height) for i in query]
    h_min = 10.0
    id_h_min = 1
    bdate_min = datetime(1900,1,1,0,0)
    id_bdate_min = 1   
    for k in lpoisk:
        if k[2] != None:
            if np.absolute(float(k[2]) - h) < np.absolute(float(k[2]) - h_min):
                h_min = float(k[2])
                id_h_min = k[0]
        if k[1] != None:
            if np.absolute(k[1] - bdate) < np.absolute(k[1] - bdate_min):
                bdate_min = k[1]
                id_bdate_min = k[0]
    
    query = session.query(Athelete).filter(Athelete.id == int(id_h_min))
    print("\nНаиболее близкий атлет по росту:")
    st = "{:<5} {:<20} {:<11} {:<6} {:<20} {:<20}"
    print(st.format("id", "name", "birthdate", "height", "sport", "country"))
    bdate_ = datetime.strptime(query[0].birthdate,'%Y-%m-%d').strftime('%d.%m.%Y') if query[0].birthdate else ""
    print(st.format(query[0].id if query[0].id else "", query[0].name if query[0].name else "" , bdate_, 
                    query[0].height if query[0].height else "",
                    query[0].sport if query[0].sport else "", query[0].country if query[0].country else ""))
    
    query = session.query(Athelete).filter(Athelete.id == int(id_bdate_min))
    print("\nНаиболее близкий атлет по возрасту:")
    print(st.format("id", "name", "birthdate", "height", "sport", "country"))
    bdate_ = datetime.strptime(query[0].birthdate,'%Y-%m-%d').strftime('%d.%m.%Y') if query[0].birthdate else ""
    print(st.format(query[0].id if query[0].id else "", query[0].name if query[0].name else "" , bdate_, 
                    query[0].height if query[0].height else "",
                    query[0].sport if query[0].sport else "", query[0].country if query[0].country else ""))

def main():
    session = connect_db()
    print("Поиск атлетов по возрасту и росту пользователя")

    query = session.query(User).all()
    st = ", ".join(map(lambda x: str(x), [i.id for i in query]))
    print('Список идентификатор пользователей из БД:', st)
    id_ = int(input("Введи идентификатор пользователя для поиска (например 2): "))
    bdate, h = find_user(id_, session)
    if bdate != -1:
        find_athelete(bdate, float(h), session)

if __name__ == "__main__":
    main()       
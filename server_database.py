from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Integer, String, Text, DateTime, ForeignKey, Column, create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime


class ServerStorage:

    Base = declarative_base()

    class Users(Base):
        __tablename__ = 'users'
        id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
        login = Column(String, unique=True)
        last_entrance = Column(DateTime)

        def __init__(self, login):
            self.login = login
            self.last_entrance = datetime.now()

    class ActiveUsers(Base):
        __tablename__ = 'active_users'
        id = Column(Integer, primary_key=True)
        user_id = Column(Integer, ForeignKey('users.id'), unique=True)
        entrance_time = Column(DateTime)
        ip_address = Column(String)
        port = Column(Integer)

        def __init__(self, user_id, ip_address, port):
            self.user_id = user_id
            self.entrance_time = datetime.now()
            self.ip_address = ip_address
            self.port = port

    class UsersHistory(Base):
        __tablename__ = 'users_history'
        id = Column(Integer, primary_key=True)
        user_id = Column(Integer, ForeignKey('users.id'))
        entrance_time = Column(DateTime)
        ip_address = Column(String)
        port = Column(Integer)

        def __init__(self, user_id, ip_address, port):
            self.user_id = user_id
            self.entrance_time = datetime.now()
            self.ip_address = ip_address
            self.port = port

    def __init__(self):
        self.database_engine = create_engine('sqlite:///server_base.db3', echo=False, pool_recycle=7200)
        self.Base.metadata.create_all(self.database_engine)
        Session = sessionmaker(bind=self.database_engine)
        self.session = Session()
        self.session.query(self.ActiveUsers).delete()
        self.session.commit()

    def user_login(self, username, ip_address, port):

        data = self.session.query(self.Users).filter_by(login=username)
        if data.count():
            user = data.first()
            user.last_entrance = datetime.now()
        else:
            user = self.Users(username)
            self.session.add(user)
            self.session.commit()

        active_user = self.ActiveUsers(user.id, ip_address, port)
        self.session.add(active_user)

        user_history = self.UsersHistory(user.id, ip_address, port)
        self.session.add(user_history)

        self.session.commit()

    def user_logout(self, username):
        user = self.session.query(self.Users).filter_by(login=username).first()
        self.session.query(self.ActiveUsers).filter_by(user_id=user.id).delete()
        self.session.commit()

    def users_list(self):
        return self.session.query(self.Users.login, self.Users.last_entrance).all()

    def active_users_list(self):
        return self.session.query(self.Users.login,
                                  self.ActiveUsers.ip_address,
                                  self.ActiveUsers.port,
                                  self.ActiveUsers.entrance_time).join(self.Users).all()

    def show_history(self, username=None):
        query = self.session.query(self.Users.login,
                                   self.UsersHistory.entrance_time,
                                   self.UsersHistory.ip_address,
                                   self.UsersHistory.port).join(self.Users)
        return query.filter(self.Users.login == username).all() if username else query.all()


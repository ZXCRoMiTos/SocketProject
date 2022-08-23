from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Integer, String, DateTime, ForeignKey, Column, create_engine
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

    class UsersContacts(Base):
        __tablename__ = 'users_contacts'
        id = Column(Integer, primary_key=True)
        user_id = Column(Integer, ForeignKey('users.id'))
        contact_id = Column(Integer, ForeignKey('users.id'))

        def __init__(self, user_id, contact_id):
            self.user_id = user_id
            self.contact_id = contact_id

    class ActionHistory(Base):
        __tablename__ = 'action_history'
        id = Column(Integer, primary_key=True)
        user_id = Column(Integer, ForeignKey('users.id'))
        sent = Column(Integer)
        accepted = Column(Integer)

        def __init__(self, user_id):
            self.user_id = user_id
            self.sent = 0
            self.accepted = 0

    def __init__(self, path):
        self.database_engine = create_engine(f'sqlite:///{path}', echo=False, pool_recycle=7200,
                                             connect_args={'check_same_thread': False})
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
            user_in_history = self.ActionHistory(user.id)
            self.session.add(user_in_history)

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

    def process_message(self, sender, recipient):
        sender_id = self.session.query(self.Users).filter_by(login=sender).first().id
        recipient_id = self.session.query(self.Users).filter_by(login=recipient).first().id
        sender_row = self.session.query(self.ActionHistory).filter_by(user_id=sender_id).first()
        sender_row.sent += 1
        recipient_row = self.session.query(self.ActionHistory).filter_by(user_id=recipient_id).first()
        recipient_row.accepted += 1
        self.session.commit()

    def add_contact(self, username, contactname):
        user = self.session.query(self.Users).filter_by(login=username).first()
        contact = self.session.query(self.Users).filter_by(login=contactname).first()

        if not contact or self.session.query(self.UsersContacts).\
                filter_by(user_id=user.id, contact_id=contact.id).count():
            return

        new_contact = self.UsersContacts(user.id, contact.id)
        self.session.add(new_contact)
        self.session.commit()

    def get_contacts(self, username):
        user = self.session.query(self.Users).filter_by(login=username).first()
        query = self.session.query(self.UsersContacts, self.Users.login).filter_by(user_id=user.id).\
            join(self.Users, self.UsersContacts.contact_id == self.Users.id).all()
        return [contact[1] for contact in query]

    def remove_contact(self, username, contactname):
        user = self.session.query(self.Users).filter_by(login=username).first()
        contact = self.session.query(self.Users).filter_by(login=contactname).first()
        if contact:
            self.session.query(self.UsersContacts).filter_by(user_id=user.id, contact_id=contact.id).delete()
            self.session.commit()


if __name__ == '__main__':
    database = ServerStorage()
    database.user_login('test1', '192.168.1.1', 7777)
    database.user_login('test2', '192.168.1.1', 7777)
    database.add_contact('test1', 'test2')
    print(database.get_contacts('test1'))
    database.remove_contact('test1', 'test2')
    print(database.get_contacts('test1'))

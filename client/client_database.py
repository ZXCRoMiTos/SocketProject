from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Integer, String, Text, DateTime, Column, create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime


class ClientStorage:
    Base = declarative_base()

    class KnownUsers(Base):
        __tablename__ = 'known_users'
        id = Column(Integer, primary_key=True)
        username = Column(String)

        def __init__(self, username):
            self.username = username

    class MessageHistory(Base):
        __tablename__ = 'message_history'
        id = Column(Integer, primary_key=True)
        contact = Column(String)
        direction = Column(String)
        message = Column(Text)
        date = Column(DateTime)

        def __init__(self, contact, direction, message):
            self.contact = contact
            self.direction = direction
            self.message = message
            self.date = datetime.now()

    class Contacs(Base):
        __tablename__ = 'contacts'
        id = Column(Integer, primary_key=True)
        username = Column(String, unique=True)

        def __init__(self, username):
            self.username = username

    def __init__(self, name):
        self.database_engine = create_engine(f'sqlite:///client_{name}_base.db3', echo=True, pool_recycle=7200,
                                             connect_args={'check_same_thread': False})
        self.Base.metadata.create_all(self.database_engine)
        Session = sessionmaker(bind=self.database_engine)
        self.session = Session()
        self.session.query(self.Contacs).delete()
        self.session.commit()

    def add_contact(self, username):
        if not self.session.query(self.Contacs).filter_by(username=username).count():
            new_contact = self.Contacs(username)
            self.session.add(new_contact)
            self.session.commit()

    def get_contacts(self):
        return [contact[0] for contact in self.session.query(self.Contacs.username).all()]

    def del_contact(self, username):
        self.session.query(self.Contacs).filter_by(username=username).delete()
        self.session.commit()

    def check_contact(self, username):
        return True if self.session.query(self.Contacs).filter_by(username=username).count() else False

    def add_users(self, users_list):
        self.session.query(self.KnownUsers).delete()
        for username in users_list:
            new_user = self.KnownUsers(username)
            self.session.add(new_user)
        self.session.commit()

    def get_users(self):
        return [user[0] for user in self.session.query(self.KnownUsers.username).all()]

    def check_user(self, username):
        return True if self.session.query(self.KnownUsers).filter_by(username=username).count() else False

    def save_message(self, contact, direction, message):
        message_row = self.MessageHistory(contact, direction, message)
        self.session.add(message_row)
        self.session.commit()

    def delete_message_history(self):
        self.session.query(self.MessageHistory).delete()
        self.session.commit()

    def get_history(self, contact):
        query = self.session.query(self.MessageHistory).filter_by(contact=contact)
        return [(history_row.contact, history_row.direction,
                 history_row.message, history_row.date)
                for history_row in query.all()]

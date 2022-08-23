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
        from_user = Column(String)
        to_user = Column(String)
        message = Column(Text)
        date = Column(DateTime)

        def __init__(self, from_user, to_user, message):
            self.from_user = from_user
            self.to_user = to_user
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

    def check_contacts(self, username):
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

    def save_message(self, from_user, to_user, message):
        new_message = self.MessageHistory(from_user, to_user, message)
        self.session.add(new_message)
        self.session.commit()

    def delete_message_history(self):
        self.session.query(self.MessageHistory).delete()
        self.session.commit()

    def get_message_history(self, from_user=None, to_user=None):
        rows = self.session.query(self.MessageHistory)
        if from_user and to_user:
            rows = rows.filter_by(from_user=from_user, to_user=to_user)
        elif from_user:
            rows = rows.filter_by(from_user=from_user)
        elif to_user:
            rows = rows.filter_by(to_user=to_user)

        return [(row.from_user, row.to_user, row.message, row.date) for row in rows.all()]


if __name__ == '__main__':
    database = ClientStorage('some_name')

    print(database.get_contacts())
    database.add_contact('test1')
    print(database.check_contacts('test1'))
    print(database.get_contacts())
    database.del_contact('test1')
    print(database.get_contacts())

    database.add_users(['usertest1', 'usertest2'])
    print(database.get_users())
    print(database.check_user('usertest2'))

    database.delete_message_history()
    database.save_message('testuser1', 'testuser2', 'test message for test')
    database.save_message('testuser1', 'testuser3', 'test message for test')
    database.save_message('testuser3', 'testuser2', 'test message for test')
    print(database.get_message_history())
    print(database.get_message_history(from_user='testuser1'))
    print(database.get_message_history(to_user='testuser2'))
    print(database.get_message_history(from_user='testuser1', to_user='testuser2'))
    print(database.get_message_history(from_user='unknown_user'))

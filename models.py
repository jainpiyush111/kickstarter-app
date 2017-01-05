from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Text, DateTime


# engine = create_engine('sqlite:///database.db', echo=True)
engine = create_engine('postgres://nwpzolgh:wZbR4Q7D1YpI0PI0velMGKyFkKxPEuHi@elmer.db.elephantsql.com:5432/nwpzolgh', echo=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

# Set your classes here.


class Pledges(Base):
    __tablename__ = 'pledges'

    id = Column(Integer, primary_key=True, unique=True)
    project_id = Column(Integer, ForeignKey('projects.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    amount = Column(Integer)
    time_created = Column(DateTime)


class User(Base):

    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, unique=True)
    username = Column(String(30), primary_key=True)
    email = Column(String(30), primary_key=True)
    password = Column(String(15))
    authenticated = Column(Boolean, default=False)
    projects = relationship('Projects', backref="creator")
    #pledges = relationship('Pledges',backref="pledger", foreign_key="Pledges.user_id")
    pledges = relationship('Pledges', backref="pledger", primaryjoin= id == Pledges.user_id)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

    def is_active(self):
        """True, as all users are active."""
        return True

    def get_id(self):
        """Return the email address to satisfy Flask-Login's requirements."""
        return self.email

    def is_authenticated(self):
        """Return True if the user is authenticated."""
        return True

    def is_anonymous(self):
        """False, as anonymous users aren't supported."""
        return False


class Projects(Base):

    __tablename__ = 'projects'

    id = Column(Integer, primary_key=True, unique=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    name = Column(String(100))
    short_description = Column(Text)
    long_description = Column(Text)
    goal_amount = Column(Integer)
    time_start = Column(DateTime)
    time_end = Column(DateTime)
    time_created = Column(DateTime)
    pledges = relationship('Pledges', backref="project", primaryjoin= id == Pledges.project_id)



'''
class User(Base):
    __tablename__ = 'Users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(30))

    def __init__(self, name=None, password=None):
        self.name = name
        self.password = password
'''

# Create tables.
Base.metadata.create_all(bind=engine)

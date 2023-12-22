from sqlalchemy import create_engine, String, Column, Integer
from sqlalchemy.orm import sessionmaker, declarative_base


# SEARCHING FOR THE FILE/CREATING IT
def find_file(name):
    '''Trying to read the file. If it doesn't exist, it'll be created.
    The parameter is the name of the file.'''
    try:
        a = open(name, 'rt')
        a.close()
    except:
        a = open(name, 'wt+')
        a.close()
        print('File created successfully.')
    else:
        print('File already exists.')


# CONNECTING WITH THE DATABASE
engine = create_engine('sqlite:///system.db')

# CREATING THE SESSION
Session = sessionmaker(bind=engine)
session = Session()

# MAPPING
Base = declarative_base()


# CREATING THE CLASS
class System(Base):
    '''Creating the class/table on the Database'''

    __tablename__ = 'system'
    '''Table's name on the DB'''

    id = Column(Integer, primary_key=True)
    user = Column(String(20), nullable=False)
    name = Column(String(50), nullable=False)
    email = Column(String(30), nullable=False)
    passwd = Column(String(35), nullable=False)


Base.metadata.create_all(engine)
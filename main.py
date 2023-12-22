from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from system import System
from time import sleep

# CONNECTING TO THE DB
engine = create_engine('sqlite:///system.db')

# CREATING A SESSION
Session = sessionmaker(bind=engine)
session = Session()


# FILTERING THE INPUT
def user():
    # Filtering the input for User Column.
    user = str(input('Username: ')).strip().lower()[0:20]
    return user


def name():
    # Creating a pattern for Names.
    while True:
        try:
            name = str(input('Your full name: ')).strip().title()[0:50]
            for letter in name:
                if letter.isalpha() or letter == ' ':
                    pass
                else:
                    raise ValueError
        except:
            print('Only letter and spaces are accepted.')
        else:
            return name


def email():
    # Creating a pattern for Email Column.
    while True:
        email = str(input('Email: ')).strip().lower()[0:30]
        if '@' not in email:
            email += '@gmail.com'
        return email


def passwd():
    from hashlib import sha256
    # Creating a pattern for the password
    while True:
        passwd = str(input('Password: ')).strip()
        if not any(letter.isupper() for letter in passwd):
            print('Your password MUST contain an upper case letter.')
        elif not any(letter.isdigit() for letter in passwd):
            print('Your password MUST contain a number.')
        elif len(passwd) < 8 and len(passwd) > 20:
            print('No less than 8 and no more than 20 letter/numbers.')
        else:
            passwd = sha256(passwd.encode()).hexdigest()
            return passwd


# INSERTING DATA
def insert_data():
    # Inserting the data into the Db only if the email is not into the database
    person = System(user=user(),
            name=name(),
            email=email(),
            passwd=passwd())
    try:
        check_email = lambda x: session.query(System).filter(System.email == person.email).first() is not None
        exists = check_email(person.email)
        if exists:
            raise ValueError
        else:
            session.add(person)
    except:
        print(f'\033[31m{person.name} NOT ADDED TO THE DATABASE\033[m')
        session.rollback()
    else:
        print(f'{person.name} SUCCESSFULLY ADDED.')
        session.commit()
    finally:
        session.close()


# READING DATA
def read_table():
    # Printing the entire Db
    data = session.query(System).all()
    print(f'\033[1;30;44m{"USERNAME":<20}{"FULL NAME":<50}{"EMAIL":<30}{"PASSWORD":<35}\033[m')
    for line in data:
        print(f'{line.user:<20}{line.name:<50}{line.email:<30}{line.passwd:<35}')
    session.close()


def read_line(cond):
    # Printing a specific search
    try:
        data = session.query(System).filter(cond)
        print(f'\033[1;30;44m{"USERNAME":<20}{"FULL NAME":<50}{"EMAIL":<30}{"PASSWORD":<35}\033[m')
        for line in data:
            print(f'{line.user:<20}{line.name:<50}{line.email:<30}{line.passwd:<35}')
    except:
        print('\033[31mEMAIL NOT FOUND\033[m')
    finally:
        session.close()


# FILTERING RESULTS
def filter_email():
    # Returning a specific result
    email = str(input('Type your email: ')).strip().lower()
    if '@' not in email:
        email += '@gmail.com'
    check_email = lambda email: session.query(System).filter(System.email == email).first() is not None
    exists = check_email(email)
    if exists:
        cond = System.email == email
        return cond
    else:
        return 0


# UPDATING DATA
def update_data():
    try:
        data = session.query(System).filter(filter_email())
        print('Now type the new values:')
        for info in data:
            info.user = user()
            info.name = name()
            info.email = email()
            info.passwd = passwd()
        session.commit()
        session.close()
        print(f'UPDATED SUCCESSFULLY')
    except:
        print(f'\033[31mEMAIL NOT FOUND.\033[m')
    finally:
        session.close()


def update_passwd():
    try:
        data = session.query(System).filter(filter_email())
        print('Insert the new password:')
        for info in data:
            info.passwd = passwd()
        session.commit()
        session.close()
        print(f'UPDATED SUCCESSFULLY')
    except:
        print(f'\033[31mEMAIL NOT FOUND.\033[m')
    finally:
        session.close()


# DELETING DATA
def del_data():
    try:
        data = session.query(System).filter(filter_email()).first()
        print(f'{data.name} SUCCESSFULLY DELETED.')
        session.delete(data)
        session.commit()
    except:
        session.rollback()
        print('\033[31mEMAIL NOT FOUND\033[m')
    finally:
        session.close()


# IMPLEMENTING CRIPTOGRAPHY
def sign_in():
    from hashlib import sha256
    try:
        data = session.query(System).filter(filter_email())
    except:
        print('\033[31mEMAIL NOT FOUND\033[m')
    else:
        login_passwd = str(input('Password: ')).strip()
        login_passwd = sha256(login_passwd.encode()).hexdigest()
        for info in data:
            if login_passwd == info.passwd:
                print('SUCCESSFULLY LOGGED IN')
            else:
                print('\033[31mWRONG PASSWORD\033[m')        


while True:
    print(f'\033[1;30;44m{"MAIN MENU":^135}\033[m')
    try:
        print(f'\033[34m[1] READ DATABASE\n[2] SEARCH BY EMAIL\n[3] SIGN UP\n[4] UPDATE INFORMATION\n[5] DELETE PERSON\n[6] CHANGE PASSWORD\n[7] SIGN IN\n[8] EXIT\033[m')
        opt = int(input('Choose your option: '))
        assert 1 <= opt <= 8
    except KeyboardInterrupt:
        break
    except:
        print('\033[31mINVALID OPTION\033[m')
        sleep(1)
    else:
        if opt == 1:
            read_table()
            sleep(3)
        elif opt == 2:
            read_line(filter_email())
            sleep(3)
        elif opt == 3:
            insert_data()
            sleep(3)
        elif opt == 4:
            update_data()
            sleep(3)
        elif opt == 5:
            del_data()
            sleep(3)
        elif opt == 6:
            update_passwd()
            sleep(3)
        elif opt == 7:
            sign_in()
            sleep(3)
        elif opt == 8:
            print('\033[34mPROGRAM FINISHED.\033[m')
            sleep(3)
            break
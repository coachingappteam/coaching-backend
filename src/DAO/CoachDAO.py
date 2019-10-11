"""
This Class contain DAO methods for the tables of Coach, Payment, Athletes, Teams, Member, Focus
"""
import psycopg2
import datetime
import hashlib

from src.ORM.CoachingORM import Database, Coach


class CoachDAO:

    def __init__(self):

        self.conn = Database()

    # ============================== Create Methods =========================== #

    '''
    Add a new Coach
    '''
    def createCoach(self, password, firstName, lastName, phone, email, prefersImperial):
        coach = Coach(password=str(hashlib.md5(password.encode()).hexdigest()), firstName=firstName, lastName=lastName,
                      email=email, phone=phone, prefersImperial=prefersImperial)
        session = self.conn.getNewSession()
        session.add(coach)
        session.commit()
        session.close()

    # ============================== Read Methods =========================== #

    '''
    Read Coach
    '''
    def readCoach(self, email, password):
        session = self.conn.getNewSession()
        hashed = str(hashlib.md5(password.encode()).hexdigest())
        result = session.query(Coach).filter(Coach.email == email,
                                             Coach.password == hashed).first()
        session.close()
        return result

    '''
    Read Email
    '''
    def existsEmail(self, email):
        session = self.conn.getNewSession()
        result = session.query(Coach).filter(Coach.email == email).first()
        session.close()
        return result is not None

    # ============================== Update Methods =========================== #
    '''
    Update Coach
    '''
    def updatePassword(self, email, password):
        session = self.conn.getNewSession()
        hashed = str(hashlib.md5(password.encode()).hexdigest())
        result = session.query(Coach).filter(Coach.email == email).update({Coach.password: hashed})
        session.commit()
        session.close()
        return result

    '''
    Delete Coach
    '''
    def deleteCoach(self, email, password):
        session = self.conn.getNewSession()
        hashed = str(hashlib.md5(password.encode()).hexdigest())
        result = session.query(Coach).filter(Coach.email == email,
                                             Coach.password == hashed).update({Coach.isActiveUser: False})
        session.close()
        return result

    # ============================== Delete Methods =========================== #


# DAO = CoachDAO()
#
# DAO.createCoach('HelloWorld1234', 'Al', 'Pachino', '7877877788', 'a@bc.com', True)
#
# r = DAO.readCoach('a@bc.com', 'HelloWorld1234')
#
# print('Done')
# print(r)

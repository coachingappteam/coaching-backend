"""
This Class contain DAO methods for the entity Security
"""
import secrets
from datetime import datetime
from src.ORM.CoachingORM import Database, Security


class SecurityDAO:

    def __init__(self):

        self.conn = Database()

    # ============================== Create Methods =========================== #
    def createToken(self, coachID):

        coachToken = self.getToken(coachID)

        if coachToken is not None:
            return coachToken.token

        session = self.conn.getNewSession()
        token = None

        while token is None:
            token = secrets.token_urlsafe()
            if self.checkToken(token):
                token = None

        security = Security(coachID=coachID, token=token)

        session.add(security)
        session.commit()
        session.close()

        return token

    # ============================== Read Methods =========================== #
    def checkToken(self, token):
        session = self.conn.getNewSession()

        result = session.query(Security).filter(Security.token == token).first()

        session.close()

        return result is not None

    def getToken(self, coachID):
        session = self.conn.getNewSession()

        result = session.query(Security).filter(Security.coachID == coachID).first()

        session.close()

        return result

    def getSecurity(self, token):
        session = self.conn.getNewSession()

        result = session.query(Security).filter(Security.token == token).first()

        session.close()

        return result

    # ============================== Update Methods =========================== #
    def validateToken(self, token):
        session = self.conn.getNewSession()

        if not self.checkToken(token):
            return False

        record = self.getSecurity(token)

        t1 = record.lastAccess
        t2 = datetime.today()

        days = t2 - t1

        if days.days > 5:

            self.deleteToken(token)
        else:
            session.query(Security).filter(Security.token == token).update({Security.lastAccess: datetime.today()})

        session.commit()
        session.close()

        return days.days > 5

    # ============================== Delete Methods =========================== #
    def deleteToken(self, token):
        session = self.conn.getNewSession()

        record = self.checkToken(token)

        session.delete(record)
        session.commit()
        session.close()


# DAO = SecurityDAO()
#
# token = DAO.createToken('3e3ca73a-6f67-4142-ae39-3fd4d5fc897b')
# print(token)
#
# print(DAO.validateToken(token))
#
# DAO.deleteToken(token)
#
# print(DAO.validateToken(token))




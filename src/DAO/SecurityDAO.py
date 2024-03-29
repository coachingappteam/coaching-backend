"""
This Class contain DAO methods for the entity Security
"""
import os
import json
import secrets
from datetime import datetime
from src.ORM.CoachingORM import Database, Security, Coach


class SecurityDAO:

    def __init__(self):

        self.conn = Database()

    # ============================== Create Methods =========================== #
    def createToken(self, coachID):

        coachToken = self.getToken(coachID)

        if coachToken is not None:
            self.deleteToken(coachToken.token)

        session = self.conn.getNewSession()
        token = None

        while token is None:
            token = secrets.token_urlsafe()
            if self.checkToken(token):
                token = None

        security = Security(coachID=str(coachID), token=token)

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

        result = session.query(Security).filter(Security.coachID == str(coachID)).first()

        session.close()

        return result

    def getSecurity(self, token):
        session = self.conn.getNewSession()

        result = session.query(Security).filter(Security.token == token).first()

        session.close()

        return result

    def getTokenOwner(self, token):

        self.validateToken(token)

        session = self.conn.getNewSession()

        result = session.query(Security).filter(Security.token == token).first()

        session.close()
        if result is None:
            return None
        return result.coachID

    def getIfAdmin(self, token):

        coachID = self.getTokenOwner(token)

        session = self.conn.getNewSession()

        coach = session.query(Coach).filter(Coach.coachID == coachID).first()
        session.close()

        if coach is None:
            return False
        return coach.isAdmin

    def getIfML(self, token):
        if os.environ.get('AZURE_CODE'):
            azureToken = os.environ.get('AZURE_CODE')
        else:
            with open('config.json') as f:
                obj = json.load(f)
                azureToken = obj['AZURE_CODE']

        return token == azureToken

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

        return days.days < 5

    # ============================== Delete Methods =========================== #
    def deleteToken(self, token):
        session = self.conn.getNewSession()

        session.query(Security).filter(Security.token == token).delete()
        session.commit()
        session.close()

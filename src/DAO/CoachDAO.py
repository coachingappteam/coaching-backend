"""
This Class contain DAO methods for the tables of Coach, Payment, Athletes, Teams, Member, Focus, Support, Attendance
"""
from datetime import datetime
import hashlib

from sqlalchemy import or_

from src.ORM.CoachingORM import Database, Coach, Team, Athlete, Payment, Focus, Member, Support, Attendance


class CoachDAO:

    def __init__(self):

        self.conn = Database()

    # ============================== Create Methods =========================== #

    '''
    Add a new Coach
    '''
    def createCoach(self, password, firstName, lastName, phone, email):
        coach = Coach(password=str(hashlib.md5(password.encode()).hexdigest()), firstName=firstName, lastName=lastName,
                      email=email, phone=phone)
        session = self.conn.getNewSession()
        session.add(coach)
        session.commit()
        session.close()

    def createAthlete(self, coachID, firstName, lastName, email, phone, sex, birthdate):
        athl = Athlete(coachID=coachID, firstName=firstName, lastName=lastName, email=email, phone=phone, sex=sex, birthdate = birthdate)
        session = self.conn.getNewSession()
        session.add(athl)
        session.commit()
        session.close()

    def createPayment(self, coachID, recieptID, payTotal, paySource):
        payment = Payment(coachID=coachID, sourceReceiptID=recieptID, payTotal=payTotal, paymentSource=paySource)
        session = self.conn.getNewSession()
        session.add(payment)
        session.commit()
        session.close()

    def createTeam(self, coachID, sportID, teamName, teamDescription):
        team = Team(coachID=coachID, sportID=sportID, teamName=teamName, teamDescription=teamDescription)
        session = self.conn.getNewSession()
        session.add(team)
        session.commit()
        session.close()

    def createMember(self, athleteID, teamID):
        member = Member(athleteID=athleteID, teamID=teamID)
        session = self.conn.getNewSession()
        session.add(member)
        session.commit()
        session.close()

    def createFocus(self, athleteID, roleID, isPrimaryFocus):
        focus = Focus(athleteID=athleteID, roleID=roleID, isPrimaryFocus=isPrimaryFocus)
        session = self.conn.getNewSession()
        session.add(focus)
        session.commit()
        session.close()

    def createSupport(self, coachID, teamID):
        support = Support(coachID=coachID, teamID=teamID)
        session = self.conn.getNewSession()
        session.add(support)
        session.commit()
        session.close()

    def createAttendance(self, sessionID, athleteID):
        attendance = Attendance(sessionID=sessionID, athleteID=athleteID)
        session = self.conn.getNewSession()
        session.add(attendance)
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
    Read Teams
    '''
    def readTeamsForCoach(self, coachID):
        session = self.conn.getNewSession()
        result = session.query(Team).filter(Team.coachID == coachID).all()
        return result

    '''
    Read Coach
    '''
    def readCoachByID(self, coachID):
        session = self.conn.getNewSession()
        result = session.query(Coach).filter(Coach.coachID == coachID).first()
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

    '''
    Read recent payment
    '''
    def readLatestsPayment(self, coachID):
        session = self.conn.getNewSession()
        result = session.query(Payment).filter(Payment.coachID == coachID).order_by(Payment.payDate.asc())
        session.close()
        return result.first()

    # ============================== Update Methods =========================== #
    '''
    Update Coach
    '''
    def updatePassword(self, coachID, password):
        session = self.conn.getNewSession()
        hashed = str(hashlib.md5(password.encode()).hexdigest())
        result = session.query(Coach).filter(Coach.coachID == coachID).update({Coach.password: hashed})
        session.commit()
        session.close()
        return result

    '''
    Update membership
    '''
    def updateMemebership(self, coachID):

        lastPayment = self.readLatestsPayment(coachID)

        t1 = lastPayment.lastAccess
        t2 = datetime.today()

        days = t2 - t1

        session = self.conn.getNewSession()

        if days.days > lastPayment.membershipLength:
            session.query(Coach).filter(Coach.coachID == coachID).update({Coach.isActiveMember: True})
        else:
            session.query(Coach).filter(Coach.coachID == coachID).update({Coach.isActiveMember: False})

    # ============================== Delete Methods =========================== #
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




    def readIfTeamFromCoach(self, coachID, teamID):
        session = self.conn.getNewSession()
        result = session.query(Team).filter(Team.teamID == teamID, Team.coachID == coachID).first()
        return result is not None

    def searchCoach(self, search):
        session = self.conn.getNewSession()
        result = session.query(Coach).filter(or_(Coach.firstName.like(search), Coach.lastName.like(search), Coach.email.like(search))).all()
        return result

    def readIfAthleteFromCoach(self, coachID, athleteID):
        session = self.conn.getNewSession()
        result = session.query(Athlete).filter(Athlete.athleteID == athleteID, Athlete.coachID == coachID).first()
        return result is not None

    def updateCoach(self, coachID, fname, lname, phone, email):
        session = self.conn.getNewSession()
        update = dict()
        if fname is not None:
            update[Coach.firstName] = fname
        if lname is not None:
            update[Coach.lastName] = lname
        if phone is not None:
            update[Coach.phone] = phone
        if email is not None:
            update[Coach.email] = email
        result = session.query(Coach).filter(Coach.coachID == coachID).update(update)
        session.commit()
        session.close()
        return result

# DAO = CoachDAO()
#
# DAO.createCoach('HelloWorld1234', 'Al', 'Pachino', '7877877788', 'a@bc.com', True)
#
# r = DAO.readCoach('a@bc.com', 'HelloWorld1234')
#
# print('Done')
# print(r)

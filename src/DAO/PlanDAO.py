"""
This Class contain DAO methods for the tables of Training Plan, Session, Practice, Results
"""
from sqlalchemy import or_

from src.ORM.CoachingORM import Database, TrainingPlan, Session, Practice, Result, Exercise, Team, Support


class PlanDAO:

    def __init__(self):

        self.conn = Database()

    # ============================== Create Methods =========================== #

    def createTrainingPlan(self, teamID, parentPlanID, title, startDate, endDate, planDescription):
        trainingPlan = TrainingPlan(teamID=teamID, parentPlanID=parentPlanID, title=title,
                                    isParentPlan=parentPlanID is None, startDate=startDate, endDate=endDate,
                                    planDescription=planDescription)
        session = self.conn.getNewSession()
        session.add(trainingPlan)
        session.commit()
        session.close()

    def createSession(self, planID, parentSessionID, sessionTitle, location, isCompetition, sessionDate, sessionDescription):
        planSession = Session(planID=planID, parentSessionID=parentSessionID, sessionTitle=sessionTitle, location=location, isCompetition=isCompetition,
                              sessionDate=sessionDate, sessionDescription=sessionDescription)
        session = self.conn.getNewSession()
        session.add(planSession)
        session.commit()
        session.close()

    def createPractice(self, exerciseID, sessionID, repetitions):
        practice = Practice(exerciseID=exerciseID, sessionID=sessionID, repetitions=repetitions)
        session = self.conn.getNewSession()
        session.add(practice)
        session.commit()
        session.close()

    def createResult(self, practiceID, athleteID, unitID, resultDate, resultDescription):
        result = Result(practiceID=practiceID, athleteID=athleteID, unitID=unitID, resultDate=resultDate, resultDescription=resultDescription)
        session = self.conn.getNewSession()
        session.add(result)
        session.commit()
        session.close()

    # ============================== Read Methods =========================== #

    def readPracticesInSession(self, sessionID):
        session = self.conn.getNewSession()
        result = session.query(Practice).filter(Practice.sessionID == sessionID).all()
        return result

    def readExercisesInSession(self, sessionID):
        session = self.conn.getNewSession()
        result = session.query(Practice, Exercise).filter(Practice.sessionID == sessionID).all()
        return result

    def readResultForSession(self, sessionID):
        session = self.conn.getNewSession()
        result = session.query(Practice, Result).filter(Practice.sessionID == sessionID).all()
        return result

    def readIfCoachManagePlan(self, coachID, planID):
        session = self.conn.getNewSession()
        result = session.query(TrainingPlan, Team).filter(TrainingPlan.teamID == Team.teamID, 
                                                          TrainingPlan.planID == planID, 
                                                          Team.coachID == coachID).first()
        return result is not None
    
    def readIfCoachSupportPlan(self, coachID, planID):
        session = self.conn.getNewSession()
        result = session.query(TrainingPlan, Team, Support).filter(TrainingPlan.teamID == Team.teamID, 
                                                          TrainingPlan.planID == planID, Support.teamID == Team.teamID, 
                                                          Support.coachID == coachID).first()
        return result is not None

    def readPlanByID(self, planID):
        session = self.conn.getNewSession()
        result = session.query(TrainingPlan).filter(TrainingPlan.planID == planID).first()
        
        return result

    def searchPlans(self, teamID, search):
        session = self.conn.getNewSession()
        result = session.query(TrainingPlan).filter(TrainingPlan.teamID == teamID,
                                                          TrainingPlan.isDeleted == False, 
                                                          TrainingPlan.parentPlanID == None,
            or_(TrainingPlan.title.like(search), TrainingPlan.planDescription.like(search), 
                TrainingPlan.startDate.like(search), TrainingPlan.endDate.like(search))).all()
        return result

    def updatePlan(self, planID, title, startDate, endDate, planDescription):

        session = self.conn.getNewSession()
        update = dict()
        if title is not None and not title == '':
            update[TrainingPlan.title] = title
        if startDate is not None and not startDate == '':
            update[TrainingPlan.startDate] = startDate
        if endDate is not None and not endDate == '':
            update[TrainingPlan.endDate] = endDate
        if planDescription is not None and not planDescription == '':
            update[TrainingPlan.planDescription] = planDescription

        result = session.query(TrainingPlan).filter(TrainingPlan.planID == planID).update(update)
        session.commit()
        session.close()
        return result

    def deletePlan(self, planID, isDeleted):
        session = self.conn.getNewSession()
        update = dict()
        update[TrainingPlan.isDeleted] = isDeleted
        result = session.query(TrainingPlan).filter(TrainingPlan.planID == planID).update(update)
        session.commit()
        session.close()
        return result

    def readIfCoachManageSession(self, coachID, sessionID):
        session = self.conn.getNewSession()
        result = session.query(Session, TrainingPlan, Team).filter(TrainingPlan.teamID == Team.teamID,
                                                          TrainingPlan.planID == Session.planID,
                                                          Session.sessionID == sessionID,
                                                          Team.coachID == coachID).first()
        return result is not None

    def readIfCoachSupportSession(self, coachID, sessionID):
        session = self.conn.getNewSession()
        result = session.query(Session, TrainingPlan, Team, Support).filter(TrainingPlan.teamID == Team.teamID,
                                                          TrainingPlan.planID == Session.planID,
                                                          Support.teamID == Team.teamID,
                                                          Session.sessionID == sessionID,
                                                          Support.coachID == coachID).first()
        return result is not None

    def readSessionByID(self, sessionID):
        session = self.conn.getNewSession()
        result = session.query(Session).filter(Session.sessionID == sessionID).first()

        return result

    def searchSessions(self, planID, search):
        session = self.conn.getNewSession()
        result = session.query(Session).filter(Session.planID == planID,
                                                          Session.isDeleted == False,
                                                          Session.parentSessionID == None,
            or_(Session.sessionDescription.like(search), Session.sessionDate.like(search),
                Session.sessionTitle.like(search))).all()
        return result

    def updateSession(self, sessionID, sessionTitle, location, sessionDate, sessionDescription, isCompetition):
        session = self.conn.getNewSession()
        update = dict()
        if sessionTitle is not None and not sessionTitle == '':
            update[Session.sessionTitle] = sessionTitle
        if location is not None and not location == '':
            update[Session.location] = location
        if sessionDate is not None and not sessionDate == '':
            update[Session.sessionDate] = sessionDate
        if sessionDescription is not None and not sessionDescription == '':
            update[Session.sessionDescription] = sessionDescription
        if isCompetition is not None and not isCompetition == '':
            update[Session.isCompetition] = isCompetition
        result = session.query(Session).filter(Session.sessionID == sessionID).update(update)
        session.commit()
        session.close()
        return result

    def deleteSession(self, sessionID, isDeleted):
        session = self.conn.getNewSession()
        update = dict()
        update[Session.isDeleted] = isDeleted
        result = session.query(Session).filter(Session.sessionID == sessionID).update(update)
        session.commit()
        session.close()
        return result

    def searchSubPlans(self, parentPlanID, search):
        session = self.conn.getNewSession()
        result = session.query(TrainingPlan).filter(TrainingPlan.isDeleted == False,
                                                          TrainingPlan.parentPlanID == parentPlanID,
            or_(TrainingPlan.title.like(search), TrainingPlan.planDescription.like(search),
                TrainingPlan.startDate.like(search), TrainingPlan.endDate.like(search))).all()
        return result

    def searchSubSessions(self, parentSessionID, search):
        session = self.conn.getNewSession()
        result = session.query(Session).filter(Session.isDeleted == False, Session.parentSessionID == parentSessionID,
                                               or_(Session.sessionDescription.like(search),
                                                   Session.sessionDate.like(search),
                                                   Session.sessionTitle.like(search))).all()
        return result

    def readPracticeByID(self, practiceID):
        session = self.conn.getNewSession()
        result = session.query(Practice, Exercise).filter(Practice.exerciseID == Exercise.exerciseID,
                                                          Practice.practiceID == practiceID).first()

        return result

    def readIfCoachManagePractice(self, coachID, practiceID):
        session = self.conn.getNewSession()
        result = session.query(Practice, Session, TrainingPlan, Team).filter(TrainingPlan.teamID == Team.teamID,
                                                          Practice.sessionID == Session.sessionID,
                                                          TrainingPlan.planID == Session.planID,
                                                          Practice.practiceID == practiceID,
                                                          Team.coachID == coachID).first()
        return result is not None

    def readIfCoachSupportPractice(self, coachID, practiceID):
        session = self.conn.getNewSession()
        result = session.query(Practice, Session, TrainingPlan, Team, Support).filter(
                                                          TrainingPlan.teamID == Team.teamID,
                                                          Practice.sessionID == Session.sessionID,
                                                          TrainingPlan.planID == Session.planID,
                                                          Practice.practiceID == practiceID,
                                                          Team.teamID == Support.teamID,
                                                          Support.coachID == coachID).first()
        return result is not None

    def searchPractices(self, sessionID, search):
        session = self.conn.getNewSession()
        result = session.query(Practice, Exercise).filter(Practice.sessionID == sessionID,
                                                          Practice.isDeleted == False,
            or_(Practice.repetitions.like(search), Exercise.exerciseName.like(search),
                Exercise.exerciseDescription.like(search), Exercise.style.like(search),
                Exercise.measure.like(search))).all()
        return result

    def updatePractice(self, practiceID, repetitions):
        session = self.conn.getNewSession()
        update = dict()
        if repetitions is not None and not repetitions == '':
            update[Practice.repetitions] = repetitions
        result = session.query(Practice).filter(Practice.practiceID == practiceID).update(update)
        session.commit()
        session.close()
        return result
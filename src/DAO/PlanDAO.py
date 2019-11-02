"""
This Class contain DAO methods for the tables of Training Plan, Session, Practice, Results
"""

from src.ORM.CoachingORM import Database, TrainingPlan, Session, Practice, Result, Exercise


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

    def readTrainingPlansForTeam(self, teamID):
        session = self.conn.getNewSession()
        result = session.query(TrainingPlan).filter(TrainingPlan.teamID == teamID, TrainingPlan.parentPlanID == None).all()
        return result

    def readSessionsForTrainingPlan(self, planID):
        session = self.conn.getNewSession()
        result = session.query(Session).filter(Session.planID == planID, Session.parentSessionID == None).all()
        return result

    def readSubTrainingPlansForTeam(self, teamID, parentPlanID):
        session = self.conn.getNewSession()
        result = session.query(TrainingPlan).filter(TrainingPlan.teamID == teamID, TrainingPlan.parentPlanID == parentPlanID).all()
        return result

    def readSubSessionsForTrainingPlan(self, planID, parentSessionID):
        session = self.conn.getNewSession()
        result = session.query(Session).filter(Session.planID == planID, Session.parentSessionID == parentSessionID).all()
        return result

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
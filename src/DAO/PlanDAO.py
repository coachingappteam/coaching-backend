"""
This Class contain DAO methods for the tables of Training Plan, Session, Practice, Results
"""

from src.ORM.CoachingORM import Database, TrainingPlan, Session, Practice, Result


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

    def createSession(self, planID, sessionTitle, location, isCompetition, sessionDate, sessionDescription):
        planSession = Session(planID=planID, sessionTitle=sessionTitle, location=location, isCompetition=isCompetition,
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
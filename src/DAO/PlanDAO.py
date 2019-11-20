"""
This Class contain DAO methods for the tables of Training Plan, Session, Practice, Results and Analyzed
"""
from sqlalchemy import or_, func

from src.ORM.CoachingORM import Database, TrainingPlan, Session, Practice, Result, Exercise, Team, Support, Unit, \
    Improves, Role, Athlete, Analyzed


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
        session.flush()
        session.refresh(trainingPlan)
        id = trainingPlan.planID
        session.commit()
        session.close()
        return id

    def createSession(self, planID, parentSessionID, sessionTitle, location, isCompetition, isMain, sessionDate, sessionDescription):
        planSession = Session(planID=planID, parentSessionID=parentSessionID, sessionTitle=sessionTitle, location=location, isCompetition=isCompetition,
                              sessionDate=sessionDate, sessionDescription=sessionDescription, isMain=isMain)
        session = self.conn.getNewSession()
        session.add(planSession)
        session.flush()
        session.refresh(planSession)
        id = planSession.sessionID
        session.commit()
        session.close()
        return id

    def createPractice(self, exerciseID, sessionID, repetitions, unitID, measure):
        practice = Practice(exerciseID=exerciseID, sessionID=sessionID, repetitions=repetitions, unitID=unitID, measure=measure)
        session = self.conn.getNewSession()
        session.add(practice)
        session.flush()
        session.refresh(practice)
        id = practice.practiceID
        session.commit()
        session.close()
        return id

    def createResult(self, practiceID, athleteID, unitID, result, resultDate, resultDescription):
        result = Result(practiceID=practiceID, athleteID=athleteID, unitID=unitID, result=result, resultDate=resultDate,resultDescription=resultDescription)
        session = self.conn.getNewSession()
        session.add(result)
        session.flush()
        session.refresh(result)
        id = result.resultID
        session.commit()
        session.close()
        return id

    def createAnalyzed(self, athleteID, roleID, sessionID, performance):
        result = Analyzed(athleteID=athleteID, roleID=roleID, sessionID=sessionID, performance=performance)
        session = self.conn.getNewSession()
        session.add(result)
        session.flush()
        session.refresh(result)
        id = result.analyzedID
        session.commit()
        session.close()
        return id

    # ============================== Read Methods =========================== #

    def readPracticesInSession(self, sessionID):
        session = self.conn.getNewSession()
        result = [e for e in session.query(Practice).filter(Practice.sessionID == sessionID).all()]
        session.close()
        return result

    def readExercisesInSession(self, sessionID):
        session = self.conn.getNewSession()
        result = [e for e in session.query(Practice, Exercise).filter(Practice.sessionID == sessionID).all()]
        session.close()
        return result

    def readResultForSession(self, sessionID):
        session = self.conn.getNewSession()
        result = [e for e in session.query(Practice, Result).filter(Practice.sessionID == sessionID).all()]
        session.close()
        return result

    def readIfCoachManagePlan(self, coachID, planID):
        session = self.conn.getNewSession()
        result = session.query(TrainingPlan, Team).filter(TrainingPlan.teamID == Team.teamID, 
                                                          TrainingPlan.planID == planID, 
                                                          Team.coachID == coachID).first()
        ans = result is not None
        session.close()
        return ans
    
    def readIfCoachSupportPlan(self, coachID, planID):
        session = self.conn.getNewSession()
        result = session.query(TrainingPlan, Team, Support).filter(TrainingPlan.teamID == Team.teamID, 
                                                          TrainingPlan.planID == planID, Support.teamID == Team.teamID, 
                                                          Support.coachID == coachID).first()
        ans = result is not None
        session.close()
        return ans

    def readPlanByID(self, planID):
        session = self.conn.getNewSession()
        result = [e for e in session.query(TrainingPlan).filter(TrainingPlan.planID == planID).all()]
        session.close()
        if len(result) <= 0:
            return None
        return result[0]

    def searchPlans(self, teamID, search):
        session = self.conn.getNewSession()
        result = [e for e in session.query(TrainingPlan).filter(TrainingPlan.teamID == teamID,
                                                          TrainingPlan.isDeleted == False, 
                                                          TrainingPlan.parentPlanID == None,
            or_(TrainingPlan.title.like(search), TrainingPlan.planDescription.like(search))).all()]
        session.close()
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
        if len(update) <= 0:
            return None
        result = session.query(TrainingPlan).filter(TrainingPlan.planID == planID).update(update)
        session.commit()
        session.close()
        return result

    def deletePlan(self, planID, isDeleted):
        session = self.conn.getNewSession()
        update = dict()
        update[TrainingPlan.isDeleted] = isDeleted
        if len(update) <= 0:
            return None
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
        ans = result is not None
        session.close()
        return ans

    def readIfCoachSupportSession(self, coachID, sessionID):
        session = self.conn.getNewSession()
        result = session.query(Session, TrainingPlan, Team, Support).filter(TrainingPlan.teamID == Team.teamID,
                                                          TrainingPlan.planID == Session.planID,
                                                          Support.teamID == Team.teamID,
                                                          Session.sessionID == sessionID,
                                                          Support.coachID == coachID).first()
        ans = result is not None
        session.close()
        return ans

    def readSessionByID(self, sessionID):
        session = self.conn.getNewSession()
        result = [e for e in session.query(Session).filter(Session.sessionID == sessionID).all()]
        session.close()
        if len(result) <= 0:
            return None
        return result[0]

    def searchSessions(self, planID, search):
        session = self.conn.getNewSession()
        result = [e for e in session.query(Session).filter(Session.planID == planID,
                                                          Session.isDeleted == False,
                                                          Session.parentSessionID == None,
            or_(Session.sessionDescription.like(search), Session.sessionTitle.like(search))).all()]
        session.close()
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
        if isCompetition is not None:
            update[Session.isCompetition] = isCompetition
        if len(update) <= 0:
            return None
        result = session.query(Session).filter(Session.sessionID == sessionID).update(update)
        session.commit()
        session.close()
        return result

    def deleteSession(self, sessionID, isDeleted):
        session = self.conn.getNewSession()
        update = dict()
        update[Session.isDeleted] = isDeleted
        if len(update) <= 0:
            return None
        result = session.query(Session).filter(Session.sessionID == sessionID).update(update)
        session.commit()
        session.close()
        return result

    def searchSubPlans(self, parentPlanID, search):
        session = self.conn.getNewSession()
        result = [e for e in session.query(TrainingPlan).filter(TrainingPlan.isDeleted == False,
                                                          TrainingPlan.parentPlanID == parentPlanID,
            or_(TrainingPlan.title.like(search), TrainingPlan.planDescription.like(search))).all()]
        session.close()
        return result

    def searchSubSessions(self, parentSessionID, search):
        session = self.conn.getNewSession()
        result = [e for e in session.query(Session).filter(Session.isDeleted == False,
                                                           Session.parentSessionID == parentSessionID,
                                               or_(Session.sessionDescription.like(search),
                                                   Session.sessionTitle.like(search))).all()]
        session.close()
        return result

    def readPracticeByID(self, practiceID):
        session = self.conn.getNewSession()
        result = [e for e in session.query(Practice, Exercise).filter(Practice.exerciseID == Exercise.exerciseID,
                                                          Practice.practiceID == practiceID).all()]
        session.close()
        if len(result) <= 0:
            return None
        return result[0]

    def readIfCoachManagePractice(self, coachID, practiceID):
        session = self.conn.getNewSession()
        result = session.query(Practice, Session, TrainingPlan, Team).filter(TrainingPlan.teamID == Team.teamID,
                                                          Practice.sessionID == Session.sessionID,
                                                          TrainingPlan.planID == Session.planID,
                                                          Practice.practiceID == practiceID,
                                                          Team.coachID == coachID).first()
        ans = result is not None
        session.close()
        return ans

    def readIfCoachSupportPractice(self, coachID, practiceID):
        session = self.conn.getNewSession()
        result = session.query(Practice, Session, TrainingPlan, Team, Support).filter(
                                                          TrainingPlan.teamID == Team.teamID,
                                                          Practice.sessionID == Session.sessionID,
                                                          TrainingPlan.planID == Session.planID,
                                                          Practice.practiceID == practiceID,
                                                          Team.teamID == Support.teamID,
                                                          Support.coachID == coachID).first()
        ans = result is not None
        session.close()
        return ans

    def searchPractices(self, sessionID, search):
        session = self.conn.getNewSession()
        result = [e for e in session.query(Practice, Exercise, Unit).filter(Practice.sessionID == sessionID,
                                                          Practice.isDeleted == False, Unit.unitID == Practice.unitID,
            or_(Practice.repetitions.like(search), Exercise.exerciseName.like(search),
                Exercise.exerciseDescription.like(search), Exercise.style.like(search), Unit.unit.like(search))).all()]
        session.close()
        return result

    def updatePractice(self, practiceID, repetitions, unitID, measure):
        session = self.conn.getNewSession()
        update = dict()
        if repetitions is not None and not repetitions == '':
            update[Practice.repetitions] = repetitions
        if unitID is not None and not unitID == '':
            update[Practice.unitID] = unitID
        if measure is not None and not measure == '':
            update[Practice.measure] = measure
        if len(update) <= 0:
            return None
        result = session.query(Practice).filter(Practice.practiceID == practiceID).update(update)
        session.commit()
        session.close()
        return result

    def deletePractice(self, practiceID, isDeleted):
        session = self.conn.getNewSession()
        update = dict()
        update[Practice.isDeleted] = isDeleted
        if len(update) <= 0:
            return None
        result = session.query(Practice).filter(Practice.practiceID == practiceID).update(update)
        session.commit()
        session.close()
        return result

    def readIfCoachManageResult(self, coachID, resultID):
        session = self.conn.getNewSession()
        result = session.query(Result, Practice, Session, TrainingPlan, Team).filter(TrainingPlan.teamID == Team.teamID,
                                                          Practice.sessionID == Session.sessionID,
                                                          Result.practiceID == Practice.practiceID,
                                                          TrainingPlan.planID == Session.planID,
                                                          Result.resultID == resultID,
                                                          Team.coachID == coachID).first()
        ans = result is not None
        session.close()
        return ans

    def readIfCoachSupportResult(self, coachID, resultID):
        session = self.conn.getNewSession()
        result = session.query(Result, Practice, Session, TrainingPlan, Team, Support).filter(
                                                          TrainingPlan.teamID == Team.teamID,
                                                          Practice.sessionID == Session.sessionID,
                                                          Result.practiceID == Practice.practiceID,
                                                          TrainingPlan.planID == Session.planID,
                                                          Result.resultID == resultID,
                                                          Team.teamID == Support.teamID,
                                                          Support.coachID == coachID).first()
        ans = result is not None
        session.close()
        return ans

    def updateResult(self, resultID, unitID, result, resultDate, resultDescription):
        session = self.conn.getNewSession()
        update = dict()
        if unitID is not None and not unitID == '':
            update[Result.unitID] = unitID
        if result is not None and not result == '':
            update[Result.result] = result
        if resultDate is not None and not resultDate == '':
            update[Result.resultDate] = resultDate
        if resultDescription is not None and not resultDescription == '':
            update[Result.resultDescription] = resultDescription
        if len(update) <= 0:
            return None
        result = session.query(Result).filter(Result.resultID == resultID).update(update)
        session.commit()
        session.close()
        return result

    def deleteResult(self, resultID):
        session = self.conn.getNewSession()

        session.query(Result).filter(Result.resultID == resultID).delete()
        session.commit()
        session.close()

    def readResultByID(self, resultID):
        session = self.conn.getNewSession()
        result = [e for e in session.query(Result).filter(Result.resultID == resultID).all()]
        session.close()
        if len(result) <= 0:
            return None
        return result[0]

    def searchResultsForAthleteInPractice(self, practiceID, athleteID, search):
        session = self.conn.getNewSession()
        result = [e for e in session.query(Result).filter(Result.practiceID == practiceID, Result.athleteID == athleteID,
            or_(Result.resultDescription.like(search), Result.result.like(search))).all()]
        session.close()
        return result

    def searchResultsInPractice(self, practiceID, search):
        session = self.conn.getNewSession()
        result = [e for e in session.query(Result).filter(Result.practiceID == practiceID,
            or_(Result.resultDescription.like(search), Result.result.like(search))).all()]
        session.close()
        return result

    def searchResultsForAthlete(self, athleteID, search):
        session = self.conn.getNewSession()
        result = [e for e in session.query(Result).filter(Result.athleteID == athleteID,
                                              or_(Result.resultDescription.like(search),
                                                  Result.result.like(search))).all()]
        session.close()
        return result

    def readResultsForAthleteInSession(self, athleteID, sessionID):
        session = self.conn.getNewSession()
        result = [e for e in session.query(Exercise.style, Practice.repetitions, Practice.measure,
                                           func.avg(Result.result).label('avg_result')).
            filter(Session.sessionID == Practice.sessionID, Practice.exerciseID == Exercise.exerciseID,
                   Practice.practiceID == Result.practiceID, Result.athleteID == athleteID,
                   Session.sessionID == sessionID).
            group_by(Exercise.style, Practice.measure, Practice.repetitions).all()]
        session.close()
        return result

    def searchTimeline(self, coachID, search):
        session = self.conn.getNewSession()
        result = [e for e in session.query(Team, TrainingPlan, Session).filter(Team.coachID == coachID,
                                                                   Team.teamID == TrainingPlan.teamID,
                                                                   TrainingPlan.planID == Session.planID,
                                                                   Session.parentSessionID == None,
                                                                   Session.sessionTitle.like(search),
                                                                   Session.sessionDescription.like(search))
            .order_by(Session.sessionDate).all()]
        session.close()
        return result

    def searchSupportTimeline(self, coachID, search):
        session = self.conn.getNewSession()
        result = [e for e in session.query(Support, Team, TrainingPlan, Session).filter(Support.coachID == coachID,
                                                                            Support.teamID == Team.teamID,
                                                                            Team.teamID == TrainingPlan.teamID,
                                                                            TrainingPlan.planID == Session.planID,
                                                                            Session.parentSessionID == None,
                                                                            Session.sessionTitle.like(search),
                                                                            Session.sessionDescription.like(search))\
            .order_by(Session.sessionDate).all()]
        session.close()
        return result

    def searchSessionResultsByAthleteAndRoleID(self, athleteID, roleID):
        session = self.conn.getNewSession()
        result = [e for e in session.query(Athlete.firstName, Athlete.lastName, Role.roleName, Session.sessionDate,
                                          func.avg(Result.result).label('avg_result'),  Unit.unit)
            .filter(Role.roleID == Improves.roleID,
            Improves.exerciseID == Exercise.exerciseID, Exercise.exerciseID == Practice.exerciseID,
        Session.sessionID == Practice.sessionID, Practice.practiceID == Result.practiceID, Unit.unitID == Result.unitID,
        Session.isCompetition == True, Result.athleteID == Athlete.athleteID, Athlete.athleteID == athleteID,
            Role.roleID == roleID).group_by(Athlete.firstName, Athlete.lastName, Role.roleName, Session.sessionDate,
                                            Unit.unitID).order_by(Session.sessionDate).all()]
        session.close()
        return result

    def alreadyAnalyzed(self, sessionID, athleteID, roleID):
        session = self.conn.getNewSession()
        result = session.query(Analyzed).filter(Analyzed.sessionID == sessionID, Analyzed.athleteID == athleteID
                                                , Analyzed.roleID == roleID).first()
        ans = result is not None
        session.close()
        return ans

    def updateAnalyze(self, analyzedID, feedback):
        session = self.conn.getNewSession()
        update = dict()
        if feedback is not None and not feedback == '':
            update[Analyzed.feedback] = feedback
        if len(update) <= 0:
            return None
        result = session.query(Analyzed).filter(Analyzed.analyzedID == analyzedID).update(update)
        session.commit()
        session.close()
        return result

    def readAnalyzeByID(self, analyzedID):
        session = self.conn.getNewSession()
        result = [e for e in session.query(Analyzed).filter(Analyzed.analyzedID == analyzedID).all()]
        session.close()
        if len(result) <= 0:
            return None
        return result[0]

    def searchAnalyzedForAthleteInSession(self, sessionID, athleteID, search):
        session = self.conn.getNewSession()
        result = [e for e in session.query(Analyzed).
            filter(Analyzed.sessionID == sessionID, Analyzed.athleteID == athleteID,
                   Analyzed.roleID == Role.roleID, or_(Role.roleName.like(search),
                                                       Role.roleDescription.like(search))).all()]
        session.close()
        return result

    def searchAnalyzedInSession(self, sessionID, search):
        session = self.conn.getNewSession()
        result = [e for e in session.query(Analyzed).
            filter(Analyzed.sessionID == sessionID,
                   Analyzed.roleID == Role.roleID, or_(Role.roleName.like(search),
                                                       Role.roleDescription.like(search))).all()]
        session.close()
        return result

    def searchAnalyzedForAthlete(self, athleteID, search):
        session = self.conn.getNewSession()
        result = [e for e in session.query(Analyzed).
            filter(Analyzed.athleteID == athleteID,
                   Analyzed.roleID == Role.roleID, or_(Role.roleName.like(search),
                                                       Role.roleDescription.like(search))).all()]
        session.close()
        return result

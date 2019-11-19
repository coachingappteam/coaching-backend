"""
This Class contain DAO methods for the tables of Sport, Roles, Exercise, Improves, Units
"""
from sqlalchemy import or_

from src.ORM.CoachingORM import Database, Sport, Role, Exercise, Improves, Unit


class SportDAO:

    def __init__(self):

        self.conn = Database()

    # ============================== Create Methods =========================== #
    def createSport(self, sportName, type):
        sport = Sport(sportName=sportName, type=type)
        session = self.conn.getNewSession()
        session.add(sport)
        session.flush()
        session.refresh(sport)
        id = sport.sportID
        session.commit()
        session.close()
        return id

    def createRole(self, sportID, roleName, roleDescription):
        role = Role(sportID=sportID, roleName=roleName, roleDescription=roleDescription)
        session = self.conn.getNewSession()
        session.add(role)
        session.flush()
        session.refresh(role)
        id = role.roleID
        session.commit()
        session.close()
        return id

    def createExercise(self, exerciseName, exerciseDescription, style):
        exercise = Exercise(exerciseName=exerciseName, exerciseDescription=exerciseDescription, style=style)
        session = self.conn.getNewSession()
        session.add(exercise)
        session.flush()
        session.refresh(exercise)
        id = exercise.exerciseID
        session.commit()
        session.close()
        return id

    def createImproves(self, exerciseID, roleID):
        improves = Improves(exerciseID=exerciseID, roleID=roleID)
        session = self.conn.getNewSession()
        session.add(improves)
        session.commit()
        session.close()

    def createUnit(self, unitName, unit):
        unit = Unit(unitName=unitName, unit=unit)
        session = self.conn.getNewSession()
        session.add(unit)
        session.flush()
        session.refresh(unit)
        id = unit.unitID
        session.commit()
        session.close()
        return id

    # ============================== Read Methods =========================== #

    def readUnit(self, unitID):
        session = self.conn.getNewSession()
        result = [e for e in session.query(Unit).filter(Unit.unitID == unitID).all()]
        session.close()
        if len(result) <= 0:
            return None
        return result[0]

    def readSport(self, sportID):
        session = self.conn.getNewSession()
        result = [e for e in session.query(Sport).filter(Sport.sportID == sportID).all()]
        session.close()
        if len(result) <= 0:
            return None
        return result[0]

    def readRole(self, roleID):
        session = self.conn.getNewSession()
        result = [e for e in session.query(Role).filter(Role.roleID == roleID).all()]
        session.close()
        if len(result) <= 0:
            return None
        return result[0]

    def readExercise(self, exerciseID):
        session = self.conn.getNewSession()
        result = [e for e in session.query(Exercise).filter(Exercise.exerciseID == exerciseID).all()]
        session.close()
        if len(result) <= 0:
            return None
        return result[0]

    def readExercisesForRole(self, roleID):
        session = self.conn.getNewSession()
        result = [e for e in session.query(Exercise, Improves).filter(Improves.roleID == roleID,
                                                          Exercise.exerciseID == Improves.exerciseID).all()]
        session.close()
        return result

    def readRolesForSport(self, sportID):
        session = self.conn.getNewSession()
        result = [e for e in session.query(Sport, Role).filter(Sport.sportID == sportID).all()]
        session.close()
        return result

    def readSportDetails(self, sportID):
        session = self.conn.getNewSession()
        result = [e for e in session.query(Sport).filter(Sport.sportID == sportID).all()]
        session.close()
        if len(result) <= 0:
            return None
        return result[0]

    def searchSport(self, search):
        session = self.conn.getNewSession()
        result = [e for e in session.query(Sport).filter(Sport.isDeleted == False,
                                                         or_(Sport.sportName.like(search))).all()]
        session.close()
        return result

    def deleteSport(self, sportID, isDeleted):
        session = self.conn.getNewSession()
        update = dict()
        update[Sport.isDeleted] = isDeleted
        result = session.query(Sport).filter(Sport.sportID == sportID).update(update)
        session.commit()
        session.close()
        return result

    def readUnitDetails(self, unitID):
        session = self.conn.getNewSession()
        result = [e for e in session.query(Unit).filter(Unit.unitID == unitID).all()]
        session.close()
        if len(result) <= 0:
            return None
        return result[0]

    def searchUnit(self, search):
        session = self.conn.getNewSession()
        result = [e for e in session.query(Unit).filter(Unit.isDeleted == False,
                                            or_(Unit.unit.like(search), Unit.unitName.like(search))).all()]
        session.close()
        return result

    def deleteUnit(self, unitID, isDeleted):
        session = self.conn.getNewSession()
        update = dict()
        update[Unit.isDeleted] = isDeleted
        result = session.query(Unit).filter(Unit.unitID == unitID).update(update)
        session.commit()
        session.close()
        return result

    def deleteRole(self, roleID, isDeleted):
        session = self.conn.getNewSession()
        update = dict()
        update[Role.isDeleted] = isDeleted
        result = session.query(Role).filter(Role.roleID == roleID).update(update)
        session.commit()
        session.close()
        return result

    def searchRole(self, search):
        session = self.conn.getNewSession()
        result = [e for e in session.query(Role).filter(Role.isDeleted == False,
                                            or_(Role.roleName.like(search), Role.roleDescription.like(search))).all()]
        session.close()
        return result

    def deleteExercise(self, exerciseID, isDeleted):
        session = self.conn.getNewSession()
        update = dict()
        update[Exercise.isDeleted] = isDeleted
        result = session.query(Exercise).filter(Exercise.exerciseID == exerciseID).update(update)
        session.commit()
        session.close()
        return result

    def searchExercise(self, search):
        session = self.conn.getNewSession()
        result = [e for e in session.query(Exercise).filter(Exercise.isDeleted == False,
                                                or_(Exercise.exerciseName.like(search),
                                                    Exercise.exerciseDescription.like(search),
                                                    Exercise.style.like(search))).all()]
        session.close()
        return result

    def readRoleDetails(self, roleID):
        session = self.conn.getNewSession()
        result = [e for e in session.query(Role).filter(Role.roleID == roleID).all()]
        session.close()
        if len(result) <= 0:
            return None
        return result[0]

    def readExerciseDetails(self, exerciseID):
        session = self.conn.getNewSession()
        result = [e for e in session.query(Exercise).filter(Exercise.exerciseID == exerciseID).all()]
        session.close()
        if len(result) <= 0:
            return None
        return result[0]

    def getRolesByExerciseID(self, exerciseID):
        session = self.conn.getNewSession()
        result = [e for e in session.query(Role, Improves).filter(Improves.exerciseID == exerciseID,
                                                      Improves.roleID == Role.roleID).all()]
        session.close()
        return result

    def getExerciseByRoleID(self, roleID):
        session = self.conn.getNewSession()
        result = [e for e in session.query(Exercise, Improves).filter(Improves.roleID == roleID,
                                                      Improves.exerciseID == Exercise.exerciseID).all()]
        session.close()
        return result

    def deleteImproves(self, roleID, exerciseID):
        session = self.conn.getNewSession()

        session.query(Improves).filter(Improves.exerciseID == exerciseID, Improves.roleID == roleID).delete()
        session.commit()
        session.close()
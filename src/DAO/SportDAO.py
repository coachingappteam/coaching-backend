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

    def createExercise(self, exerciseName, exerciseDescription, unitID, style, measure):
        exercise = Exercise(exerciseName=exerciseName, exerciseDescription=exerciseDescription, unitID=unitID, style=style, measure=measure)
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
    def readAllSports(self):
        session = self.conn.getNewSession()
        result = session.query(Sport).all()
        return result

    def readAllUnits(self):
        session = self.conn.getNewSession()
        result = session.query(Unit).all()
        return result

    def readAllRoles(self):
        session = self.conn.getNewSession()
        result = session.query(Role).all()
        return result

    def readAllExercises(self):
        session = self.conn.getNewSession()
        result = session.query(Exercise).all()
        return result

    def readUnit(self, unitID):
        session = self.conn.getNewSession()
        result = session.query(Unit).filter(Unit.unitID == unitID).first()
        return result

    def readSport(self, sportID):
        session = self.conn.getNewSession()
        result = session.query(Sport).filter(Sport.sportID == sportID).first()
        return result

    def readRole(self, roleID):
        session = self.conn.getNewSession()
        result = session.query(Role).filter(Role.roleID == roleID).first()
        return result

    def readExercise(self, exerciseID):
        session = self.conn.getNewSession()
        result = session.query(Exercise).filter(Exercise.exerciseID == exerciseID).first()
        return result

    def readExercisesForRole(self, roleID):
        session = self.conn.getNewSession()
        result = session.query(Exercise, Improves).filter(Improves.roleID == roleID,
                                                          Exercise.exerciseID == Improves.exerciseID).all()
        return result

    def readRolesForSport(self, sportID):
        session = self.conn.getNewSession()
        result = session.query(Sport, Role).filter(Sport.sportID == sportID).all()
        return result

    def readSportDetails(self, sportID):
        session = self.conn.getNewSession()
        result = session.query(Sport).filter(Sport.sportID == sportID).first()
        session.close()
        return result

    def searchSport(self, search):
        session = self.conn.getNewSession()
        result = session.query(Sport).filter(Sport.isDeleted == False,or_(Sport.sportName.like(search))).all()
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
        result = session.query(Unit).filter(Unit.unitID == unitID).first()
        session.close()
        return result

    def searchUnit(self, search):
        session = self.conn.getNewSession()
        result = session.query(Unit).filter(Unit.isDeleted == False,
                                            or_(Unit.unit.like(search), Unit.unitName.like(search))).all()
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
        result = session.query(Role).filter(Role.isDeleted == False,
                                            or_(Role.roleName.like(search), Role.roleDescription.like(search))).all()
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
        result = session.query(Exercise).filter(Exercise.isDeleted == False,
                                                or_(Exercise.exerciseName.like(search), Exercise.measure.like(search),
                                                    Exercise.exerciseDescription.like(search),
                                                    Exercise.style.like(search))).all()
        return result

    def readRoleDetails(self, roleID):
        session = self.conn.getNewSession()
        result = session.query(Role).filter(Role.roleID == roleID).first()
        session.close()
        return result

    def readExerciseDetails(self, exerciseID):
        session = self.conn.getNewSession()
        result = session.query(Exercise).filter(Exercise.exerciseID == exerciseID).first()
        session.close()
        return result

    def getRolesByExerciseID(self, exerciseID):
        session = self.conn.getNewSession()
        result = session.query(Role, Improves).filter(Improves.exerciseID == exerciseID,
                                                      Improves.roleID == Role.roleID).all()
        session.close()
        return result

    def getExerciseByRoleID(self, roleID):
        session = self.conn.getNewSession()
        result = session.query(Exercise, Improves).filter(Improves.roleID == roleID,
                                                      Improves.exerciseID == Exercise.exerciseID).all()
        session.close()
        return result

    def deleteImproves(self, roleID, exerciseID):
        session = self.conn.getNewSession()

        session.query(Improves).filter(Improves.exerciseID == exerciseID, Improves.roleID == roleID).delete()
        session.commit()
        session.close()
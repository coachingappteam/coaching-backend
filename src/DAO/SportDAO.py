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
        session.commit()
        session.close()

    def createRole(self, sportID, roleName, roleDescription):
        sport = Role(sportID=sportID, roleName=roleName, roleDescription=roleDescription)
        session = self.conn.getNewSession()
        session.add(sport)
        session.commit()
        session.close()

    def createExercise(self, exerciseName, exerciseDescription):
        exercise = Exercise(exerciseName=exerciseName, exerciseDescription=exerciseDescription)
        session = self.conn.getNewSession()
        session.add(exercise)
        session.commit()
        session.close()

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
        session.commit()
        session.close()

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
        result = session.query(Sport).filter(or_(Sport.sportName.like(search))).all()
        return result

    def deleteSport(self, sportID):
        session = self.conn.getNewSession()

        session.query(Sport).filter(Sport.sportID == sportID).delete()
        session.commit()
        session.close()

    def readUnitDetails(self, unitID):
        session = self.conn.getNewSession()
        result = session.query(Unit).filter(Unit.unitID == unitID).first()
        session.close()
        return result

    def searchUnit(self, search):
        session = self.conn.getNewSession()
        result = session.query(Unit).filter(or_(Unit.unit.like(search), Unit.unitName.like(search))).all()
        return result

    def deleteUnit(self, unitID):
        session = self.conn.getNewSession()

        session.query(Unit).filter(Unit.unitID == unitID).delete()
        session.commit()
        session.close()

    def deleteRole(self, roleID):
        session = self.conn.getNewSession()

        session.query(Role).filter(Role.roleID == roleID).delete()
        session.commit()
        session.close()

    def searchRole(self, search):
        session = self.conn.getNewSession()
        result = session.query(Role).filter(or_(Role.roleName.like(search), Role.roleDescription.like(search))).all()
        return result

    def deleteExercise(self, exerciseID):
        session = self.conn.getNewSession()

        session.query(Exercise).filter(Exercise.exerciseID == exerciseID).delete()
        session.commit()
        session.close()

    def searchExercise(self, search):
        session = self.conn.getNewSession()
        result = session.query(Exercise).filter(or_(Exercise.exerciseName.like(search), Exercise.measure.like(search),
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

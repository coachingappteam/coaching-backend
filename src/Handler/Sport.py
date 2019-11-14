from flask import jsonify
from src.DAO.SportDAO import SportDAO
from src.DAO.SecurityDAO import SecurityDAO
from src.ORM.CoachingORM import Type

dao = SportDAO()
securityDAO = SecurityDAO()


def createSport(json):
    if json != 2:
        sportName = json["sportName"]
        type = json["type"]
        if sportName and type:
            if type == 'Individual':
                dao.createSport(sportName, Type.Individual)
            elif type == 'Team':
                dao.createSport(sportName, Type.Team)
            elif type == 'Mixed':
                dao.createSport(sportName, Type.Mixed)
            else:
                return jsonify(Error="Type does not exist"), 400
            return jsonify(Success="Sport added"), 200
        else:
            return jsonify(Error="Required Parameter is missing"), 400


def createRole(json):
    if json != 3:
        sportID = json["sportID"]
        roleName = json["roleName"]
        roleDescription = json["roleDescription"]
        if sportID and roleName:
            dao.createRole(sportID=sportID, roleName=roleName, roleDescription=roleDescription)
            return jsonify(Success="Sport added"), 200
        else:
            return jsonify(Error="Required Parameter is missing"), 400


def sportDetails(json):
    sportID = json['sportID']
    if sportID:
        result = dao.readSportDetails(sportID)
        if result is not None:
            return jsonify(Sport=result.json()), 200
        else:
            return jsonify(Sport="Nothing Found"), 200
    else:
        return jsonify(Error="Required Parameter is missing"), 400


def sportSearch(json):
    search = '%' + str(json['search']) + '%'
    result = dao.searchSport(search)
    sports = list()
    for sport in result:
        sports.append(sport.json())
    return jsonify(Sports=sports), 200


def unitSearch(json):
    search = '%' + str(json['search']) + '%'
    result = dao.searchUnit(search)
    units = list()
    for unit in result:
        units.append(unit.json())
    return jsonify(Units=units), 200


def unitDetails(json):
    unitID = json['unitID']
    if unitID:
        result = dao.readUnitDetails(unitID)
        if result is not None:
            return jsonify(Sport=result.json()), 200
        else:
            return jsonify(Sport="Nothing Found"), 200
    else:
        return jsonify(Error="Required Parameter is missing"), 400


def createUnit(json):
    if json != 2:
        unitName = json["unitName"]
        unit = json["unit"]
        if unitName and unit:
            dao.createUnit(unitName, unit)
            return jsonify(Success="Unit added"), 200
        else:
            return jsonify(Error="Required Parameter is missing"), 400


def roleDetails(json):
    roleID = json['roleID']
    if roleID:
        result = dao.readRoleDetails(roleID)
        if result is not None:
            return jsonify(Role=result.json()), 200
        else:
            return jsonify(Role="Nothing Found"), 200
    else:
        return jsonify(Error="Required Parameter is missing"), 400


def roleSearch(json):
    search = '%' + str(json['search']) + '%'
    result = dao.searchRole(search)
    roles = list()
    for role in result:
        roles.append(role.json())
    return jsonify(Roles=roles), 200


def createExercise(json):
    if json != 2:
        exerciseName = json["exerciseName"]
        exerciseDescription = json["exerciseDescription"]
        if exerciseName:
            dao.createExercise(exerciseName, exerciseDescription)
            return jsonify(Success="Exercise added"), 200
        else:
            return jsonify(Error="Required Parameter is missing"), 400


def exerciseDetails(json):
    exerciseID = json['exerciseID']
    if exerciseID:
        result = dao.readExerciseDetails(exerciseID)
        if result is not None:
            return jsonify(Exercise=result.json()), 200
        else:
            return jsonify(Exercise="Nothing Found"), 200
    else:
        return jsonify(Error="Required Parameter is missing"), 400


def exerciseSearch(json):
    search = '%' + str(json['search']) + '%'
    result = dao.searchExercise(search)
    exercises = list()
    for exercise in result:
        exercises.append(exercise.json())
    return jsonify(Exercise=exercises), 200


def deleteSport(json):
    sportID = json['sportID']
    if sportID:
        dao.deleteSport(sportID)
        return jsonify(Success="Sport was deleted"), 200
    else:
        return jsonify(Error="Required Parameter is missing"), 400


def deleteUnit(json):
    unitID = json['unitID']
    if unitID:
        dao.deleteUnit(unitID)
        return jsonify(Success="Unit was deleted"), 200
    else:
        return jsonify(Error="Required Parameter is missing"), 400


def deleteRole(json):
    roleID = json['roleID']
    if roleID:
        dao.deleteRole(roleID)
        return jsonify(Success="Role was deleted"), 200
    else:
        return jsonify(Error="Required Parameter is missing"), 400


def deleteExercise(json):
    exerciseID = json['exerciseID']
    if exerciseID:
        dao.deleteExercise(exerciseID)
        return jsonify(Success="Exercise was deleted"), 200
    else:
        return jsonify(Error="Required Parameter is missing"), 400


def addExerciseToRole(json):
    exerciseID = json['exerciseID']
    roleID = json['roleID']
    if exerciseID and roleID:
        dao.createImproves(exerciseID, roleID)
        return jsonify(Success="Member added"), 200
    else:
        return jsonify(Error="Required Parameter is missing"), 400


def readRolesForExercise(json):
    exerciseID = json['exerciseID']
    if exerciseID:
        result = dao.getRolesByExerciseID(exerciseID)
        roles = list()
        for role in result:
            roles.append(role[0].json())
        return jsonify(Roles=roles), 200
    else:
        return jsonify(Error="Required Parameter is missing"), 400


def readExercisesOfRole(json):
    roleID = json['roleID']
    if roleID:
        result = dao.getExerciseByRoleID(roleID)
        exercises = list()
        for exercise in result:
            exercises.append(exercise[0].json())
        return jsonify(Exercises=exercises), 200
    else:
        return jsonify(Error="Required Parameter is missing"), 400


def deleteImprovement(json):
    roleID = json['roleID']
    exerciseID = json['exerciseID']
    if roleID and exerciseID:
        dao.deleteImproves(roleID, exerciseID)
        return jsonify(Success="Improve was deleted"), 200
    else:
        return jsonify(Error="Required Parameter is missing"), 400
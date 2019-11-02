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
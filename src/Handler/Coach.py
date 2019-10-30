from flask import jsonify
from src.DAO.CoachDAO import CoachDAO
from src.DAO.SecurityDAO import SecurityDAO

dao = CoachDAO()
securityDAO = SecurityDAO()


def loginCoach(json):
    if len(json) != 2:
        return jsonify(Error="Wrong number of parameters")
    email = json['email']
    password = json['password']

    if email and password:
        coach = dao.readCoach(email, password)
        if coach:
            token = securityDAO.createToken(coach.coachID)
            if not securityDAO.checkToken(token):
                return jsonify(Error="Token was not created.")
            return jsonify(Coach=coach.json(), token=token), 200
        else:
            return jsonify(Error="Wrong username or password"), 400

    else:
        return jsonify(Error="Misssing required parameter"), 400


def signupCoach(json):
    if len(json) != 6:
        return jsonify(Error="Missing Parameters"), 400
    password = json['password']
    fname = json['firstName']
    lname = json['lastName']
    phone = json['phone']
    email = json['email']
    imperial = json['prefersImperial']
    if password and fname and lname and email:
        coach = dao.readCoach(email, password)
        if coach is not None:
            return jsonify(Error="Coach with given email exists."), 401
        dao.createCoach(password, fname, lname, phone, email, imperial)
        coach = dao.readCoach(email, password)
        if coach is None:
            return jsonify(Error="Insert not successful"), 401
        return jsonify(Coach=coach.json()), 200
    else:
        return jsonify(Error="Required Parameter is missing"), 400


def signoutCoach(header):
    token = header['token']
    securityDAO.deleteToken(token)
    if securityDAO.validateToken(token):
        return jsonify(Error="Log out unsuccessful"), 400
    return jsonify(Success="Log out successful"), 200


def checkToken(header):
    token = header['token']
    return securityDAO.validateToken(token)


def createAthlete(headers, json):
    coachID = securityDAO.getTokenOwner(headers['token'])

    if json != 6:
        firstName = json["firstName"]
        lastName = json["lastName"]
        email = json["email"]
        phone = json["phone"]
        sex = json["sex"]
        birthdate = json["birthdate"]

        if coachID and firstName and lastName and email and sex and birthdate:
            dao.createAthlete(coachID, firstName, lastName, email, phone, sex, birthdate)
            return  jsonify(Success="Athlete added"), 200
        else:
            return jsonify(Error="Required Parameter is missing"), 400


def createTeam(headers, json):
    coachID = securityDAO.getTokenOwner(headers['token'])
    if json != 3:
        sportID = json['sportID']
        teamName = json['teamName']
        teamDescription = json['teamDescription']

        if coachID and sportID and teamName:
            dao.createTeam(coachID, sportID, teamName, teamDescription)
            return  jsonify(Success="Team added"), 200
        else:
            return jsonify(Error="Required Parameter is missing"), 400
from flask import jsonify
from src.DAO.CoachDAO import CoachDAO
from src.DAO.SecurityDAO import SecurityDAO
from src.ORM.CoachingORM import Sex

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
    if len(json) != 5:
        return jsonify(Error="Missing Parameters"), 400
    password = json['password']
    fname = json['firstName']
    lname = json['lastName']
    phone = json['phone']
    email = json['email']
    if password and fname and lname and email:
        coach = dao.readCoach(email, password)
        if coach is not None:
            return jsonify(Error="Coach with given email exists."), 401
        dao.createCoach(password, fname, lname, phone, email)
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


def checkAdminToken(header):
    coachID = securityDAO.getTokenOwner(header['token'])
    return securityDAO.getIfAdmin(coachID)


def createAthlete(headers, json):
    coachID = securityDAO.getTokenOwner(headers['token'])

    if json != 6:
        firstName = json["firstName"]
        lastName = json["lastName"]
        email = json["email"]
        phone = json["phone"]
        sex = json["sex"]
        if sex == 'F':
            sex = Sex.F
        elif sex == 'M':
            sex = Sex.M
        else:
            sex = Sex.X
        birthdate = json["birthdate"]

        if coachID and firstName and lastName and email and sex and birthdate:
            dao.createAthlete(coachID, firstName, lastName, email, phone, sex, birthdate)
            return jsonify(Success="Athlete added"), 200
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
            return jsonify(Success="Team added"), 200
        else:
            return jsonify(Error="Required Parameter is missing"), 400


def addCoachToTeam(headers, json):
    coachID = securityDAO.getTokenOwner(headers['token'])
    supportCoachID = json['supportCoachID']
    teamID = json['teamID']
    if coachID and supportCoachID and teamID:
        if dao.readIfTeamFromCoach(coachID, teamID):
            dao.createSupport(supportCoachID, teamID)
        else:
            return jsonify(Error="User doesnt have access to team"), 400
        return jsonify(Success="Support added"), 200
    else:
        return jsonify(Error="Required Parameter is missing"), 400


def searchCoaches(json):
    search = '%' + str(json['search']) + '%'
    result = dao.searchCoach(search)
    coaches = list()
    for coach in result:
        coaches.append(coach.json())
    return jsonify(Coaches=coaches), 200


def addAthleteToTeam(headers, json):
    coachID = securityDAO.getTokenOwner(headers['token'])
    teamID = json['teamID']
    athleteID = json['athleteID']
    if coachID and athleteID and teamID:
        if dao.readIfTeamFromCoach(coachID, teamID) and dao.readIfAthleteFromCoach(coachID, athleteID):
            dao.createMember(athleteID, teamID)
        else:
            return jsonify(Error="User doesnt have access to team"), 400
        return jsonify(Success="Member added"), 200
    else:
        return jsonify(Error="Required Parameter is missing"), 400


def readCoach(headers):
    coachID = securityDAO.getTokenOwner(headers['token'])
    if coachID:
        result = dao.readCoachByID(coachID)
        if result is not None:
            return jsonify(Coach=result.json()), 200
        else:
            return jsonify(Coach="Nothing Found"), 200
    else:
        return jsonify(Error="Required Parameter is missing"), 400


def updateCoach(headers, json):
    coachID = securityDAO.getTokenOwner(headers['token'])
    password = json['password']
    fname = json['firstName']
    lname = json['lastName']
    phone = json['phone']
    isActiveMember = json['isActiveMember']
    if coachID and (fname or lname or phone or isActiveMember is not None):
        if fname or lname or phone:
            dao.updateCoach(coachID, fname, lname, phone, isActiveMember)
        if password and not password == '':
            dao.updatePassword(coachID, password)
        return jsonify(Success="Coach Updated"), 200
    else:
        return jsonify(Error="Required Parameter is missing"), 400


def deleteCoach(headers):
    coachID = securityDAO.getTokenOwner(headers['token'])
    if coachID:
        dao.deleteCoach(coachID)
        return jsonify(Success="Coach Deleted"), 200
    else:
        return jsonify(Error="Required Parameter is missing"), 400


def athleteDetails(headers, json):
    coachID = securityDAO.getTokenOwner(headers['token'])
    athleteID = json['athleteID']
    if coachID and athleteID:
        if dao.readIfAthleteFromCoach(coachID, athleteID) or dao.readIfAthleteInTeamFromSupport(coachID, athleteID):
            result = dao.readAthleteByID(athleteID)
            if result is not None:
                return jsonify(Athlete=result.json()), 200
            else:
                return jsonify(Athlete="Nothing Found"), 200
        else:
            return jsonify(Error="User doesnt have access to athlete"), 400
    else:
        return jsonify(Error="Required Parameter is missing"), 400


def athleteSearch(headers, json):
    coachID = securityDAO.getTokenOwner(headers['token'])
    if coachID:
        search = '%' + str(json['search']) + '%'
        result = dao.searchAthletes(coachID, search)
        athletes = list()
        for athlete in result:
            athletes.append(athlete.json())
        return jsonify(Athletes=athletes), 200
    else:
        return jsonify(Error="Required Parameter is missing"), 400


def athleteUpdate(headers, json):
    coachID = securityDAO.getTokenOwner(headers['token'])
    athleteID = json['athleteID']
    firstName = json["firstName"]
    lastName = json["lastName"]
    email = json["email"]
    phone = json["phone"]
    sex = json["sex"]
    if sex == 'F':
        sex = Sex.F
    elif sex == 'M':
        sex = Sex.M
    elif sex == 'X':
        sex = Sex.X
    birthdate = json["birthdate"]

    if coachID and athleteID and (firstName or lastName or phone or email or birthdate or sex):
        if dao.readIfAthleteFromCoach(coachID, athleteID):
            dao.updateAthlete(coachID, athleteID, firstName, lastName, phone, email, birthdate, sex)
            return jsonify(Success="Athlete Updated"), 200
        else:
            return jsonify(Error="User cant access this athlete"), 400
    else:
        return jsonify(Error="Required Parameter is missing"), 400


def athleteDelete(headers, json):
    coachID = securityDAO.getTokenOwner(headers['token'])
    athleteID = json['athleteID']
    if coachID and athleteID:
        if dao.readIfAthleteFromCoach(coachID, athleteID):
            dao.deleteAthlete(coachID, athleteID)
            return jsonify(Success="Athlete Deleted"), 200
        else:
            return jsonify(Error="User cant access this athlete"), 400
    else:
        return jsonify(Error="Required Parameter is missing"), 400


def teamDetails(headers, json):
    coachID = securityDAO.getTokenOwner(headers['token'])
    teamID = json['teamID']
    if coachID and teamID:
        if dao.readIfTeamFromCoach(coachID, teamID) or dao.readIfCoachIsSupport(coachID, teamID):
            result = dao.readTeamByID(teamID)
            if result is not None:
                return jsonify(Team=result.json()), 200
            else:
                return jsonify(Team="Nothing Found"), 200
        else:
            return jsonify(Error="User doesnt have access to team"), 400
    else:
        return jsonify(Error="Required Parameter is missing"), 400


def teamSearch(headers, json):
    coachID = securityDAO.getTokenOwner(headers['token'])
    if coachID:
        search = '%' + str(json['search']) + '%'
        result = dao.searchTeams(coachID, search)
        result2 = dao.getTeamsByCoachID(coachID, search)
        teams = list()
        for team in result:
            teams.append(team.json())
        for team in result2:
            teams.append(team.json())
        return jsonify(Teams=teams), 200
    else:
        return jsonify(Error="Required Parameter is missing"), 400


def teamUpdate(headers, json):
    coachID = securityDAO.getTokenOwner(headers['token'])
    teamID = json['teamID']
    teamName = json["teamName"]
    teamDescription = json["teamDescription"]

    if coachID and teamID and (teamName or teamDescription):
        if dao.readIfTeamFromCoach(coachID, teamID):
            dao.updateTeam(coachID, teamID, teamName, teamDescription)
            return jsonify(Success="Team Updated"), 200
        else:
            return jsonify(Error="User cant access this team"), 400
    else:
        return jsonify(Error="Required Parameter is missing"), 400


def teamDelete(headers, json):
    coachID = securityDAO.getTokenOwner(headers['token'])
    teamID = json['teamID']
    if coachID and teamID:
        if dao.readIfTeamFromCoach(coachID, teamID):
            dao.deleteTeam(coachID, teamID)
            return jsonify(Success="Team Deleted"), 200
        else:
            return jsonify(Error="User cant access this team"), 400
    else:
        return jsonify(Error="Required Parameter is missing"), 400


def readCoachesInCharge(headers, json):
    coachID = securityDAO.getTokenOwner(headers['token'])
    teamID = json['teamID']
    if coachID and teamID:
        if dao.readIfCoachIsSupport(coachID, teamID) or dao.readIfTeamFromCoach(coachID, teamID):
            result = dao.getCoachesByTeamID(teamID)
            coaches = list()
            creator = dao.getTeamCreator(teamID)
            if creator:
                coaches.append(creator[0].json())
            for coach in result:
                coaches.append(coach[0].json())
            return jsonify(Coachs=coaches), 200
        else:
            return jsonify(Error="User cant access this team"), 400
    else:
        return jsonify(Error="Required Parameter is missing"), 400


def readTeamsOfCoach(headers):
    coachID = securityDAO.getTokenOwner(headers['token'])
    if coachID:
        result = dao.getTeamsByCoachID(coachID, "")
        teams = list()
        for team in result:
            teams.append(team[0].json())
        return jsonify(Teams=teams), 200
    else:
        return jsonify(Error="Required Parameter is missing"), 400


def deleteSupport(headers, json):
    coachID = securityDAO.getTokenOwner(headers['token'])
    supportCoachID = json['supportCoachID']
    teamID = json['teamID']
    if coachID and supportCoachID and teamID:
        if dao.readIfTeamFromCoach(coachID, teamID):
            dao.deleteSupport(supportCoachID, teamID)
            return jsonify(Success="Coach was removed from team"), 200
        else:
            return jsonify(Error="User doesnt have access to team"), 400
    else:
        return jsonify(Error="Required Parameter is missing"), 400


def readAthletesInTeam(headers, json):
    coachID = securityDAO.getTokenOwner(headers['token'])
    teamID = json['teamID']
    if coachID and teamID:
        if dao.readIfCoachIsSupport(coachID, teamID) or dao.readIfTeamFromCoach(coachID, teamID):
            result = dao.getAthletesByTeamID(teamID)
            athletes = list()
            for athlete in result:
                athletes.append(athlete[0].json())
            return jsonify(Athletes=athletes), 200
    else:
        return jsonify(Error="Required Parameter is missing"), 400


def readTeamsOfAthlete(headers, json):
    coachID = securityDAO.getTokenOwner(headers['token'])
    athleteID = json['athleteID']
    if coachID and athleteID:
        if dao.readIfAthleteInTeamFromSupport(coachID, athleteID):
            result = dao.getTeamsByAthleteID(athleteID)
            teams = list()
            for team in result:
                teams.append(team[0].json())
            return jsonify(Teams=teams), 200
        else:
            return jsonify(Error="User doesnt have access to athlete"), 400
    else:
        return jsonify(Error="Required Parameter is missing"), 400


def deleteMember(headers, json):
    coachID = securityDAO.getTokenOwner(headers['token'])
    athleteID = json['athleteID']
    teamID = json['teamID']
    if coachID and athleteID and teamID:
        if dao.readIfTeamFromCoach(coachID, teamID):
            dao.deleteMember(athleteID, teamID)
            return jsonify(Success="Coach was removed from team"), 200
        else:
            return jsonify(Error="User doesnt have access to team"), 400
    else:
        return jsonify(Error="Required Parameter is missing"), 400


def addRoleToAthlete(headers, json):
    coachID = securityDAO.getTokenOwner(headers['token'])
    roleID = json['roleID']
    athleteID = json['athleteID']
    if coachID and athleteID and roleID:
        if dao.readIfAthleteFromCoach(coachID, athleteID):
            dao.createFocus(athleteID, roleID, False)
        else:
            return jsonify(Error="User doesnt have access to team"), 400
        return jsonify(Success="Member added"), 200
    else:
        return jsonify(Error="Required Parameter is missing"), 400


def readAthletesInRole(headers, json):
    coachID = securityDAO.getTokenOwner(headers['token'])
    roleID = json['roleID']
    if coachID and roleID:
        result = dao.getAthletesByRoleID(coachID, roleID)
        athletes = list()
        for athlete in result:
            athletes.append(athlete[0].json())
        return jsonify(Athletes=athletes), 200
    else:
        return jsonify(Error="Required Parameter is missing"), 400


def readRolesOfAthlete(headers, json):
    coachID = securityDAO.getTokenOwner(headers['token'])
    athleteID = json['athleteID']
    if coachID and athleteID:
        if dao.readIfAthleteFromCoach(coachID, athleteID) or dao.readIfAthleteInTeamFromSupport(coachID, athleteID):
            result = dao.getRolesByAthleteID(athleteID)
            teams = list()
            for team in result:
                teams.append(team[0].json())
            return jsonify(Teams=teams), 200
        else:
            return jsonify(Error="User doesnt have access to athlete"), 400
    else:
        return jsonify(Error="Required Parameter is missing"), 400


def deleteFocus(headers, json):
    coachID = securityDAO.getTokenOwner(headers['token'])
    athleteID = json['athleteID']
    roleID = json['roleID']
    if coachID and athleteID and roleID:
        if dao.readIfAthleteFromCoach(coachID, athleteID):
            dao.deleteFocus(athleteID, roleID)
            return jsonify(Success="Role was removed from athlete"), 200
        else:
            return jsonify(Error="User doesnt have access to athlete"), 400
    else:
        return jsonify(Error="Required Parameter is missing"), 400


def readCoachByID(json):
    coachID = json['coachID']
    if coachID:
        result = dao.readCoachByID(coachID)
        if result is not None:
            return jsonify(Coach=result.json()), 200
        else:
            return jsonify(Coach="Nothing Found"), 200
    else:
        return jsonify(Error="Required Parameter is missing"), 400
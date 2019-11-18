from flask import jsonify

from src.DAO.CoachDAO import CoachDAO
from src.DAO.PlanDAO import PlanDAO
from src.DAO.SecurityDAO import SecurityDAO

dao = PlanDAO()
securityDAO = SecurityDAO()
coachDAO = CoachDAO()


def createPlan(headers, json):
    coachID = securityDAO.getTokenOwner(headers['token'])
    if json != 6:
        teamID = json['teamID']
        parentPlanID = json['parentPlanID']
        title = json['title']
        startDate = json['startDate']
        endDate = json['endDate']
        planDescription = json['planDescription']

        if coachID and teamID and title and startDate and endDate:
            if coachDAO.readIfTeamFromCoach(coachID, teamID) or coachDAO.readIfCoachIsSupport(coachID, teamID):
                id = dao.createTrainingPlan(teamID, parentPlanID, title, startDate, endDate, planDescription)
                if id:
                    return jsonify(planID=id)
                return jsonify(Success="Plan added"), 200
            else:
                return jsonify(Error="User can't access team")
        else:
            return jsonify(Error="Required Parameter is missing"), 400


def planDetails(headers, json):
    coachID = securityDAO.getTokenOwner(headers['token'])
    planID = json['planID']
    if coachID and planID:
        if dao.readIfCoachManagePlan(coachID, planID) or dao.readIfCoachSupportPlan(coachID, planID):
            result = dao.readPlanByID(planID)
            if result is not None:
                return jsonify(Plan=result.json()), 200
            else:
                return jsonify(Plan="Nothing Found"), 200
        else:
            return jsonify(Error="User doesnt have access to plan"), 400
    else:
        return jsonify(Error="Required Parameter is missing"), 400


def planSearch(headers, json):
    coachID = securityDAO.getTokenOwner(headers['token'])
    teamID = json['teamID']
    if coachID and teamID:
        if coachDAO.readIfTeamFromCoach(coachID, teamID) or coachDAO.readIfCoachIsSupport(coachID, teamID):
            search = '%' + str(json['search']) + '%'
            result = dao.searchPlans(teamID, search)
            plans = list()
            for plan in result:
                plans.append(plan.json())
            return jsonify(Plans=plans), 200
        else:
            return jsonify(Error="User doesnt have access to plan"), 400
    else:
        return jsonify(Error="Required Parameter is missing"), 400


def planUpdate(headers, json):
    coachID = securityDAO.getTokenOwner(headers['token'])
    planID = json['planID']
    title = json['title']
    startDate = json['startDate']
    endDate = json['endDate']
    planDescription = json['planDescription']

    if coachID and planID and (title or startDate or endDate or planDescription):
        if dao.readIfCoachManagePlan(coachID, planID):
            dao.updatePlan(planID, title, startDate, endDate, planDescription)
            return jsonify(Success="Plan Updated"), 200
        else:
            return jsonify(Error="User cant access this plan"), 400
    else:
        return jsonify(Error="Required Parameter is missing"), 400


def planDelete(headers, json):
    coachID = securityDAO.getTokenOwner(headers['token'])
    planID = json['planID']
    isDeleted = json['isDeleted']
    if coachID and planID and isDeleted is not None:
        if dao.readIfCoachManagePlan(coachID, planID):
            dao.deletePlan(planID, isDeleted)
            return jsonify(Success="Plan Delete Status changed."), 200
        else:
            return jsonify(Error="User cant access this plan"), 400
    else:
        return jsonify(Error="Required Parameter is missing"), 400


def createSession(headers, json):
    coachID = securityDAO.getTokenOwner(headers['token'])
    if json != 6:
        planID = json['planID']
        parentSessionID = json['parentSessionID']
        sessionTitle = json['sessionTitle']
        location = json['location']
        sessionDate = json['sessionDate']
        sessionDescription = json['sessionDescription']
        isCompetition = json['isCompetition']
        isMain = json['isMain']

        if coachID and planID and sessionTitle and sessionDate and isCompetition is not None and isMain is not None:
            if dao.readIfCoachManagePlan(coachID, planID) or dao.readIfCoachSupportPlan(coachID, planID):
                id = dao.createSession(planID, parentSessionID, sessionTitle, location, isCompetition, isMain,
                                  sessionDate, sessionDescription)
                if id:
                    return jsonify(sessionID=id)
                return jsonify(Success="Session added"), 200
            else:
                return jsonify(Error="User can't access plan")
        else:
            return jsonify(Error="Required Parameter is missing"), 400


def sessionDetails(headers, json):
    coachID = securityDAO.getTokenOwner(headers['token'])
    sessionID = json['sessionID']
    if coachID and sessionID:
        if dao.readIfCoachManageSession(coachID, sessionID) or dao.readIfCoachSupportSession(coachID, sessionID):
            result = dao.readSessionByID(sessionID)
            if result is not None:
                return jsonify(Plan=result.json()), 200
            else:
                return jsonify(Plan="Nothing Found"), 200
        else:
            return jsonify(Error="User doesnt have access to plan"), 400
    else:
        return jsonify(Error="Required Parameter is missing"), 400


def sessionSearch(headers, json):
    coachID = securityDAO.getTokenOwner(headers['token'])
    planID = json['planID']
    if coachID and planID:
        if dao.readIfCoachManagePlan(coachID, planID) or dao.readIfCoachSupportPlan(coachID, planID):
            search = '%' + str(json['search']) + '%'
            result = dao.searchSessions(planID, search)
            sessions = list()
            for session in result:
                sessions.append(session.json())
            return jsonify(Sessions=sessions), 200
        else:
            return jsonify(Error="User doesnt have access to plan"), 400
    else:
        return jsonify(Error="Required Parameter is missing"), 400


def sessionUpdate(headers, json):
    coachID = securityDAO.getTokenOwner(headers['token'])
    sessionID = json['sessionID']
    sessionTitle = json['sessionTitle']
    location = json['location']
    sessionDate = json['sessionDate']
    sessionDescription = json['sessionDescription']
    isCompetition = json['isCompetition']

    if coachID and sessionID and (sessionTitle or location or sessionDate or sessionDescription or isCompetition is not None):
        if dao.readIfCoachManageSession(coachID, sessionID):
            dao.updateSession(sessionID, sessionTitle, location, sessionDate, sessionDescription, isCompetition)
            return jsonify(Success="Session Updated"), 200
        else:
            return jsonify(Error="User cant access this session"), 400
    else:
        return jsonify(Error="Required Parameter is missing"), 400


def sessionDelete(headers, json):
    coachID = securityDAO.getTokenOwner(headers['token'])
    sessionID = json['sessionID']
    isDeleted = json['isDeleted']
    if coachID and sessionID and isDeleted is not None:
        if dao.readIfCoachManageSession(coachID, sessionID):
            dao.deleteSession(sessionID, isDeleted)
            return jsonify(Success="Session Delete Status changed."), 200
        else:
            return jsonify(Error="User cant access this session"), 400
    else:
        return jsonify(Error="Required Parameter is missing"), 400


def readPlanSubPlans(headers, json):
    coachID = securityDAO.getTokenOwner(headers['token'])
    parentPlanID = json['parentPlanID']
    if coachID and parentPlanID:
        if dao.readIfCoachManagePlan(coachID, parentPlanID) or dao.readIfCoachSupportPlan(coachID, parentPlanID):
            search = '%' + str(json['search']) + '%'
            result = dao.searchSubPlans(parentPlanID, search)
            plans = list()
            for plan in result:
                plans.append(plan.json())
            return jsonify(Plans=plans), 200
        else:
            return jsonify(Error="User doesnt have access to plan"), 400
    else:
        return jsonify(Error="Required Parameter is missing"), 400


def readSessionSubSessions(headers, json):
    coachID = securityDAO.getTokenOwner(headers['token'])
    parentSessionID = json['parentSessionID']
    if coachID and parentSessionID:
        if dao.readIfCoachManageSession(coachID, parentSessionID) or\
                dao.readIfCoachSupportSession(coachID, parentSessionID):
            search = '%' + str(json['search']) + '%'
            result = dao.searchSubSessions(parentSessionID, search)
            sessions = list()
            for session in result:
                sessions.append(session.json())
            return jsonify(Sessions=sessions), 200
        else:
            return jsonify(Error="User doesnt have access to session"), 400
    else:
        return jsonify(Error="Required Parameter is missing"), 400


def createPractice(headers, json):
    coachID = securityDAO.getTokenOwner(headers['token'])
    if json != 3:
        sessionID = json['sessionID']
        exerciseID = json['exerciseID']
        repetitions = json['repetitions']

        if coachID and sessionID and exerciseID and repetitions:
            if dao.readIfCoachManageSession(coachID, sessionID) or dao.readIfCoachSupportSession(coachID, sessionID):
                id = dao.createPractice(exerciseID, sessionID, repetitions)
                if id:
                    return jsonify(practiceID=id)
                return jsonify(Success="Practice added"), 200
            else:
                return jsonify(Error="User can't access practice")
        else:
            return jsonify(Error="Required Parameter is missing"), 400


def practiceDetails(headers, json):
    coachID = securityDAO.getTokenOwner(headers['token'])
    practiceID = json['practiceID']
    if coachID and practiceID:
        if dao.readIfCoachManagePractice(coachID, practiceID) or dao.readIfCoachSupportPractice(coachID, practiceID):
            result = dao.readPracticeByID(practiceID)
            if result is not None:
                practice = result[0].json()
                practice.update(result[1].json())
                return jsonify(Practice=practice), 200
            else:
                return jsonify(Practice="Nothing Found"), 200
        else:
            return jsonify(Error="User doesnt have access to plan"), 400
    else:
        return jsonify(Error="Required Parameter is missing"), 400


def practiceSearch(headers, json):
    coachID = securityDAO.getTokenOwner(headers['token'])
    sessionID = json['sessionID']
    if coachID and sessionID:
        if dao.readIfCoachManageSession(coachID, sessionID) or dao.readIfCoachSupportSession(coachID, sessionID):
            search = '%' + str(json['search']) + '%'
            result = dao.searchPractices(sessionID, search)
            practices = list()
            for practice in result:
                record = practice[0].json()
                record.update(practice[1].json())
                practices.append(record)
            return jsonify(Practices=practices), 200
        else:
            return jsonify(Error="User doesnt have access to session"), 400
    else:
        return jsonify(Error="Required Parameter is missing"), 400


def practiceUpdate(headers, json):
    coachID = securityDAO.getTokenOwner(headers['token'])
    practiceID = json['practiceID']
    repetitions = json['repetitions']

    if coachID and practiceID and repetitions:
        if dao.readIfCoachManagePractice(coachID, practiceID):
            dao.updatePractice(practiceID, repetitions)
            return jsonify(Success="Practice Updated"), 200
        else:
            return jsonify(Error="User cant access this Practice"), 400
    else:
        return jsonify(Error="Required Parameter is missing"), 400


def practiceDelete(headers, json):
    coachID = securityDAO.getTokenOwner(headers['token'])
    practiceID = json['practiceID']
    isDeleted = json['isDeleted']
    if coachID and practiceID and isDeleted is not None:
        if dao.readIfCoachManagePractice(coachID, practiceID):
            dao.deletePractice(practiceID, isDeleted)
            return jsonify(Success="Practice Delete Status changed."), 200
        else:
            return jsonify(Error="User cant access this practice"), 400
    else:
        return jsonify(Error="Required Parameter is missing"), 400


def createResult(headers, json):
    coachID = securityDAO.getTokenOwner(headers['token'])
    if json != 6:
        practiceID = json['practiceID']
        athleteID = json['athleteID']
        unitID = json['unitID']
        result = json['result']
        resultDate = json['resultDate']
        resultDescription = json['resultDescription']

        if coachID and practiceID and athleteID and unitID and result:
            if dao.readIfCoachManagePractice(coachID, practiceID) or dao.readIfCoachSupportPractice(coachID, practiceID):
                id = dao.createResult(practiceID, athleteID, unitID, result, resultDate, resultDescription)
                if id:
                    return jsonify(resultID=id)
                return jsonify(Success="Result added"), 200
            else:
                return jsonify(Error="User can't access practice")
        else:
            return jsonify(Error="Required Parameter is missing"), 400


def resultUpdate(headers, json):
    coachID = securityDAO.getTokenOwner(headers['token'])
    resultID = json['resultID']
    unitID = json['unitID']
    result = json['result']
    resultDate = json['resultDate']
    resultDescription = json['resultDescription']

    if coachID and resultID and (unitID or result or resultDate or resultDescription):
        if dao.readIfCoachManageResult(coachID, resultID):
            dao.updateResult(resultID, unitID, result, resultDate, resultDescription)
            return jsonify(Success="Result Updated"), 200
        else:
            return jsonify(Error="User cant access this result"), 400
    else:
        return jsonify(Error="Required Parameter is missing"), 400


def resultDelete(headers, json):
    coachID = securityDAO.getTokenOwner(headers['token'])
    resultID = json['resultID']
    if coachID and resultID:
        if dao.readIfCoachManageResult(coachID, resultID):
            dao.deleteResult(resultID)
            return jsonify(Success="Result Deleted."), 200
        else:
            return jsonify(Error="User cant access this result"), 400
    else:
        return jsonify(Error="Required Parameter is missing"), 400


def resultDetails(headers, json):
    coachID = securityDAO.getTokenOwner(headers['token'])
    resultID = json['resultID']
    if coachID and resultID:
        if dao.readIfCoachManageResult(coachID, resultID) or dao.readIfCoachSupportResult(coachID, resultID):
            result = dao.readResultByID(resultID)
            if result is not None:
                return jsonify(Result=result.json()), 200
            else:
                return jsonify(Practice="Nothing Found"), 200
        else:
            return jsonify(Error="User doesnt have access to result"), 400
    else:
        return jsonify(Error="Required Parameter is missing"), 400


def resultSearch(headers, json):
    coachID = securityDAO.getTokenOwner(headers['token'])
    practiceID = json['practiceID']
    athleteID = json['athleteID']
    if coachID and practiceID and athleteID:
        if (dao.readIfCoachManagePractice(coachID, practiceID) or dao.readIfCoachSupportPractice(coachID, practiceID))\
                and (coachDAO.readIfAthleteInTeamFromSupport(coachID, athleteID) or
                     coachDAO.readIfAthleteFromCoach(coachID, athleteID)):
            search = '%' + str(json['search']) + '%'
            result = dao.searchResultsForAthleteInPractice(practiceID, athleteID, search)
            results = list()
            for row in result:
                results.append(row.json())
            return jsonify(Results=results), 200
        else:
            return jsonify(Error="User doesnt have access to athlete or practice"), 400
    elif coachID and practiceID:
        if dao.readIfCoachManagePractice(coachID, practiceID) or dao.readIfCoachSupportPractice(coachID, practiceID):
            search = '%' + str(json['search']) + '%'
            result = dao.searchResultsInPractice(practiceID, search)
            results = list()
            for row in result:
                results.append(row.json())
            return jsonify(Results=results), 200
        else:
            return jsonify(Error="User doesnt have access to practice"), 400
    elif coachID and athleteID:
        if coachDAO.readIfAthleteInTeamFromSupport(coachID, athleteID) or \
                coachDAO.readIfAthleteFromCoach(coachID, athleteID):
            search = '%' + str(json['search']) + '%'
            result = dao.searchResultsForAthlete(athleteID, search)
            results = list()
            for row in result:
                results.append(row.json())
            return jsonify(Results=results), 200
        else:
            return jsonify(Error="User doesnt have access to athlete"), 400
    else:
        return jsonify(Error="Required Parameter is missing"), 400


def timelineSearch(headers, json):
    coachID = securityDAO.getTokenOwner(headers['token'])
    if coachID:
            search = '%' + str(json['search']) + '%'
            result = dao.searchTimeline(coachID, search)
            result2 = dao.searchSupportTimeline(coachID, search)
            sessions = list()
            for session in result:
                team = session[0].json()
                team.update(session[1].json())
                team.update(session[2].json())
                sessions.append(team)
            for session in result2:
                team = session[0].json()
                team.update(session[1].json())
                team.update(session[2].json())
                team.update(session[3].json())
                sessions.append(team)
            return jsonify(Sessions=sessions), 200

    else:
        return jsonify(Error="Required Parameter is missing"), 400


def mlAnalyze(headers, json):
    coachID = securityDAO.getTokenOwner(headers['token'])
    athletes = json['athletes']
    sessions = json['sessions']
    competition_week = json['cw']
    if len(athletes) <= 0 or len(sessions) <= 0:
        return jsonify(Error="Insufficient Data for analysis"), 400
    requestjson = [competition_week]
    for athleteID in athletes:
        for sessionID in sessions:
            record = dao.readResultsForAthleteIInSession(athleteID, sessionID)
            requestjson.append(record)
    return jsonify(Results=requestjson)

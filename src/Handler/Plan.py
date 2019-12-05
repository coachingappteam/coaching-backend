import json

import eventlet
from flask import jsonify
import requests
from src.config import AZURE_CODE, AZURE_URL
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
                    return jsonify(planID=id), 200
                return jsonify(Success="Plan added"), 200
            else:
                return jsonify(Error="User can't access team"), 403
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
                return jsonify(Plan="Nothing Found"), 404
        else:
            return jsonify(Error="User doesnt have access to plan"), 403
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
            return jsonify(Error="User doesnt have access to plan"), 403
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
            return jsonify(Error="User cant access this plan"), 403
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
            return jsonify(Error="User cant access this plan"), 403
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
                    return jsonify(sessionID=id), 200
                return jsonify(Success="Session added"), 200
            else:
                return jsonify(Error="User can't access plan"), 403
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
                return jsonify(Plan="Nothing Found"), 404
        else:
            return jsonify(Error="User doesnt have access to plan"), 403
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
            return jsonify(Error="User doesnt have access to plan"), 403
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
            return jsonify(Error="User cant access this session"), 403
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
            return jsonify(Error="User cant access this session"), 403
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
            return jsonify(Error="User doesnt have access to plan"), 403
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
            return jsonify(Error="User doesnt have access to session"), 403
    else:
        return jsonify(Error="Required Parameter is missing"), 400


def createPractice(headers, json):
    coachID = securityDAO.getTokenOwner(headers['token'])
    if json != 3:
        sessionID = json['sessionID']
        exerciseID = json['exerciseID']
        repetitions = json['repetitions']
        unitID = json['unitID']
        measure = json['measure']

        if coachID and sessionID and exerciseID and repetitions and unitID and measure:
            if dao.readIfCoachManageSession(coachID, sessionID) or dao.readIfCoachSupportSession(coachID, sessionID):
                id = dao.createPractice(exerciseID, sessionID, repetitions, unitID, measure)
                if id:
                    return jsonify(practiceID=id), 200
                return jsonify(Success="Practice added"), 200
            else:
                return jsonify(Error="User can't access practice"), 403
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
                return jsonify(Practice="Nothing Found"), 404
        else:
            return jsonify(Error="User doesnt have access to plan"), 403
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
                record.update(practice[2].json())
                practices.append(record)
            return jsonify(Practices=practices), 200
        else:
            return jsonify(Error="User doesnt have access to session"), 403
    else:
        return jsonify(Error="Required Parameter is missing"), 400


def practiceUpdate(headers, json):
    coachID = securityDAO.getTokenOwner(headers['token'])
    practiceID = json['practiceID']
    repetitions = json['repetitions']
    unitID = json['unitID']
    measure = json['measure']

    if coachID and practiceID and (repetitions or unitID or measure):
        if dao.readIfCoachManagePractice(coachID, practiceID):
            dao.updatePractice(practiceID, repetitions, unitID, measure)
            return jsonify(Success="Practice Updated"), 200
        else:
            return jsonify(Error="User cant access this Practice"), 403
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
            return jsonify(Error="User cant access this practice"), 403
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
                    return jsonify(resultID=id), 200
                return jsonify(Success="Result added"), 200
            else:
                return jsonify(Error="User can't access practice"), 403
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
            return jsonify(Error="User cant access this result"), 403
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
            return jsonify(Error="User cant access this result"), 403
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
                return jsonify(Practice="Nothing Found"), 404
        else:
            return jsonify(Error="User doesnt have access to result"), 403
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
            return jsonify(Error="User doesnt have access to athlete or practice"), 403
    elif coachID and practiceID:
        if dao.readIfCoachManagePractice(coachID, practiceID) or dao.readIfCoachSupportPractice(coachID, practiceID):
            search = '%' + str(json['search']) + '%'
            result = dao.searchResultsInPractice(practiceID, search)
            results = list()
            for row in result:
                results.append(row.json())
            return jsonify(Results=results), 200
        else:
            return jsonify(Error="User doesnt have access to practice"), 403
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
            return jsonify(Error="User doesnt have access to athlete"), 403
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


def mlAnalyze(headers, jsonObj):
    coachID = securityDAO.getTokenOwner(headers['token'])
    athletes = jsonObj['athletes']
    sessions = jsonObj['sessions']
    competition_week = jsonObj['cw']
    if len(athletes) <= 0 or len(sessions) <= 0 or competition_week is None or \
            competition_week > 1 or competition_week < 0:
        return jsonify(Error="Insufficient Data for analysis"), 400
    # requestjson = list()
    for sessionID in sessions:
        jsonObj = {"results": [],
                "sessionID": sessionID,
                "competition_week": competition_week
                   }
        if dao.readIfCoachManageSession(coachID, sessionID) or dao.readIfCoachSupportSession(coachID, sessionID):
            for athleteID in athletes:
                if coachDAO.readIfAthleteInTeamFromSupport(coachID, athleteID) \
                        or coachDAO.readIfAthleteFromCoach(coachID, athleteID):
                    resultTemp = {"id": athleteID, "role": None, "back": [], "breast": [], "butterfly": [], "drill": [],
                                  "free": [], "im": [], "kick": [], "pull_paddle": []}
                    record = dao.readResultsForAthleteInSession(athleteID, sessionID)
                    if len(record) > 0:
                        for row in record:
                            resultTemp[row[0]] = [row[1], row[2], row[3]]
                        roles = coachDAO.getRolesByAthleteID(athleteID)
                        if len(roles) > 0:
                            for role in roles:
                                resultTemp['role'] = role[0].json()['roleID']
                                if not dao.alreadyAnalyzed(sessionID, resultTemp['id'], resultTemp['role']):
                                    jsonObj['results'].append(resultTemp)
                                    requests.post(AZURE_URL + AZURE_CODE, data=json.dumps(jsonObj))
    return jsonify(Succes="Sent predictions")


def analyticForAthleteInCompetition(headers, json):
    coachID = securityDAO.getTokenOwner(headers['token'])
    athleteID = json['athleteID']
    roleID = json['roleID']
    if coachID and athleteID and roleID:
        if (coachDAO.readIfAthleteInTeamFromSupport(coachID, athleteID) or
                     coachDAO.readIfAthleteFromCoach(coachID, athleteID)):
            result = dao.searchSessionResultsByAthleteAndRoleID(athleteID, roleID)
            stat = list()
            for row in result:
                stat.append({
                    "firstName": row[0], "lastName": row[1], "sessionDate": row[3], "roleName": row[2],
                    "result": row[4], "unit": row[5]
                })
            return jsonify(Results=stat), 200
        else:
            return jsonify(Error="User cant access this athlete"), 403
    else:
        return jsonify(Error="Required Parameter is missing"), 400


def mlRecordResult(json):
    predictions = json['predictions']
    sessionID = json['sessionID']
    if len(predictions) > 0:
        for row in predictions:
            if not dao.readIfPairAdded(row['id'], row['role'], sessionID):
                dao.createAnalyzed(row['id'], row['role'], sessionID, row['performance'])
        return jsonify(Success="All performance results added."), 200
    return jsonify(Error="Insufficient Arguments"), 400


def mlRecordFeedback(headers, json):
    coachID = securityDAO.getTokenOwner(headers['token'])
    analyzedID = json['analyzedID']
    feedback = json['feedback']
    if coachID and analyzedID and feedback is not None:
        dao.updateAnalyze(analyzedID, feedback)
    else:
        return jsonify(Error="Required Parameter is missing"), 400


def mlAnalyzeDetails(headers, json):
    coachID = securityDAO.getTokenOwner(headers['token'])
    analyzedID = json['analyzedID']
    if coachID and analyzedID:
        result = dao.readAnalyzeByID(analyzedID)
        if result is not None:
            return jsonify(Analyze=result.json()), 200
        else:
            return jsonify(Analyze="Nothing Found"), 404
    else:
        return jsonify(Error="Required Parameter is missing"), 400


def mlAnlyzedSearch(headers, json):
    coachID = securityDAO.getTokenOwner(headers['token'])
    sessionID = json['sessionID']
    athleteID = json['athleteID']
    if coachID and sessionID and athleteID:
        if (dao.readIfCoachManageSession(coachID, sessionID) or dao.readIfCoachSupportSession(coachID, sessionID)) \
                and (coachDAO.readIfAthleteInTeamFromSupport(coachID, athleteID) or
                     coachDAO.readIfAthleteFromCoach(coachID, athleteID)):
            search = '%' + str(json['search']) + '%'
            result = dao.searchAnalyzedForAthleteInSession(sessionID, athleteID, search)
            results = list()
            for row in result:
                results.append(row.json())
            return jsonify(Analyzed=results), 200
        else:
            return jsonify(Error="User doesnt have access to athlete or session"), 403
    elif coachID and sessionID:
        if dao.readIfCoachManageSession(coachID, sessionID) or dao.readIfCoachSupportSession(coachID, sessionID):
            search = '%' + str(json['search']) + '%'
            result = dao.searchAnalyzedInSession(sessionID, search)
            results = list()
            for row in result:
                results.append(row.json())
            return jsonify(Analyzed=results), 200
        else:
            return jsonify(Error="User doesnt have access to session"), 403
    elif coachID and athleteID:
        if coachDAO.readIfAthleteInTeamFromSupport(coachID, athleteID) or \
                coachDAO.readIfAthleteFromCoach(coachID, athleteID):
            search = '%' + str(json['search']) + '%'
            result = dao.searchAnalyzedForAthlete(athleteID, search)
            results = list()
            for row in result:
                results.append(row.json())
            return jsonify(Analyzed=results), 200
        else:
            return jsonify(Error="User doesnt have access to athlete"), 403
    else:
        return jsonify(Error="Required Parameter is missing"), 400
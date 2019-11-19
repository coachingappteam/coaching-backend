from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
from src.Handler import Coach, Plan, Sport
import sys
import src.config as config

app = Flask(__name__, template_folder='./src/template')
CORS(app)


# ==================== Main Methods ====================== #
@app.route('/')
def mainPage():
    return render_template('mainpage.html')


@app.route('/test', methods=['GET'])
def testMethod():
    if request.method == 'GET':
        return jsonify(Success="Method allowed"), 200
    else:
        return jsonify(Error="Method not allowed"), 404

# ==================== Coach Methods ====================== #
@app.route('/coach/login', methods=['POST'])
def coachLogin():
    if request.method == 'POST':
        print(str(request))
        result = Coach.loginCoach(request.json)
        return result
    else:
        return jsonify(Error="Method not allowed"), 404


@app.route('/coach/signup', methods=['POST'])
def coachSignup():
    if request.method == 'POST':
        result = Coach.signupCoach(request.json)
        return result
    else:
        return jsonify(Error="Method not allowed"), 404


@app.route('/coach/signout', methods=['DELETE'])
def coachSignout():
    if request.method == 'DELETE':
        result = Coach.signoutCoach(request.headers)
        return result
    else:
        return jsonify(Error="Method not allowed"), 404


@app.route('/coach', methods=['GET'])
def coachDetails():
    if request.method == 'GET':
        if not Coach.checkToken(request.headers):
            return jsonify(Error="Invalid or Missing Security Token"), 404
        result = Coach.readCoach(request.headers)
        return result
    else:
        return jsonify(Error="Method not allowed"), 404


@app.route('/coach/details/<string:coachID>', methods=['GET'])
def coachDetailsByID(coachID):
    if request.method == 'GET':
        if not Coach.checkToken(request.headers):
            return jsonify(Error="Invalid or Missing Security Token"), 404
        result = Coach.readCoachByID({"coachID": coachID})
        return result
    else:
        return jsonify(Error="Method not allowed"), 404


@app.route('/coach/search', methods=['POST'])
def coachSearch():
    if request.method == 'POST':
        if not Coach.checkToken(request.headers):
            return jsonify(Error="Invalid or Missing Security Token"), 404
        result = Coach.searchCoaches(request.json)
        return result
    else:
        return jsonify(Error="Method not allowed"), 404


@app.route('/coach/update', methods=['PATCH'])
def coachUpdate():
    if request.method == 'PATCH':
        if not Coach.checkToken(request.headers):
            return jsonify(Error="Invalid or Missing Security Token"), 404
        result = Coach.updateCoach(request.headers, request.json)
        return result
    else:
        return jsonify(Error="Method not allowed"), 404


@app.route('/coach/delete', methods=['PATCH'])
def coachDelete():
    if request.method == 'PATCH':
        if not Coach.checkToken(request.headers):
            return jsonify(Error="Invalid or Missing Security Token"), 404
        result = Coach.deleteCoach(request.headers, request.json)
        return result
    else:
        return jsonify(Error="Method not allowed"), 404

# ==================== Athlete Methods ====================== #
@app.route('/coach/athlete/create', methods=['POST'])
def createAthlete():
    if request.method == 'POST':
        if not Coach.checkToken(request.headers):
            return jsonify(Error="Invalid or Missing Security Token"), 404
        result = Coach.createAthlete(request.headers, request.json)
        return result
    else:
        return jsonify(Error="Method not allowed"), 404


@app.route('/coach/athlete/details/<int:athleteID>', methods=['GET'])
def athleteDetails(athleteID):
    if request.method == 'GET':
        if not Coach.checkToken(request.headers):
            return jsonify(Error="Invalid or Missing Security Token"), 404
        result = Coach.athleteDetails(request.headers, {"athleteID": athleteID})
        return result
    else:
        return jsonify(Error="Method not allowed"), 404


@app.route('/coach/athlete/search', methods=['POST'])
def athleteSearch():
    if request.method == 'POST':
        if not Coach.checkToken(request.headers):
            return jsonify(Error="Invalid or Missing Security Token"), 404
        result = Coach.athleteSearch(request.headers, request.json)
        return result
    else:
        return jsonify(Error="Method not allowed"), 404


@app.route('/coach/athlete/update', methods=['PATCH'])
def athleteUpdate():
    if request.method == 'PATCH':
        if not Coach.checkToken(request.headers):
            return jsonify(Error="Invalid or Missing Security Token"), 404
        result = Coach.athleteUpdate(request.headers, request.json)
        return result
    else:
        return jsonify(Error="Method not allowed"), 404


@app.route('/coach/athlete/delete', methods=['PATCH'])
def athleteDelete():
    if request.method == 'PATCH':
        if not Coach.checkToken(request.headers):
            return jsonify(Error="Invalid or Missing Security Token"), 404
        result = Coach.athleteDelete(request.headers, request.json)
        return result
    else:
        return jsonify(Error="Method not allowed"), 404

# ==================== Team Methods ====================== #
@app.route('/coach/team/create', methods=['POST'])
def createTeam():
    if request.method == 'POST':
        if not Coach.checkToken(request.headers):
            return jsonify(Error="Invalid or Missing Security Token"), 404
        result = Coach.createTeam(request.headers, request.json)
        return result
    else:
        return jsonify(Error="Method not allowed"), 404


@app.route('/coach/team/details/<int:teamID>', methods=['GET'])
def teamDetails(teamID):
    if request.method == 'GET':
        if not Coach.checkToken(request.headers):
            return jsonify(Error="Invalid or Missing Security Token"), 404
        result = Coach.teamDetails(request.headers, {"teamID": teamID})
        return result
    else:
        return jsonify(Error="Method not allowed"), 404


@app.route('/coach/team/search', methods=['POST'])
def teamSearch():
    if request.method == 'POST':
        if not Coach.checkToken(request.headers):
            return jsonify(Error="Invalid or Missing Security Token"), 404
        result = Coach.teamSearch(request.headers, request.json)
        return result
    else:
        return jsonify(Error="Method not allowed"), 404


@app.route('/coach/team/update', methods=['PATCH'])
def teamUpdate():
    if request.method == 'PATCH':
        if not Coach.checkToken(request.headers):
            return jsonify(Error="Invalid or Missing Security Token"), 404
        result = Coach.teamUpdate(request.headers, request.json)
        return result
    else:
        return jsonify(Error="Method not allowed"), 404


@app.route('/coach/team/delete', methods=['DELETE'])
def teamDelete():
    if request.method == 'DELETE':
        if not Coach.checkToken(request.headers):
            return jsonify(Error="Invalid or Missing Security Token"), 404
        result = Coach.teamDelete(request.headers, request.json)
        return result
    else:
        return jsonify(Error="Method not allowed"), 404


# ==================== Support Methods ====================== #
@app.route('/coach/team/support/create', methods=['POST'])
def createTeamSupport():
    if request.method == 'POST':
        if not Coach.checkToken(request.headers):
            return jsonify(Error="Invalid or Missing Security Token"), 404
        result = Coach.addCoachToTeam(request.headers, request.json)
        return result
    else:
        return jsonify(Error="Method not allowed"), 404


@app.route('/coach/team/support/coaches/<int:teamID>', methods=['GET'])
def readTeamCoaches(teamID):
    if request.method == 'GET':
        if not Coach.checkToken(request.headers):
            return jsonify(Error="Invalid or Missing Security Token"), 404
        result = Coach.readCoachesInCharge(request.headers, {"teamID": teamID})
        return result
    else:
        return jsonify(Error="Method not allowed"), 404


@app.route('/coach/team/support/teams', methods=['GET'])
def readCoachTeams():
    if request.method == 'GET':
        if not Coach.checkToken(request.headers):
            return jsonify(Error="Invalid or Missing Security Token"), 404
        result = Coach.readTeamsOfCoach(request.headers)
        return result
    else:
        return jsonify(Error="Method not allowed"), 404


@app.route('/coach/team/support/delete', methods=['DELETE'])
def deleteTeamSupport():
    if request.method == 'DELETE':
        if not Coach.checkToken(request.headers):
            return jsonify(Error="Invalid or Missing Security Token"), 404
        result = Coach.deleteSupport(request.headers, request.json)
        return result
    else:
        return jsonify(Error="Method not allowed"), 404


# ==================== Member Methods ====================== #
@app.route('/coach/team/member/create', methods=['POST'])
def createTeamMember():
    if request.method == 'POST':
        if not Coach.checkToken(request.headers):
            return jsonify(Error="Invalid or Missing Security Token"), 404
        result = Coach.addAthleteToTeam(request.headers, request.json)
        return result
    else:
        return jsonify(Error="Method not allowed"), 404


@app.route('/coach/team/member/athletes/<int:teamID>', methods=['GET'])
def readTeamAthletes(teamID):
    if request.method == 'GET':
        if not Coach.checkToken(request.headers):
            return jsonify(Error="Invalid or Missing Security Token"), 404
        result = Coach.readAthletesInTeam(request.headers, {"teamID": teamID})
        return result
    else:
        return jsonify(Error="Method not allowed"), 404


@app.route('/coach/team/member/teams/<int:athleteID>', methods=['GET'])
def readAthleteTeams(athleteID):
    if request.method == 'GET':
        if not Coach.checkToken(request.headers):
            return jsonify(Error="Invalid or Missing Security Token"), 404
        result = Coach.readTeamsOfAthlete(request.headers, {"athleteID": athleteID})
        return result
    else:
        return jsonify(Error="Method not allowed"), 404


@app.route('/coach/team/member/delete', methods=['DELETE'])
def deleteTeamMember():
    if request.method == 'DELETE':
        if not Coach.checkToken(request.headers):
            return jsonify(Error="Invalid or Missing Security Token"), 404
        result = Coach.deleteMember(request.headers, request.json)
        return result
    else:
        return jsonify(Error="Method not allowed"), 404


# ==================== Focus Methods ====================== #
@app.route('/coach/athlete/focus/create', methods=['POST'])
def createAthleteFocus():
    if request.method == 'POST':
        if not Coach.checkToken(request.headers):
            return jsonify(Error="Invalid or Missing Security Token"), 404
        result = Coach.addRoleToAthlete(request.headers, request.json)
        return result
    else:
        return jsonify(Error="Method not allowed"), 404


@app.route('/coach/athlete/focus/athletes/<int:roleID>', methods=['GET'])
def readAthletesForRole(roleID):
    if request.method == 'GET':
        if not Coach.checkToken(request.headers):
            return jsonify(Error="Invalid or Missing Security Token"), 404
        result = Coach.readAthletesInRole(request.headers, {"roleID": roleID})
        return result
    else:
        return jsonify(Error="Method not allowed"), 404


@app.route('/coach/athlete/focus/roles/<int:athleteID>', methods=['GET'])
def readRolesForAthlete(athleteID):
    if request.method == 'GET':
        if not Coach.checkToken(request.headers):
            return jsonify(Error="Invalid or Missing Security Token"), 404
        result = Coach.readRolesOfAthlete(request.headers, {"athleteID": athleteID})
        return result
    else:
        return jsonify(Error="Method not allowed"), 404


@app.route('/coach/athlete/focus/delete', methods=['DELETE'])
def deleteAthleteFocus():
    if request.method == 'DELETE':
        if not Coach.checkToken(request.headers):
            return jsonify(Error="Invalid or Missing Security Token"), 404
        result = Coach.deleteFocus(request.headers, request.json)
        return result
    else:
        return jsonify(Error="Method not allowed"), 404


# ==================== Attendance Methods ====================== #
@app.route('/coach/athlete/attendance/create', methods=['POST'])
def createAthleteAttendance():
    if request.method == 'POST':
        if not Coach.checkToken(request.headers):
            return jsonify(Error="Invalid or Missing Security Token"), 404
        result = Coach.addAttendanceToAthlete(request.headers, request.json)
        return result
    else:
        return jsonify(Error="Method not allowed"), 404


@app.route('/coach/athlete/attendance/athletes/<int:sessionID>', methods=['GET'])
def readAthletesForSession(sessionID):
    if request.method == 'GET':
        if not Coach.checkToken(request.headers):
            return jsonify(Error="Invalid or Missing Security Token"), 404
        result = Coach.readAthletesInSession(request.headers, {"sessionID": sessionID})
        return result
    else:
        return jsonify(Error="Method not allowed"), 404


@app.route('/coach/athlete/attendance/sessions/<int:athleteID>', methods=['GET'])
def readSessionsForAthlete(athleteID):
    if request.method == 'GET':
        if not Coach.checkToken(request.headers):
            return jsonify(Error="Invalid or Missing Security Token"), 404
        result = Coach.readSessionsOfAthlete(request.headers, {"athleteID": athleteID})
        return result
    else:
        return jsonify(Error="Method not allowed"), 404


@app.route('/coach/athlete/attendance/update', methods=['PATCH'])
def updateAthleteAttendance():
    if request.method == 'DELETE':
        if not Coach.checkToken(request.headers):
            return jsonify(Error="Invalid or Missing Security Token"), 404
        result = Coach.updateAttendance(request.headers, request.json)
        return result
    else:
        return jsonify(Error="Method not allowed"), 404


@app.route('/coach/athlete/attendance/delete', methods=['DELETE'])
def deleteAthleteAttendance():
    if request.method == 'DELETE':
        if not Coach.checkToken(request.headers):
            return jsonify(Error="Invalid or Missing Security Token"), 404
        result = Coach.deleteAttendance(request.headers, request.json)
        return result
    else:
        return jsonify(Error="Method not allowed"), 404


# ==================== Sport Methods ====================== #
@app.route('/sport/create', methods=['POST'])
def createSport():
    if request.method == 'POST':
        if not Coach.checkAdminToken(request.headers):
            return jsonify(Error="Invalid or Missing Admin Security Token"), 404
        result = Sport.createSport(request.json)
        return result
    else:
        return jsonify(Error="Method not allowed"), 404


@app.route('/sport/details/<int:sportID>', methods=['GET'])
def sportDetails(sportID):
    if request.method == 'GET':
        if not Coach.checkToken(request.headers):
            return jsonify(Error="Invalid or Missing Security Token"), 404
        result = Sport.sportDetails({"sportID": sportID})
        return result
    else:
        return jsonify(Error="Method not allowed"), 404


@app.route('/sport/search', methods=['POST'])
def sportSearch():
    if request.method == 'POST':
        if not Coach.checkToken(request.headers):
            return jsonify(Error="Invalid or Missing Security Token"), 404
        result = Sport.sportSearch(request.json)
        return result
    else:
        return jsonify(Error="Method not allowed"), 404


@app.route('/sport/delete', methods=['DELETE'])
def deleteSport():
    if request.method == 'DELETE':
        if not Coach.checkAdminToken(request.headers):
            return jsonify(Error="Invalid or Missing Admin Security Token"), 404
        result = Sport.deleteSport(request.json)
        return result
    else:
        return jsonify(Error="Method not allowed"), 404


# ==================== Unit Methods ====================== #
@app.route('/unit/create', methods=['POST'])
def createUnit():
    if request.method == 'POST':
        if not Coach.checkAdminToken(request.headers):
            return jsonify(Error="Invalid or Missing Admin Security Token"), 404
        result = Sport.createUnit(request.json)
        return result
    else:
        return jsonify(Error="Method not allowed"), 404


@app.route('/unit/details/<int:unitID>', methods=['GET'])
def unitDetails(unitID):
    if request.method == 'GET':
        if not Coach.checkToken(request.headers):
            return jsonify(Error="Invalid or Missing Security Token"), 404
        result = Sport.unitDetails({"unitID": unitID})
        return result
    else:
        return jsonify(Error="Method not allowed"), 404


@app.route('/unit/search', methods=['POST'])
def unitSearch():
    if request.method == 'POST':
        if not Coach.checkToken(request.headers):
            return jsonify(Error="Invalid or Missing Security Token"), 404
        result = Sport.unitSearch(request.json)
        return result
    else:
        return jsonify(Error="Method not allowed"), 404


@app.route('/unit/delete', methods=['DELETE'])
def deleteUnit():
    if request.method == 'DELETE':
        if not Coach.checkAdminToken(request.headers):
            return jsonify(Error="Invalid or Missing Admin Security Token"), 404
        result = Sport.deleteUnit(request.json)
        return result
    else:
        return jsonify(Error="Method not allowed"), 404


# ==================== Role Methods ====================== #
@app.route('/sport/role/create', methods=['POST'])
def createRole():
    if request.method == 'POST':
        if not Coach.checkAdminToken(request.headers):
            return jsonify(Error="Invalid or Missing Admin Security Token"), 404
        result = Sport.createRole(request.json)
        return result
    else:
        return jsonify(Error="Method not allowed"), 404


@app.route('/sport/role/details/<int:roleID>', methods=['GET'])
def roleDetails(roleID):
    if request.method == 'GET':
        if not Coach.checkToken(request.headers):
            return jsonify(Error="Invalid or Missing Security Token"), 404
        result = Sport.roleDetails({"roleID": roleID})
        return result
    else:
        return jsonify(Error="Method not allowed"), 404


@app.route('/sport/role/search', methods=['POST'])
def roleSearch():
    if request.method == 'POST':
        if not Coach.checkToken(request.headers):
            return jsonify(Error="Invalid or Missing Security Token"), 404
        result = Sport.roleSearch(request.json)
        return result
    else:
        return jsonify(Error="Method not allowed"), 404


@app.route('/sport/role/delete', methods=['DELETE'])
def deleteRole():
    if request.method == 'DELETE':
        if not Coach.checkAdminToken(request.headers):
            return jsonify(Error="Invalid or Missing Admin Security Token"), 404
        result = Sport.deleteRole(request.json)
        return result
    else:
        return jsonify(Error="Method not allowed"), 404


# ==================== Exercise Methods ====================== #
@app.route('/sport/exercise/create', methods=['POST'])
def createExercise():
    if request.method == 'POST':
        if not Coach.checkAdminToken(request.headers):
            return jsonify(Error="Invalid or Missing Admin Security Token"), 404
        result = Sport.createExercise(request.json)
        return result
    else:
        return jsonify(Error="Method not allowed"), 404


@app.route('/sport/exercise/details/<int:exerciseID>', methods=['GET'])
def exerciseDetails(exerciseID):
    if request.method == 'GET':
        if not Coach.checkToken(request.headers):
            return jsonify(Error="Invalid or Missing Security Token"), 404
        result = Sport.exerciseDetails({"exerciseID": exerciseID})
        return result
    else:
        return jsonify(Error="Method not allowed"), 404


@app.route('/sport/exercise/search', methods=['POST'])
def exerciseSearch():
    if request.method == 'POST':
        if not Coach.checkToken(request.headers):
            return jsonify(Error="Invalid or Missing Security Token"), 404
        result = Sport.exerciseSearch(request.json)
        return result
    else:
        return jsonify(Error="Method not allowed"), 404


@app.route('/sport/exercise/delete', methods=['DELETE'])
def deleteExercise():
    if request.method == 'DELETE':
        if not Coach.checkAdminToken(request.headers):
            return jsonify(Error="Invalid or Missing Admin Security Token"), 404
        result = Sport.deleteExercise(request.json)
        return result
    else:
        return jsonify(Error="Method not allowed"), 404


# ==================== Improve Methods ====================== #
@app.route('/sport/role/improve/create', methods=['POST'])
def createRoleImprove():
    if request.method == 'POST':
        if not Coach.checkAdminToken(request.headers):
            return jsonify(Error="Invalid or Missing Security Token"), 404
        result = Sport.addExerciseToRole(request.json)
        return result
    else:
        return jsonify(Error="Method not allowed"), 404


@app.route('/sport/role/improve/roles/<int:exerciseID>', methods=['GET'])
def readRolesForExercise(exerciseID):
    if request.method == 'GET':
        if not Coach.checkToken(request.headers):
            return jsonify(Error="Invalid or Missing Security Token"), 404
        result = Sport.readRolesForExercise({"exerciseID": exerciseID})
        return result
    else:
        return jsonify(Error="Method not allowed"), 404


@app.route('/sport/role/improve/exercises/<int:roleID>', methods=['GET'])
def readSessionsForRole(roleID):
    if request.method == 'GET':
        if not Coach.checkToken(request.headers):
            return jsonify(Error="Invalid or Missing Security Token"), 404
        result = Sport.readExercisesOfRole({"roleID": roleID})
        return result
    else:
        return jsonify(Error="Method not allowed"), 404


@app.route('/sport/role/improve/delete', methods=['DELETE'])
def deleteRoleImprove():
    if request.method == 'DELETE':
        if not Coach.checkAdminToken(request.headers):
            return jsonify(Error="Invalid or Missing Security Token"), 404
        result = Sport.deleteImprovement(request.json)
        return result
    else:
        return jsonify(Error="Method not allowed"), 404


# ==================== Training Plan Methods ====================== #
@app.route('/plan/create', methods=['POST'])
def createPlan():
    if request.method == 'POST':
        if not Coach.checkToken(request.headers):
            return jsonify(Error="Invalid or Missing Security Token"), 404
        result = Plan.createPlan(request.headers, request.json)
        return result
    else:
        return jsonify(Error="Method not allowed"), 404


@app.route('/plan/details/<int:planID>', methods=['GET'])
def planDetails(planID):
    if request.method == 'GET':
        if not Coach.checkToken(request.headers):
            return jsonify(Error="Invalid or Missing Security Token"), 404
        result = Plan.planDetails(request.headers, {"planID": planID})
        return result
    else:
        return jsonify(Error="Method not allowed"), 404


@app.route('/plan/search/sub', methods=['POST'])
def getPlanSubPlans():
    if request.method == 'POST':
        if not Coach.checkToken(request.headers):
            return jsonify(Error="Invalid or Missing Security Token"), 404
        result = Plan.readPlanSubPlans(request.headers, request.json)
        return result
    else:
        return jsonify(Error="Method not allowed"), 404


@app.route('/plan/search', methods=['POST'])
def planSearch():
    if request.method == 'POST':
        if not Coach.checkToken(request.headers):
            return jsonify(Error="Invalid or Missing Security Token"), 404
        result = Plan.planSearch(request.headers, request.json)
        return result
    else:
        return jsonify(Error="Method not allowed"), 404


@app.route('/plan/update', methods=['PATCH'])
def planUpdate():
    if request.method == 'PATCH':
        if not Coach.checkToken(request.headers):
            return jsonify(Error="Invalid or Missing Security Token"), 404
        result = Plan.planUpdate(request.headers, request.json)
        return result
    else:
        return jsonify(Error="Method not allowed"), 404


@app.route('/plan/delete', methods=['DELETE'])
def planDelete():
    if request.method == 'DELETE':
        if not Coach.checkToken(request.headers):
            return jsonify(Error="Invalid or Missing Security Token"), 404
        result = Plan.planDelete(request.headers, request.json)
        return result
    else:
        return jsonify(Error="Method not allowed"), 404


# ==================== Session Methods ====================== #
@app.route('/plan/session/create', methods=['POST'])
def createSession():
    if request.method == 'POST':
        if not Coach.checkToken(request.headers):
            return jsonify(Error="Invalid or Missing Security Token"), 404
        result = Plan.createSession(request.headers, request.json)
        return result
    else:
        return jsonify(Error="Method not allowed"), 404


@app.route('/plan/session/details/<int:sessionID>', methods=['GET'])
def sessionDetails(sessionID):
    if request.method == 'GET':
        if not Coach.checkToken(request.headers):
            return jsonify(Error="Invalid or Missing Security Token"), 404
        result = Plan.sessionDetails(request.headers, {"sessionID": sessionID})
        return result
    else:
        return jsonify(Error="Method not allowed"), 404


@app.route('/plan/session/search', methods=['POST'])
def sessionSearch():
    if request.method == 'POST':
        if not Coach.checkToken(request.headers):
            return jsonify(Error="Invalid or Missing Security Token"), 404
        result = Plan.sessionSearch(request.headers, request.json)
        return result
    else:
        return jsonify(Error="Method not allowed"), 404

@app.route('/plan/session/timeline/search', methods=['POST'])
def timelineSearch():
    if request.method == 'POST':
        if not Coach.checkToken(request.headers):
            return jsonify(Error="Invalid or Missing Security Token"), 404
        result = Plan.timelineSearch(request.headers, request.json)
        return result
    else:
        return jsonify(Error="Method not allowed"), 404


@app.route('/plan/session/search/sub', methods=['POST'])
def getSessionSubSessions():
    if request.method == 'POST':
        if not Coach.checkToken(request.headers):
            return jsonify(Error="Invalid or Missing Security Token"), 404
        result = Plan.readSessionSubSessions(request.headers, request.json)
        return result
    else:
        return jsonify(Error="Method not allowed"), 404


@app.route('/plan/session/update', methods=['PATCH'])
def sessionUpdate():
    if request.method == 'PATCH':
        if not Coach.checkToken(request.headers):
            return jsonify(Error="Invalid or Missing Security Token"), 404
        result = Plan.sessionUpdate(request.headers, request.json)
        return result
    else:
        return jsonify(Error="Method not allowed"), 404


@app.route('/plan/session/delete', methods=['DELETE'])
def sessionDelete():
    if request.method == 'DELETE':
        if not Coach.checkToken(request.headers):
            return jsonify(Error="Invalid or Missing Security Token"), 404
        result = Plan.sessionDelete(request.headers, request.json)
        return result
    else:
        return jsonify(Error="Method not allowed"), 404


# ==================== Practice Methods ====================== #
@app.route('/plan/session/practice/create', methods=['POST'])
def createPractice():
    if request.method == 'POST':
        if not Coach.checkToken(request.headers):
            return jsonify(Error="Invalid or Missing Security Token"), 404
        result = Plan.createPractice(request.headers, request.json)
        return result
    else:
        return jsonify(Error="Method not allowed"), 404


@app.route('/plan/session/practice/details/<int:practiceID>', methods=['GET'])
def practiceDetails(practiceID):
    if request.method == 'GET':
        if not Coach.checkToken(request.headers):
            return jsonify(Error="Invalid or Missing Security Token"), 404
        result = Plan.practiceDetails(request.headers, {"practiceID": practiceID})
        return result
    else:
        return jsonify(Error="Method not allowed"), 404


@app.route('/plan/session/practice/search', methods=['POST'])
def practiceSearch():
    if request.method == 'POST':
        if not Coach.checkToken(request.headers):
            return jsonify(Error="Invalid or Missing Security Token"), 404
        result = Plan.practiceSearch(request.headers, request.json)
        return result
    else:
        return jsonify(Error="Method not allowed"), 404


@app.route('/plan/session/practice/update', methods=['PATCH'])
def practiceUpdate():
    if request.method == 'PATCH':
        if not Coach.checkToken(request.headers):
            return jsonify(Error="Invalid or Missing Security Token"), 404
        result = Plan.practiceUpdate(request.headers, request.json)
        return result
    else:
        return jsonify(Error="Method not allowed"), 404


@app.route('/plan/session/practice/delete', methods=['DELETE'])
def practiceDelete():
    if request.method == 'DELETE':
        if not Coach.checkToken(request.headers):
            return jsonify(Error="Invalid or Missing Security Token"), 404
        result = Plan.practiceDelete(request.headers, request.json)
        return result
    else:
        return jsonify(Error="Method not allowed"), 404


# ==================== Result Methods ====================== #
@app.route('/plan/session/practice/result/create', methods=['POST'])
def createResult():
    if request.method == 'POST':
        if not Coach.checkToken(request.headers):
            return jsonify(Error="Invalid or Missing Security Token"), 404
        result = Plan.createResult(request.headers, request.json)
        return result
    else:
        return jsonify(Error="Method not allowed"), 404


@app.route('/plan/session/practice/result/details/<int:resultID>', methods=['GET'])
def resultDetails(resultID):
    if request.method == 'GET':
        if not Coach.checkToken(request.headers):
            return jsonify(Error="Invalid or Missing Security Token"), 404
        result = Plan.resultDetails(request.headers, {"resultID": resultID})
        return result
    else:
        return jsonify(Error="Method not allowed"), 404


@app.route('/plan/session/practice/result/search', methods=['POST'])
def resultSearch():
    if request.method == 'POST':
        if not Coach.checkToken(request.headers):
            return jsonify(Error="Invalid or Missing Security Token"), 404
        result = Plan.resultSearch(request.headers, request.json)
        return result
    else:
        return jsonify(Error="Method not allowed"), 404


@app.route('/plan/session/practice/result/update', methods=['PATCH'])
def resultUpdate():
    if request.method == 'PATCH':
        if not Coach.checkToken(request.headers):
            return jsonify(Error="Invalid or Missing Security Token"), 404
        result = Plan.resultUpdate(request.headers, request.json)
        return result
    else:
        return jsonify(Error="Method not allowed"), 404


@app.route('/plan/session/practice/result/delete', methods=['DELETE'])
def resultDelete():
    if request.method == 'DELETE':
        if not Coach.checkToken(request.headers):
            return jsonify(Error="Invalid or Missing Security Token"), 404
        result = Plan.resultDelete(request.headers, request.json)
        return result
    else:
        return jsonify(Error="Method not allowed"), 404


# ==================== Machine Learning Methods ====================== #
@app.route('/ml/analyze', methods=['POST'])
def mlAnalyze():
    if request.method == 'POST':
        if not Coach.checkToken(request.headers):
            return jsonify(Error="Invalid or Missing Security Token"), 404
        result = Plan.mlAnalyze(request.headers, request.json)
        return result
    else:
        return jsonify(Error="Method not allowed"), 404


# ==================== Analytic Methods ====================== #
@app.route('/analytic/athlete/role/competition', methods=['POST'])
def analyticForAthleteInCompetition():
    if request.method == 'POST':
        if not Coach.checkToken(request.headers):
            return jsonify(Error="Invalid or Missing Security Token"), 404
        result = Plan.analyticForAthleteInCompetition(request.headers, request.json)
        return result
    else:
        return jsonify(Error="Method not allowed"), 404


# TODO add a route to get all exercises that can only be given in meets
if __name__ == '__main__':
    if len(sys.argv) == 2 :
        app.run(debug=((sys.argv[1].lower()) == "true"))
    else:
        config.local = False
        app.run()








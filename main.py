from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
from src.Handler import Coach, Plan, Sport

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


@app.route('/coach/details', methods=['GET'])
def coachDetailsByID():
    if request.method == 'GET':
        if not Coach.checkToken(request.headers):
            return jsonify(Error="Invalid or Missing Security Token"), 404
        result = Coach.readCoachByID(request.json)
        return result
    else:
        return jsonify(Error="Method not allowed"), 404


@app.route('/coach/search', methods=['GET'])
def coachSearch():
    if request.method == 'GET':
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


@app.route('/coach/athlete/details', methods=['GET'])
def athleteDetails():
    if request.method == 'GET':
        if not Coach.checkToken(request.headers):
            return jsonify(Error="Invalid or Missing Security Token"), 404
        result = Coach.athleteDetails(request.headers, request.json)
        return result
    else:
        return jsonify(Error="Method not allowed"), 404


@app.route('/coach/athlete/search', methods=['GET'])
def athleteSearch():
    if request.method == 'GET':
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


@app.route('/coach/team/details', methods=['GET'])
def teamDetails():
    if request.method == 'GET':
        if not Coach.checkToken(request.headers):
            return jsonify(Error="Invalid or Missing Security Token"), 404
        result = Coach.teamDetails(request.headers, request.json)
        return result
    else:
        return jsonify(Error="Method not allowed"), 404


@app.route('/coach/team/search', methods=['GET'])
def teamSearch():
    if request.method == 'GET':
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


@app.route('/coach/team/support/coaches', methods=['GET'])
def readTeamCoaches():
    if request.method == 'GET':
        if not Coach.checkToken(request.headers):
            return jsonify(Error="Invalid or Missing Security Token"), 404
        result = Coach.readCoachesInCharge(request.headers, request.json)
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


@app.route('/coach/team/member/athletes', methods=['GET'])
def readTeamAthletes():
    if request.method == 'GET':
        if not Coach.checkToken(request.headers):
            return jsonify(Error="Invalid or Missing Security Token"), 404
        result = Coach.readAthletesInTeam(request.headers, request.json)
        return result
    else:
        return jsonify(Error="Method not allowed"), 404


@app.route('/coach/team/member/teams', methods=['GET'])
def readAthleteTeams():
    if request.method == 'GET':
        if not Coach.checkToken(request.headers):
            return jsonify(Error="Invalid or Missing Security Token"), 404
        result = Coach.readTeamsOfAthlete(request.headers, request.json)
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


@app.route('/coach/athlete/focus/athletes', methods=['GET'])
def readAthletesForRole():
    if request.method == 'GET':
        if not Coach.checkToken(request.headers):
            return jsonify(Error="Invalid or Missing Security Token"), 404
        result = Coach.readAthletesInRole(request.headers, request.json)
        return result
    else:
        return jsonify(Error="Method not allowed"), 404


@app.route('/coach/athlete/focus/roles', methods=['GET'])
def readRolesForAthlete():
    if request.method == 'GET':
        if not Coach.checkToken(request.headers):
            return jsonify(Error="Invalid or Missing Security Token"), 404
        result = Coach.readRolesOfAthlete(request.headers, request.json)
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


@app.route('/sport/details', methods=['GET'])
def sportDetails():
    if request.method == 'GET':
        if not Coach.checkToken(request.headers):
            return jsonify(Error="Invalid or Missing Security Token"), 404
        result = Sport.sportDetails(request.json)
        return result
    else:
        return jsonify(Error="Method not allowed"), 404


@app.route('/sport/search', methods=['GET'])
def sportSearch():
    if request.method == 'GET':
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


@app.route('/unit/details', methods=['GET'])
def unitDetails():
    if request.method == 'GET':
        if not Coach.checkToken(request.headers):
            return jsonify(Error="Invalid or Missing Security Token"), 404
        result = Sport.unitDetails(request.json)
        return result
    else:
        return jsonify(Error="Method not allowed"), 404


@app.route('/unit/search', methods=['GET'])
def unitSearch():
    if request.method == 'GET':
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


@app.route('/sport/role/details', methods=['GET'])
def roleDetails():
    if request.method == 'GET':
        if not Coach.checkToken(request.headers):
            return jsonify(Error="Invalid or Missing Security Token"), 404
        result = Sport.roleDetails(request.json)
        return result
    else:
        return jsonify(Error="Method not allowed"), 404


@app.route('/sport/role/search', methods=['GET'])
def roleSearch():
    if request.method == 'GET':
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


@app.route('/sport/exercise/details', methods=['GET'])
def exerciseDetails():
    if request.method == 'GET':
        if not Coach.checkToken(request.headers):
            return jsonify(Error="Invalid or Missing Security Token"), 404
        result = Sport.exerciseDetails(request.json)
        return result
    else:
        return jsonify(Error="Method not allowed"), 404


@app.route('/sport/exercise/search', methods=['GET'])
def exerciseSearch():
    if request.method == 'GET':
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


@app.route('/plan/details', methods=['GET'])
def planDetails():
    if request.method == 'GET':
        if not Coach.checkToken(request.headers):
            return jsonify(Error="Invalid or Missing Security Token"), 404
        result = Plan.planDetails(request.headers, request.json)
        return result
    else:
        return jsonify(Error="Method not allowed"), 404


@app.route('/plan/search', methods=['GET'])
def planSearch():
    if request.method == 'GET':
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


@app.route('/plan/session/details', methods=['GET'])
def sessionDetails():
    if request.method == 'GET':
        if not Coach.checkToken(request.headers):
            return jsonify(Error="Invalid or Missing Security Token"), 404
        result = Plan.sessionDetails(request.headers, request.json)
        return result
    else:
        return jsonify(Error="Method not allowed"), 404


@app.route('/plan/session/search', methods=['GET'])
def sessionSearch():
    if request.method == 'GET':
        if not Coach.checkToken(request.headers):
            return jsonify(Error="Invalid or Missing Security Token"), 404
        result = Plan.sessionSearch(request.headers, request.json)
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


if __name__ == '__main__':
    app.run()

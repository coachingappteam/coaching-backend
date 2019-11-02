from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
from src.Handler import Coach, Plan, Sport

app = Flask(__name__, template_folder='./src/template')
CORS(app)


@app.route('/')
def mainPage():
    return render_template('mainpage.html')

# ==================== Coach Methods ====================== #
@app.route('/coach/login', methods=['POST'])
def coachLogin():
    if request.method == 'POST':
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


@app.route('/coach/details', methods=['GET'])
def coachDetails():
    if request.method == 'GET':
        result = Coach.readCoach(request.headers)
        return result
    else:
        return jsonify(Error="Method not allowed"), 404

@app.route('/coach/search', methods=['POST'])
def coachLogin():
    if request.method == 'POST':
        result = Coach.searchCoaches(request.json)
        return result
    else:
        return jsonify(Error="Method not allowed"), 404


@app.route('/coach/athlete/create', methods=['POST'])
def createAthlete():
    if request.method == 'POST':
        if not Coach.checkToken(request.headers):
            return jsonify(Error="Invalid or Missing Security Token"), 404
        result = Coach.createAthlete(request.headers, request.json)
        return result
    else:
        return jsonify(Error="Method not allowed"), 404


@app.route('/coach/team/create', methods=['POST'])
def createTeam():
    if request.method == 'POST':
        if not Coach.checkToken(request.headers):
            return jsonify(Error="Invalid or Missing Security Token"), 404
        result = Coach.createTeam(request.headers, request.json)
        return result
    else:
        return jsonify(Error="Method not allowed"), 404


@app.route('/coach/team/support/create', methods=['POST'])
def createTeamSupport():
    if request.method == 'POST':
        if not Coach.checkToken(request.headers):
            return jsonify(Error="Invalid or Missing Security Token"), 404
        result = Coach.addCoachToTeam(request.headers, request.json)
        return result
    else:
        return jsonify(Error="Method not allowed"), 404


@app.route('/coach/team/member/create', methods=['POST'])
def createTeamMember():
    if request.method == 'POST':
        if not Coach.checkToken(request.headers):
            return jsonify(Error="Invalid or Missing Security Token"), 404
        result = Coach.addAthleteToTeam(request.headers, request.json)
        return result
    else:
        return jsonify(Error="Method not allowed"), 404


@app.route('/sport/create', methods=['POST'])
def createSport():
    if request.method == 'POST':
        result = Sport.createSport(request.json)
        return result
    else:
        return jsonify(Error="Method not allowed"), 404


@app.route('/sport/role/create', methods=['POST'])
def createRole():
    if request.method == 'POST':
        result = Sport.createRole(request.json)
        return result
    else:
        return jsonify(Error="Method not allowed"), 404


@app.route('/test', methods=['GET'])
def testMethod():
    if request.method == 'GET':
        return jsonify(Success="Method allowed"), 200
    else:
        return jsonify(Error="Method not allowed"), 404


if __name__ == '__main__':
    app.run()

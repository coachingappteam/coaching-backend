from flask import Flask, jsonify, request
from flask_cors import CORS
from src.mainpage import mainpage
from src.Handler import Coach

app = Flask(__name__)

CORS(app)


@app.route('/')
def mainPage():
    return mainpage


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


@app.route('/coach/athlete/create', methods=['POST'])
def createAthlete():
    if request.method == 'POST':
        if not Coach.checkToken(request.headers):
            return jsonify(Error="Invalid or Missing Security Token"), 404
        result = Coach.createAthlete(request.json, request.headers)
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

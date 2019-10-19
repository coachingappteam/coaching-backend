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

    # request.headers.get('your-header-name')
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

@app.route('/coach/athlete/create', methods=['POST'])
def createAthlete():
    # request.headers.get('your-header-name')
    if request.method == 'POST':
        result = Coach.createAthlete(request.json, request.headers)
        return result
    else:
        return jsonify(Error="Method not allowed"), 404

if __name__ == '__main__':
    app.run()

import json
import eventlet
import requests

data = {"results": [{"id": 1,"role": 5,"competition_week": 0,"back": [1,100,33],"breast": [1,200,33],"butterfly": [],"drill": [],"free": [2,100,33],"im": [],"kick": [],"pull_paddle": []},{"id": 2,"role": 0,"competition_week": 0,"back": [1,300,25.6],"breast": [1,300,25.6],"butterfly": [1,300,25.6],"drill": [1,300,25.6],"free": [1,300,25.6],"im": [1,300,25.6],"kick": [1,300,25.6],"pull_paddle": []}]}

print(json.dumps(data))

with eventlet.Timeout(5):
    requests.post("https://coaching-predictions.azurewebsites.net/api/PredictionsHttpTrigger?code=FCLBiz6D9yMaNFYgURHuEeKJJ0VZo6fCfyfRMbdeSI6t0iUacWop1w==", data=json.dumps(data))
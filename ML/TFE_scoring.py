import pandas as pd
import tensorflow as tf
from tensorflow_core.estimator import inputs
from tensorflow import feature_column
from tensorflow.python.client import device_lib
import json
# tf.debugging.set_log_device_placement(True)




role = feature_column.numeric_column("Role")
competition_week = feature_column.numeric_column("CompetitionWeek")
back_reps = feature_column.numeric_column("BackReps")
back_distance = feature_column.numeric_column("BackDistance")
back_split = feature_column.numeric_column("BackAverageSplit")
breast_reps = feature_column.numeric_column("BreastReps")
breast_distance = feature_column.numeric_column("BreastDistance")
breast_split = feature_column.numeric_column("BreastAverageSplit")
butterfly_reps = feature_column.numeric_column("ButterflyReps")
butterfly_distance = feature_column.numeric_column("ButterflyDistance")
butterfly_split = feature_column.numeric_column("ButterflyAverageSplit")
drill_reps = feature_column.numeric_column("DrillReps")
drill_distance = feature_column.numeric_column("DrillDistance")
drill_split = feature_column.numeric_column("DrillAverageSplit")
free_reps = feature_column.numeric_column("FreeReps")
free_distance = feature_column.numeric_column("FreeDistance")
free_split = feature_column.numeric_column("FreeAverageSplit")
im_reps = feature_column.numeric_column("ImReps")
im_distance = feature_column.numeric_column("ImDistance")
im_split = feature_column.numeric_column("ImAverageSplit")
kick_reps = feature_column.numeric_column("KickReps")
kick_distance = feature_column.numeric_column("KickDistance")
kick_split = feature_column.numeric_column("KickAverageSplit")
pull_reps = feature_column.numeric_column("PullPaddleReps")
pull_distance = feature_column.numeric_column("PullPaddleDistance")
pull_split = feature_column.numeric_column("PullPaddleAverageSplit")
total_distance = feature_column.numeric_column("TotalDistance")

feature_columns = [role, competition_week, back_reps, back_distance,
                back_split, breast_reps, breast_distance, 
                breast_split, butterfly_reps, butterfly_distance,
                butterfly_split, drill_reps, drill_distance,
                drill_split, free_reps, free_distance,
                free_split, im_reps, im_distance, 
                im_split, kick_reps, kick_distance,
                kick_split, pull_reps, pull_distance,
                pull_split, total_distance
            ]

model = tf.estimator.LinearClassifier(feature_columns=feature_columns,model_dir="model", n_classes=2)

objects = [
    {
    "id": 1,
    "role": 5,
    "competition_week": 0,
    "back": [1, 100, 33],
    "breast": [1, 200, 33],
    "butterfly": [],
    "drill": [],
    "free": [2, 100, 33],
    "im": [],
    "kick": [],
    "pull_paddle": []
    },
    {
    "id": 2,
    "role": 0,
    "competition_week": 0,
    "back": [1, 300, 25.6],
    "breast": [1, 300, 25.6],
    "butterfly": [1, 300, 25.6],
    "drill": [1, 300, 25.6],
    "free": [1, 300, 25.6],
    "im": [1, 300, 25.6],
    "kick": [1, 300, 25.6],
    "pull_paddle": []
    },
    {
    "id": 3,
    "role": 0,
    "competition_week": 0,
    "back": [1, 300, 25.6],
    "breast": [1, 300, 25.6],
    "butterfly": [1, 300, 25.6],
    "drill": [1, 300, 25.6],
    "free": [1, 300, 25.6],
    "im": [1, 300, 25.6],
    "kick": [1, 300, 25.6],
    "pull_paddle": []
    },
    {
    "id": 5,
    "role": 0,
    "competition_week": 0,
    "back": [1, 100, 25.6],
    "breast": [],
    "butterfly": [1, 100, 25.6],
    "drill": [],
    "free": [3, 50, 25.6],
    "im": [2, 50, 25.6],
    "kick": [2, 50, 25.6],
    "pull_paddle": []
    },

]

styles = [
    "back",
    "breast",
    "butterfly",
    "drill",
    "free",
    "im",
    "kick",
    "pull_paddle"    
]

COLUMNS = ['id', 'Role', 'CompetitionWeek', 'BackReps', 'BackDistance',
       'BackAverageSplit', 'BreastReps', 'BreastDistance',
       'BreastAverageSplit', 'ButterflyReps', 'ButterflyDistance',
       'ButterflyAverageSplit', 'DrillReps', 'DrillDistance',
       'DrillAverageSplit', 'FreeReps', 'FreeDistance', 'FreeAverageSplit',
       'ImReps', 'ImDistance', 'ImAverageSplit', 'KickReps', 'KickDistance',
       'KickAverageSplit', 'PullPaddleReps', 'PullPaddleDistance',
       'PullPaddleAverageSplit', 'TotalDistance']

def json_to_df(json_objects):
    # json_objects = json.loads(json_objects)
    result = []
    for obj in json_objects:
        row = []
        row.append(obj["id"])
        row.append(obj["competition_week"])
        row.append(obj["role"])
        total_distance = 0
        for style in styles:
            if obj[style]:
                row.extend(obj[style])
                total_distance = total_distance + (obj[style][0] * obj[style][1])
            else:
                row.extend([0,0,0])
        row.append(total_distance)

        result.append(row)
    return pd.DataFrame(result, columns=COLUMNS)



def predict_input_fn(data):
    return tf.compat.v1.estimator.inputs.pandas_input_fn(
        x=data,
        num_epochs=1,
        shuffle=False
    )

def process(objects):
    df = json_to_df(objects)
    results = [ int(r["classes"][0]) for r in model.predict(input_fn=predict_input_fn(df.drop("id", axis=1)))]
    df["Label"] = results
    dic = {}
    for index, result in df.iterrows():
       dic[result["id"]] = result["Label"]
    return json.dumps(dic)

def lambda_handler(event, context):
    # TODO implement
    data = json.loads(event["body"])
    return {
        'statusCode': 200,
        'body': process(data)
    }








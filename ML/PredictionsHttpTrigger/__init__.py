import logging
import pandas as pd
import tensorflow as tf
from tensorflow_core.estimator import inputs
from tensorflow import feature_column
from tensorflow.python.client import device_lib
import json
import azure.functions as func
import azure

global model
model = None

def load_model(function_dir):
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
    
    return tf.estimator.LinearClassifier(feature_columns=feature_columns,model_dir=function_dir+"/model", n_classes=2)







def json_to_df(json_objects):
    styles = [
    "back",
    "breast",
    "butterfly",
    "drill",
    "free",
    "im",
    "kick",
    "pull_paddle"]

    COLUMNS = ['id', 'Role', 'CompetitionWeek', 'BackReps', 'BackDistance',
       'BackAverageSplit', 'BreastReps', 'BreastDistance',
       'BreastAverageSplit', 'ButterflyReps', 'ButterflyDistance',
       'ButterflyAverageSplit', 'DrillReps', 'DrillDistance',
       'DrillAverageSplit', 'FreeReps', 'FreeDistance', 'FreeAverageSplit',
       'ImReps', 'ImDistance', 'ImAverageSplit', 'KickReps', 'KickDistance',
       'KickAverageSplit', 'PullPaddleReps', 'PullPaddleDistance',
       'PullPaddleAverageSplit', 'TotalDistance']
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

def process(objects, model):
    df = json_to_df(objects)
    results = [ int(r["classes"][0]) for r in model.predict(input_fn=predict_input_fn(df.drop("id", axis=1)))]
    df["Label"] = results
    dic = {}
    for index, result in df.iterrows():
       dic[int(result["id"])] = int(result["Label"])
    return json.dumps(dic)

def main(req: func.HttpRequest, context: azure.functions.Context) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    global model
    if not model:
        model = load_model(context.function_directory)

    
    req_body = req.get_json()
    


    return func.HttpResponse(body=process(req_body["results"], model), status_code=200, mimetype='application/json')

    
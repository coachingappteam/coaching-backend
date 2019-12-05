#This file contains the data base configuration information
import json
import os


if os.environ.get("DATABASE_URL"):
    DATABASE_URL = os.environ.get("DATABASE_URL")
    AZURE_CODE = os.environ.get("AZURE_CODE")
    AZURE_URL = os.environ.get("AZURE_URL")
    LOCAL_DB = None
else:
    __location__ = os.path.realpath(
        os.path.join(os.getcwd(), os.path.dirname(__file__)))
    with open(os.path.join(__location__, "config.json")) as f:
        obj = json.load(f)
    DATABASE_URL = obj["DATABASE_URL"] if not obj["LOCAL"] else obj["LOCAL_DB"]
    AZURE_CODE = obj["AZURE_CODE"]
    AZURE_URL = obj["AZURE_URL"]
    LOCAL_DB = obj["LOCAL_DB"]

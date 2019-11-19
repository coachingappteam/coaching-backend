#This file contains the data base configuration information
import json
import os


if os.environ.get("DATABASE_URL"):
    DATABASE_URL = os.environ.get("DATABASE_URL")
    AZURE_CODE = os.environ.get("AZURE_CODE")
else:
    with open("config.json") as f:
        obj = json.load(f)
    DATABASE_URL = obj["DATABASE_URL"] if not obj["LOCAL"] else obj["LOCAL_DB"]
    AZURE_CODE = obj["AZURE_CODE"]




"""


pg_config = {
    'user':'coaching_admin',
    'passwd': 'admin',
    'dbname':'coaching_app',
    'host': '127.0.0.1',
    'port': 5432
}
"""
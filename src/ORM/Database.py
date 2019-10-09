import sys
from src.ORM.CoachingORM import Database

if len(sys.argv) is not 2:
    print('Databse uses one argument only!')

elif sys.argv[1] == 'create':
    db = Database()
    db.createTables()

elif sys.argv[1] == 'refresh':
    db = Database()
    db.refreshTables()

elif sys.argv[1] == 'drop':
    db = Database()
    db.dropTables()

else:
    print('Program only accepts: create, refresh or destroy')
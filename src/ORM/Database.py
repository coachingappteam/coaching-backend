import sys
from src.ORM.CoachingORM import Database
from src.ORM import DBDump


if len(sys.argv) is not 2:
    print('Databse uses one argument only!')

elif sys.argv[1] == 'create':
    db = Database()
    db.createTables()
    data = DBDump.Factory()
    data.pushDBDump()

elif sys.argv[1] == 'refresh':
    db = Database()
    db.refreshTables()
    data = DBDump.Factory()
    data.pushDBDump()


elif sys.argv[1] == 'drop':
    db = Database()
    db.dropTables()

else:
    print('Program only accepts: create, refresh or destroy')
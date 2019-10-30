from sqlalchemy.dialects.postgresql import UUID, DOUBLE_PRECISION
from sqlalchemy.ext.declarative import declarative_base
from uuid import uuid4
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, TIMESTAMP, Text, Boolean, ForeignKey, Date, \
    PrimaryKeyConstraint, Enum, create_engine
from datetime import datetime
from src.pg_config import pg_config

Base = declarative_base()


class Database:

    def __init__(self):
        self.__DATABASE_URI = 'postgres+psycopg2://%s:%s@%s:%s/%s' % \
                              (pg_config['user'], pg_config['passwd'], pg_config['host'],
                               pg_config['port'], pg_config['dbname'])
        self.db = create_engine(self.__DATABASE_URI)
        self.session = sessionmaker(bind=self.db)

    def createTables(self):
        Base.metadata.create_all(self.db)

    def dropTables(self):
        Base.metadata.drop_all(self.db)

    def refreshTables(self):
        self.dropTables()
        self.createTables()

    def getNewSession(self):
        return self.session()


class Coach(Base):
    __tablename__ = 'coach'
    coachID = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    password = Column(String, nullable=False)
    firstName = Column(String, nullable=False)
    lastName = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    phone = Column(String)
    isActiveMember = Column(Boolean, nullable=False, default=False)
    isActiveUser = Column(Boolean, nullable=False, default=True)
    createDate = Column(TIMESTAMP, nullable=False, default=datetime.today())

    def __repr__(self):
        return "<coach(firstName='{}', lastName='{}', email={}, isActiveMember={})>" \
            .format(self.firstName, self.lastName, self.email, self.isActiveMember)

    def json(self):
        return {
            "coachID": self.coachID,
            "firstName": self.firstName,
            "lastName": self.lastName,
            "email": self.email,
            "phone": self.phone,
            "isActiveMember": self.isActiveMember,
            "isActiveUser": self.isActiveUser,
            "createDate": self.createDate
        }


class Security(Base):
    __tablename__ = 'security'
    securityID = Column(Integer, primary_key=True, autoincrement=True)
    coachID = Column(UUID, ForeignKey('coach.coachID'), nullable=False)
    token = Column(String, nullable=False, unique=True)
    createDate = Column(TIMESTAMP, nullable=False, default=datetime.today())
    lastAccess = Column(TIMESTAMP, nullable=False, default=datetime.today())

    def __repr__(self):
        return "<security(coachID='{}', createDate='{}', lastAccess={})>" \
            .format(self.coachID, self.createDate, self.lastAccess)

    def json(self):
        return {
            "securityID": self.securityID,
            "coachID": self.coachID,
            "token": self.token,
            "createDate": self.createDate,
            "lastAccess": self.lastAccess
        }


class Payment(Base):
    __tablename__ = 'payment'
    paymentID = Column(Integer, primary_key=True, autoincrement=True)
    coachID = Column(UUID, ForeignKey('coach.coachID'), nullable=False)
    payDate = Column(TIMESTAMP, nullable=False, default=datetime.today())
    payTotal = Column(DOUBLE_PRECISION, nullable=False)
    paymentSource = Column(Text, nullable=False)
    sourceReceiptID = Column(Text, nullable=False)
    membershipLength = Column(Integer, nullable=False)

    def __repr__(self):
        return "<payment(paymentSource='{}', sourceReceiptID='{}', payDate={}, payTotal={})>" \
            .format(self.paymentSource, self.sourceReceiptID, self.payDate, self.payTotal)


class Sport(Base):
    __tablename__ = 'sport'
    sportID = Column(Integer, primary_key=True)
    sportName = Column(String, nullable=False)
    type = Column(Enum('Individual', 'Team', 'Mixed', name='Type'), nullable=False)

    def __repr__(self):
        return "<sport(sportName='{}', type='{}')>" \
            .format(self.sportName, self.type)


class Team(Base):
    __tablename__ = 'team'
    teamID = Column(Integer, primary_key=True, autoincrement=True)
    coachID = Column(UUID, ForeignKey('coach.coachID'), nullable=False)
    sportID = Column(Integer, ForeignKey('sport.sportID'), nullable=False)
    teamName = Column(String, nullable=False)
    isDeleted = Column(Boolean, nullable=False, default=False)
    creationDate = Column(TIMESTAMP, nullable=False, default=datetime.today())
    teamDescription = Column(Text)

    def __repr__(self):
        return "<team(teamName='{}', creationDate='{}', teamDescription={}, teamDescription={})>" \
            .format(self.teamName, self.creationDate, self.teamDescription, self.teamDescription)


class Support(Base):
    __tablename__ = 'support'
    coachID = Column(UUID,  ForeignKey('coach.coachID'), nullable=False)
    teamID = Column(Integer, ForeignKey('team.teamID'), nullable=False)
    creationDate = Column(TIMESTAMP, nullable=False, default=datetime.today())
    __table_args__ = (PrimaryKeyConstraint('coachID', 'teamID'), {},)

    def __repr__(self):
        return "<athlete(athleteID='{}', sessionID='{}')>" \
            .format(self.coachID, self.teamID)


class Athlete(Base):
    __tablename__ = 'athlete'
    athleteID = Column(Integer, primary_key=True, autoincrement=True)
    coachID = Column(UUID, ForeignKey('coach.coachID'), nullable=False)
    firstName = Column(String, nullable=False)
    lastName = Column(String, nullable=False)
    email = Column(String, nullable=False)
    phone = Column(String)
    sex = Column(Enum('M', 'F', 'X', name='Sex'), nullable=False)
    birthdate = Column(Date, nullable=False)
    isDeleted = Column(Boolean, nullable=False, default=False)
    creationDate = Column(TIMESTAMP, nullable=False, default=datetime.today())

    def __repr__(self):
        return "<athlete(firstName='{}', lastName='{}', email={}, birthdate={})>" \
            .format(self.firstName, self.lastName, self.email, self.birthdate)


class Member(Base):
    __tablename__ = 'member'
    athleteID = Column(Integer, ForeignKey('athlete.athleteID'), nullable=False)
    teamID = Column(Integer, ForeignKey('team.teamID'), nullable=False)
    isActive = Column(Boolean, nullable=False, default=True)
    __table_args__ = (PrimaryKeyConstraint('athleteID', 'teamID'), {},)

    def __repr__(self):
        return "<athlete(athleteID='{}', teamID='{}', isActive={})>" \
            .format(self.athleteID, self.teamID, self.isActive)


class Role(Base):
    __tablename__ = 'role'
    roleID = Column(Integer, primary_key=True, autoincrement=True)
    sportID = Column(Integer, ForeignKey('sport.sportID'), nullable=False)
    roleName = Column(String, nullable=False)
    roleDescription = Column(Text)
    creatorID = Column(UUID, ForeignKey('coach.coachID'), nullable=True, default=None)
    isDeleted = Column(Boolean, nullable=False, default=False)
    creationDate = Column(TIMESTAMP, nullable=False, default=datetime.today())

    def __repr__(self):
        return "<athlete(roleName='{}', roleDescription='{}')>" \
            .format(self.roleName, self.roleDescription)


class Focus(Base):
    __tablename__ = 'focus'
    athleteID = Column(Integer,  ForeignKey('athlete.athleteID'), nullable=False)
    roleID = Column(Integer, ForeignKey('role.roleID'), nullable=False)
    isPrimaryFocus = Column(Boolean, nullable=False, default=False)
    isDeleted = Column(Boolean, nullable=False, default=False)
    __table_args__ = (PrimaryKeyConstraint('athleteID', 'roleID'), {},)

    def __repr__(self):
        return "<athlete(athleteID='{}', roleID='{}', isPrimaryFocus='{}')>" \
            .format(self.athleteID, self.roleID, self.isPrimaryFocus)


class TrainingPlan(Base):
    __tablename__ = 'trainingPlan'
    planID = Column(Integer, primary_key=True, autoincrement=True)
    teamID = Column(Integer, ForeignKey('team.teamID'), nullable=False)
    parentPlanID = Column(Integer, ForeignKey('trainingPlan.planID'), nullable=True)
    title = Column(String, nullable=False)
    isParentPlan = Column(Boolean, nullable=False, default=False)
    isDeleted = Column(Boolean, nullable=False, default=False)
    startDate = Column(Date, nullable=False)
    endDate = Column(Date, nullable=False)
    planDescription = Column(Text)
    creationDate = Column(TIMESTAMP, nullable=False, default=datetime.today())

    def __repr__(self):
        return "<athlete(title='{}', planDescription='{}', startDate={}, endDate={})>" \
            .format(self.title, self.planDescription, self.startDate, self.endDate)


class Unit(Base):
    __tablename__ = 'unit'
    unitID = Column(Integer, primary_key=True, autoincrement=True)
    unitName = Column(String, nullable=False)
    unit = Column(String, nullable=False)

    def __repr__(self):
        return "<athlete(unitName='{}', unit='{}')>" \
            .format(self.unitName, self.unit)


class Exercise(Base):
    __tablename__ = 'exercise'
    exerciseID = Column(Integer, primary_key=True, autoincrement=True)
    unitID = Column(Integer, ForeignKey('unit.unitID'), nullable=False)
    exerciseName = Column(String, nullable=False)
    exerciseDescription = Column(Text)
    style = Column(String, nullable=False)
    measure = Column(DOUBLE_PRECISION, nullable=False)
    creatorID = Column(UUID, ForeignKey('coach.coachID'), nullable=True, default=None)
    isDeleted = Column(Boolean, nullable=False, default=False)
    creationDate = Column(TIMESTAMP, nullable=False, default=datetime.today())

    def __repr__(self):
        return "<athlete(exerciseName='{}', exerciseDescription='{}')>" \
            .format(self.exerciseName, self.exerciseDescription)


class Improves(Base):
    __tablename__ = 'improves'
    exerciseID = Column(Integer,  ForeignKey('exercise.exerciseID'), nullable=False)
    roleID = Column(Integer, ForeignKey('role.roleID'), nullable=False)
    __table_args__ = (PrimaryKeyConstraint('exerciseID', 'roleID'), {},)

    def __repr__(self):
        return "<athlete(exerciseID='{}', roleID='{}')>" \
            .format(self.exerciseID, self.roleID)


class Session(Base):
    __tablename__ = 'session'
    sessionID = Column(Integer, primary_key=True, autoincrement=True)
    planID = Column(Integer, ForeignKey('trainingPlan.planID'), nullable=False)
    sessionTitle = Column(String, nullable=False)
    location = Column(Text)
    isCompetition = Column(Boolean, default=False)
    isCompleted = Column(Boolean, nullable=False, default=False)
    isDeleted = Column(Boolean, nullable=False, default=False)
    sessionDate = Column(Date, nullable=False)
    sessionDescription = Column(Text)
    creationDate = Column(TIMESTAMP, nullable=False, default=datetime.today())

    def __repr__(self):
        return "<athlete(sessionTitle='{}', sessionDescription='{}', startDsessionDateate={}, location={})>" \
            .format(self.sessionTitle, self.sessionDescription, self.sessionDate, self.location)


class Attendance(Base):
    __tablename__ = 'attendance'
    sessionID = Column(Integer,  ForeignKey('session.sessionID'), nullable=False)
    athleteID = Column(Integer, ForeignKey('athlete.athleteID'), nullable=False)
    creationDate = Column(TIMESTAMP, nullable=False, default=datetime.today())
    __table_args__ = (PrimaryKeyConstraint('sessionID', 'athleteID'), {},)

    def __repr__(self):
        return "<athlete(athleteID='{}', sessionID='{}')>" \
            .format(self.athleteID, self.sessionID)


class Practice(Base):
    __tablename__ = 'practice'
    practiceID = Column(Integer, primary_key=True, autoincrement=True)
    exerciseID = Column(Integer,  ForeignKey('exercise.exerciseID'), nullable=False)
    sessionID = Column(Integer, ForeignKey('session.sessionID'), nullable=False)
    repetitions = Column(Integer, nullable=False)

    def __repr__(self):
        return "<athlete(practiceID='{}', sessionID='{}')>" \
            .format(self.practiceID, self.sessionID)


class Result(Base):
    __tablename__ = 'result'
    resultID = Column(Integer, primary_key=True, autoincrement=True)
    practiceID = Column(Integer, ForeignKey('practice.practiceID'), nullable=False)
    athleteID = Column(Integer, ForeignKey('athlete.athleteID'), nullable=False)
    unitID = Column(Integer, ForeignKey('unit.unitID'), nullable=False)
    resultDate = Column(Date, nullable=False, default=datetime.today())
    resultDescription = Column(Text)
    creationDate = Column(TIMESTAMP, nullable=False, default=datetime.today())

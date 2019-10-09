from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, TIMESTAMP, Text, Boolean, ForeignKey, Date
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class Database:

    def __init__(self, user, password, host, port, db):
        self.__DATABASE_URI = 'postgres+psycopg2://' + str(user) + ':' + str(password) + '@' + str(host) + \
                            ':' + str(port) + '/' + str(db)
        self.db = create_engine(self.__DATABASE_URI)
        self.session = None

    def createTables(self):
        Base.metadata.create_all(self.db)

    def dropTables(self):
        Base.metadata.drop_all(self.db)

    def refreshTables(self):
        self.dropTables()
        self.createTables()

    def openSession(self):
        if self.session is None:
            self.session = sessionmaker(bind=self.db)
        return self.session()

    def closeSession(self):
        if self.session is not None:
            self.session().close()


class Coach(Base):
    __tablename__ = 'coach'
    coachID = Column(UUID, primary_key=True)
    password = Column(Text, nullable=False)
    firstName = Column(String, nullable=False)
    lastName = Column(String, nullable=False)
    email = Column(String, nullable=False)
    phone = Column(String)
    isActiveMember = Column(Boolean, nullable=False, default=False)
    isActiveUser = Column(Boolean, nullable=False, default=True)
    prefersImperial = Column(Boolean, nullable=False)
    createDate = Column(TIMESTAMP, nullable=False)

    def __repr__(self):
        return "<coach(firstName='{}', lastName='{}', email={}, isActiveMember={})>" \
            .format(self.firstName, self.lastName, self.email, self.isActiveMember)


class Security(Base):
    __tablename__ = 'security'
    securityID = Column(Integer, primary_key=True)
    coachID = Column(UUID, ForeignKey('coach.coachID'), nullable=False)
    token = Column(String, nullable=False)
    createDate = Column(TIMESTAMP, nullable=False, default=datetime.today())
    lastAccess = Column(TIMESTAMP, nullable=False, default=datetime.today())
    isActive = Column(Boolean, nullable=False, default=True)

    def __repr__(self):
        return "<security(coachID='{}', createDate='{}', lastAccess={}, isActive={})>" \
            .format(self.coachID, self.createDate, self.lastAccess, self.isActive)


class Payment(Base):
    __tablename__ = 'payment'
    securityID = Column(Integer, primary_key=True)
    coachID = Column(UUID, ForeignKey('coach.coachID'), nullable=False)
    token = Column(String, nullable=False)
    createDate = Column(TIMESTAMP, nullable=False, default=datetime.today())
    lastAccess = Column(TIMESTAMP, nullable=False, default=datetime.today())
    isActive = Column(Boolean, nullable=False, default=True)

    def __repr__(self):
        return "<security(coachID='{}', createDate='{}', lastAccess={}, isActive={})>" \
            .format(self.coachID, self.createDate, self.lastAccess, self.isActive)
#
# CREATE TABLE payment (
#     paymentID uuid,
#     coachID uuid NOT NULL,
#     payDate TIMESTAMP,
#     payTotal DOUBLE PRECISION,
#     paymentSource text,
#     sourceReceiptID VARCHAR(100),
#     PRIMARY KEY (paymentID),
#     FOREIGN KEY (coachID) REFERENCES coach(coachID)
# );
#
# CREATE TABLE sport (
#     sportID BIGSERIAL,
#     sportName VARCHAR(30) NOT NULL,
#     type SportType NOT NULL,
#     PRIMARY KEY (sportID)
# );
#
# CREATE TABLE team (
#     teamID BIGSERIAL,
#     coachID uuid NOT NULL,
#     sportID BIGINT NOT NULL,
#     teamName varchar(20) NOT NULL,
#     isDeleted BOOLEAN,
#     creationDate TIMESTAMP NOT NULL ,
#     description TEXT,
#     PRIMARY KEY (teamID),
#     FOREIGN KEY (coachID) REFERENCES coach(coachID),
#     FOREIGN KEY (sportID) REFERENCES sport(sportID)
# );
#
# CREATE TABLE athlete (
#     athleteID bigserial,
#     coachID uuid NOT NULL,
#     firstName varchar(20) NOT NULL ,
#     lastName varchar(20) NOT NULL ,
#     phone varchar(11),
#     email varchar(50) NOT NULL ,
#     weight DOUBLE PRECISION NOT NULL ,
#     height DOUBLE PRECISION NOT NULL ,
#     birthDate DATE NOT NULL ,
#     sex Sex NOT NULL,
#     creationDate TIMESTAMP NOT NULL ,
#     PRIMARY KEY (athleteID),
#     FOREIGN KEY (coachID) REFERENCES coach(coachID)
# );
#
# CREATE TABLE member (
#     athleteID BIGINT NOT NULL ,
#     teamID BIGINT NOT NULL ,
#     isActivePlayer BOOLEAN,
#     PRIMARY KEY (athleteID, teamID),
#     FOREIGN KEY (athleteID) REFERENCES athlete(athleteID),
#     FOREIGN KEY (teamID) REFERENCES team(teamID)
#  );
#
# CREATE TABLE role (
#     roleID BIGSERIAL,
#     sportID BIGINT NOT NULL ,
#     roleName varchar(30) NOT NULL ,
#     roleDescription varchar(300),
#     PRIMARY KEY (roleID),
#     FOREIGN KEY (sportID) REFERENCES sport(sportID)
# );
#
# CREATE TABLE focus(
#     athleteID BIGINT,
#     roleID BIGINT,
#     isPrimaryFocus BOOLEAN,
#     PRIMARY KEY (athleteID, roleID),
#     FOREIGN KEY (athleteID) REFERENCES athlete(athleteID),
#     FOREIGN KEY (roleID) REFERENCES role(roleID)
# );
#
# CREATE TABLE trainingPlan(
#     planID BIGSERIAL,
#     teamID BIGINT NOT NULL,
#     parentPlanID BIGINT,
#     title varchar(20) NOT NULL,
#     isParentPlan BOOLEAN,
#     isDeleted BOOLEAN,
#     startDate DATE NOT NULL,
#     endDate DATE NOT NULL,
#     description text,
#     PRIMARY KEY (planID),
#     FOREIGN KEY (teamID) REFERENCES team(teamID),
#     FOREIGN KEY (parentPlanID) REFERENCES trainingPlan(planID)
# );
#
# CREATE TABLE exercise(
#     exerciseID BIGSERIAL,
#     exerciseName varchar(20) NOT NULL,
#     exerciseDescription text,
#     PRIMARY KEY (exerciseID)
# );
#
# CREATE TABLE improves(
#     exerciseID BIGINT NOT NULL,
#     roleID BIGINT NOT NULL,
#     PRIMARY KEY (exerciseID, roleID),
#     FOREIGN KEY (exerciseID) REFERENCES exercise(exerciseID),
#     FOREIGN KEY (roleID) REFERENCES role(roleID)
# );
#
# CREATE TABLE session(
#     sessionID BIGSERIAL,
#     planID BIGINT NOT NULL,
#     parentSessionID BIGINT,
#     sessionTitle varchar(20) NOT NULL,
#     sessionDescription text,
#     sessionDate DATE NOT NULL,
#     location text,
#     isCompetition boolean,
#     isCompleted boolean,
#     PRIMARY KEY (sessionID),
#     FOREIGN KEY (planID) REFERENCES trainingPlan(planID),
#     FOREIGN KEY (parentSessionID) REFERENCES session(sessionID)
# );
#
# CREATE TABLE attendance(
#     sessionID BIGINT NOT NULL,
#     athleteID BIGINT NOT NULL,
#     PRIMARY KEY (sessionID, athleteID),
#     FOREIGN KEY (sessionID) REFERENCES session(sessionID),
#     FOREIGN KEY (athleteID) REFERENCES athlete(athleteID)
# );
#
# CREATE TABLE practice(
#   practiceID BIGSERIAL,
#   exerciseID BIGINT,
#   sessionID BIGINT,
#   PRIMARY KEY(practiceID),
#   FOREIGN KEY (exerciseID) REFERENCES exercise(exerciseID),
#   FOREIGN KEY (sessionID) REFERENCES session(sessionID)
# );
#
# CREATE TABLE unit (
#     unitID BIGSERIAL,
#     unitName VARCHAR(30) NOT NULL,
#     units VARCHAR(10) NOT NULL,
#     PRIMARY KEY (unitID)
# );
#
# CREATE TABLE conversion (
#     conversionID BIGSERIAL,
#     fromUnit BIGINT NOT NULL,
#     toUnit BIGINT NOT NULL,
#     conversion text,
#     PRIMARY KEY (conversionID),
#     FOREIGN KEY (fromUnit) REFERENCES unit(unitID),
#     FOREIGN KEY (toUnit) REFERENCES unit(unitID)
# );
#
# CREATE TABLE result (
#     resultID BIGSERIAL,
#     practiceID BIGINT NOT NULL,
#     athleteID BIGINT NOT NULL,
#     unitID BIGINT NOT NULL,
#     resultDate TIMESTAMP NOT NULL,
#     resultDescription text,
#     PRIMARY KEY (resultID),
#     FOREIGN KEY (practiceID) REFERENCES practice(practiceID),
#     FOREIGN KEY (athleteID) REFERENCES athlete(athleteID),
#     FOREIGN KEY (unitID) REFERENCES unit(unitID)
# );
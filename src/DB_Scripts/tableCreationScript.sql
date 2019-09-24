DROP TABLE IF EXISTS result;
DROP TABLE IF EXISTS conversion;
DROP TABLE IF EXISTS unit;
DROP TABLE IF EXISTS practice;
DROP TABLE IF EXISTS attendance;
DROP TABLE IF EXISTS session;
DROP TABLE IF EXISTS improves;
DROP TABLE IF EXISTS exercise;
DROP TABLE IF EXISTS trainingPlan;
DROP TABLE IF EXISTS focus;
DROP TABLE IF EXISTS role;
DROP TABLE IF EXISTS member;
DROP TABLE IF EXISTS athlete;
DROP TABLE IF EXISTS team;
DROP TABLE IF EXISTS sport;
DROP TABLE IF EXISTS payment;
DROP TABLE IF EXISTS security;
DROP TABLE IF EXISTS coach;

DROP TYPE IF EXISTS SportType;
DROP TYPE IF EXISTS PaySource;


CREATE TYPE SportType AS ENUM ('individual', 'team', 'hybrid');
CREATE TYPE PaySource AS ENUM ('paypal', 'amazon_pay', 'google_pay', 'apple_pay');

CREATE TABLE coach (
    coachID uuid,
    firstName VARCHAR(20) NOT NULL,
    lastName VARCHAR(20) NOT NULL,
    email VARCHAR(50) NOT NULL,
    phone VARCHAR(11),
    isActiveMember BOOLEAN,
    isActiveUser BOOLEAN,
    prefersImperial BOOLEAN,
    createDate TIMESTAMP,
    PRIMARY KEY (coachID)
);

CREATE TABLE security (
    securityID BIGSERIAL,
    coachID uuid NOT NULL,
    token varchar(50) NOT NULL,
    creationDate TIMESTAMP,
    lastAccess TIMESTAMP,
    isActive BOOLEAN,
    PRIMARY KEY (securityID),
    FOREIGN KEY (coachID) REFERENCES coach(coachID)
);

CREATE TABLE payment (
    paymentID uuid,
    coachID uuid NOT NULL,
    payDate TIMESTAMP,
    payTotal DOUBLE PRECISION,
    paymentSource PaySource,
    sourceReceiptID VARCHAR(100),
    PRIMARY KEY (paymentID),
    FOREIGN KEY (coachID) REFERENCES coach(coachID)
);

CREATE TABLE sport (
    sportID BIGSERIAL,
    sportName VARCHAR(30) NOT NULL,
    type SportType NOT NULL,
    PRIMARY KEY (sportID)
);

CREATE TABLE team (
    teamID BIGSERIAL,
    coachID uuid NOT NULL,
    sportID BIGINT NOT NULL,
    teamName varchar(20) NOT NULL,
    isDeleted BOOLEAN,
    creationDate TIMESTAMP NOT NULL ,
    description TEXT,
    PRIMARY KEY (teamID),
    FOREIGN KEY (coachID) REFERENCES coach(coachID),
    FOREIGN KEY (sportID) REFERENCES sport(sportID)
);

CREATE TABLE athlete (
    athleteID bigserial,
    coachID uuid NOT NULL,
    firstName varchar(20) NOT NULL ,
    lastName varchar(20) NOT NULL ,
    phone varchar(11),
    email varchar(50) NOT NULL ,
    weight DOUBLE PRECISION NOT NULL ,
    height DOUBLE PRECISION NOT NULL ,
    birthDate DATE NOT NULL ,
    creationDate TIMESTAMP NOT NULL ,
    PRIMARY KEY (athleteID),
    FOREIGN KEY (coachID) REFERENCES coach(coachID)
);

CREATE TABLE member (
    athleteID BIGINT NOT NULL ,
    teamID BIGINT NOT NULL ,
    isActivePlayer BOOLEAN,
    PRIMARY KEY (athleteID, teamID),
    FOREIGN KEY (athleteID) REFERENCES athlete(athleteID),
    FOREIGN KEY (teamID) REFERENCES team(teamID)
 );

CREATE TABLE role (
    roleID BIGSERIAL,
    sportID BIGINT NOT NULL ,
    roleName varchar(30) NOT NULL ,
    roleDescription varchar(300),
    PRIMARY KEY (roleID),
    FOREIGN KEY (sportID) REFERENCES sport(sportID)
);

CREATE TABLE focus(
    athleteID BIGINT,
    roleID BIGINT,
    isPrimaryFocus BOOLEAN,
    PRIMARY KEY (athleteID, roleID),
    FOREIGN KEY (athleteID) REFERENCES athlete(athleteID),
    FOREIGN KEY (roleID) REFERENCES role(roleID)
);

CREATE TABLE trainingPlan(
    planID BIGSERIAL,
    teamID BIGINT NOT NULL,
    parentPlanID BIGINT,
    title varchar(20) NOT NULL,
    isParentPlan BOOLEAN,
    isDeleted BOOLEAN,
    startDate DATE NOT NULL,
    endDate DATE NOT NULL,
    description text,
    PRIMARY KEY (planID),
    FOREIGN KEY (teamID) REFERENCES team(teamID),
    FOREIGN KEY (parentPlanID) REFERENCES trainingPlan(planID)
);

CREATE TABLE exercise(
    exerciseID BIGSERIAL,
    exerciseName varchar(20) NOT NULL,
    exerciseDescription text,
    PRIMARY KEY (exerciseID)
);

CREATE TABLE improves(
    exerciseID BIGINT NOT NULL,
    roleID BIGINT NOT NULL,
    PRIMARY KEY (exerciseID, roleID),
    FOREIGN KEY (exerciseID) REFERENCES exercise(exerciseID),
    FOREIGN KEY (roleID) REFERENCES role(roleID)
);

CREATE TABLE session(
    sessionID BIGSERIAL,
    planID BIGINT NOT NULL,
    parentSessionID BIGINT,
    sessionDescription text,
    sessionDate DATE NOT NULL,
    location text,
    isCompetition boolean,
    isCompleted boolean,
    PRIMARY KEY (sessionID),
    FOREIGN KEY (planID) REFERENCES trainingPlan(planID),
    FOREIGN KEY (parentSessionID) REFERENCES session(sessionID)
);

CREATE TABLE attendance(
    sessionID BIGINT NOT NULL,
    athleteID BIGINT NOT NULL,
    PRIMARY KEY (sessionID, athleteID),
    FOREIGN KEY (sessionID) REFERENCES session(sessionID),
    FOREIGN KEY (athleteID) REFERENCES athlete(athleteID)
);

CREATE TABLE practice(
  practiceID BIGSERIAL,
  exerciseID BIGINT,
  sessionID BIGINT,
  PRIMARY KEY(practiceID),
  FOREIGN KEY (exerciseID) REFERENCES exercise(exerciseID),
  FOREIGN KEY (sessionID) REFERENCES session(sessionID)
);

CREATE TABLE unit (
    unitID BIGSERIAL,
    unitName VARCHAR(30) NOT NULL,
    units VARCHAR(10) NOT NULL,
    PRIMARY KEY (unitID)
);

CREATE TABLE conversion (
    conversionID BIGSERIAL,
    fromUnit BIGINT NOT NULL,
    toUnit BIGINT NOT NULL,
    conversion text,
    PRIMARY KEY (conversionID),
    FOREIGN KEY (fromUnit) REFERENCES unit(unitID),
    FOREIGN KEY (toUnit) REFERENCES unit(unitID)
);

CREATE TABLE result (
    resultID BIGSERIAL,
    practiceID BIGINT NOT NULL,
    athleteID BIGINT NOT NULL,
    unitID BIGINT NOT NULL,
    resultDate TIMESTAMP NOT NULL,
    resultDescription text,
    PRIMARY KEY (resultID),
    FOREIGN KEY (practiceID) REFERENCES practice(practiceID),
    FOREIGN KEY (athleteID) REFERENCES athlete(athleteID),
    FOREIGN KEY (unitID) REFERENCES unit(unitID)
);
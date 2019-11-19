import datetime
import random

from src.DAO import CoachDAO, SportDAO, PlanDAO


class Factory:

    def __init__(self):

        self.admin = {"password": "coachingpr",
                      "firstName": "Coaching",
                      "lastName": "App",
                      "email": "coachingappteam@gmail.com",
                      "phone": "7873619803"
                      }

        self.user = {"password": "testing",
                     "firstName": "Test",
                     "lastName": "Testington",
                     "email": "testing@gmail.com",
                     "phone": "7871633089"
                     }

        self.sports = [{"sportName": "Swimming",
                        "type": "Mixed"
                        }, {"sportName": "Tennis",
                            "type": "Individual"
                            }, {"sportName": "Soccer",
                                "type": "Team"
                                }
                       ]
        self.units = [{"unitName": "Distance",
                       "unit": "m"
                       }, {"unitName": "Time",
                           "unit": "s"
                           }, {"unitName": "Mass",
                               "unit": "kg"
                               }, {"unitName": "Weight",
                                   "unit": "lb"
                                   }, {"unitName": "Time",
                                       "unit": "min"
                                       }
                      ]
        self.roles = [{"sportID": "1",
                       "roleName": "50 Free",
                       "roleDescription": "50 Free Event."
                       }, {"sportID": "1",
                           "roleName": "100 Free",
                           "roleDescription": "100 Free Event."
                           }, {"sportID": "1",
                               "roleName": "200 Free",
                               "roleDescription": "200 Free Event."
                               }, {"sportID": "1",
                                   "roleName": "400 Free",
                                   "roleDescription": "400 Free Event."
                                   }, {"sportID": "1",
                                       "roleName": "800 Free",
                                       "roleDescription": "800 Free Event."
                                       }, {"sportID": "1",
                                           "roleName": "1500 Free",
                                           "roleDescription": "1500 Free Event."
                                           }, {"sportID": "1",
                                               "roleName": "50 Backstroke",
                                               "roleDescription": "50 Backstroke Event."
                                               }, {"sportID": "1",
                                                   "roleName": "100 Backstroke",
                                                   "roleDescription": "100 Backstroke Event."
                                                   }, {"sportID": "1",
                                                       "roleName": "200 Backstroke",
                                                       "roleDescription": "200 Backstroke Event."
                                                       }, {"sportID": "1",
                                                           "roleName": "50 Breaststroke",
                                                           "roleDescription": "50 Breaststroke Event."
                                                           }, {"sportID": "1",
                                                               "roleName": "100 Breaststroke",
                                                               "roleDescription": "100 Breaststroke Event."
                                                               }, {"sportID": "1",
                                                                   "roleName": "200 Breaststroke",
                                                                   "roleDescription": "200 Breaststroke Event."
                                                                   }, {"sportID": "1",
                                                                       "roleName": "50 Butterfly",
                                                                       "roleDescription": "50 Butterfly Event."
                                                                       }, {"sportID": "1",
                                                                           "roleName": "100 Butterfly",
                                                                           "roleDescription": "100 Butterfly Event."
                                                                           }, {"sportID": "1",
                                                                               "roleName": "200 Butterfly",
                                                                               "roleDescription": "200 Butterfly Event."
                                                                               }, {"sportID": "1",
                                                                                   "roleName": "200 IM",
                                                                                   "roleDescription": "200 IM Event."
                                                                                   }, {"sportID": "1",
                                                                                       "roleName": "400 IM",
                                                                                       "roleDescription": "400 IM Event."
                                                                                       }
                      ]
        self.exercises = [{"exerciseName": "Free",
                           "exerciseDescription": "Free Event.",
                           "style": "free",
                           }, {"exerciseName": "Backstroke",
                               "exerciseDescription": "Backstroke Event.",
                               "style": "back",
                               }, {"exerciseName": "Breaststroke",
                                   "exerciseDescription": "Breaststroke Event.",
                                   "style": "breast",
                                   }, {"exerciseName": "Butterfly",
                                       "exerciseDescription": "Butterfly Event.",
                                       "style": "butterfly",
                                       }, {"exerciseName": "IM",
                                           "exerciseDescription": "IM Event.",
                                           "style": "im",
                                           }, {"exerciseName": "Drill",
                                               "exerciseDescription": "Drill Event.",
                                               "style": "drill",
                                               }, {"exerciseName": "Kick",
                                                   "exerciseDescription": "Kick Event.",
                                                   "style": "kick",
                                                   }, {"exerciseName": "Pull and Paddle",
                                                       "exerciseDescription": "Pull and Paddle Event.",
                                                       "style": "pull_paddle",
                                                       }, {"exerciseName": "Running",
                                                           "exerciseDescription": "Running Event.",
                                                           "style": "run",
                                                           }, {"exerciseName": "Stretching",
                                                               "exerciseDescription": "Stretching Event.",
                                                               "style": "stretch",
                                                               }
                          ]

        self.improves = [{"exerciseID": 1,
                          "roleID": 1
                          }, {"exerciseID": 1,
                              "roleID": 2
                              }, {"exerciseID": 1,
                                  "roleID": 3
                                  }, {"exerciseID": 1,
                                      "roleID": 4
                                      }, {"exerciseID": 1,
                                          "roleID": 5
                                          }, {"exerciseID": 1,
                                              "roleID": 6
                                              }, {"exerciseID": 2,
                                                  "roleID": 7
                                                  }, {"exerciseID": 2,
                                                      "roleID": 8
                                                      }, {"exerciseID": 2,
                                                          "roleID": 9
                                                          }, {"exerciseID": 3,
                                                              "roleID": 10
                                                              }, {"exerciseID": 3,
                                                                  "roleID": 11
                                                                  }, {"exerciseID": 3,
                                                                      "roleID": 12
                                                                      }, {"exerciseID": 4,
                                                                          "roleID": 13
                                                                          }, {"exerciseID": 4,
                                                                              "roleID": 14
                                                                              }, {"exerciseID": 4,
                                                                                  "roleID": 15
                                                                                  }, {"exerciseID": 5,
                                                                                      "roleID": 16
                                                                                      }, {"exerciseID": 5,
                                                                                          "roleID": 17
                                                                                          }
                         ]

        self.athletes = [{"coachID": None,
                          "firstName": "Miles",
                          "lastName": "Edgeworth",
                          "email": "miles.edgeworth@gmail.com",
                          "phone": "7879603193",
                          "sex": "M",
                          "birthdate": datetime.datetime(1992, 10, 11).date()
                          }, {"coachID": None,
                              "firstName": "Kay",
                              "lastName": "Faraday",
                              "email": "kayfay@gmail.com",
                              "phone": "8886738257",
                              "sex": "F",
                              "birthdate": datetime.datetime(1998, 5, 21).date()
                              }, {"coachID": None,
                                  "firstName": "Penny",
                                  "lastName": "Nichols",
                                  "email": "nichols@gmail.com",
                                  "phone": "",
                                  "sex": "X",
                                  "birthdate": datetime.datetime(2001, 1, 16).date()
                                  }
                         ]

        self.supportAthletes = [{"coachID": None,
                                 "firstName": "Phoenix",
                                 "lastName": "Wright",
                                 "email": "phoenix@gmail.com",
                                 "phone": "8877602593",
                                 "sex": "M",
                                 "birthdate": datetime.datetime(1994, 9, 5).date()
                                 }, {"coachID": None,
                                     "firstName": "Maya",
                                     "lastName": "Fey",
                                     "email": "Mayfey@gmail.com",
                                     "phone": "8536728267",
                                     "sex": "F",
                                     "birthdate": datetime.datetime(1999, 3, 24).date()
                                     }, {"coachID": None,
                                         "firstName": "Fraciska",
                                         "lastName": "VonKarma",
                                         "email": "vonkarma@gmail.com",
                                         "phone": "",
                                         "sex": "X",
                                         "birthdate": datetime.datetime(1997, 6, 29).date()
                                         }
                                ]
        self.teams = [{"coachID": None,
                       "sportID": 1,
                       "teamName": "UPRM Swimming 2019 Team",
                       "teamDescription": "The UPRM's 2019 swimming athletes."
                       }, {"coachID": None,
                           "sportID": 3,
                           "teamName": "UPRM Basketball 2019 Team",
                           "teamDescription": "The UPRM's 2019 basketball athletes."
                           }
                      ]

        self.supportTeams = [{"coachID": None,
                              "sportID": 1,
                              "teamName": "UPRM LAI 2019 Swim Team",
                              "teamDescription": "The UPRM's 2019 LAI swimming athletes."
                              }
                             ]
        self.plan = {"teamID": 1,
                     "parentPlanID": None,
                     "title": "LAI Swimming Competition",
                     "startDate": datetime.datetime(2019, 2, 1).date(),
                     "endDate": datetime.datetime(2019, 5, 21).date(),
                     "planDescription": "LAI Swimming Competition Training Plan."
                     }
        self.sessions = [{"planID": 1,
                          "parentSessionID": None,
                          "sessionTitle": "Practice #1",
                          "location": "Gym",
                          "isCompetition": False,
                          "isMain": False,
                          "sessionDate": datetime.datetime(2019, 2, 2).date(),
                          "sessionDescription": "Practice #1."
                          }, {"planID": 1,
                              "parentSessionID": None,
                              "sessionTitle": "Competition #2",
                              "location": "Gym",
                              "isCompetition": True,
                              "isMain": False,
                              "sessionDate": datetime.datetime(2019, 5, 21).date(),
                              "sessionDescription": "LAI Swimming Competition."
                              }, {"planID": 1,
                                  "parentSessionID": None,
                                  "sessionTitle": "Practice #2",
                                  "location": "Gym",
                                  "isCompetition": False,
                                  "isMain": False,
                                  "sessionDate": datetime.datetime(2019, 4, 5).date(),
                                  "sessionDescription": "Practice #2."
                                  }, {"planID": 1,
                                      "parentSessionID": None,
                                      "sessionTitle": "Practice #3",
                                      "location": "Gym",
                                      "isCompetition": False,
                                      "isMain": False,
                                      "sessionDate": datetime.datetime(2019, 4, 6).date(),
                                      "sessionDescription": "Practice #3."
                                      }, {"planID": 1,
                                          "parentSessionID": None,
                                          "sessionTitle": "Practice #4",
                                          "location": "Gym",
                                          "isCompetition": False,
                                          "isMain": False,
                                          "sessionDate": datetime.datetime(2019, 4, 7).date(),
                                          "sessionDescription": "Practice #4."
                                          }, {"planID": 1,
                                              "parentSessionID": None,
                                              "sessionTitle": "Practice #5",
                                              "location": "Gym",
                                              "isCompetition": False,
                                              "isMain": False,
                                              "sessionDate": datetime.datetime(2019, 5, 19).date(),
                                              "sessionDescription": "Practice #5."
                                              }, {"planID": 1,
                                                  "parentSessionID": None,
                                                  "sessionTitle": "Competition #1",
                                                  "location": "Gym",
                                                  "isCompetition": True,
                                                  "isMain": False,
                                                  "sessionDate": datetime.datetime(2019, 4, 4).date(),
                                                  "sessionDescription": "LAI Swimming Competition."
                                                  }
                         ]

        self.subSessions = [{"planID": 1,
                             "parentSessionID": None,
                             "sessionTitle": "WarmUp",
                             "location": "Gym",
                             "isCompetition": False,
                             "isMain": False,
                             "sessionDate": None,
                             "sessionDescription": ""
                             }, {"planID": 1,
                                 "parentSessionID": None,
                                 "sessionTitle": "Main Session",
                                 "location": "Gym",
                                 "isCompetition": False,
                                 "isMain": True,
                                 "sessionDate": None,
                                 "sessionDescription": ""
                                 }, {"planID": 1,
                                     "parentSessionID": None,
                                     "sessionTitle": "Cool Down",
                                     "location": "Gym",
                                     "isCompetition": False,
                                     "isMain": False,
                                     "sessionDate": None,
                                     "sessionDescription": ""
                                     }
                            ]

    def pushDBDump(self):
        coachDAO = CoachDAO.CoachDAO()
        sportDAO = SportDAO.SportDAO()
        planDAO = PlanDAO.PlanDAO()

        # Create Admin
        coachID = str(coachDAO.createAdmin(self.admin['password'], self.admin['firstName'], self.admin['lastName'],
                                           self.admin['phone'], self.admin['email']))

        # Create User
        supportID = str(coachDAO.createCoach(self.user['password'], self.user['firstName'], self.user['lastName'],
                                             self.user['phone'], self.user['email']))
        # Create Sports
        for sport in self.sports:
            sportDAO.createSport(sport['sportName'], sport['type'])

        # Create Units
        for unit in self.units:
            sportDAO.createUnit(unit['unitName'], unit['unit'])

        # Create Roles
        for role in self.roles:
            sportDAO.createRole(role['sportID'], role['roleName'], role['roleDescription'])

        # Create Exercises
        for exercise in self.exercises:
            sportDAO.createExercise(exercise['exerciseName'], exercise['exerciseDescription'], exercise['style'])

        # Create Improvements
        for improve in self.improves:
            sportDAO.createImproves(improve['exerciseID'], improve['roleID'])

        # Create Athletes
        for athlete in self.athletes:
            coachDAO.createAthlete(coachID, athlete['firstName'], athlete['lastName'],
                                   athlete['email'], athlete['phone'], athlete['sex'], athlete['birthdate'])

        for athlete in self.supportAthletes:
            coachDAO.createAthlete(supportID, athlete['firstName'], athlete['lastName'],
                                   athlete['email'], athlete['phone'], athlete['sex'], athlete['birthdate'])

        # Create Teams
        for team in self.teams:
            coachDAO.createTeam(coachID, team['sportID'], team['teamName'],
                                team['teamDescription'])

        for team in self.supportTeams:
            coachDAO.createTeam(supportID, team['sportID'], team['teamName'],
                                team['teamDescription'])

        # Create Support
        coachDAO.createSupport(coachID, 3)
        coachDAO.createSupport(supportID, 1)

        # Create Member
        coachDAO.createMember(1, 1)
        coachDAO.createMember(2, 1)
        coachDAO.createMember(3, 1)
        coachDAO.createMember(4, 1)
        coachDAO.createMember(4, 3)
        coachDAO.createMember(5, 3)
        coachDAO.createMember(6, 3)

        # Create Focus
        coachDAO.createFocus(1, 1, True)
        coachDAO.createFocus(1, 8, False)

        coachDAO.createFocus(2, 2, True)
        coachDAO.createFocus(2, 9, False)
        coachDAO.createFocus(2, 13, False)

        coachDAO.createFocus(3, 14, False)
        coachDAO.createFocus(3, 3, True)
        coachDAO.createFocus(3, 16, False)
        coachDAO.createFocus(3, 10, False)

        coachDAO.createFocus(4, 4, True)
        coachDAO.createFocus(4, 15, False)
        coachDAO.createFocus(4, 17, False)
        coachDAO.createFocus(4, 5, False)
        coachDAO.createFocus(4, 1, False)
        coachDAO.createFocus(4, 2, False)
        coachDAO.createFocus(4, 3, False)
        coachDAO.createFocus(4, 5, False)
        coachDAO.createFocus(4, 6, False)
        coachDAO.createFocus(4, 7, False)
        coachDAO.createFocus(4, 8, False)
        coachDAO.createFocus(4, 9, False)
        coachDAO.createFocus(4, 10, False)
        coachDAO.createFocus(4, 12, False)
        coachDAO.createFocus(4, 13, False)
        coachDAO.createFocus(4, 11, False)
        coachDAO.createFocus(4, 14, False)
        coachDAO.createFocus(4, 16, False)

        coachDAO.createFocus(5, 6, True)
        coachDAO.createFocus(5, 11, False)

        coachDAO.createFocus(6, 7, True)
        coachDAO.createFocus(6, 12, False)

        # Create Training Plan
        planDAO.createTrainingPlan(self.plan['teamID'], self.plan['parentPlanID'], self.plan['title'],
                                   self.plan['startDate'], self.plan['endDate'], self.plan['planDescription'])

        # Create Sessions
        for session in self.sessions:
            sessionID = planDAO.createSession(session['planID'], session['parentSessionID'], session['sessionTitle'],
                                              session['location'], session['isCompetition'], session['isMain'],
                                              session['sessionDate'], session['sessionDescription'])

            coachDAO.createAttendance(sessionID, 1)
            coachDAO.createAttendance(sessionID, 2)
            coachDAO.createAttendance(sessionID, 3)
            coachDAO.createAttendance(sessionID, 4)

            if not session['isCompetition']:
                warmupID = planDAO.createSession(self.subSessions[0]['planID'], sessionID,
                                                 self.subSessions[0]['sessionTitle'], self.subSessions[0]['location'],
                                                 session['isCompetition'], self.subSessions[0]['isMain'],
                                                 session['sessionDate'], self.subSessions[0]['sessionDescription'])

                planDAO.createPractice(9, warmupID, 1, 5, 30)

                coolDownID = planDAO.createSession(self.subSessions[2]['planID'], sessionID,
                                                   self.subSessions[2]['sessionTitle'], self.subSessions[2]['location'],
                                                   session['isCompetition'], self.subSessions[2]['isMain'],
                                                   session['sessionDate'], self.subSessions[2]['sessionDescription'])
                planDAO.createPractice(10, coolDownID, 1, 5, 5)

            mainID = planDAO.createSession(self.subSessions[1]['planID'], sessionID,
                                           self.subSessions[1]['sessionTitle'], self.subSessions[1]['location'],
                                           session['isCompetition'], self.subSessions[1]['isMain'],
                                           session['sessionDate'], self.subSessions[1]['sessionDescription'])

            if session['isCompetition']:
                exerciseList = set()
                while len(exerciseList) < 3:
                    exerciseList.add(random.randint(1, 5))

                idHolder = planDAO.createPractice(exerciseList.pop(), mainID, 1,
                                                  1, 100 * random.randint(1, 2))

                planDAO.createResult(idHolder, 1, 2, random.randrange(22, 28) + (0.01 * random.randrange(0, 100))
                                     , session["sessionDate"], "Great")
                planDAO.createResult(idHolder, 2, 2, random.randrange(22, 28) + (0.01 * random.randrange(0, 100))
                                     , session["sessionDate"], "Great")
                planDAO.createResult(idHolder, 4, 2, random.randrange(22, 28) + (0.01 * random.randrange(0, 100))
                                     , session["sessionDate"], "Great")

                idHolder = planDAO.createPractice(exerciseList.pop(), mainID, 1,
                                                  1, 100 * random.randint(1, 2))

                planDAO.createResult(idHolder, 2, 2, random.randrange(22, 28) + (0.01 * random.randrange(0, 100))
                                     , session["sessionDate"], "Great")
                planDAO.createResult(idHolder, 3, 2, random.randrange(22, 28) + (0.01 * random.randrange(0, 100))
                                     , session["sessionDate"], "Great")
                planDAO.createResult(idHolder, 4, 2, random.randrange(22, 28) + (0.01 * random.randrange(0, 100))
                                     , session["sessionDate"], "Great")

                idHolder = planDAO.createPractice(exerciseList.pop(), mainID, 1,
                                                  1, 100 * random.randint(1, 2))

                planDAO.createResult(idHolder, 3, 2, random.randrange(22, 28) + (0.01 * random.randrange(0, 100))
                                     , session["sessionDate"], "Great")
                planDAO.createResult(idHolder, 4, 2, random.randrange(22, 28) + (0.01 * random.randrange(0, 100))
                                     , session["sessionDate"], "Great")
            else:
                exerciseList = set()
                while len(exerciseList) < 3:
                    exerciseList.add(random.randint(1, 8))

                repetitions = random.randint(1, 3)
                idHolder = planDAO.createPractice(exerciseList.pop(), mainID, repetitions,
                                                  1, 25 * random.randint(1, 32))
                for x in range(repetitions):
                    planDAO.createResult(idHolder, 1, 2, random.randrange(22, 28) + (0.01 * random.randrange(0, 100))
                                         , session["sessionDate"], "Great")
                    planDAO.createResult(idHolder, 2, 2, random.randrange(22, 28) + (0.01 * random.randrange(0, 100))
                                         , session["sessionDate"], "Great")
                    planDAO.createResult(idHolder, 3, 2, random.randrange(22, 28) + (0.01 * random.randrange(0, 100))
                                         , session["sessionDate"], "Great")
                    planDAO.createResult(idHolder, 4, 2, random.randrange(22, 28) + (0.01 * random.randrange(0, 100))
                                         , session["sessionDate"], "Great")

                repetitions = random.randint(1, 3)
                idHolder = planDAO.createPractice(exerciseList.pop(), mainID, repetitions,
                                                  1, 25 * random.randint(1, 32))

                for x in range(repetitions):
                    planDAO.createResult(idHolder, 1, 2, random.randrange(22, 28) + (0.01 * random.randrange(0, 100))
                                         , session["sessionDate"], "Great")
                    planDAO.createResult(idHolder, 2, 2, random.randrange(22, 28) + (0.01 * random.randrange(0, 100))
                                         , session["sessionDate"], "Great")
                    planDAO.createResult(idHolder, 3, 2, random.randrange(22, 28) + (0.01 * random.randrange(0, 100))
                                         , session["sessionDate"], "Great")
                    planDAO.createResult(idHolder, 4, 2, random.randrange(22, 28) + (0.01 * random.randrange(0, 100))
                                         , session["sessionDate"], "Great")

                repetitions = random.randint(1, 3)
                idHolder = planDAO.createPractice(exerciseList.pop(), mainID, repetitions,
                                                  1, 25 * random.randint(1, 32))

                for x in range(repetitions):
                    planDAO.createResult(idHolder, 1, 2, random.randrange(22, 28) + (0.01 * random.randrange(0, 100))
                                         , session["sessionDate"], "Great")
                    planDAO.createResult(idHolder, 2, 2, random.randrange(22, 28) + (0.01 * random.randrange(0, 100))
                                         , session["sessionDate"], "Great")
                    planDAO.createResult(idHolder, 3, 2, random.randrange(22, 28) + (0.01 * random.randrange(0, 100))
                                         , session["sessionDate"], "Great")
                    planDAO.createResult(idHolder, 4, 2, random.randrange(22, 28) + (0.01 * random.randrange(0, 100))
                                         , session["sessionDate"], "Great")

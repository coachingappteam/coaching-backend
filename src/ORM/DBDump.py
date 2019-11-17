import datetime

from src.DAO import CoachDAO, SportDAO


class Factory:

    def __init__(self):

        self.user = {"password": "coachingpr",
                     "firstName": "Coaching",
                     "lastName": "App",
                     "email": "coachingappteam@gmail.com",
                     "phone": "7873619803"
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
                       "roleName": "Velocist",
                       "roleDescription": "Swim athlete that focuses on being improving speed."
                       }, {"sportID": "1",
                           "roleName": "Fondist",
                           "roleDescription": "Swim athlete that focuses on being improving resitance."
                           }
                      ]
        self.exercises = [{"exerciseName": "50 Free",
                           "exerciseDescription": "50 Free Event.",
                           "unitID": 1,
                           "style": "Free",
                           "measure": 50
                           }, {"exerciseName": "100 Free",
                               "exerciseDescription": "100 Free Event.",
                               "unitID": 1,
                               "style": "Free",
                               "measure": 100
                               }, {"exerciseName": "200 Free",
                                   "exerciseDescription": "200 Free Event.",
                                   "unitID": 1,
                                   "style": "Free",
                                   "measure": 200
                                   }, {"exerciseName": "400 Free",
                                       "exerciseDescription": "400 Free Event.",
                                       "unitID": 1,
                                       "style": "Free",
                                       "measure": 400
                                       }, {"exerciseName": "800 Free",
                                           "exerciseDescription": "800 Free Event.",
                                           "unitID": 1,
                                           "style": "Free",
                                           "measure": 800
                                           }, {"exerciseName": "1500 Free",
                                               "exerciseDescription": "1500 Free Event.",
                                               "unitID": 1,
                                               "style": "Free",
                                               "measure": 1500
                                               }, {"exerciseName": "50 Backstroke",
                                                   "exerciseDescription": "50 Backstroke Event.",
                                                   "unitID": 1,
                                                   "style": "Backstroke",
                                                   "measure": 50
                                                   }, {"exerciseName": "100 Backstroke",
                                                       "exerciseDescription": "100 Backstroke Event.",
                                                       "unitID": 1,
                                                       "style": "Backstroke",
                                                       "measure": 100
                                                       }, {"exerciseName": "200 Backstroke",
                                                           "exerciseDescription": "200 Backstroke Event.",
                                                           "unitID": 1,
                                                           "style": "Backstroke",
                                                           "measure": 200
                                                           }, {"exerciseName": "50 Breaststroke",
                                                               "exerciseDescription": "50 Free Breaststroke.",
                                                               "unitID": 1,
                                                               "style": "Breaststroke",
                                                               "measure": 50
                                                               }, {"exerciseName": "100 Breaststroke",
                                                                   "exerciseDescription": "100 Breaststroke Event.",
                                                                   "unitID": 1,
                                                                   "style": "Breaststroke",
                                                                   "measure": 100
                                                                   }, {"exerciseName": "200 Breaststroke",
                                                                       "exerciseDescription": "200 Breaststroke Event.",
                                                                       "unitID": 1,
                                                                       "style": "Breaststroke",
                                                                       "measure": 200
                                                                       }, {"exerciseName": "50 Butterfly",
                                                                           "exerciseDescription": "50 Free Butterfly.",
                                                                           "unitID": 1,
                                                                           "style": "Butterfly",
                                                                           "measure": 50
                                                                           }, {"exerciseName": "100 Butterfly",
                                                                               "exerciseDescription": "100 Butterfly Event.",
                                                                               "unitID": 1,
                                                                               "style": "Butterfly",
                                                                               "measure": 100
                                                                               }, {"exerciseName": "200 Butterfly",
                                                                                   "exerciseDescription": "200 Butterfly Event.",
                                                                                   "unitID": 1,
                                                                                   "style": "Butterfly",
                                                                                   "measure": 200
                                                                                   }, {"exerciseName": "200 IM",
                                                                                       "exerciseDescription": "200 IM Event.",
                                                                                       "unitID": 1,
                                                                                       "style": "IM",
                                                                                       "measure": 200
                                                                                       }, {"exerciseName": "400 IM",
                                                                                           "exerciseDescription": "400 IM Event.",
                                                                                           "unitID": 1,
                                                                                           "style": "IM",
                                                                                           "measure": 400
                                                                                           }, {"exerciseName": "30 Min Run",
                                                                                               "exerciseDescription": "30 min run event",
                                                                                               "unitID": 5,
                                                                                               "style": "Run",
                                                                                               "measure": 30
                                                                                               }, {"exerciseName": "5 Min Streching",
                                                                                                   "exerciseDescription": "5 min streching event",
                                                                                                   "unitID": 5,
                                                                                                   "style": "Run",
                                                                                                   "measure": 5
                                                                                                   }
                          ]

        self.improves = [{"exerciseID": 1,
                          "roleID": 1
                          }, {"exerciseID": 2,
                              "roleID": 1
                              }, {"exerciseID": 3,
                                  "roleID": 1
                                  }, {"exerciseID": 4,
                                      "roleID": 1
                                      }, {"exerciseID": 5,
                                          "roleID": 2
                                          }, {"exerciseID": 6,
                                              "roleID": 2
                                              }, {"exerciseID": 7,
                                                  "roleID": 1
                                                  }, {"exerciseID": 8,
                                                      "roleID": 1
                                                      }, {"exerciseID": 9,
                                                          "roleID": 1
                                                          }, {"exerciseID": 10,
                                                              "roleID": 1
                                                              }, {"exerciseID": 11,
                                                                  "roleID": 1
                                                                  }, {"exerciseID": 12,
                                                                      "roleID": 1
                                                                      }, {"exerciseID": 13,
                                                                          "roleID": 1
                                                                          }, {"exerciseID": 14,
                                                                              "roleID": 1
                                                                              }, {"exerciseID": 15,
                                                                                  "roleID": 1
                                                                                  }, {"exerciseID": 16,
                                                                                      "roleID": 1
                                                                                      }, {"exerciseID": 17,
                                                                                          "roleID": 1
                                                                                          }
                         ]
        self.athletes = [{"coachID": None,
                     "firstName": "Miles",
                     "lastName": "Edgeworth",
                     "email": "coachingappteam@gmail.com",
                     "phone": "7873619803",
                     "sex": "M",
                     "birthdate": datetime.datetime(1996, 10, 11).date()
                     }]

    def pushDBDump(self):
        # Create User
        coachID = CoachDAO.CoachDAO().createAdmin(self.user['password'], self.user['firstName'], self.user['lastName'],
                                        self.user['phone'], self.user['email'])

        sportDAO = SportDAO.SportDAO()
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
            sportDAO.createExercise(exercise['exerciseName'], exercise['exerciseDescription'], exercise['unitID'],
                                    exercise['style'], exercise['measure'])

        # Create Improvements
        for improve in self.improves:
            sportDAO.createImproves(improve['exerciseID'], improve['roleID'])

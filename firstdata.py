############################################################################################################################
# FirstData                                                                                                                #
# Data Retrieval from FIRST API                                                                                            #
############################################################################################################################

import requests
import json

class MatchData:
    def __init__(self, config):
        # Class Imports
        self.config = config

    ### Data Retrieval Functions ###
    ## Gets Data from the FIRST API
    # @param dprint - formats the json dictionary into a readable format and prints it
    def getScheduleData(self, dprint = False):
        if (self.config.dataretrieval == "Manual"):
            with open('manual/manualqualscheduledata.json') as json_file:
                self.qualScheduleData = json.load(json_file)
            with open('manual/manualplayoffscheduledata.json') as json_file:
                self.playoffScheduleData = json.load(json_file)
        elif (self.config.dataretrieval == "Testing"):
            with open('testing/qualscheduledata.json') as json_file:
                self.qualScheduleData = json.load(json_file)
            with open('testing/playoffscheduledata.json') as json_file:
                self.playoffScheduleData = json.load(json_file)
        else:
            try:    
                response = requests.get('%s/v2.0/%s/schedule/%s/qual/hybrid' % (self.config.host, str(self.config.season), self.config.eventid), headers={'Accept': 'application/json', 'Authorization': 'Basic %s' % self.config.authString})
                self.qualScheduleData = response.json()["Schedule"]
                response = requests.get('%s/v2.0/%s/schedule/%s/playoff/hybrid' % (self.config.host, str(self.config.season), self.config.eventid), headers={'Accept': 'application/json', 'Authorization': 'Basic %s' % self.config.authString})
                self.playoffScheduleData = response.json()["Schedule"]
            except:
                print("Cannot retrieve Match Data from FIRST API!")
        if dprint == True:
            print(json.dumps(self.qualScheduleData, sort_keys=True, indent=4))
            print(json.dumps(self.playoffScheduleData, sort_keys=True, indent=4))

    def getScoreData(self, dprint = False):
        if (self.config.dataretrieval == "Manual"):
            with open('manual/manualqualscoredata.json') as json_file:
                self.qualScoreData = json.load(json_file)
            with open('manual/manualplayoffscoredata.json') as json_file:
                self.playoffScoreData = json.load(json_file)
        elif (self.config.dataretrieval == "Testing"):
            with open('testing/qualscoredata.json') as json_file:
                self.qualScoreData = json.load(json_file)
            with open('testing/playoffscoredata.json') as json_file:
                self.playoffScoreData = json.load(json_file)
        else:
            try:
                response = requests.get('%s/v2.0/%s/scores/%s/qual' % (self.config.host, self.config.season, self.config.eventid), headers={'Accept': 'application/json', 'Authorization': 'Basic %s' % self.config.authString})
                self.qualScoreData = response.json()["MatchScores"]
                response = requests.get('%s/v2.0/%s/scores/%s/playoff' % (self.config.host, self.config.season, self.config.eventid), headers={'Accept': 'application/json', 'Authorization': 'Basic %s' % self.config.authString})
                self.playoffScoreData = response.json()["MatchScores"]
            except:
                print("Cannot retrieve Score Data from FIRST API!")
        if dprint == True:
            print(json.dumps(self.qualScoreData, sort_keys=True, indent=4))
            print(json.dumps(self.playoffScoreData, sort_keys=True, indent=4))

    def getEventData(self, dprint = False):
        if (self.config.dataretrieval == "Manual"):
            with open('manual/manualeventdata.json') as json_file:
                self.eventData = json.load(json_file)
        elif (self.config.dataretrieval == "Testing"):
            with open('testing/eventdata.json') as json_file:
                self.eventData = json.load(json_file)
        else:
            try:
                response = requests.get('%s/v2.0/%s/events?eventCode=%s' % (self.config.host, self.config.season, self.config.eventid), headers={'Accept': 'application/json', 'Authorization': 'Basic %s' % self.config.authString})
                self.eventData = response.json()["Events"][0]
            except:
                print("Cannot retrieve Event Data from FIRST API!")
        if dprint == True:
            print(json.dumps(self.eventData, sort_keys=True, indent=4))

    def getTeamData(self, dprint = False):
        if (self.config.dataretrieval == "Manual"):
            with open('manual/manualteamdata.json') as json_file:
                self.teamData = json.load(json_file)
        elif (self.config.dataretrieval == "Testing"):
            with open('testing/teamdata.json') as json_file:
                self.teamData = json.load(json_file)
        else:
            try: 
                response = requests.get('%s/v2.0/%s/teams?eventCode=%s' % (self.config.host, self.config.season, self.config.eventid), headers={'Accept': 'application/json', 'Authorization': 'Basic %s' % self.config.authString})
                if (response.json()["pageTotal"] > 1):
                    pageList = []
                    self.teamData = {"teams" : []}
                    for x in range(0, response.json()["pageTotal"]):
                        tempresponse = requests.get('%s/v2.0/%s/teams?eventCode=%s?page=%s' % (self.config.host, self.config.season, self.config.eventid, x), headers={'Accept': 'application/json', 'Authorization': 'Basic %s' % self.config.authString})
                        pageList.insert(len(pageList), tempresponse.json()['teams'])
                    for x in pageList:
                        self.teamData["teams"] += x
                else:
                    self.teamData = response.json()["teams"]
            except:
                print("Cannot retrieve Team Data from FIRST API!")
        if dprint == True:
            print(json.dumps(self.teamData, sort_keys=True, indent=4))
            
    def dataChanged(self):
        # Stores the old schedules to check
        oldQualSchedule = self.qualScheduleData
        oldQualScore = self.qualScoreData
        oldPlayoffSchedule = self.playoffScheduleData
        oldPlayoffScore = self.playoffScoreData
        # Gets the new data
        self.getScoreData()
        self.getScheduleData()
        # Checks to see if any of them have changed
        if oldQualSchedule != self.qualScheduleData or oldQualScore != self.qualScoreData or oldPlayoffSchedule != self.playoffScheduleData or oldPlayoffScore != self.playoffScoreData:
            print("Detected Change in Data from FIRST API!")
            return True
        else:
            return False
    
    def checkIfMatchValid(self):
        # Checks to see if the match actually exists
        # Used to protect against program crashing if an invalid
        # match ID or season is entered
        try:
            # Attempts to get the event data
            response = requests.get('%s/v2.0/%s/events?eventCode=%s' % (self.config.host, self.config.season, self.config.eventid), headers={'Accept': 'application/json', 'Authorization': 'Basic %s' % self.config.authString})
            tempEventData = response.json()["Events"][0]
            return True
        except:
            # If it fails then return false
            print("Invalid Event Entered: %s" % self.config.eventid)
            return False

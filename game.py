#!/usr/bin/env python3

class Game:

    def __init__(self):
        self.home_team = Team()
        self.away_team = Team()
        self.OT = 0
        self.game_num = 0
        self.date = 0
        self.round = 0
        self.year = 0

    def printme(self):
        print("Game " + str(self.game_num) + ", Round " + str(self.round))
        print(self.away_team.team_name, self.away_team.score, "@", self.home_team.team_name, self.home_team.score)
        print()
        self.away_team.printme()
        print()
        self.home_team.printme()

class Team():

    def __init__(self):
        self.city = ""
        self.nickname = ""
        self.players = list()
        self.score = 0
        self.home = False
        self.opp_team = None
        self.game = None

    def get_team_name(self):
        return self.city + " " + self.nickname

    def printme(self):
        print(self.team_name.upper())
        for player in self.players:
            print(player.name, player.points)

    team_name = property(get_team_name)

class Player():
    def __init__(self):
        self.name = ""
        self.team = None
        self.opp_team = None
        self.game = None
        self.points = 0
        self.rebounds = 0
        self.assists = 0
        self.steals = 0
        self.blocks = 0
        self.turnovers = 0
        self.FG = 0
        self.FGA = 0
        self.FG3 = 0
        self.FGA3 = 0
        self.FT = 0
        self.FTA = 0
        self.plus_minus = 0

    def get_game_score(self):
        return self.points + self.rebounds + 1.5*self.assists + 2*self.steals + 2*self.blocks - \
            1.5*self.turnovers + (self.FG*3 - self.FGA)/2 + (self.FG3*3 - self.FGA3)/1.5 + \
            (self.FT*2.5 - self.FTA)/4 + self.plus_minus/3

    game_score = property(get_game_score)



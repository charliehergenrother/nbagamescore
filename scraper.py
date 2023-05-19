#!/usr/bin/env python3

from game import Game, Team, Player
import os
import time
import sys

SCHED_URL_START = "https://www.basketball-reference.com/playoffs/NBA_"
SCHED_URL_END = "_games.html"
GAME_URL_START = "https://www.basketball-reference.com"
SEPARATOR_LINE = "RESULTS ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"

CITIES = ["Anderson", "Atlanta", "Baltimore", "Boston", "Brooklyn", \
        "Buffalo", "Capital", "Charlotte", "Cincinnati", "Cleveland", \
        "Chicago", "Dallas", "Denver", "Detroit", "Fort Wayne", \
        "Golden State", "Houston", "Indiana", "Indianapolis", "Kansas City", \
        "Kansas City-Omaha", "Los Angeles", "Memphis", "Miami", "Milwaukee", \
        "Minneapolis", "Minnesota", "New Jersey", "New Orleans", "New York", 
        "Oklahoma City", "Orlando", "Philadelphia", "Phoenix", "Portland", \
        "Rochester", "Sacramento", "San Antonio", "San Diego", "San Francisco", \
        "Seattle", "Sheboygan", "St. Louis", "Syracuse", "Toronto", \
        "Tri-Cities", "Utah", "Washington"]

NICKNAMES = ["76ers", "Blackhawks", "Bobcats", "Braves", "Bucks", \
        "Bullets", "Bulls", "Capitols", "Cavaliers", "Celtics",
        "Clippers", "Grizzlies", "Hawks", "Heat", "Hornets",
        "Jazz", "Kings", "Knicks", "Lakers", "Mavericks",
        "Magic", "Nationals", "Nets", "Nuggets", "Olympians", \
        "Pacers", "Packers", "Pelicans", "Pistons", "Raptors", \
        "Red Skins", "Rockets", "Royals", "Spurs", "Stags", \
        "Suns", "SuperSonics", "Timberwolves", "Thunder", "Trail Blazers", \
        "Warriors", "Wizards"]

#takes in a full team name (e.g. "Washington Wizards") and returns the city and the nickname separately
def process_team_name(team):
    spl = team.split(" ")
    if len(spl) == 2 and spl[0] in CITIES and spl[1] in NICKNAMES:
        return spl[0], spl[1]
    elif len(spl) == 3:
        if spl[0] in CITIES and spl[1] + " " + spl[2] in NICKNAMES:
            return spl[0], spl[1] + " " + spl[2]
        if spl[0] + " " + spl[1] in CITIES and spl[2] in NICKNAMES:
            return spl[0] + " " + spl[1], spl[2]
    print("problem! (add me?)", team)
    sys.exit()

#process command line arguments
def process_args():
    argcounter = 1
    count_max = 100
    year = "2023"
    start_year = ""
    end_year = ""
    individual = True
    while argcounter < len(sys.argv):
        if sys.argv[argcounter] == '-y':
            if int(sys.argv[argcounter + 1]):
                year = sys.argv[argcounter + 1]
                argcounter += 1
        elif sys.argv[argcounter] == '-r':
            if int(sys.argv[argcounter + 1]) and int(sys.argv[argcounter + 2]):
                start_year = sys.argv[argcounter + 1]
                end_year = sys.argv[argcounter + 2]
                argcounter += 2
        elif sys.argv[argcounter] == '-m':
            if int(sys.argv[argcounter + 1]):
                count_max = int(sys.argv[argcounter + 1])
                argcounter += 1
        elif sys.argv[argcounter] == '-c':
            individual = False
        elif sys.argv[argcounter] == '-h':
            print("Welcome to the NBA Playoff game tracker!")
            print("I print out the best playoff player-games in a particular year.")
            print("Usage: ./scraper.py [-h] [-m <max>] [-y <year>] [-r <start year> <end year> [-c/-i]]")
            print("     -h: print this help message")
            print("     -m: print this many games. (Default: 100)")
            print("     -y: Use this year. (Default: 2023)")
            print("     -r: Use this year range instead of a single year.")
            print("     -c: When doing a year range, combine the years to give an overall look at that span of time.")
            print("     -i: When doing a year range, process and print each year individually. (default)")
            sys.exit()
        argcounter += 1
    return year, start_year, end_year, count_max, individual

#records stats for a particular player in a particular game
def process_player(line, player_team, opp_team, game):
    p = Player()
    p.team = player_team
    p.opp_team = opp_team
    p.game = game
    p.name = line[line.find(".html")+7:line.find("</a>")]
    p.points = int(line[line.find('"pts"')+7:line.find("</td>", line.find('"pts"'))])
    try:
        p.rebounds = int(line[line.find('"trb"')+7:line.find("</td>", line.find('"trb"'))])
    except ValueError:
        p.rebounds = 0
    try:
        p.assists = int(line[line.find('"ast"')+7:line.find("</td>", line.find('"ast"'))])
    except ValueError:
        p.assists = 0
    try:
        p.steals = int(line[line.find('"stl"')+7:line.find("</td>", line.find('"stl"'))])
    except ValueError:
        p.steals = 0
    try:
        p.blocks = int(line[line.find('"blk"')+7:line.find("</td>", line.find('"blk"'))])
    except ValueError:
        p.blocks = 0
    try:
        p.turnovers = int(line[line.find('"tov"')+7:line.find("</td>", line.find('"tov"'))])
    except ValueError:
        p.turnovers = 0
    try:
        p.FG = int(line[line.find('"fg"')+6:line.find("</td>", line.find('"fg"'))])
        p.FGA = int(line[line.find('"fga"')+7:line.find("</td>", line.find('"fga"'))])
    except ValueError:
        p.FG = 0
        p.FGA = 0
    try:
        p.FG3 = int(line[line.find('"fg3"')+7:line.find("</td>", line.find('"fg3"'))])
        p.FGA3 = int(line[line.find('"fg3a"')+8:line.find("</td>", line.find('"fg3a"'))])
    except ValueError:
        p.FG3 = 0
        p.FGA3 = 0
    p.FT = int(line[line.find('"ft"')+6:line.find("</td>", line.find('"ft"'))])
    p.FTA = int(line[line.find('"fta"')+7:line.find("</td>", line.find('"fta"'))])
    try:
        p.plus_minus = int(line[line.find('"plus_minus"')+14:line.find("</td>", line.find('"plus_minus"'))])
    except ValueError:
        p.plus_minus = 0
    return p

#records stats for both teams for a particular game given the path pointing to the file
def process_game(filename, year):
    f = open(filename)
    game = Game()
    team_1_searching = False
    team_2_searching = False
    for line in f:
        if "BreadcrumbList" in line:
            #record team cities and nicknames
            away_team = line[line.find("Game")+8:line.find(" at ")]
            game.away_team.city, game.away_team.nickname = process_team_name(away_team)
            home_team = line[line.find(" at ")+4:line.find(" Box Score,")]
            game.home_team.city, game.home_team.nickname = process_team_name(home_team)
            game.home_team.home = True
            game.home_team.opp_team = game.away_team
            game.away_team.opp_team = game.home_team
            game.home_team.game = game
            game.away_team.game = game
            game.year = year

            #record game number and round
            game.game_num = int(line[line.find("Game")+5])
            if "First Round" in line:
                game.round = 1
            elif "Conference Semifinals" in line:
                game.round = 2
            elif "Conference Finals" in line:
                game.round = 3
            elif "NBA Finals" in line:
                game.round = 4
            continue

        if game.away_team.team_name + " Basic and Advanced Stats Table" in line:
            team_1_searching = True
        if game.home_team.team_name + " Basic and Advanced Stats Table" in line:
            team_2_searching = True

        #record stats for each player in the game
        if team_1_searching and "data-append-csv" in line and "pts" in line:
            game.away_team.players.append(process_player(line, game.away_team, game.home_team, game))
            game.away_team.score += game.away_team.players[-1].points
        if team_1_searching and "</table>" in line:
            team_1_searching = False
        if team_2_searching and "data-append-csv" in line and "pts" in line:
            game.home_team.players.append(process_player(line, game.home_team, game.away_team, game))
            game.home_team.score += game.home_team.players[-1].points
        if team_2_searching and "</table>" in line: #end of the second table is the end of relevant data
            team_2_searching = False
            break

    f.close()
    return game

#returns a stringified percentage to be used for field goals, etc.
def get_pct_out(makes, attempts):
    if makes == 0:
        return "0.00%"
    return str(round(makes/attempts*100, 2)) + "%"

#scrape web pages of playoff games for data, requesting them via wget if necessary
def do_scrape(year):
    url = SCHED_URL_START + year + SCHED_URL_END
    if not os.path.isdir("./data/" + year):
        os.mkdir("./data/" + year)
    if not os.path.isfile("./data/" + year + "/" + year + "games.txt"):
        os.system("wget -O data/" + year + "/" + year + "games.txt " + url)
    f = open("data/" + year + "/" + year + "games.txt")
    games = list()
    for line in f:
        if "date_game" in line and "boxscores" in line:
            url_end = line[line.find("/boxscores/" + year):line.find("Box Score")-2]
            game_url = GAME_URL_START + url_end
            game_file = game_url[game_url.find("/boxscores/")+11:]
            while not os.path.isfile("./data/" + year + "/" + game_file):
                os.system("wget --retry-on-http-error=429 --wait=1 --random-wait -O data/" + year + "/" + game_file + " " + game_url)
                time.sleep(4)
            game = process_game("data/" + year + "/" + game_file, int(year))
            games.append(game)
    f.close()
    return games

#check existence of a key in a dictionary; if present, increment it; if not, add it
def check_and_add(dictionary, key, value, increment):
    if key in dictionary:
        dictionary[key] += increment
    else:
        dictionary[key] = value

#process and print results for a particular year in the NBA playoffs
def process_playoffs(games, count_max, individual, year_range=""):
    team_games = [x.home_team for x in games] + [x.away_team for x in games]
    player_games = list()
    for x in team_games:
        player_games += x.players
    name_len = max([len(x.name) for x in player_games])
    nickname_len = max([len(x) for x in NICKNAMES])
    player_totals, team_totals = print_games(count_max, name_len, nickname_len, player_games, individual, year_range)
    print_players(player_totals, team_totals, name_len)
    print_teams(team_totals)

#print the best individual player-games for a particular year or range of years
def print_games(count_max, name_len, nickname_len, player_games, individual, year_range):
    if individual:
        year_title = str(player_games[0].game.year)
    else:
        year_title = year_range
    print(year_title, SEPARATOR_LINE)
    print("Player".ljust(name_len), "Team".ljust(nickname_len), "Opponent/Game".ljust(nickname_len + 10), "Pt Rb As St Bk TO FG%    3FG%   FT%    +/- FG At 3P At FT At Score")
    player_series_tracker = dict()
    player_totals = dict()
    team_totals = dict()
    game_count = 0
    for player_game in sorted(player_games, key=lambda x: x.game_score, reverse=True):
        counts = True
        check_and_add(player_series_tracker, tuple([player_game.name, player_game.opp_team.nickname, \
                player_game.game.year]), 1, 1)
        if player_series_tracker[tuple([player_game.name, player_game.opp_team.nickname, player_game.game.year])] >= 5:
            count_max += 1
            counts = False
        if counts and player_game.name in player_totals:
            player_totals[player_game.name]["score"] += player_game.game_score
            player_totals[player_game.name]["games"] += 1
        elif counts:
            player_totals[player_game.name] = {"score": player_game.game_score, \
                    "team": player_game.team.city + " " + player_game.team.nickname, \
                    "games": 1}
        full_team = player_game.team.city + " " + player_game.team.nickname
        if counts:
            if full_team in team_totals:
                team_totals[full_team]["score"] += player_game.game_score
            else:
                team_totals[full_team] = {"score": player_game.game_score, "players": list()}
        opp_string = ""
        if not individual:
            opp_string = str(player_game.game.year) + " "
        if player_game.team.home:
            opp_string += "v. "
        else:
            opp_string += "@ "
        if player_game.plus_minus >= 0:
            pm_string = "+" + str(player_game.plus_minus)
        else:
            pm_string = str(player_game.plus_minus)
        opp_string += player_game.opp_team.nickname + " Game " + str(player_game.game.game_num)
        FG_string = get_pct_out(player_game.FG, player_game.FGA)
        FG3_string = get_pct_out(player_game.FG3, player_game.FGA3)
        FT_string = get_pct_out(player_game.FT, player_game.FTA)
        print(player_game.name.ljust(name_len), player_game.team.nickname.ljust(nickname_len), \
                opp_string.ljust(nickname_len + 10), str(player_game.points).rjust(2), \
                str(player_game.rebounds).rjust(2), str(player_game.assists).rjust(2), \
                str(player_game.steals).rjust(2), str(player_game.blocks).rjust(2), \
                str(player_game.turnovers).rjust(2), FG_string.ljust(6), FG3_string.ljust(6), \
                FT_string.ljust(6), pm_string.rjust(3), \
                str(player_game.FG).rjust(2), str(player_game.FGA).rjust(2), \
                str(player_game.FG3).rjust(2), str(player_game.FGA3).rjust(2), \
                str(player_game.FT).rjust(2), str(player_game.FTA).rjust(2), \
                round(player_game.game_score, 4))
        game_count += 1
        if game_count >= count_max:
            break
    print()
    return player_totals, team_totals

#print the players with the best run in a particular playoff year
def print_players(player_totals, team_totals, name_len):
    rank = 1
    for player in sorted(player_totals, key=lambda x: player_totals[x]["score"], reverse=True):
        if player_totals[player]["games"] == 1:
            game_str = " game)"
        else:
            game_str = " games)"
        print(str(rank).rjust(2) + ".", player.ljust(name_len), str(round(player_totals[player]["score"], 4)).rjust(9), \
                "(" + str(player_totals[player]["games"]) + game_str)
        team_totals[player_totals[player]["team"]]["players"].append(player + " (" + str(rank) + ")")
        rank += 1
    print()

#print the teams with the best run in a particular playoff year
def print_teams(team_totals):
    rank = 1
    for team in sorted(team_totals, key=lambda x: team_totals[x]["score"], reverse=True):
        print(str(rank).rjust(2) + ".", team, round(team_totals[team]["score"], 4))
        for player in team_totals[team]["players"]:
            print("    " + player)
        print()
        rank += 1
    print()

def main():
    year, start_year, end_year, count_max, individual = process_args()
    if start_year:
        games = list()
        for year in range(int(start_year), int(end_year) + 1):
            if individual:
                games = do_scrape(str(year))
                process_playoffs(games, count_max, individual)
            else:
                games += do_scrape(str(year))
        if not individual:
            process_playoffs(games, count_max, individual, start_year + "-" + end_year)

    else:
        games = do_scrape(str(year))
        process_playoffs(games, count_max, individual)

if __name__ == '__main__':
    main()

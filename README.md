Welcome to the NBA playoff game tracker!

The goal of this project is to find the NBA players who have been the most dominant in the playoffs over a particular postseason, span of time, or all time. The way this is done is by calculating a game score for each player in each game. The top game scores for a particular year are taken and added together for a player so that a number is assigned to how many times they took over a game and the degree of their dominance when doing so. This can therefore be used, for example, to compare players against their peers in a year (1. Nikola Jokic, 2. Jimmy Butler in 2023), teams over a range of time (1. Golden State Warriors, 2. Oklahoma City Thunder from 2010-2019), or players against each other for their entire careers (1. LeBron James, 2. Michael Jordan all time). Some example queries:

For a report on the top 100 games of the 2023 season:
./scraper.py -y 2023 -m 100
(Best player-games from the above command:)
1. Jayson Tatum v. 76ers Game 7, 51/13/5, score of 106.7
2. Devin Booker v. Nuggets Game 3, 47/6/9, score of 95.25
3. Devin Booker v. Clippers Game 5, 47/8/10, score of 93.125

For a report on the top 150 games per year from 2010 to 2019, combined and added:
./scraper.py -r 2010 2019 -p 150 -c
(Best player totals from the above command:)
1. LeBron James 7967.9 (121 games)
2. Kevin Durant 5022.0 (82 games)
3. Stephen Curry 3750.3 (60 games)

For a report on the top 50 individual games of all time:
./scraper.py -r 1950 2023 -m 50 -c
(Best player-games from the above command:)
1. Damian Lillard @ Nuggets 2021 Game 5, 55/6/10, 112.5 
2. Vince Carter v. 76ers 2001 Game 3, 50/6/7, 107.5
3. Kevin Durant v. Bucks 2021 Game 5, 49/17/10, 107.1

For a report on the top 50 playoff runs over Michael Jordan's Bulls career:
./scraper.py -r 1985 1998 -p 100 -c -f
(Best runs from the above command:)
1. 1995 Hakeem Olajuwon 1100.2
2. 1994 Hakeem Olajuwon 1057.9
3. 1993 Charles Barkley 1035.0
(this really wasn't supposed to be a Jordan diss, I'm a Bulls fan. eep)

And my personal favorite. For a report on the entire history of basketball:
./scraper.py -r 1950 2023 -p 150 -c

SCROLL HERE FOR MATH & LOGISTICS

The game score is calculated as follows:
- 1 point per point
- 1 point per rebound
- 1.5 points per assist
- 2 points per block
- 2 points per steal
- -1.5 points per turnover
- 1 point for every 3 points of positive plus-minus (or -1 for every 3 points of negative +/-)
- 0 points for 33.3% FG. 1.5 points for every FG made over 33% (or -1.5 for every FG under 33%)
- 0 points for 33.3% 3FG. 2 points for every 3FG made over 33% (or -2 for every 3FG under 33%)
- 0 points for 40% FT. 0.625 points for every FT made over 40% (or -0.625 for every FT under 40%)

Once the game score has been calculated for every player-game of a playoff year, the top 100 (changeable by -m) player-game scores are listed and tracked. Each player may only record 4 games which count per series, even if they are in the top 100 five or more times for a series. If this happens, the 101st-best overall game score is taken so that 100 games are always counted.

After the 100 games are finalized, they are printed out in full. Then, the players are printed out by their total score for the games that count. Finally, the teams who had a player recording a top 100 game are printed in order of combined total score for all players who did so.






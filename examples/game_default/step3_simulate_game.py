import os
import json
from gator_poking import Game, League, GatorLeague


HERE = os.path.abspath(os.path.dirname(__file__))


def main():
    teams = load_teams()
    congs = load_congregations()

    t1 = teams[0]
    t2 = teams[1]
    cong = congs[0]

    gp = Game(t1, t2, cong)
    #gp.simulate()


def load_teams():
    league_file = os.path.join(HERE, 'league.json')
    league = League(league_file)
    teams = league.get_teams()
    return teams


def load_congregations():
    gleague_file = os.path.join(HERE, 'gatorleague.json')
    gleague = GatorLeague(gleague_file)
    congs = gleague.get_congregations()
    return congs


if __name__=="__main__":
    main()

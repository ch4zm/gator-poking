import os
import json
from pprint import pprint
from gator_poking.core import League, GatorLeague


HERE = os.path.abspath(os.path.dirname(__file__))

league_file = os.path.join(HERE, 'league.json')
league = League(league_file)
teams = league.get_teams()

pprint(teams)

gleague_file = os.path.join(HERE, 'gatorleague.json')
gleague = GatorLeague(gleague_file)
congs = gleague.get_congregations()

pprint(congs)

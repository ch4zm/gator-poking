import os
import json
from gator_poking import LeagueGenerator, GatorLeagueGenerator


# Provide optional working directory arg to generate()
HERE = os.path.abspath(os.path.dirname(__file__))


# Everything goes in the tournament/ dir
wd = os.path.join(HERE, 'tournament')
if not os.path.exists(wd):
    os.mkdir(wd)

lg = LeagueGenerator()
league, league_filename = lg.generate(working_dir=wd)
print("-"*40)
print(f"Wrote league to {league_filename}")
print("-"*40)
print(json.dumps(league, indent=4))

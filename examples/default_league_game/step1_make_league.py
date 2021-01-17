import os
import json
from gator_poking import LeagueGenerator, GatorLeagueGenerator


# Provide optional working directory arg to generate()
HERE = os.path.abspath(os.path.dirname(__file__))


lg = LeagueGenerator()
league, league_filename = lg.generate(working_dir=HERE)
print("-"*40)
print(f"Wrote league to {league_filename}")
print("-"*40)

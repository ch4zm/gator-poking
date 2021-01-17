import os
import json
from gator_poking import LeagueGenerator, GatorLeagueGenerator


# Provide optional working directory arg to generate()
HERE = os.path.abspath(os.path.dirname(__file__))
cities_file = os.path.join(HERE, 'wi_cities.txt')
nicknames_file = os.path.join(HERE, 'wi_nicknames.txt')

# Use Wisconsin cities
lg = LeagueGenerator(
    cities_file = cities_file,
    nicknames_file = nicknames_file
)
league, league_filename = lg.generate(working_dir=HERE)
print("-"*40)
print(f"Wrote league to {league_filename}")
print("-"*40)
print(json.dumps(league, indent=4))

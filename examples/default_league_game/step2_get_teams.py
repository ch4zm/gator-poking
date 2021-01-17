import os
import json
from gator_poking.core import Team


HERE = os.path.abspath(os.path.dirname(__file__))


json_file = os.path.join(HERE, 'league.json')
with open(json_file, 'r') as f:
    league = json.load(f)

for teamid, teamjson in league.items():
    team = Team.from_json(teamjson)
    print(json.dumps(team.to_json(), indent=4))

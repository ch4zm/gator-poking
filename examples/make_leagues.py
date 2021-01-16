import json
from gator_poking import LeagueGenerator


lg = LeagueGenerator()
league = lg.generate()
print(json.dumps(league, indent=4))

#glg = GatorLeagueGenerator()
#gleague = glg.generate()
#print(json.dumps(gleague, indent=4))

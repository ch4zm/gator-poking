import json
from gator_poking import LeagueGenerator, GatorLeagueGenerator


lg = LeagueGenerator()
league = lg.generate()
final = {}
for team in league:
    final[team['id']] = team
print(json.dumps(final, indent=4))

glg = GatorLeagueGenerator()
gleague = glg.generate()
final = {}
for cong in gleague:
    final[cong['id']] = cong
print(json.dumps(final, indent=4))

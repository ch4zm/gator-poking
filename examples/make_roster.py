import json
from gator_poking import RosterGenerator


rg = RosterGenerator()
print(json.dumps(rg.generate(), indent=4))

from gator_poking import GameSimulator
from gator_poking.core import Config, DefaultConfig, Team, Congregation


config = DefaultConfig()
t1 = Team("St. Petersburg Paradoxes", size=config['PLAYERS_PER_SIDE'])
t2 = Team("Tallahassee Rasslers", size=config['PLAYERS_PER_SIDE'])
congregation = Congregation("Everglades Glories")

gp = GameSimulator()
gp.simulate()

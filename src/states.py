class GameState(object):
    """
    Simple class to store game state.
    Game state includes:
    - configuration
    - both teams
    - both team states
    - gator congregation
    """
    def __init__(self, config, team1, team2, state1, state2, congregation):
        self.config = config
        self.team1 = team1
        self.team2 = team2
        self.state1 = state1
        self.state2 = state2
        self.congregation = congregation


class TeamState(object):
    """Simple class to store team state"""
    def __init__(self, team):
        self.team = team
        self.pokers = [None, None]
        self.runs = 0
        self.wickets = 0
        self.done = False

    def inning_start(self):
        self.team.inning_start()
        self.pokers = [self.team.get_next_player(), self.team.get_next_player()]

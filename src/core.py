import uuid
import random


class Config(dict):
    def __init__(self, config : dict):
        req_keys = [
            'PLAYERS_PER_SIDE',
            'OVERS_PER_INNING',
            'PLAYS_PER_OVER',
        ]
        for rk in req_keys:
            if rk not in config.keys():
                raise Exception(f"Missing required config key: {rk}")
        for k,v in config.items():
            self[k] = v


class Team(object):
    """
    Define a class for teams.
    Holds the roster and team name.
    Also returns players in order, retaining state.
    This is useful for Games.
    """
    roster = []

    def __init__(self, name, size):
        self.name = name
        for i in range(size):
            self.roster.append(Player())
        self.index = 0

    def inning_start(self):
        self.index = 0

    def has_next_player(self):
        """
        Check if there is a next player to return
        """
        return self.index < len(self.roster)

    def get_next_player(self):
        """
        Get the next player
        """
        if self.has_next_player():
            return self.roster[self.index]
        else:
            return None


class Player(object):
    def __init__(self):
        self.id = str(uuid.uuid4())
        self.attr = {}
        self.attr['agg'] = random.randint(1,5)
        self.attr['rea'] = random.randint(1,5)
        self.attr['rxn'] = random.randint(1,5)
        self.attr['con'] = random.randint(1,5)


class Congregation(object):
    """
    Define a congregation of gators.
    This is the "team" of gators that occupy a field.
    """
    def __init__(self, name):
        self.name = name

    def get_next_gator(self):
        return Gator()


class Gator(object):
    def __init__(self):
        self.id = str(uuid.uuid4())
        self.attr = {}
        self.attr['agg'] = random.randint(1,5)
        self.attr['rea'] = random.randint(1,5)
        self.attr['rxn'] = random.randint(1,5)
        self.attr['con'] = random.randint(1,5)

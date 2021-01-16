import os
import json
import uuid
import random


class Config(dict):
    def __init__(self, config_dict):
        config = config_dict

        # Load and validate the config dict
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


class DefaultConfig(Config):
    """Config object with default values"""
    def __init__(self):
        self['PLAYERS_PER_SIDE'] = 11
        self['OVERS_PER_INNING'] = 20
        self['PLAYS_PER_OVER']   = 6


class Team(object):
    """
    Define a class for teams.
    Holds information about the team, plus a pointer to a roster.
    Loads the roster to return players in order, retaining state.
    Useful for Game simulator.
    """
    def __init__(self, teamid, city, nickname, color):
        self.id = teamid
        self.city = city
        self.nickname = nickname
        self.color = color
        self.name = city + " " + nickname
        self.roster = None

    def init_roster(self, working_dir):
        if not os.path.isdir(working_dir):
            raise Exception(f"Error: specified working directory {working_dir} is not a directory")
        self.working_dir = working_dir
        # Create a new roster in the working dir
        self.roster = None

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

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "nickname": self.nickname,
            "city": self.city,
            "color": self.color
        }


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

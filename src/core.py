import os
import json
import uuid
import random
from .errors import GatorPokingError as GPE


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
                raise GPE(f"Missing required config key: {rk}")
        for k,v in config.items():
            self[k] = v


class DefaultConfig(Config):
    """Config object with default values"""
    def __init__(self):
        self['PLAYERS_PER_SIDE'] = 11
        self['OVERS_PER_INNING'] = 20
        self['PLAYS_PER_OVER']   = 6


##################################
# Leagues/GatorLeagues

class LeagueBase(object):
    req_keys = []
    def __init__(self, league_json_file):
        # Make sure data file exists
        if not os.path.exists(league_json_file):
            raise GPE(f"Error: league file {league_json_file} does not exist")

        # Load the data file
        with open(league_json_file, 'r') as f:
            self.data = json.load(f)

        # Validate the loaded data
        team_req_keys = self.req_keys
        for teamid, teamdict in self.data.items():
            for rk in team_req_keys:
                if rk not in teamdict:
                    raise GPE(f"Error: could not create league from json file {league_json_file}, team missing key {rk}")


class League(LeagueBase):
    req_keys = ['id', 'city', 'nickname', 'color', 'name']

    def get_teams(self):
        teams = []
        for teamid, teamjson in self.data.items():
            teams.append(Team.from_json(teamjson))
        return teams


class GatorLeague(LeagueBase):
    req_keys = ['id', 'place', 'nickname', 'name']

    def get_congregations(self):
        congs = []
        for congid, congjson in self.data.items():
            congs.append(Congregation.from_json(congjson))
        return congs



##################################
# Teams/Congregations

class Team(object):
    """
    Define a class for teams.
    Holds information about the team.
    Useful for Game simulator.
    """
    req_keys = ['city', 'nickname', 'color']

    def __init__(self, **kwargs):
        req_keys = self.req_keys
        for rk in req_keys:
            if rk not in kwargs:
                raise GPE(f"Error: missing required key {rk} in Team constructor")
            setattr(self, rk, kwargs[rk])
        if 'id' not in kwargs:
            playerid = str(uuid.uuid4())
        else:
            playerid = kwargs['id']
        setattr(self, 'id', playerid)
        self.name = self.city + " " + self.nickname

    def __repr__(self):
        return self.name

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "nickname": self.nickname,
            "city": self.city,
            "color": self.color
        }

    @classmethod
    def from_json(cls, data_dict):
        req_keys = ['id', 'city', 'nickname', 'color']
        for rk in req_keys:
            if rk not in data_dict:
                raise GPE(f"Error: could not create team from dictionary data, missing key {rk}")
        return cls(**data_dict)

    ### def set_start_roster(self, working_dir, roster=None):
    ###     if not os.path.isdir(working_dir):
    ###         raise GPE(f"Error: specified working directory {working_dir} is not a directory")
    ###     self.working_dir = working_dir

    ###     if roster is None:
    ###         self.roster = Roster()
    ###     else:
    ###         self.roster = roster

    ### def inning_start(self):
    ###     self.index = 0

    ### def has_next_player(self):
    ###     """
    ###     Check if there is a next player to return
    ###     """
    ###     return self.index < len(self.roster)

    ### def get_next_player(self):
    ###     """
    ###     Get the next player
    ###     """
    ###     if self.has_next_player():
    ###         return self.roster[self.index]
    ###     else:
    ###         return None


class Congregation(object):
    """
    Define a congregation of gators.
    This is the "team" of gators that occupy a field.
    """
    req_keys = ['place', 'nickname']
    def __init__(self, **kwargs):
        req_keys = self.req_keys
        for rk in req_keys:
            if rk not in kwargs:
                raise GPE(f"Error: missing required key {rk} from Congregation constructor")
            setattr(self, rk, kwargs[rk])
        if 'id' not in kwargs:
            playerid = str(uuid.uuid4())
        else:
            playerid = kwargs['id']
        setattr(self, 'id', playerid)
        self.name = self.place + " " + self.nickname

    def __repr__(self):
        return self.name

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "place": self.place,
            "nickname": self.nickname
        }

    @classmethod
    def from_json(cls, data_dict):
        req_keys = ['id', 'place', 'nickname', 'name']
        for rk in req_keys:
            if rk not in data_dict:
                raise GPE(f"Error: could not create team from dictionary data, missing key {rk}")
        return cls(**data_dict)

    def get_next_gator(self):
        return Gator(
            name = self.name,
            agg = self.agg,
            rea = self.rea,
            rxn = self.rxn,
            con = self.con
        )

    def set_attributes(self):
        attr_keys = ['agg', 'rea', 'rxn', 'con']
        for k in attr_keys:
            setattr(self, k, random.randint(1,5))


##################################
# Players/Gators

class PlayerBase(object):
    req_keys = ['name', 'agg', 'rea', 'rxn', 'con']
    def __init__(self, **kwargs):
        req_keys = self.req_keys
        for rk in req_keys:
            if rk not in kwargs:
                raise GPE(f"Error: missing required key {rk} from {type(self).__name__} constructor")
            setattr(self, rk, kwargs[rk])
        if 'id' not in kwargs:
            playerid = str(uuid.uuid4())
        else:
            playerid = kwargs['id']
        setattr(self, 'id', playerid)

    def __repr__(self):
        s = f"{self.name} (agg {self.agg}/rea {self.rea}/rxn {self.rxn}/con {self.con})"
        return s


class Player(PlayerBase):
    pass


class Gator(object):
    pass

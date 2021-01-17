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


class League(object):
    def __init__(self, league_json_file):
        if not os.path.exists(league_json_file):
            raise Exception(f"Error: league file {league_json_file} does not exist")
        with open(league_json_file, 'r') as f:
            self.data = json.load(f)

    def get_teams(self):
        teams = []
        for teamid, teamjson in self.data:
            teams.append(Teams.from_json(teamjson))
        return teams


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
        self.nick = nickname
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
            "nickname": self.nick,
            "city": self.city,
            "color": self.color
        }

    @classmethod
    def from_json(cls, data_dict):
        req_keys = ['id', 'city', 'nickname', 'color', 'name']
        for rk in req_keys:
            if rk not in data_dict:
                raise Exception(f"Error: could not create team from dictionary data, missing key {rk}")
        return cls(data_dict['id'], data_dict['city'], data_dict['nickname'], data_dict['color'])

    @classmethod
    def from_json_file(cls, data_file):
        if not os.path.exists(data_file):
            raise Exception(f"Error: specified data file {data_file} does not exist")
        with open(data_file, 'r') as f:
            data_dict = json.load(f)
        req_keys = ['id', 'city', 'nickname', 'color', 'name']
        for rk in req_keys:
            if rk not in data_dict:
                raise Exception(f"Error: could not create team from json file {data_file}, missing key {rk}")
        return cls(data_dict['id'], data_dict['city'], data_dict['nickname'], data_dict['color'])


class Player(object):
    def __init__(self, **kwargs):
        req_keys = ['id', 'name', 'agg', 'rea', 'rxn', 'con']
        for rk in req_keys:
            if rk not in kwargs:
                raise Exception(f"Error: missing required key {rk} from player constructor")
        self.id = kwargs['id']
        self.agg = kwargs['agg']
        self.rea = kwargs['rea']
        self.rxn = kwargs['rxn']
        self.con = kwargs['con']


class RandomPlayer(Player):
    def __init__(self):
        ng = NameGenerator(firstnames_file, lastnames_file)
        name = ng.generate()
        # name = "Joe Blog"
        super().__init__(
            id = str(uuid.uuid4()),
            name = name,
            agg = random.randint(1,5),
            rea = random.randint(1,5),
            rxn = random.randint(1,5),
            con = random.randint(1,5)
        )


class Congregation(object):
    """
    Define a congregation of gators.
    This is the "team" of gators that occupy a field.
    """
    def __init__(self, gatorid, place, nickname):
        self.id = gatorid
        self.place = place
        self.nick = nickname
        self.name = place + " " + nickname

    def get_next_gator(self):
        return Gator()

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "place": self.place,
            "nickname": self.nick
        }


class Gator(object):
    def __init__(self):
        self.id = str(uuid.uuid4())
        self.attr = {}
        self.attr['agg'] = random.randint(1,5)
        self.attr['rea'] = random.randint(1,5)
        self.attr['rxn'] = random.randint(1,5)
        self.attr['con'] = random.randint(1,5)


class NameGenerator(object):
    """
    Generate first + last names.
    """
    def __init__(
        self,
        firstnames_file,
        lastnames_file
    ):
        if firstnames_file is None:
            firstnames_file = os.path.join(HERE, 'data', 'firstnames.txt')
        if lastnames_file is None:
            lastnames_file = os.path.join(HERE, 'data', 'lastnames.txt')
        # verify file exists
        for data_file in [firstnames_file, lastnames_file]:
            if not os.path.exists(data_file):
                raise Exception(f"Error: Could not find data file {data_file}")
        # load first names
        with open(firstnames_file, 'r') as f:
            firstnamesdata = f.readlines()
        self.firstnamesdata = [j.strip() for j in firstnamesdata]
        # load last names
        with open(lastnames_file, 'r') as f:
            lastnamesdata = f.readlines()
        self.lastnamesdata = [j.strip() for j in lastnamesdata]

    def generate(self, size=1):
        names = []
        for i in range(size):
            name = random.choice(self.firstnamesdata) + ' ' + random.choice(self.lastnamesdata)
            names.append(name)
        return names

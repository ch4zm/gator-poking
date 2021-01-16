import uuid
import random
import os
from .core import Team


HERE = os.path.abspath(os.path.dirname(__file__))


###############################################################
# Classes below are intended to be imported and used

class LeagueGenerator(object):
    """
    Generate a league (a collection of teams in the form of a team id: team json map).
    Team JSON contains:
    - id
    - city
    - nickname
    - color
    """
    def __init__(
        self, 
        cities_file = None,
        nicknames_file = None,
        colors_file = None
    ):
        # Set default values for filenames
        if cities_file is None:
            cities_file = os.path.join(HERE, 'data', 'cities.txt')
        if nicknames_file is None:
            nicknames_file = os.path.join(HERE, 'data', 'teamnicknames.txt')
        if colors_file is None:
            colors_file = os.path.join(HERE, 'data', 'colors.txt')

        # The team generator does all the hard work
        self.team_generator = TeamGenerator(cities_file, nicknames_file, colors_file)

    def generate(self, size=2):
        if size%2 != 0:
            raise Exception(f"Error: leagues must have an even number of teams")
        league = self.team_generator.generate(size = size)
        return league


class GatorLeagueGenerator(object):
    """
    Generate a gator league (a collection of congregations in the form of a congregation id: congregation json map).
    """
    def __init__(
        self,
        gatorplaces_file = None,
        gatornicknames_file = None
    ):
        # Set default values for filenames
        if gatortypes_file is None:
            gatortypes_file = os.path.join(HERE, 'data', 'gatortypes.txt')
        if gatornicknames_file is None:
            gatornicknames_file = os.path.join(HERE, 'data', 'gatornicknames.txt')

        # The congregation generator does all the hard work
        self.congregation_generator = CongregationGenerator(gatorplaces_file, gatornicknames_file)
    
    def generate(self, size=2):
        if size%2 != 0:
            raise Exception(f"Error: gator leagues msut have an even number of congregations")
        gleague = self.congregation_generator.generate(size = size)
        return gleague


class RosterGenerator(object):
    """
    Generate a roster (a collection of players in the form of a player id: player json map).
    """
    def __init__(
        self,
        firstnames_file = None,
        lastnames_file = None
    ):
        self.player_generator = PlayerGenerator(firstnames_file, lastnames_file)

    def generate(self, size=1):
        roster = {}
        for i in range(size):
            p = self.player_generator.generate()[0]
            roster[p['id']] = p
        return roster


###############################################################
# Classes below are mostly for internal use

class BaseGenerator(object):
    """
    Base class to load lines from plain text file into list
    """
    def __init__(
        self, 
        data_file
    ):
        # Verify file exists
        if not os.path.exists(data_file):
            raise Exception(f"Error: specified data file {data_file} does not exist!")
        # Load data
        with open(data_file, 'r') as f:
            data = f.readlines()
        self.data = [j.strip() for j in data]

    def generate(self, size=1):
        if size > len(self.data):
            raise Exception(f"Error: requested size {size} was larger than size of data {len(self.data)}")
        return random.choices(self.data, k=size)


class TeamGenerator(object):
    """
    Generate info about teams
    """
    def __init__(
        self, 
        cities_file, 
        nicknames_file, 
        colors_file
    ):
        self.city_generator     = BaseGenerator(cities_file)
        self.nickname_generator = BaseGenerator(nicknames_file)
        self.color_generator    = BaseGenerator(colors_file)

    def generate(self, size=1):
        cities = self.city_generator.generate(size = size)
        nicknames = self.nickname_generator.generate(size = size)
        colors = self.color_generator.generate(size = size)
        teams = []
        for (city, nickname, color) in zip(cities, nicknames, colors):
            t = Team(city, nickname, color, 



            t = Team({'city': city, 'nickname': nickname, 'color': color}, size=1)
            teams.append(t.to_json())
        return teams


class CongregationGenerator(object):
    def __init__(
        self,
        gatortypes_file,
        gatornicknames_file
    ):
        self.type_generator = BaseGenerator(gatortypes_file)
        self.nick_generator = BaseGenerator(gatornicknames_file)

    def generate(self, size=1):
        types = self.type_generator.generate(size = size)
        nicks = self.nick_generator.generate(size = size)
        congregations = []
        for (t, n) in zip(types, nicks):
            name = t + " " + n
            congregations.append(Congregation(name))
        return congregations


class PlayerGenerator(object):
    """
    Generate a player JSON with help from NameGenerator.
    Player JSON contains:
    - id
    - name
    - agg (aggressiveness)
    - rea (reach)
    - rxn (reaction time)
    - con (consistency)
    """
    def __init__(
        self, 
        firstnames_file,
        lastnames_file
    ):
        self.name_generator = NameGenerator(firstnames_file, lastnames_file)

    def generate(self, size=1):
        players = []
        for i in range(size):
            player = {}
            player['id'] = str(uuid.uuid4())
            player['name'] = self.name_generator.generate()[0]
            player['agg'] = random.randint(1,5)
            player['rea'] = random.randint(1,5)
            player['rxn'] = random.randint(1,5)
            player['con'] = random.randint(1,5)
            players.append(player)
        return players


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

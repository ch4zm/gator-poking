import json
import logging
import uuid
import random
import os
from .core import Team, Congregation, Player, Gator


HERE = os.path.abspath(os.path.dirname(__file__))
logger = logging.getLogger('gp')


###############################################################
# Base classes

class LeagueGeneratorBase(object):
    default_filename = None

    def write_file(self, league_map, working_dir, output_file):
        # if working_dir specified, write league_map to output_file
        if working_dir is not None:
            # default output filename
            if output_file is None:
                # make sure calling a derived class that defines default_filename
                if self.default_filename is None:
                    raise NotImplementedError("Error: do not use LeagueBase class")
                json_output_file = os.path.join(working_dir, self.default_filename)
            # dump
            with open(json_output_file, 'w') as f:
                json.dump(league_map, f, indent=4)
            return json_output_file
        return None


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
        data = self.data[:]
        random.shuffle(data)
        return data[:size]


#####################################
# Public classes

class LeagueGenerator(LeagueGeneratorBase):
    """
    Generate a league (a collection of teams in the form of a team id: team json map).
    Team JSON contains:
    - id
    - city
    - nickname
    - color
    """
    default_filename = 'league.json'

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

    def generate(self, working_dir=None, output_file=None, size=4):
        if working_dir is not None:
            if not os.path.isdir(working_dir):
                raise Exception(f"Error: provided working directory {working_dir} is not a directory")
        if size%4 != 0:
            raise Exception(f"Error: leagues must have a number of teams divisible by 4")

        # rearrange data into a map
        league_list = self.team_generator.generate(size = size)
        league_map = {}
        for team in league_list:
            league_map[team['id']] = team

        # write to json file, if working_dir is specified
        json_file = self.write_file(league_map, working_dir, output_file)

        # finally return the json to the user
        return league_map, json_file


class GatorLeagueGenerator(LeagueGeneratorBase):
    """
    Generate a gator league (a collection of congregations in the form of a congregation id: congregation json map).
    """
    default_filename = 'gatorleague.json'

    def __init__(
        self,
        gatorplaces_file = None,
        gatornicknames_file = None
    ):
        # Set default values for filenames
        if gatorplaces_file is None:
            gatorplaces_file = os.path.join(HERE, 'data', 'gatorplaces.txt')
        if gatornicknames_file is None:
            gatornicknames_file = os.path.join(HERE, 'data', 'gatornicknames.txt')
        self.cong_gen = CongregationGenerator(gatorplaces_file, gatornicknames_file)

    def generate(self, working_dir=None, output_file=None, size=2):
        if working_dir is not None:
            if not os.path.isdir(working_dir):
                raise Exception(f"Error: provided working directory {working_dir} is not a directory")
        if size%2 != 0:
            raise Exception(f"Error: gator leagues must have an even number of congregations")

        # rearrange data into a map
        gleague_list = self.cong_gen.generate(size = size)
        gleague_map = {}
        for cong in gleague_list:
            gleague_map[cong['id']] = cong

        # write to json file, if working_dir is specified
        json_file = self.write_file(gleague_map, working_dir, output_file)

        # finally return the json to the user
        return gleague_map, json_file


### class RosterGenerator(object):
###     """
###     Generate a roster (a collection of players in the form of a player id: player json map).
###     """
###     def __init__(
###         self,
###         firstnames_file = None,
###         lastnames_file = None
###     ):
###         if firstnames_file is None:
###             firstnames_file = os.path.join(HERE, 'firstnames.txt')
###         if lastnames_file is None:
###             lastnames_file = os.path.join(HERE, 'lastnames.txt')
###         self.player_generator = PlayerGenerator(firstnames_file, lastnames_file)
### 
###     def generate(self, size=1):
###         roster = {}
###         for i in range(size):
###             p = self.player_generator.generate()[0]
###             roster[p['id']] = p
###         return roster


###############################################################
# Generator classes for internal use

# -------------------------
# Teams/Congregations

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
            t = Team(
                id = str(uuid.uuid4()),
                city = city,
                nickname = nickname,
                color = color
            )
            teams.append(t.to_json())
        return teams


class CongregationGenerator(object):
    def __init__(
        self,
        gatorplaces_file,
        gatornicknames_file
    ):
        self.place_generator = BaseGenerator(gatorplaces_file)
        self.nick_generator = BaseGenerator(gatornicknames_file)

    def generate(self, size=1):
        places = self.place_generator.generate(size = size)
        nicks = self.nick_generator.generate(size = size)
        congregations = []
        for (p, n) in zip(places, nicks):
            c = Congregation(
                id = str(uuid.uuid4()),
                place = p,
                nickname = n
            )
            congregations.append(c.to_json())
        return congregations


# -------------------------
# Names

class GatorNameGenerator(object):
    """
    Generate names of gator types (not individual gators)
    """
    def __init__(
        self,
        gatorplaces_file = None,
        gatornicknames_file = None
    ):
        # Set default values for filenames
        if gatorplaces_file is None:
            gatorplaces_file = os.path.join(HERE, 'data', 'gatorplaces.txt')
        if gatornicknames_file is None:
            gatornicknames_file = os.path.join(HERE, 'data', 'gatornicknames.txt')

        # load place names
        with open(gatorplaces_file, 'r') as f:
            gatorplaces = f.readlines()
        self.gatorplaces = [j.strip() for j in gatorplaces]
        # load names
        with open(gatornicknames_file, 'r') as f:
            gatornicknames = f.readlines()
        self.gatornicknames = [j.strip() for j in gatornicknames]

    def generate(self, size=1):
        names = []
        for i in range(size):
            name = random.choice(self.gatorplaces) + ' ' + random.choice(self.gatornicknames)
            names.append(name)
        return names


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


# -------------------------
# Random players/gators

class RandomPlayer(object):
    def __new__(cls):
        ng = NameGenerator(firstnames_file, lastnames_file)
        name = ng.generate()
        p = Player(
            id = str(uuid.uuid4()),
            name = name,
            agg = random.randint(1,5),
            rea = random.randint(1,5),
            rxn = random.randint(1,5),
            con = random.randint(1,5)
        )
        return p


class RandomGator(Gator):
    """
    Generate a random ggator
    """
    def __new__(cls):
        gng = GatorNameGenerator(gatorplaces_file, gatornicknames_file)
        name = gng.generate()
        g = Gator(
            id = str(uuid.uuid4()),
            name = name,
            agg = random.randint(1,5),
            rea = random.randint(1,5),
            rxn = random.randint(1,5),
            con = random.randint(1,5)
        )
        return g


### class PlayerGenerator(object):
###     """
###     Generate a player JSON with help from NameGenerator.
###     Player JSON contains:
###     - id
###     - name
###     - agg (aggressiveness)
###     - rea (reach)
###     - rxn (reaction time)
###     - con (consistency)
###     """
###     def __init__(
###         self,
###         firstnames_file,
###         lastnames_file
###     ):
###         self.name_generator = NameGenerator(firstnames_file, lastnames_file)
###
###     def generate(self, size=1):
###         players = []
###         for i in range(size):
###             player = {}
###             player['id'] = str(uuid.uuid4())
###             player['name'] = self.name_generator.generate()[0]
###             player['agg'] = random.randint(1,5)
###             player['rea'] = random.randint(1,5)
###             player['rxn'] = random.randint(1,5)
###             player['con'] = random.randint(1,5)
###             players.append(player)
###         return players



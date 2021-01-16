import random
import os


HERE = os.path.abspath(os.path.dirname(__file__))


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
        if cities_file is None:
            cities_file = os.path.join(HERE, 'data', 'cities.txt')
        if nicknames_file is None:
            nicknames_file = os.path.join(HERE, 'data', 'teamnicknames.txt')
        if colors_file is None:
            colors_file = os.path.join(HERE, 'data', 'colors.txt')
        self.team_generator = TeamGenerator(cities_file, nicknames_file, colors_file)

    def generate(self, size = league_size):
        if league_size%2 != 0:
            raise Exception(f"Error: leagues must have an even number of teams")
        league = self.team_generator.generate(size = size)
        return league


class GatorLeagueGenerator(object):
    def __init__(
        self,
        gatortypes_file = None
    ):
        if gatortypes_file is None:
            gatortypes_file = os.path.join(HERE, 'data', 'gatortypes.txt')


def BaseGenerator(object):
    """
    Base class to load lines from plain text file into list
    """
    def __init__(self, data_file):
        # verify file exists
        if not os.path.exists(data_file):
            raise Exception(f"Error: specified data file {data_file} does not exist!")
        # load data
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
            t = Team({'city': city, 'nickname': nickname, 'color': color})
            teams.append(t.to_json())
        return teams


class RosterGenerator(object):
    """
    Populate a roster with Players (their JSONs)
    """
    def __init__(
        self,
        firstnames_file = None,
        lastnames_file = None
    ):
        self.player_generator = PlayerGenerator(firstnames_file, lastnames_file)

    def generate(self, size=1):
        roster = []
        for i in range(size):
            p = self.player_generator.generate()


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


class NameGenerator(object):
    """
    Generate first + last names.
    """
    def __init__(
        self, 
        firstname_data_file, 
        lastname_data_file
    ):
        if firstnames_file is None:
            firstnames_file = os.path.join(HERE, 'data', 'firstnames.txt')
        if lastnames_file is None:
            lastnames_file = os.path.join(HERE, 'data', 'lastnames.txt')
        # verify file exists
        for data_file in [firstname_data_file, lastname_data_file]:
            if not os.path.exists(data_file):
                raise Exception(f"Error: Could not find data file {data_file}")
        # load first names
        with open(firstname_data_file, 'r') as f:
            firstname_data = f.readlines()
        self.firstname_data = [j.strip() for j in firstname_data]
        # load last names
        with open(lastname_data_file, 'r') as f:
            lastname_data = f.readlines()
        self.lastname_data = [j.strip() for j in lastname_data]

    def generate(self, size=1):
        names = []
        for i in range(size):
            name = random.choice(self.firstname_data) + ' ' + random.choice(self.lastname_data)
            names.append(name)
        return names

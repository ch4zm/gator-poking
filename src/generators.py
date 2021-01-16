import os


class NameGenerator(object):
    def __init__(self, data_file):
        if not os.path.exists(data_file):
            raise Exception(f"Error: Could not find data file {data_file}")
        with open(data_file, 'r') as f:
            data = f.readlines()
        self.data = [j.strip() for j in data]

class LeagueGenerator(object):
    pass

class TeamGenerator(object):
    pass

class PlayerGenerator(object):
    pass

class GatorGenerator(object):
    pass


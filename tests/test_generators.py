import os
import unittest
from tempfile import TemporaryDirectory
from gator_poking.generators import (
    LeagueGenerator,
    GatorLeagueGenerator
)


HERE = os.path.split(os.path.abspath(__file__))[0]


class LeagueGeneratorTest(unittest.TestCase):
    def test_league_generator(self):
        with TemporaryDirectory() as wd:
            if not os.path.exists(wd):
                os.mkdir(wd)
            lg = LeagueGenerator()
            league, league_filename = lg.generate(working_dir=wd)
            self.assertTrue(os.path.exists(league_filename))
    
    def test_custom_league_generator(self):
        with TemporaryDirectory() as wd:
            if not os.path.exists(wd):
                os.mkdir(wd)
            cities_file = os.path.join(HERE, 'fixtures', 'wi_cities.txt')
            nicknames_file = os.path.join(HERE, 'fixtures', 'wi_nicknames.txt')
            lg = LeagueGenerator(
                cities_file = cities_file,
                nicknames_file = nicknames_file
            )
            league, league_filename = lg.generate(working_dir=wd)
            self.assertTrue(os.path.exists(league_filename))


class GatorLeagueGeneratorTest(unittest.TestCase):
    def test_gator_league_generator(self):
        with TemporaryDirectory() as wd:
            if not os.path.exists(wd):
                os.mkdir(wd)
            glg = GatorLeagueGenerator()
            gleague, gleague_filename = glg.generate(working_dir=wd)
            self.assertTrue(os.path.exists(gleague_filename))

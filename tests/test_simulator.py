import os
import unittest
from tempfile import TemporaryDirectory
from gator_poking.game import Game
from gator_poking.core import DefaultConfig, League, GatorLeague


HERE = os.path.split(os.path.abspath(__file__))[0]


class TestGame(unittest.TestCase):
    def test_one_game(self):
        with TemporaryDirectory() as wd:
            if not os.path.exists(wd):
                os.mkdir(wd)
            fixture_league = os.path.join(HERE, 'fixtures', 'fixture_league.json')
            lea = League(fixture_league)
            teams = lea.get_teams()

            fixture_league = os.path.join(HERE, 'fixtures', 'fixture_gatorleague.json')
            lea = GatorLeague(fixture_league)
            congs = lea.get_congregations()

            t1 = teams[0]
            t2 = teams[1]
            cong = congs[0]
            config = DefaultConfig()
            gp = Game(
                config = config,
                team1 = t1,
                team2 = t2,
                congregation = cong
            )

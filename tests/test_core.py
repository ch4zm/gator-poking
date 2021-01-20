import json
import os
import unittest
from .fixtures import TEAM_JSON, CONGREGATION_JSON
from gator_poking.core import (
    Config,
    DefaultConfig,
    League,
    GatorLeague,
    Team,
    Congregation
)


HERE = os.path.split(os.path.abspath(__file__))[0]


class CoreTest(unittest.TestCase):
    """
    Test gator_poking.core
    """
    def test_config(self):
        g = {
            "PLAYERS_PER_SIDE": 11,
            "OVERS_PER_INNING": 20,
            "PLAYS_PER_OVER": 6
        }
        c = Config(g)
        self.assertDictEqual(c, g)

        d = DefaultConfig()
        self.assertDictEqual(d, g)


class LeagueTest(unittest.TestCase):
    def test_league(self):
        fixture_league = os.path.join(HERE, 'fixtures', 'fixture_league.json')
        lea = League(fixture_league)
        teams = lea.get_teams()
        for team in teams:
            self.assertEqual(type(team), Team)


class GatorLeagueTest(unittest.TestCase):
    def test_gator_league(self):
        fixture_league = os.path.join(HERE, 'fixtures', 'fixture_gatorleague.json')
        lea = GatorLeague(fixture_league)
        congs = lea.get_congregations()
        for cong in congs:
            self.assertEqual(type(cong), Congregation)


class TeamTest(unittest.TestCase):
    def test_team(self):
        t = Team.from_json(TEAM_JSON)
        td = t.to_json()
        self.assertDictEqual(td, TEAM_JSON)
        name = TEAM_JSON['name']
        self.assertEqual(name, t.name)
        self.assertEqual(name, str(t))


class CongregationTest(unittest.TestCase):
    def test_congregations(self):
        c = Congregation.from_json(CONGREGATION_JSON)
        cd = c.to_json()
        self.assertDictEqual(cd, CONGREGATION_JSON)
        name = CONGREGATION_JSON['name']
        self.assertEqual(name, c.name)
        self.assertEqual(name, str(c))

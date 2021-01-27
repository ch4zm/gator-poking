import json
import os
import unittest
from .fixtures import TEAM1_JSON, TEAM2_JSON, CONGREGATION_JSON
from gator_poking.core import (
    Config,
    DefaultConfig,
    League,
    GatorLeague,
    Team,
    Congregation,
)
from gator_poking.errors import GatorPokingError


HERE = os.path.split(os.path.abspath(__file__))[0]


class CoreTest(unittest.TestCase):
    """
    Test gator_poking.core
    """

    def test_config(self):
        g = {"PLAYERS_PER_SIDE": 11, "OVERS_PER_INNING": 20, "PLAYS_PER_OVER": 6}
        c = Config(g)
        self.assertDictEqual(c, g)

        d = DefaultConfig()
        self.assertDictEqual(d, g)

    def test_invalid_config_keys(self):
        invalid = {"peanut": "butter", "jelly": "time"}
        with self.assertRaises(GatorPokingError):
            ic = Config(invalid)

    def test_invalid_config_values(self):
        invalid = {
            "PLAYERS_PER_SIDE": "invalid",
            "OVERS_PER_INNING": "invalid",
            "PLAYS_PER_OVER": "invalid",
        }
        with self.assertRaises(GatorPokingError):
            ic = Config(invalid)


class LeagueTest(unittest.TestCase):
    def test_league(self):
        fixture_league = os.path.join(HERE, "fixtures", "fixture_league.json")
        lea = League(fixture_league)
        teams = lea.get_teams()
        for team in teams:
            self.assertEqual(type(team), Team)


class GatorLeagueTest(unittest.TestCase):
    def test_gator_league(self):
        fixture_league = os.path.join(HERE, "fixtures", "fixture_gatorleague.json")
        lea = GatorLeague(fixture_league)
        congs = lea.get_congregations()
        for cong in congs:
            self.assertEqual(type(cong), Congregation)


class TeamTest(unittest.TestCase):
    def test_team(self):
        for TEAM_JSON in [TEAM1_JSON, TEAM2_JSON]:
            t = Team.from_json(TEAM_JSON)
            td = t.to_json()
            self.assertDictEqual(td, TEAM_JSON)
            name = TEAM_JSON["name"]
            self.assertEqual(name, t.name)
            self.assertEqual(name, str(t))

    def test_inconsistent_name_nick_city(self):
        INCONSISTENT = {
            "id": "c19197fa-2d84-47b2-8e51-1aecb5da6200",
            "name": "Jacksonville Jaguars",
            "nickname": "Mixing Bowls",
            "city ": "Orlando",
        }
        with self.assertRaises(GatorPokingError):
            it = Team.from_json(INCONSISTENT)


class CongregationTest(unittest.TestCase):
    def test_congregations(self):
        c = Congregation.from_json(CONGREGATION_JSON)
        cd = c.to_json()
        self.assertDictEqual(cd, CONGREGATION_JSON)
        name = CONGREGATION_JSON["name"]
        self.assertEqual(name, c.name)
        self.assertEqual(name, str(c))

    def test_inconsistent_name_nick_city(self):
        INCONSISTENT = {
            "id": "3d9be88f-5adc-4fa8-a335-9da09029c84e",
            "name": "Deepwater Snappers",
            "nickname": "Chompers",
            "place": "Everglades",
        }
        with self.assertRaises(GatorPokingError):
            ic = Congregation.from_json(INCONSISTENT)

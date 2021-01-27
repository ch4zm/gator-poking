import os
import unittest
from gator_poking.core import (
    Config,
    DefaultConfig,
    Team,
    Congregation
)
from gator_poking.states import (
    GameState,
    TeamState
)
from .fixtures import TEAM1_JSON, TEAM2_JSON, CONGREGATION_JSON


HERE = os.path.split(os.path.abspath(__file__))[0]


class StatesTest(unittest.TestCase):
    def test_team_state(self):
        for TEAM_JSON in [TEAM1_JSON, TEAM2_JSON]:
            team = Team.from_json(TEAM_JSON)
            state = TeamState(team)
            self.assertEqual(state.runs, 0)
            self.assertEqual(state.wickets, 0)
            self.assertEqual(state.done, False)
            self.assertEqual(state.eaten, False)

    def test_game_state(self):
        team1 = Team.from_json(TEAM1_JSON)
        team2 = Team.from_json(TEAM2_JSON)
        state1 = TeamState(team1)
        state2 = TeamState(team2)
        congregation = Congregation.from_json(CONGREGATION_JSON)

        # Test constructor with config
        gamestate = GameState(
            config = DefaultConfig(),
            team1 = team1,
            team2 = team2,
            state1 = state1,
            state2 = state2,
            congregation = congregation
        )

        # Test attributes
        self.assertEqual(team1.name, gamestate.team1.name)
        self.assertEqual(team2.name, gamestate.team2.name)
        self.assertEqual(congregation.name, gamestate.congregation.name)
        self.assertEqual(gamestate.state1.runs, 0)
        self.assertEqual(gamestate.state2.runs, 0)

        # Constructor without correct args should raise exceptions
        with self.assertRaises(Exception):
            # Missing config
            _ = GameState(
                team1 = team1,
                team2 = team2,
                state1 = state1,
                state2 = state2,
                congregation = congregation
            )

        with self.assertRaises(Exception):
            # Missing teams
            _ = GameState(
                config = DefaultConfig(),
                state1 = state1,
                state2 = state2,
                congregation = congregation
            )

        with self.assertRaises(Exception):
            # missing states
            _ = GameState(
                config = DefaultConfig(),
                team1 = team1,
                team2 = team2,
                congregation = congregation
            )

        # Test constructor with invalid config
        with self.assertRaises(Exception):
            gamestate_invalidconfig = GameState(
                config = {},
                team1 = team1,
                team2 = team2,
                state1 = state1,
                state2 = state2,
                congregation = congregation
            )

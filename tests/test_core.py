import os
import unittest
from gator_poking.core import (
    Config,
    DefaultConfig
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

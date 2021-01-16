import logging
import random

from .logsetup import *
from .inninggenerator import InningGenerator
from .states import GameState, TeamState
from .core import Config, Team, Congregation


logger = logging.getLogger('gp')


class Game(object):
    """
    Represents a game.
    This manages each inning, and hands off details
    of each over to the over generator.
    """
    def __init__(self, config, redteam, blueteam, congregation):

        logger.warning("\n\n")
        logger.warning("---------------------- STARTING GAME -------------------------")
        logger.warning("WARNING level: on")
        logger.info("INFO level: on")
        logger.debug("DEBUG level: on")
        logger.warning("\n\n")

        self.config = config

        # Start with a coin flip to determine who goes first
        if random.random() < 0.50:
            team1 = redteam
            team2 = blueteam
        else:
            team1 = blueteam
            team2 = redteam

        state1 = TeamState(team1)
        state2 = TeamState(team1)

        self.state = GameState(config, team1, team2, state1, state2, congregation)

    def simulate(self):
        """
        Simulate a single game
        """

        logger.warning('\n\n')
        logger.warning('====================================')
        logger.warning('============ TOP INNING ============')
        logger.warning('====================================')
        t1_w, t1_r = InningGenerator.generate_half(self.config, self.state, True)

        logger.warning('\n\n')
        logger.warning('====================================')
        logger.warning('============ BOT INNING ============')
        logger.warning('====================================')
        t2_w, t2_r = InningGenerator.generate_half(self.config, self.state, False)

        logger.warning('\n\n')
        logger.warning('====================================')
        logger.warning('=========== GAME SUMMARY ===========')
        logger.warning('====================================')
        state = self.state
        logger.info(f"{state.team1.name:>35}: {state.state1.wickets}{'*' if state.state1.eaten else ''} / {state.state1.runs} - {len(t1_r)}.{len(t1_r[-1])}")
        logger.info(f"{state.team2.name:>35}: {state.state2.wickets}{'*' if state.state2.eaten else ''} / {state.state2.runs} - {len(t2_r)}.{len(t2_r[-1])}")


class GameSimulator(object):

    def simulate(self):

        logger.warning("\n\n")
        logger.warning("---------------------- STARTING SIMULATOR -------------------------")
        logger.warning("logger warning level: on")
        logger.info("logger info level: on")
        logger.debug("logger debug level: on")
        logger.warning("\n\n")

        config_dict = dict(
            PLAYERS_PER_SIDE = 11,
            OVERS_PER_INNING = 20,
            PLAYS_PER_OVER = 6,
        )
        config = Config(config_dict)

        #t1 = Team("Jacksonville Wet Bandits")
        #t2 = Team("Palm Beach Pazookies")
        t1 = Team("St. Petersburg Paradoxes", size=config['PLAYERS_PER_SIDE'])
        t2 = Team("Tallahassee Rasslers", size=config['PLAYERS_PER_SIDE'])
        congregation = Congregation("Everglades Glories")

        self.game = Game(config, t1, t2, congregation)
        self.game.simulate()

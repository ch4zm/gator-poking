import logging
import numpy as np
from .betaroll import BetaRoll


logger = logging.getLogger('gp')


# Magic Numbers
#
# Construct the scale that maps stars to expected roll outcomes
PLAYER_ATTR_MIN = 0.4
PLAYER_ATTR_MAX = 0.8

GATOR_ATTR_MIN = 0.3
GATOR_ATTR_MAX = 0.6

# Construct the scale that maps consistency to log(alpha)
PLAYER_LOGALPHA_MIN = -0.4
PLAYER_LOGALPHA_MAX = 0.4

GATOR_LOGALPHA_MIN = -0.4
GATOR_LOGALPHA_MAX = 0.4

# Map margins of victory (in attribute rolls) to outcomes
PLAYER_SIX_LIMIT = 0.66  # Margin of victory must be greater than this to get 6 runs
PLAYER_FOUR_LIMIT = 0.33
PLAYER_ONE_LIMIT = 0.05

GATOR_EAT_LIMIT = 0.66
GATOR_LIMB_LIMIT = 0.33
GATOR_FINGER_LIMIT = 0.05


class OutcomeRoll(BetaRoll):
    """
    Use beta function parameters and magic numbers to come up with an outcome for a given play.
    """

    @classmethod
    def attr_roll(cls, attr_lab, player, gator):
        """
        Use player/gator attributes to construct a beta function, and sample it randomly.
        Return the player and gator rolls (bounded between 0-1 inclusive).
        """
        nstars = 5

        # Map star ratings to new spaces
        # Expected outcome
        player_attr_min = PLAYER_ATTR_MIN
        player_attr_max = PLAYER_ATTR_MAX
        player_attr_space = np.linspace(player_attr_min, player_attr_max, nstars)
        # Consistency (alpha param of beta distribution)
        player_con_space = np.logspace(PLAYER_LOGALPHA_MIN, PLAYER_LOGALPHA_MAX, nstars)

        # Expected outcome
        gator_attr_min = GATOR_ATTR_MIN
        gator_attr_max = GATOR_ATTR_MAX
        gator_attr_space = np.linspace(gator_attr_min, gator_attr_max, nstars)
        # Consistency
        gator_con_space = np.logspace(GATOR_LOGALPHA_MIN, GATOR_LOGALPHA_MAX, nstars)

        # Get attribute
        pa = player.attr[attr_lab]
        ga = gator.attr[attr_lab]

        # Get consistency
        pc = player.attr['con']
        gc = gator.attr['con']

        # Transform to get beta function parameters (expectation E, alpha)
        p_E = player_attr_space[pa-1]
        g_E = gator_attr_space[ga-1]
        p_alpha = player_con_space[pc-1]
        g_alpha = gator_con_space[gc-1]

        _, p_outcome = cls.random_sample_beta_inv_cdf(p_E, p_alpha)
        _, g_outcome = cls.random_sample_beta_inv_cdf(g_E, g_alpha)

        return (p_outcome, g_outcome)

    @classmethod
    def outcome_roll(cls, player, gator, context=None):
        """
        Generate an outcome for a given play, given a player and a gator.
        This runs all the necessary attribute rolls and uses those to determine the outcome.
        """
        # First roll requires gator or player wins both aggressiveness and reach rolls
        agg = cls.attr_roll('agg', player, gator)
        rea = cls.attr_roll('rea', player, gator)
        rxn = cls.attr_roll('rxn', player, gator)

        agg_diff = agg[0] - agg[1]
        rea_diff = rea[0] - rea[1]
        rxn_diff = rxn[0] - rxn[1]

        if context:
            prefix = f"{context}: "
        else:
            prefix = ""

        if agg_diff > 0 and rea_diff > 0:
            # Player won
            if rxn_diff < 0:
                # Player won but gator got reversal
                logger.debug(prefix + f"Player was about to poke but flinched!")
                return 0
            else:
                # Outcome: runs
                if rxn_diff > PLAYER_SIX_LIMIT:
                    logger.debug(prefix + f"Gator got slapped! The gator retreats into the water... anther gator takes its place.")
                    return 6
                elif rxn_diff > 0.33:
                    logger.debug(prefix + f"Gator got booped in the snoot!")
                    return 4
                elif rxn_diff > 0.05:
                    logger.debug(prefix + f"Gator got poked!")
                    return 1
                else:
                    logger.debug(prefix + f"Player poked wildly, missing the gator!")
                    return 0

        elif agg_diff < 0 and rea_diff < 0:
            # Gator won
            if rxn_diff > 0:
                # Gator won but player got reversal
                logger.debug(prefix + f"Gator was about to chomp but flinched!")
                return 0
            else:
                # Outcome: wickets
                if abs(rxn_diff) > GATOR_EAT_LIMIT:
                    logger.debug(prefix + f"Player was eaten by gator! A new player takes their place. Wicket.")
                    return -3
                elif abs(rxn_diff) > GATOR_LIMB_LIMIT:
                    logger.debug(prefix + f"Player limb chomped by gator! Wicket.")
                    return -2
                elif abs(rxn_diff) > GATOR_FINGER_LIMIT:
                    logger.debug(prefix + f"Player finger chomped by gator! Wicket.")
                    return -1
                else:
                    logger.debug(prefix + f"Gator chomped but narrowly missed! Wicket.")
                    return 0
        else:
            logger.debug(prefix + f"The gator retreated back into the water.")
            return 0

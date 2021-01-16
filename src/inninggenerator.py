import logging

from .outcomeroll import OutcomeRoll


logger = logging.getLogger('gp')


class InningGenerator(object):
    """
    Provides a static method to generate one half-inning.
    """

    @classmethod
    def generate_half(cls, config, state, top):

        congregation = state.congregation

        # Set team orders
        if top:
            batting_team  = state.team1
            batting_state = state.state1

            bowling_team  = state.team2
            bowling_state = state.state2

        else:
            batting_team  = state.team2
            batting_state = state.state2

            bowling_team  = state.team1
            bowling_state = state.state1

        # Initialize team state for top of inning
        batting_state.inning_start()

        # These are the quantities we will ultimately return:
        # a list of lists, one list per over, one element per play
        final_runs = []
        final_wickets = []

        team_name = batting_team.name

        opi = config['OVERS_PER_INNING']
        ppo = config['PLAYS_PER_OVER']
        gator = congregation.get_next_gator()
        for iover in range(opi):
            this_over = []
            this_wickets = []
            for iplay in range(ppo):

                context = f"{iover+1}.{iplay+1}"
                outcome = OutcomeRoll.outcome_roll(batting_state.pokers[0], gator, context)

                # Increment runs/wickets and update pokers
                if outcome > 0:
                    # Outcome is runs for the player
                    batting_state.runs += outcome
                    this_over.append(outcome)
                    this_wickets.append(0)
                    if outcome%2 == 1:
                        # Pokers swap positions
                        batting_state.pokers = batting_state.pokers[::-1]
                    if outcome == 6:
                        # Gator got slapped
                        gator = congregation.get_next_gator()

                elif outcome < 0:
                    # Outcome is wickets
                    batting_state.wickets += 1
                    this_over.append(0)
                    this_wickets.append(1)
                    # If we have reached maximum number of wickets, this will be None, check happens below
                    batting_state.pokers[0] = batting_team.get_next_player()

                else:
                    # Nothing happens
                    this_over.append(0)
                    this_wickets.append(0)

                # Determine if the side should end
                if cls.check_runs_end_over(config, batting_state, bowling_state, top):
                    logger.warning(f"{team_name}: Over {iover+1}: Game ends due to {team_name} getting required runs!")
                    batting_state.done = True

                if cls.check_wickets_end_over(config, batting_state, bowling_state, top):
                    logger.warning(f"{team_name}: Over {iover+1}: Inning ends due to {team_name} getting maximum wickets!")
                    batting_state.done = True

                if batting_state.done:
                    break

            final_wickets.append(this_wickets)
            final_runs.append(this_over)

            logger.info("---------------")
            logger.info(f"{team_name}: This Over ({iover+1}): {sum(this_wickets)} / {'  '.join([str(z) if z>=0 else 'W' for z in this_over])}")
            logger.info(f"{team_name}: Cumulative: {batting_state.wickets} / {batting_state.runs} - {iover+1}")
            logger.info(f"--------------")

            if batting_state.done:
                break

        batting_state.done = True

        return final_wickets, final_runs

    @classmethod
    def check_runs_end_over(cls, config, batting_state, bowling_state, top):
        if not top and batting_state.runs > bowling_state.runs:
            return True
        return False

    @classmethod
    def check_wickets_end_over(cls, config, batting_state, bowling_state, top):
        pps = config['PLAYERS_PER_SIDE']
        if batting_state.wickets >= (pps - 1):
            return True
        return False


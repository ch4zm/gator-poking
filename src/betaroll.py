from scipy.stats import beta
import random


class BetaRoll(object):
    """
    Static class that provides a way to sample a beta function
    with a given expectation E and a given alpha parameter a.

    The larger the value of a, the more closely grouped the distribution
    will be around the expected value.
    """

    @classmethod
    def random_sample_beta_inv_cdf(cls, E, a):
        """
        Sample a beta inverse CDF with expectation E and alpha param a.
        The values of E and alpha will fix the value of beta.
        """
        y_in = random.random()
        b = a * (1.0/E - 1.0)
        # Use the percent point function - inverse CDF
        x_out = beta.ppf(y_in, a, b)
        x = y_in # This is the input random number, uniform between 0-1
        y = x_out # This is the output weighted random number
        return (x, y)

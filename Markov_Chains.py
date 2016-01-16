import markovify

"""
Handles all aspects of the Markov chains. Training from data, generating new posts from chains.
"""


def train_markov(old_chains, messages):
    """
    Trains the Markov chains with data and saves to DB.
    :param old_chains: A dictionary object with the Markov chains for each bot.
    :param messages: A dictionary object with the user ID as the key and the message as the value.
    :return: void
    """
    new_chains = old_chains
    # Parse training data here
    return new_chains


def generate_post(old_chains):
    """
    Generates a message for a random user based on chains in DB.
    :param old_chains: A dictionary object with the Markov chains for each bot.
    :return: A tuple containing the id of the bot and the message it is to send.
    """
    # TODO: Add grammar checking using language-check module at https://pypi.python.org/pypi/language-check
    # Generate post from chain here
    bot_id = None
    message = ""
    return bot_id, message

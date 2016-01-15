import markovify

"""
Handles all aspects of the Markov chains. Training from data, generating new posts from chains,
and all interaction with the database.
"""


def train_markov(messages):
    """
    Trains the Markov chains with data and saves to DB.
    :param messages: A dictionary object with the user ID as the key and the message as the value.
    :return: void
    """
    # TODO: Add grammar checking using language-check module at https://pypi.python.org/pypi/language-check
    pass


def generate_post():
    """
    Generates a message for a random user based on chains in DB.
    :return: A tuple containing the id of the bot and the message it is to send.
    """
    pass

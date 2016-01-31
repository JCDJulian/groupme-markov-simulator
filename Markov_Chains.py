import markovify
import random
"""
Handles all aspects of the Markov chains. Training from data, generating new posts from chains.
"""


def train_markov(user_names):
    """
    Builds a dictionary of Markov text models from the text corpus of each user.
    :param user_names: A list of the users' names to build. Assumes there is a corresponding "user.txt" corpus available
    :return: text_models - a dictionary of users and their Markovify text models
    """
    text_models = dict()
    for user in user_names:
        file_name = user + ".txt"
        with open(file_name) as f:
            text = f.read()
        text_model = markovify.Text(text)
        text_models[user] = text_model

    return text_models


def generate_post(text_models):
    """
    Generates a message for a random user based on chains
    :param old_chains: A list object with the Markov chains for each bot.
    :return: A tuple containing the id of the bot and the message it is to send.
    """
    # TODO: Add grammar checking using language-check module at https://pypi.python.org/pypi/language-check
    # Generate post from chain here
    # Select random chain
    rand_user = random.sample(text_models, 1)
    rand_model = text_models[rand_user]

    message = rand_model.make_short_sentence(150, max_overlap_ratio=.9)

    # TODO: Get corrseponding bot id for user
    bot_id = None

    return bot_id, message

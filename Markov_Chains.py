import markovify
import random
"""
Handles all aspects of the Markov chains. Training from data, generating new posts from chains.
"""


def generate_markov_models(user_names):
    """
    Builds a dictionary of user_name :: Markov text models from the text corpus of each user.
    :param user_names: A list of the users' names to build. Assumes there is a corresponding "user.txt" corpus available
    :return: text_models - a dictionary of users and their Markovify text models
    """
    text_models = dict()
    for user in user_names:
        file_name = user + ".txt"
        with open(file_name) as f:
            text = f.read()
        text_model = markovify.Text(text, state_size=2)
        text_models[user] = text_model

    return text_models


def generate_post(text_models):
    """
    Generates a message for a random user based on chains
    :param text_models: A dict object with a paring of user names and Markov models.
    :return: A tuple containing the name of the user being simulated and the message it is to send.
    """
    # TODO: Add grammar checking using language-check module at https://pypi.python.org/pypi/language-check
    # TODO: Known error: Markovify can break down if the corpus isn't long enough. But if I filter out short corpus-
    # producing users, Markovify might later try to generate a chain out of a nonexisting text file and error.

    # Generate post from chain here
    # Select random chain and markov model
    rand_user = random.sample(text_models.keys(), 2)[0]
    rand_model = text_models[rand_user]

    # Generate random message
    print("Generating random message...")
    message = None
    while message is None:
        message = rand_model.make_short_sentence(125, max_overlap_ratio=0.5, max_overlap_total=10)
    print("Message generated: ", message)

    return rand_user, message

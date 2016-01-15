import requests


def setup(self, key):
    """
    Creates a new group chat, initializes new bot versions of each participant in the original chat,
    and trains them initially with all the messages from the past month.
    :param key: The ID of the group chat to be replicated.
    :return: void
    """

def get_weekly_messages():
    """
    Sends GET request to Groupme to retrieve all messages from past week. Passes it off to Markovify to train.
    :return: messages - a list of messages to be consumed by the Markov chain
    """
    pass

def create_post(post):
    """
    Sends a post from the Markov chain to the GroupmeAPI
    :return: void
    """
    pass
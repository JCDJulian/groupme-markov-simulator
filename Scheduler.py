import GroupmeApiHandler
import Markov_Chains


"""
Scheduler handles the frequency of posts and training for the simulator.
It coordinates all communication between the API and Markov_Chain modules.
This is the script directly run on the server to accomplish the required task.
"""


def setup_wizard():
    """
    Set-up wizard to prompt for user information to setup simulation.
    :return:
    """
    pass


def train_markov():
    """
    Sends GET request to Groupme to retrieve all messages from past week. Passes it off to Markovify to train.
    :return: messages - a list of messages to be consumed by the Markov chain
    """
    messages = GroupmeApiHandler.get_weekly_messages()
    Markov_Chains.train_markov(messages)
    pass


def create_post():
    """
    Sends a post from the Markov chain to the GroupmeAPI
    :return: void
    """
    post = Markov_Chains.generate_post()
    GroupmeApiHandler.create_post(post)
    pass

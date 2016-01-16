import GroupmeApiHandler
import Markov_Chains
import sys


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


def parse_settings():
    """
    Read in and parse settings JSON object from DB
    :return: settings dictionary
    """
    pass

if __name__ == "__main__":
    # Read in sys input to determine which command to execute
    command = sys.argv[0]
    if command == "train":
        train_markov()
    elif command == "create_post":
        create_post()
    elif command == "init":
        setup_wizard()
    else:
        print("Welcome to MarkovMe. Version 1.0. \n\n"
              "Run Scheduler.py <command> where \n"
              "Possible commands are: \n"
              "init - run set-up wizard for new chain \n"
              "train - query the GroupMe for the week's training data \n"
              "create_post - generate a new Markov post and send to GroupMe \n")

import GroupmeApiHandler
import Markov_Chains
import sys
import DatabaseHandler
import json

"""
Scheduler handles the frequency of posts and training for the simulator.
It coordinates all communication between the API, DatabaseHandler, and Markov_Chain modules.
This is the script directly run on the server to accomplish the required task.
"""


def setup_wizard():
    """
    Set-up wizard to prompt for user information to setup simulation.
    :return:
    """
    print("Welcome to MarkovMe, Version 1.0. \n"
          "First we need to establish a connection to a Mongo database. \n")

    host = input("Please enter the host name: ")
    port = input("Now enter the port number of your database: ")

    db_config = {
      "system": "mongodb",
      "host": host,
      "port": str(port)
    }

    # Write to JSON file
    with open('db_config.json', 'w') as f:
        json.dumps(db_config, f)

    db = DatabaseHandler.DatabaseHandler()

    print("Now we need to connect to the GroupMe you want to simulate \n")
    # TODO: Save GroupMe settings to DB

    pass


def train_markov(db_connection):
    """
    Sends GET request to Groupme to retrieve all messages from past week. Passes it off to Markovify to train.
    :param db_connection: A DatabaseHandler object that allows interfacing w/ MongoDB
    :return: messages - a list of messages to be consumed by the Markov chain
    """
    messages = GroupmeApiHandler.get_weekly_messages()
    old_chains = db_connection.get_markov_chains()
    new_chains = Markov_Chains.train_markov(old_chains, messages)
    db_connection.update_markov_chains(new_chains)
    pass


def create_post(db_connection):
    """
    Sends a post from the Markov chain to the GroupmeAPI
    :param db_connection: A DatabaseHandler object that allows interfacing w/ MongoDB
    :return: void
    """
    old_chains = db_connection.get_markov_chains()
    (bot_id, message) = Markov_Chains.generate_post(old_chains)
    GroupmeApiHandler.create_post(bot_id, message)
    pass


def parse_settings(db_connection):
    """
    Read in and parse settings JSON object from DB
    :param db_connection: A DatabaseHandler object that allows interfacing w/ MongoDB
    :return: settings dictionary
    """
    pass

if __name__ == "__main__":
    # Read in sys input to determine which command to execute
    command = sys.argv[0]

    if command == "train":
        db = DatabaseHandler.DatabaseHandler()
        train_markov(db)
    elif command == "create_post":
        db = DatabaseHandler.DatabaseHandler()
        create_post(db)
    elif command == "init":
        setup_wizard()
    else:
        print("Welcome to MarkovMe, Version 1.0. \n\n"
              "Run Scheduler.py <command> where \n"
              "Possible commands are: \n"
              "init - run set-up wizard for new chain \n"
              "train - query the GroupMe for the week's training data \n"
              "create_post - generate a new Markov post and send to GroupMe \n")

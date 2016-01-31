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
    print("Welcome to MarkovMe, Version 1.0. \n")

    print("Downloading data from your GroupMe \n")
    messages = GroupmeApiHandler.get_all_available_messages()

    # Write all messages into separate text files
    file_names, user_names = write_messages(messages)

    # Create group
    GroupmeApiHandler.setup(user_names)


def create_post(db_connection):
    """
    Sends a post from the Markov chain to the GroupmeAPI
    :param db_connection: A DatabaseHandler object that allows interfacing w/ MongoDB
    :return: void
    """
    messages = GroupmeApiHandler.get_weekly_messages()
    file_names, user_names = update_messages(messages)
    (bot_id, message) = Markov_Chains.generate_post(file_names, user_names)
    GroupmeApiHandler.create_post(bot_id, message)
    pass


def write_messages(messages):
    """
    Takes Groupy filtered list of Messages, writes them to a .txt file for each user
    and then returns a list of filenames
    :param messages: A Groupy FilteredList of Messages
    :return: file_names - a list of file names; user_names - a list of user names
    """
    corpus_strings = dict()
    for message in messages:
        if message.text is not None:
            if message.name in corpus_strings:
                corpus_strings[message.name] += (message.text + " ")
            else:
                corpus_strings[message.name] = (message.text + " ")

    file_names = list()
    user_names = list()
    for name in corpus_strings:
        file_name = name + ".txt"
        user_names.append(name)
        file_names.append(file_name)
        with open(file_name, "w") as text_file:
            text_file.write(corpus_strings[name])
            text_file.close()

    return file_names, user_names


def update_messages(messages):
    """
    Takes Groupy filtered list of Messages, updates the .txt file for each user
    and then returns a list of filenames
    :param messages: A Groupy FilteredList of Messages
    :return: file_names - a list of file names; user_names - a list of user names
    """
    corpus_strings = dict()
    for message in messages:
        if message.text is not None:
            if message.name in corpus_strings:
                corpus_strings[message.name] += (message.text + " ")
            else:
                corpus_strings[message.name] = (message.text + " ")

    # TODO: Check if any new users have joined chat
    file_names = list()
    user_names = list()
    for name in corpus_strings:
        file_name = name + ".txt"
        user_names.append(name)
        file_names.append(file_name)
        with open(file_name, "a") as text_file:
            text_file.write(corpus_strings[name])
            text_file.close()
    return file_names, user_names

if __name__ == "__main__":
    # Read in sys input to determine which command to execute
    command = sys.argv[0]

    if command == "create_post":
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

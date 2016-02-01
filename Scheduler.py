import GroupmeApiHandler
import Markov_Chains
import sys


"""
Scheduler handles the frequency of posts and training for the simulator.
It coordinates all communication between the API, DatabaseHandler, and Markov_Chain modules.
This is the script directly run on the server to accomplish the required task.
"""


def setup_wizard():
    """
    Set-up wizard to prompt for user information to setup simulation and create a few test posts.
    :return:
    """
    print("Welcome to MarkovMe, Version 1.0. \n")
    print("Please make sure that you have set up your .groupy.key file. For more information, see the Groupy API: \n"
          "http://groupy.readthedocs.org/en/master/pages/installation.html#prerequisites")

    print("Querying for your groups...")
    groups = GroupmeApiHandler.get_groups()
    print("Found the following groups:\n")
    for group in groups:
        print(group, "\n")

    old_group = None
    while old_group is None:
        original_group_name = input("Please type the name of the group you would like to simulate: ")
        old_group = GroupmeApiHandler.get_group(original_group_name)
        if old_group is None:
            print("Error. No groups found containing this string. Try again.")

    print("Downloading data from your GroupMe \n")
    messages = GroupmeApiHandler.get_all_available_messages(old_group)

    # Write all messages into separate text files
    file_names, user_names = write_messages(messages)

    # Create group
    GroupmeApiHandler.setup(old_group, user_names)

    # Create some test posts to get started.
    create_posts(user_names)


def create_posts(user_names):
    """
    Calls on Markov Chains to generate a post and send it to the simulator group.
    TODO: Fix Known issue: The create_post method identifies the correct bot by finding the bot
    whose name is "user_name Bot". If the user is running multiple simulations with the same user name
    in multiple simulations, this could potentially cause the wrong bot to post.
    :param user_names: A list of user names corresponding to the group. Each user name should alraedy have
    a corresponding user_name.txt file generated from the API the Markove chain will read from.
    :return: void
    """
    models = Markov_Chains.generate_markov_models(user_names)
    for x in range(5):
        (user_name, message) = Markov_Chains.generate_post(models)
        GroupmeApiHandler.create_post(user_name, message)


def write_messages(messages):
    """
    Takes Groupy filtered list of Messages, writes them to a .txt file for each user
    and then returns a list of filenames
    :param messages: A Groupy FilteredList of Messages
    :return: file_names - a list of file names;
    :return: user_names - a list of user names
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
    :return: file_names - a list of file names
    :return: user_names - a list of user names
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
    command = sys.argv[1]

    if command == "create_post":
        print("Querying for your groups...")
        groups = GroupmeApiHandler.get_group_contains("Simulator")
        print("Found the following simulator groups:\n")
        for group in groups:
            print(group, "\n")

        original_group = None
        while original_group is None:
            sim_name = input("Please type the name of the simulation you would like to run: ")
            original_name = sim_name.replace(" Simulator", "")
            original_group = GroupmeApiHandler.get_group(original_name)
            if original_group is None:
                print("Error. No groups found containing this string. Try again.")
        print("Getting users...")
        user_names = GroupmeApiHandler.get_user_names(original_group)
        print("Creating posts...")
        create_posts(user_names)
    # TODO: Allow command to train the simulator by getting the last week's messages
    elif command == "init":
        setup_wizard()
    else:
        print("Welcome to MarkovMe, Version 1.0. \n\n"
              "Run Scheduler.py <command> where \n"
              "Possible commands are: \n"
              "init - run set-up wizard for new chain \n"
              "train - query the GroupMe for the week's training data \n"
              "create_post - generate a new Markov post and send to GroupMe \n")

import groupy
import time
import datetime

"""
Handles all API calls to GroupMe using groupy API wrapper.
"""


def setup(old_group, member_names):
    """
    Creates a new group chat, initializes new bot versions of each participant in the original chat.
    :param member_names: the list of the names of the members to be simulated
    :param old_group: the group to be simulated
    :return: new_group: the groupy object of the new group
    """
    new_group_name = old_group.name + " Simulator"
    # Create simulator group
    new_group = groupy.Group.create(new_group_name, description="A Markov chain simulation created with MarkovMe.", share=True)
    print("The new share URL for this group is ", new_group.share_url)
    # For each user in training group, create a bot in simulator group
    for member in member_names:
        bot_name = member + " Bot"
        groupy.Bot.create(name=bot_name, group=new_group)

    return new_group


def get_groups():
    """
    :return: List of all groups for current user
    """
    return groupy.Group.list()


def get_group(group_name):
    """
    :param group_name: Name of group the query for
    :return: Groupy group with matching name
    """
    return groupy.Group.list().filter(name__eq=group_name).first


def get_weekly_messages():
    """
    Sends GET request to Groupme to retrieve all messages from past week. Passes it off to Markovify to train.
    :return: messages - a FilteredList of this week's messages
    """

    # Get the POSIX timestamp for one week ago.
    one_week_ago = time.time() - 604800
    one_week_ago_datetime = datetime.datetime.fromtimestamp(one_week_ago)

    group = groupy.Group.list().first
    messages = group.messages()

    EOF = False
    # Keep getting pages of 100 messages until the last message in that page is older than a week
    while messages.first.created_at > one_week_ago or not EOF:
        try:
            messages.iolder()
        except ValueError:
            EOF = True
            print("No more messages")
            break

    # Then run a filter to only have messages with a timestamp in the past week and returnGr
    this_weeks_messages = messages.filter(created__ge=one_week_ago_datetime)

    return this_weeks_messages


def get_all_available_messages(group):
    """
    Sends GET request to Groupme to retrieve all messages available.
    :return: messages - a FilteredList of all GroupMe messages
    """

    messages = group.messages()

    EOF = False
    counter = 0
    # Keep getting pages of 100 messages until end
    while not EOF or counter < 100:
        try:
            messages.iolder()
            counter += 1
            print("Messages received")
        except TypeError:
            EOF = True
            print("No more messages")
            break

    return messages


def get_user_names(group):
    """
    Extracts Python list of user names from a Groupy group
    :param group: Groupy group to extract names from
    :return: List of user names
    """
    users = group.members.list()
    user_names = list()
    for user in users:
        user_names.append(user.name)

    return user_names


def create_post(user_name, message):
    """
    Lets corresponding bot post a message.
    :param user_name: The name of the user being simulated whose bot is posting the message.
    :param message: The message to be posted.
    :return:
    """

    # Find bot with matching user_name
    posting_bot = groupy.Bot.list().filter(name__contains=user_name).first
    if posting_bot is None:
        print("Error. Could not find a bot matching that name to create post.")
    else:
        posting_bot.post(message)
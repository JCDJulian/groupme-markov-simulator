import requests
import groupy
import time
import datetime


def setup(key):
    """
    Creates a new group chat, initializes new bot versions of each participant in the original chat,
    and trains them initially with all the messages from the past month.
    :param key: The ID of the group chat to be replicated.
    :return: void
    """


def get_weekly_messages(settings):
    """
    Sends GET request to Groupme to retrieve all messages from past week. Passes it off to Markovify to train.
    :return: messages - a FilteredList of this week's messages
    """

    # Get the POSIX timestamp for one week ago.
    one_week_ago = time.time() - 604800
    one_week_ago_datetime = datetime.datetime.fromtimestamp(one_week_ago)

    group = groupy.Group.list().first
    messages = group.messages()

    # Keep getting pages of 100 messages until the last message in that page is older than a week
    while messages.iolder() and messages.last.created_at > one_week_ago:
        pass

    # Then run a filter to only have messages with a timestamp in the past week and return
    this_weeks_messages = messages.filter(created__ge=one_week_ago_datetime)

    return this_weeks_messages


def create_post(post):
    """
    Sends a post from the Markov chain to the GroupmeAPI
    :return: void
    """
    pass
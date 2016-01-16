import groupy
import time
import datetime


def setup(new_group_name, old_group):
    """
    Creates a new group chat, initializes new bot versions of each participant in the original chat,
    and trains them initially with all the messages from the past month.
    :param new_group_name: string to name the new group
    :param old_group: the Groupy list to be replicated
    :return: void
    """

    # Create simulator group
    new_group = groupy.Group.create(new_group_name, description="A Markov chain simulation created with MarkovMe.")
    print("The new share URL for this group is ", new_group.share_url)
    # For each user in training group, create a bot in simulator group
    original_members = old_group.members()
    for member in original_members:
        bot_name = member.identification()['nickname'] + " Bot"
        groupy.Bot.create(bot_name, new_group)


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

    # Keep getting pages of 100 messages until the last message in that page is older than a week
    while messages.iolder() and messages.last.created_at > one_week_ago:
        pass

    # Then run a filter to only have messages with a timestamp in the past week and returnGr
    this_weeks_messages = messages.filter(created__ge=one_week_ago_datetime)

    return this_weeks_messages


def create_post(bot_id, message):
    """
    Sends a post from the Markov chain to the GroupmeAPI
    :param bot_id: The id of the bot that will make the post.
    :param message: The message to be posted.
    :return: void
    """

    # Find bot with matching bot_id
    bots = groupy.Bot.list()
    posting_bot = None
    for bot in bots:
        if bot.bot_id == bot_id:
            posting_bot = bot

    posting_bot.post(message)
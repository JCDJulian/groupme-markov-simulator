import pymongo
import json
import sys

"""
Handles all queries and connections to database.
"""


class DatabaseHandler:

    def __init__(self):
        """
        Instantiates connection to MongoDB
        :return: void
        """
        # Parse JSON from db_config.json
        with open('db_config.json') as data_file:
            data = json.load(data_file)

        host = data["host"]
        port = int(data["port"])

        try:
            self.client = pymongo.MongoClient(host, port)
            self.db = self.client.MarkovMe
        except:
            print("Error. Failed to access database.")
            sys.exit()

    def get_settings(self):
        """
        Returns settings dictionary from database
        :return: Dictionary of settings.
        """
        cursor = self.db.settings.find()
        for document in cursor:
            settings = document

        return settings

    def update_settings(self):
        """
        Updates GroupMe settings in DB.
        :return: void
        """
        pass

    def get_markov_chains(self):
        """
        Returns list of Markov chains for each bot from DB
        :return: list of Markov chains for each bot
        """
        pass

    def update_markov_chains(self, chains):
        """
        Updates the list of Markov chains in DB after training session
        :param chains: list of updated Markov chains
        :return: void
        """
        pass
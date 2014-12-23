import shelve
from pymongo import MongoClient
import pickle
import os
import datetime
global db

class Database():

    db = None

    def __init__(self, username, password):
        self.db = self.initialize_db_conn(username, password)

    def initialize_db_conn(self, username, password):

        """
        Connect to the MongoDB server and save connection
        :return:
        """

        DB_NAME = "filter_site"

        client = MongoClient('mongodb://{0}:{1}@ds063160.mongolab.com:63160/{2}'.format(username, password, DB_NAME))
        db = client[DB_NAME]
        # db.filters.ensure_index("createdAt", expireAfterSeconds=7*24*60*60)
        return db



    def saveFilter(self, Filter):
        """
        Save a serialized filter object into the MongoDB using the _id of fid
        :param Filter: Filter object
        :return: True if successfully written
        """

        collection_name = "filters"
        try:
            collection = self.db[collection_name]
            collection.insert({"_id": str(Filter.fid), "createdAt": datetime.datetime.utcnow(), "object": pickle.dumps(Filter)})
        except Exception as e:
            return False, e

    def loadAllFilters(self):
        """
        Load all of the filters in the "filters" collection in to a dict of Python Filter objects
        :return: Dict of Filter objects fid: object paris
        """

        filter_collection = self.db["filters"]
        all_filters = {}
        for filter in filter_collection.find():
            all_filters[filter["_id"]] = pickle.loads(filter["object"])

        print "Loaded {0} filters".format(len(all_filters))
        return all_filters

    def getSingleFilter(self, fid):
        """
        Get one filter from mongo for testing purposes
        :param fid: _id or FID of the filter to get from Mongo
        :return: the _id from the DB (or None if it doesn't exist)
        """

        filter_collection = self.db["filters"]
        single_filt = filter_collection.find_one({'_id': fid})
        if single_filt is not None:
            return single_filt["_id"]
        else:
            return None

    def removeFilter(self, fid):
        """
        Delete a filter based on the _id / FID
        :param fid:
        :return:
        """
        if fid is not None:
            filter_collection = self.db["filters"]
            return filter_collection.remove({"_id": fid})
        else:
            return False


    def writeKey(self, key, value):
        """
        Write a key:value into the database
        :param key: key name
        :param value:  value of the key to write
        :return: True or False and exception
        """
        return False





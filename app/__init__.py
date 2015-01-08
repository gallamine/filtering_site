__author__ = 'william'

from flask import Flask
from app import db as dbclass
from flask.ext.cors import CORS


class MyServer(Flask):

    def __init__(self, *args, **kwargs):
        super(MyServer, self).__init__(*args, **kwargs)

        try:
            APPLICATION_PATH = "/Users/william/Documents/filtering_site/app/"
            f = open(APPLICATION_PATH + '.mongo', 'r')
            username, password = f.read().split("\t")
            # Load filters from db
            self.db = dbclass.Database(username, password)

            self.all_filters = self.db.loadAllFilters() #db.readKey('all_filters')
            if self.all_filters is False:
                self.all_filters = {}

        except Exception as e:
            print e
            exit()

app = MyServer(__name__)

from app import filtering_site

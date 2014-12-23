import unittest
from app import app, db
import json
from app import filtering_site

class TestCase(unittest.TestCase):

    def setUp(self):
        """

        :return:
        """

        self.app = app.test_client()

    def tearDown(self):
        """

        :return:
        """



    def test_CreateFilter(self):
        """
        Create a filter. Verify it gets put into the database
        :return:
        """

        # Create default filter
        rv = self.app.get('/filter/new')
        # Get back a dict with the FID
        print rv.data
        assert "fid" in rv.data
        fid = json.loads(rv.data)['fid']
        # Get FID from the database to verify it was added
        assert fid == app.db.getSingleFilter(fid)
        # Delete filter
        print app.db.removeFilter(fid)


if __name__ == '__main__':
    unittest.main()
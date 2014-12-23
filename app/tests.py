import unittest
from app import app, db
import json
import numpy as np
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


    def test_runFilter(self):
        """
        Create and run filter. Test output to see if it matches what we expect
        :return:
        """
        DATA_OUT = {
            '1':[
                -4.396651114330454e-06,
                -1.3191034577015363e-05,
                -1.758658904614694e-05,
                -1.7582202454071874e-05,
                -2.1978884424607713e-05,
                -3.077777790418212e-05,
                -3.5173301471958166e-05,
                -3.516428125756255e-05,
                -3.95609941746263e-05,
                -4.836464506264179e-05,
                -5.2760137638695305e-05
              ],
            '2':[
                -4.383073791336517e-06,
                3.9595238086575286e-05,
                -1.7600537253565882e-05,
                -7.039535042073367e-05,
                -2.1964564790618972e-05,
                2.206298672741361e-05,
                -3.518799307470865e-05,
                -8.803340499983101e-05,
                -3.9545930060438293e-05,
                4.533581320688173e-06,
                -5.277557480698095e-05
              ],
            '3':[
                -5.731114743088208e-05,
                3.961104885192712e-05,
                3.535812934266989e-05,
                -7.041153532647872e-05,
                -7.49545711300194e-05
              ],
            '4':[
                4.406280188846366e-05,
                6.180601819371503e-05,
                -6.607256747095478e-05,
                -9.262279355068654e-05,
                2.653430176139889e-05
              ]
        }
        rv = self.app.get('/filter/new?num_taps=10')
        fid = json.loads(rv.data)['fid']
        # Test long data first
        data = range(1, 12)
        req = '/filter/run?fid={0}&data={1}'.format(fid, str(data).strip(" "))
        print req
        rv = self.app.get(req)
        rv = json.loads(rv.data)
        assert np.all(np.fromstring(rv['data_in'].strip("[]"),sep=',') == data)
        assert np.all(rv['data_out'] == DATA_OUT['1'])

        req = '/filter/run?fid={0}&data={1}'.format(fid, str(data).strip(" "))
        print req
        rv = self.app.get(req)
        rv = json.loads(rv.data)
        assert np.all(np.fromstring(rv['data_in'].strip("[]"),sep=',') == data)
        assert np.all(rv['data_out'] == DATA_OUT['2'])


        # Test short data now

        data = range(1, 6)
        req = '/filter/run?fid={0}&data={1}'.format(fid, str(data).strip(" "))
        print req
        rv = self.app.get(req)
        rv = json.loads(rv.data)

        print rv
        assert np.all(np.fromstring(rv['data_in'].strip("[]"),sep=',') == data)
        assert np.all(rv['data_out'] == DATA_OUT['3'])

        # Test data padding

        data = range(1, 6)
        req = '/filter/run?fid={0}&data={1}&padding=False'.format(fid, str(data).strip(" "))
        print req
        rv = self.app.get(req)
        rv = json.loads(rv.data)
        assert np.all(np.fromstring(rv['data_in'].strip("[]"),sep=',') == data)
        assert np.all(rv['data_out'] == DATA_OUT['4'])

        app.db.removeFilter(fid)

if __name__ == '__main__':
    unittest.main()
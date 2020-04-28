import unittest
import backend
import os

class TestBackend(unittest.TestCase):

    def setUp(self):
        self.SUT = backend.Backend('backend_test.db')

    def test_BackendConstructor(self):
        # assert
        self.assertIsInstance( self.SUT, backend.Backend )
        self.assertEqual(self.SUT.websites,[])
        self.assertEqual(self.SUT.titles,[])
        self.assertEqual(self.SUT.links,[])


    def test_attach(self):
        #execute
        self.SUT.attach(([100,200],[10,11],[20,30]))
        #assert
        self.assertEqual(self.SUT.websites,[100,200])
        self.assertEqual(self.SUT.titles,[10,11])
        self.assertEqual(self.SUT.links,[20,30])

    def test_collectPress(self):
        #execute
        self.SUT.collect_press()
        #
        self.assertNotEqual(self.SUT.websites,[])
        self.assertNotEqual(self.SUT.titles,[])
        self.assertNotEqual(self.SUT.links,[])

    """ def test_updateDb(self):
        # execute
        self.SUT.update_db()
        # assert
        self.assertNotEqual( self.SUT.db.readAll(), [])
 """
    def test_checkUpdateFlagDifferentLength(self):
        # setup
        self.links=['a','b']
        last_rows=(('','','','',''))
        # execute
        flag = self.SUT.checkUpdateFlag(last_rows)
        # assert
        self.assertEqual(flag,True)

    def test_checkUpdateFlagSameData(self):
        # setup
        self.SUT.links=['a','b']
        last_rows=(('','','','','a'),('','','','','b'))
        # execute
        flag = self.SUT.checkUpdateFlag(last_rows)
        # assert
        self.assertEqual(flag,False) 

    def test_checkUpdateFlagSameLengthDif(self):
        # setup
        self.SUT.links=['a','b']
        last_rows=(('','','','','a'),('','','','','c'))
        # execute
        flag = self.SUT.checkUpdateFlag(last_rows)
        # assert
        self.assertEqual(flag,True)



    def tearDown(self):
        del(self.SUT.db)
        os.remove('backend_test.db')



if __name__ == '__main__':
    unittest.main()


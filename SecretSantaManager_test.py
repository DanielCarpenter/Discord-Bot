import unittest
from SecretSantaManager import *

class TestSecretSantaManager(unittest.TestCase):
        
        #TODO: Rewrite this test after save refactor.
        def test_save(self):
            self.SS.addPerson(1)
            self.SS.addPerson(2)
            self.SS.save(self.SS.particpant_list, "participants", 2020)
            self.assertTrue(os.path.isfile("data/{}/{}/{}.json".format("test", 2020, "participants")), "file now exists")
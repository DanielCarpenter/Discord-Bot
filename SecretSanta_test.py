import unittest
from SecretSanta import *

class TestSecretSanta(unittest.TestCase):

    def setUp(self):
        self.SS = SecretSanta("test")

    def test_add_person(self):
        new_person = 1
        self.SS.addPerson(new_person)
        self.SS.addPerson(new_person)
        self.assertTrue(len(self.SS.particpant_list) is 1, "Should not add the same person twice")
        self.assertTrue(self.SS.particpant_list[0] is new_person, "Should add the correct person to the list")

    def test_constructor(self):
        self.assertEquals(self.SS.group, "test", "Correctly assigns group name")
    
    def test_set_previous(self):
        self.SS.setPrevious(1, 2)
        self.assertTrue(self.SS.previous_gifting_map.get(1) == [2], "Should set previous giftee of person1 to [person2]")
    
    def test_setPreviousChance(self):
        self.SS.setPreviousChance(100)
        self.assertEqual(self.SS.previous_giftee_weight, 1.0, "100 should result in 1.0")
        self.SS.setPreviousChance(50)
        self.assertEqual(self.SS.previous_giftee_weight, 0.5, "50 should result in 0.5")
        self.SS.setPreviousChance(0)
        self.assertEqual(self.SS.previous_giftee_weight, 0.0, "0 should result in 0")


    
        

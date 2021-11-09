import unittest
from app.models import Pitch

class PitchTest(unittest.TestCase):
    
    def setUp(self):
        self.new_category=Pitch(pitch = 'science')
        
    def test_cat(self):
        self.assertTrue(self.new_pitch is not None)   
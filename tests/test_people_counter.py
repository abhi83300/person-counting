import unittest
from src.people_counter import count_people_on_screen

class TestPeopleCounter(unittest.TestCase):
    def test_count_people_on_screen(self):
        # This is a basic test. In a real scenario, you'd need to mock the screenshot
        # and perhaps provide a known image to test against.
        count = count_people_on_screen()
        self.assertIsInstance(count, int)
        self.assertGreaterEqual(count, 0)

if __name__ == '__main__':
    unittest.main()
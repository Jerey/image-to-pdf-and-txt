import unittest
from imagetopdfandtxt import picture_rotator

class picture_rotator_test(unittest.TestCase):

    def test_get_new_name(self):
        self.assertEqual(picture_rotator.get_new_name("/some/path/my_image.jpg", "not_rotated"), "ASDF")

if __name__ == "__main__":
    unittest.main()
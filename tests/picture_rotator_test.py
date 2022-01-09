import unittest
from imagetopdfandtxt import picture_rotator

class picture_rotator_test(unittest.TestCase):

    def test_get_new_name(self):
        filename = "my_image"
        self.assertEqual(picture_rotator.get_new_name(f"/some/path/{filename}.jpg", "not_rotated"), f"{filename}_not_rotated.jpg")

if __name__ == "__main__":
    unittest.main()
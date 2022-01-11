import unittest
from imagetopdfandtxt import picture_rotator

class test_picture_rotator(unittest.TestCase):

    def test_get_new_name(self):
        filename = "my_image"
        self.assertEqual(picture_rotator.get_new_name(f"/some/path/{filename}.jpg", "not_rotated"), f"{filename}_not_rotated.jpg")

    def test_get_rotation_angle_almost_perfect(self):
        result_angle = picture_rotator.get_rotation_angle(f"tests/test_images/001/image.jpg")
        self.assertGreater(result_angle, -1)
        self.assertLess(result_angle, 1)

    def test_get_rotation_angle_skew_image(self):
        result_angle = picture_rotator.get_rotation_angle(f"tests/test_images/002/skew_image.jpg")
        self.assertGreater(result_angle, 4)
        self.assertLess(result_angle, 5.6)

if __name__ == "__main__":
    unittest.main()

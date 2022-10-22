import unittest
import cv2
from imagetopdfandtxt import picture_rotator


class test_picture_rotator(unittest.TestCase):
    def test_get_new_name(self):
        filename = "my_image"
        self.assertEqual(
            picture_rotator.get_new_name(
                f"/some/path/{filename}.jpg", "not_rotated"
            ),
            f"{filename}_not_rotated.jpg",
        )

    def test_get_rotation_angle_almost_perfect(self):
        result_angle = picture_rotator.get_rotation_angle(
            cv2.imread("tests/test_images/image.jpg")
        )
        self.assertEqual(result_angle, 0)

    def test_get_rotation_angle_skew_image_2(self):
        result_angle = picture_rotator.get_rotation_angle(
            cv2.imread("tests/test_images/image_2.jpg")
        )
        self.assertEqual(result_angle, -2)


    def test_get_rotation_angle_skew_image_m2(self):
        result_angle = picture_rotator.get_rotation_angle(
            cv2.imread("tests/test_images/image_m2.jpg")
        )
        self.assertEqual(result_angle, 2)

    
    def test_get_rotation_angle_skew_image_5(self):
        result_angle = picture_rotator.get_rotation_angle(
            cv2.imread("tests/test_images/image_5.jpg")
        )
        self.assertEqual(result_angle, -5)
    
    def test_get_rotation_angle_skew_image_m5(self):
        result_angle = picture_rotator.get_rotation_angle(
            cv2.imread("tests/test_images/image_m5.jpg")
        )
        self.assertEqual(result_angle, 5)

if __name__ == "__main__":
    unittest.main()

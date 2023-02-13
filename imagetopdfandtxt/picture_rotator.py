import argparse
import os.path
import warnings
from shutil import copyfile
import cv2
import numpy as np
import imagetopdfandtxt.helper_utils as helper_utils
import scipy.ndimage

# see https://stackoverflow.com/a/57965160
# Delta defines the degree steps to be checked.
# Limit defines the maximum skew.
def get_rotation_angle(image, delta=1, limit=5):
    def determine_score(arr, angle):
        data = scipy.ndimage.rotate(arr, angle, reshape=False, order=0)
        histogram = np.sum(data, axis=1, dtype=float)
        score = np.sum((histogram[1:] - histogram[:-1]) ** 2, dtype=float)
        return histogram, score

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

    scores = []
    angles = np.arange(-limit, limit + delta, delta)
    for angle in angles:
        histogram, score = determine_score(thresh, angle)
        scores.append(score)

    best_angle = angles[scores.index(max(scores))]

    return -best_angle


# see https://www.pyimagesearch.com/2017/02/20/text-skew-correction-opencv-python/
def rotate_image_based_on_text(path_to_image, debug=False):
    image = cv2.imread(path_to_image)
    angle = get_rotation_angle(image)

    rgb = cv2.pyrDown(image)

    # rotate the image to deskew it
    (height_bounding_rect, width_bounding_rect) = rgb.shape[:2]
    center = (width_bounding_rect // 2, height_bounding_rect // 2)
    M = cv2.getRotationMatrix2D(center, -angle, 1.0)
    rotated = cv2.warpAffine(
        rgb,
        M,
        (width_bounding_rect, height_bounding_rect),
        flags=cv2.INTER_CUBIC,
        borderMode=cv2.BORDER_REPLICATE,
    )

    # draw the correction angle on the image so we can validate it
    # cv2.putText(rotated, "Angle: {:.2f} degrees".format(angle), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
    print(f"--> Rotating picture '{path_to_image}' {angle:.2f} degrees")

    # The output directory of the copy of the image and the text.
    output_directory = "tmp/"
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    new_path_to_image = helper_utils.get_output_name_from_input(
        path_to_image, output_directory
    )
    cv2.imwrite(new_path_to_image, rotated)

    # Copy the image aswell, so everything is kept together in the result folder.
    unrotated_image_path = get_new_name(path_to_image, "not_rotated")
    copyfile(
        path_to_image,
        helper_utils.get_output_name_from_input(unrotated_image_path, output_directory),
    )

    # print("Written to '" + outputDirectory + getNewName(pathToImage, "rotated") + "'!")
    return new_path_to_image


def get_new_name(path_to_image, identifier):
    input_file_name = os.path.basename(path_to_image)
    name, ext = os.path.splitext(input_file_name)
    output_file_name = f"{name}_{identifier}{ext}"
    return output_file_name


def main():
    for image in ARGS["images"]:
        print(f"-> Trying to rotate '{image}' based on the text.")
        if os.path.isfile(image):
            rotate_image_based_on_text(image, ARGS["debug"])
        else:
            warnings.warn(f"Not a file: '{image}'! Doing nothing with it.. ")


if __name__ == "__main__":
    AP = argparse.ArgumentParser(
        description="""Takes one to many images and tries to rotate the
                            image based on the text. +-45 degrees are corrected.Further,
                            it stores the original picture and the rotated picture
                            into a result folder."""
    )
    AP.add_argument(
        "-i",
        "--image",
        action="append",
        dest="images",
        required=True,
        help="""Images,
                    which shall be rotated based on the text. Can be added multiple times.""",
    )
    AP.add_argument(
        "-d",
        "--debug",
        action="store_true",
        help="""Stores additional debug 
                    information to the pictures and prints more logs.""",
    )
    ARGS = vars(AP.parse_args())

    main()

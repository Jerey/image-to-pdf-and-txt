import argparse
import os.path
import warnings
from shutil import copyfile
import cv2
import numpy as np
import helper_utils

# see https://www.pyimagesearch.com/2017/02/20/text-skew-correction-opencv-python/
def rotate_image_based_on_text(path_to_image, debug=False):
    large = cv2.imread(path_to_image)
    rgb = cv2.pyrDown(large)
    small = cv2.cvtColor(rgb, cv2.COLOR_BGR2GRAY)

    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    grad = cv2.morphologyEx(small, cv2.MORPH_GRADIENT, kernel)

    _, black_white = cv2.threshold(grad, 0.0, 255.0, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (9, 1))
    connected = cv2.morphologyEx(black_white, cv2.MORPH_CLOSE, kernel)
    # using RETR_EXTERNAL instead of RETR_CCOMP
    contours, _ = cv2.findContours(connected.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    mask = np.zeros(black_white.shape, dtype=np.uint8)

    all_angles = []
    for idx in range(len(contours)):
        x_bounding_rect, y_bounding_rect, width_bounding_rect, height_bounding_rect = cv2.boundingRect(contours[idx])
        mask[y_bounding_rect:y_bounding_rect+height_bounding_rect, x_bounding_rect:x_bounding_rect+width_bounding_rect] = 0
        cv2.drawContours(mask, contours, idx, (255, 255, 255), -1)
        r = float(cv2.countNonZero(mask[y_bounding_rect : y_bounding_rect + height_bounding_rect, x_bounding_rect : x_bounding_rect + width_bounding_rect])) / (width_bounding_rect * height_bounding_rect)

        if r > 0.45 and width_bounding_rect > 8 and height_bounding_rect > 8:
            box = cv2.minAreaRect(contours[idx])
            angle = box[-1]

            # the `cv2.minAreaRect` function returns values in the
            # range [-90, 0); as the rectangle rotates clockwise the
            # returned angle trends to 0 -- in this special case we
            # need to add 90 degrees to the angle
            if angle < -45:
                angle = -(90 + angle)

            # otherwise, just take the inverse of the angle to make
            # it positive
            else:
                angle = -angle

            all_angles.append(angle)
            if debug:
                cv2.rectangle(rgb, (x_bounding_rect, y_bounding_rect), (x_bounding_rect+width_bounding_rect-1, y_bounding_rect+height_bounding_rect-1), (0, 255, 0), 2)
                cv2.drawContours(rgb, [np.int0(cv2.boxPoints(box))], -1, (255,255,255),3)

    if len(all_angles) > 0:
        angle = sum(all_angles)/len(all_angles)
    else:
        angle = 0
        # rotate the image to deskew it
    (height_bounding_rect, width_bounding_rect) = rgb.shape[:2]
    center = (width_bounding_rect // 2, height_bounding_rect // 2)
    M = cv2.getRotationMatrix2D(center, -angle, 1.0)
    rotated = cv2.warpAffine(rgb, M, (width_bounding_rect, height_bounding_rect),
        flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)

    # draw the correction angle on the image so we can validate it
    # cv2.putText(rotated, "Angle: {:.2f} degrees".format(angle), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
    print("--> Rotating picture '{}' {:.2f} degrees".format(path_to_image, angle))

    #The output directory of the copy of the image and the text.
    output_directory = "tmp/"
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    new_path_to_image = helper_utils.get_output_name_from_input(path_to_image, output_directory) 
    cv2.imwrite(new_path_to_image, rotated)

    #Copy the image aswell, so everything is kept together in the result folder.
    unrotated_image_path = get_new_name(path_to_image, "not_rotated")
    copyfile(path_to_image, helper_utils.get_output_name_from_input(unrotated_image_path,
                                                                    output_directory))

    #print("Written to '" + outputDirectory + getNewName(pathToImage, "rotated") + "'!")
    return new_path_to_image

def get_new_name(path_to_image, identifier):
    input_file_name = os.path.basename(path_to_image)
    name, ext = os.path.splitext(input_file_name)
    output_file_name = "{name}_{id}{ext}".format(name=name, id=identifier, ext=ext)
    return output_file_name


def main():
    for image in ARGS["images"]:
        print("-> Trying to rotate '" + image + "' based on the text.")
        if os.path.isfile(image):
            rotate_image_based_on_text(image, ARGS["debug"])
        else:
            warnings.warn("Not a file: '" + image + "'! Doing nothing with it.. ")

if __name__ == '__main__':
    AP = argparse.ArgumentParser(description="""Takes one to many images and tries to rotate the
                            image based on the text. +-45 degrees are corrected.Further,
                            it stores the original picture and the rotated picture
                            into a result folder.""")
    AP.add_argument("-i", "--image", action="append", dest="images", required=True, help="""Images,
                    which shall be rotated based on the text. Can be added multiple times.""")
    AP.add_argument("-d", "--debug", action="store_true", help="""Stores additional debug 
                    information to the pictures and prints more logs.""")
    ARGS = vars(AP.parse_args())

    main()

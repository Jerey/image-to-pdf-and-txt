import argparse
from argparse import RawTextHelpFormatter
import img2pdf


def create_pdf_from_images(list_of_images, output_dir_and_name="default.pdf"):
    with open(output_dir_and_name, "wb") as output_file:
        output_file.write(img2pdf.convert(list_of_images))
    print("--> Created '{}' from '{}'.".format(output_dir_and_name, list_of_images))

def main():
    for image in ARGS["images"]:
        pages = image.split(',')
        print("-> Trying to create a pdf from '{}'.".format(pages))
        create_pdf_from_images(pages)

if __name__ == '__main__':
    AP = argparse.ArgumentParser(description="""Takes a list of images and creates one PDF of them.
    Multi page pdf are created by delimiting with comma.
    Sample:
    \tpython3 pdf_creator.py -i DocOnePageOne.jpg -i DocTwoPageOne.jpg,DocTwoPageTwo.png
    The output file is named after the first given picture.""",
                                 formatter_class=RawTextHelpFormatter)
    AP.add_argument("-i", "--image", action="append", dest="images", required=True,
                    help="""The images, which shall be converted to a pdf.
                    Creating multipage pdf is also possible by
                    delimiting the files with a ",".""")
    ARGS = vars(AP.parse_args())

    main()

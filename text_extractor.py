import argparse
import pyocr
import pyocr.builders
from PIL import Image
from unidecode import unidecode

def extract_text_from_file(list_of_images, output_dir_and_name="default.txt"):
    tool = pyocr.get_available_tools()[0]

    with open(output_dir_and_name, "w") as output_file:
        for path_to_image in list_of_images:
            img = Image.open(path_to_image)
            #Make the image in Black and White
            img = img.convert('L')
            print("-> Reading content from '{}'.".format(path_to_image))
            outputstring_from_picture = tool.image_to_string(img, lang='deu')
            outputstring_from_picture = unidecode(outputstring_from_picture)
            output_file.write(outputstring_from_picture)

    #Splitext divides the name and the filetype.
    print("--> Wrote content to '" + output_dir_and_name + "'.")

def main():
    for image in ARGS["images"]:
        pages = image.split(',')
        print("-> Trying to extract text from '{}'.".format(pages))
        extract_text_from_file(pages)

if __name__ == '__main__':
    AP = argparse.ArgumentParser(description="""Takes one to many images,
        tries to extract text from the images and stores it in a folder.""")
    AP.add_argument("-i", "--image", action="append", dest="images", required=True,
                    help="""Images, from which text shall be extracted.
                    Can be added multiple times.""")
    ARGS = vars(AP.parse_args())
    main()

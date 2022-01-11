import argparse
import pyocr
import pyocr.builders
from PIL import Image
from unidecode import unidecode

def extract_text_from_file(list_of_images, output_dir_and_name="default.txt"):
    tool = pyocr.get_available_tools()[0]
    outputstring_from_picture = ""

    for path_to_image in list_of_images:
        img = Image.open(path_to_image)
        # Make the image black and white
        img = img.convert('L')
        print(f"-> Reading content from '{path_to_image}'.")
        outputstring_from_picture += unidecode(tool.image_to_string(img))

    if not outputstring_from_picture:
        print(f"--> No content written to '{output_dir_and_name}' as nothing could be read.")
    else:
        with open(output_dir_and_name, "w") as output_file:
            output_file.write(outputstring_from_picture)
            print(f"--> Wrote content to '{output_dir_and_name}'.")


def main():
    for image in ARGS["images"]:
        pages = image.split(',')
        print(f"-> Trying to extract text from '{pages}'.")
        extract_text_from_file(pages)

if __name__ == '__main__':
    AP = argparse.ArgumentParser(description="""Takes one to many images,
        tries to extract text from the images and stores it in a folder.""")
    AP.add_argument("-i", "--image", action="append", dest="images", required=True,
                    help="""Images, from which text shall be extracted.
                    Can be added multiple times.""")
    ARGS = vars(AP.parse_args())
    main()

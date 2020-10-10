import argparse
import os.path
import warnings
import text_extractor
import picture_rotator
import pdf_creator
import helper_utils

AP = argparse.ArgumentParser(description="""Takes one to many images, tries to extract text from the
                            images and stores it in a folder including the input image.""")
GROUP = AP.add_mutually_exclusive_group(required=True)
GROUP.add_argument("-i", "--image", action="append", dest="images", help="""Images, from
                which text shall be extracted. Can be added multiple times.""")
GROUP.add_argument("-f", "--folder", dest="folder", help="""Add a directory,
                  where the pictures are stored to be parsed.""")
ARGS = vars(AP.parse_args())


def main():
    list_of_pdfs = []
    if ARGS["folder"] != None:
        for path, _, files in os.walk(ARGS["folder"]):
            currentpdf = []
            for name in files:
                currentpdf.append(os.path.join(path, name))
            if len(currentpdf) != 0:
                currentpdf.sort()
                list_of_pdfs.append(currentpdf)
    else:
        list_of_pdfs = ARGS["images"]

    for pdf in list_of_pdfs:
        print("---------------------------")
        filename = ""
        if ARGS["images"] != None:
            pdf = pdf.split(',')
            filename = pdf[0]
        else:
            filename = os.path.basename(os.path.dirname(pdf[0]))

        for idx, page in enumerate(pdf):
            print("Working on '{}'. That is page {}/{}.".format(page, idx+1, len(pdf)))
            if os.path.isfile(page):
                pdf[idx] = picture_rotator.rotate_image_based_on_text(page)
            else:
                warnings.warn("Not a file: '" + page + "'! Doing nothing with it.. ")

        output_directory = "result/"
        if not os.path.exists(output_directory):
            os.makedirs(output_directory)
        text_output = helper_utils.get_output_name_from_input(filename, output_directory, ".txt")
        text_extractor.extract_text_from_file(pdf, text_output)
        pdf_output = helper_utils.get_output_name_from_input(filename, output_directory, ".pdf")
        pdf_creator.create_pdf_from_images(pdf, pdf_output)

    print("---------------------------")

main()

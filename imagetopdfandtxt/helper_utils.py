import os.path


def get_output_name_from_input(input_file_name, output_dir, output_extension=None):
    input_file_name = os.path.basename(input_file_name)
    output = os.path.splitext(input_file_name)
    if output_extension is None:
        output_extension = output[1]

    return output_dir + output[0] + output_extension

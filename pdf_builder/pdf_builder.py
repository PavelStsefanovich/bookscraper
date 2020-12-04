import os
import pdfkit
from shutil import copyfile



######## FUNCTIONS ########################################
def main(main_config):
    output_files = []
    input_files_paths = main_config['html_builder_output_files']

    for input_file_path in input_files_paths:
        #TODO: add support for --output_directory option
        output_file_split = os.path.split(input_file_path)
        intermediate_input_file_path = os.path.join(output_file_split[0], 'pdf_builder_input_file.html')
        intermediate_output_file_path = os.path.join(output_file_split[0], 'pdf_builder_output_file.pdf')
        output_file_path = os.path.join(output_file_split[0], output_file_split[1].replace('.html', '.pdf'))

        #TODO: load css from external files
        #TODO: move options out to file
        options = {
            'page-size': 'Letter',
            'margin-top': '0.75in',
            'margin-right': '0.75in',
            'margin-bottom': '0.75in',
            'margin-left': '0.75in',
            'encoding': "UTF-8",
            'quiet': '',
            'no-outline': None
        }

        # create intermediate files and run pdfkit
        # intermediate files used as workaround for non-ascii character in path that are not supported by pdfkit
        print(f'Printing to PDF: \'{input_file_path}\'')
        copyfile(input_file_path, intermediate_input_file_path)
        pdfkit.from_file(intermediate_input_file_path, intermediate_output_file_path, options=options)
        copyfile(intermediate_output_file_path, output_file_path)
        output_files.append(output_file_path)
        os.remove(intermediate_input_file_path)
        os.remove(intermediate_output_file_path)

    return output_files



######## MAIN #############################################
if __name__ == '__main__':
    main({})

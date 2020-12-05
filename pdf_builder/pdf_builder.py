import os
import pdfkit
from shutil import copyfile



######## FUNCTIONS ########################################
def main(main_config):
    output_files = []
    input_files_paths = main_config['html_builder_output_files']

    for input_file_pair in input_files_paths:
        output_file_split = os.path.split(input_file_pair[0])
        intermediate_input_file_path = os.path.join(output_file_split[0], 'pdf_builder_input_file.html')
        intermediate_output_file_path = os.path.join(output_file_split[0], 'pdf_builder_output_file.pdf')
        output_file_path = os.path.join(output_file_split[0], output_file_split[1].replace('.html', '.pdf'))
        
        ## css file reference
        css = input_file_pair[1]

        ## load pdfkit options
        options = main_config['pdfkit_config'].get('options')
        if not options:
            options = {}

        # create intermediate files and run pdfkit
        # intermediate files used as workaround for non-ascii character in path that are not supported by pdfkit
        print(f'Printing to PDF: \'{input_file_pair[0]}\'')
        copyfile(input_file_pair[0], intermediate_input_file_path)
        pdfkit.from_file(intermediate_input_file_path, intermediate_output_file_path, options=options, css=css)
        copyfile(intermediate_output_file_path, output_file_path)
        output_files.append(output_file_path)
        os.remove(intermediate_input_file_path)
        os.remove(intermediate_output_file_path)

    return output_files



######## MAIN #############################################
if __name__ == '__main__':
    main({})

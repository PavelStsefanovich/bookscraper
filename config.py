import os
from ruamel.yaml import YAML



######## FUNCTIONS ########################################
def parse_cmdargs(cmdargs):
    yaml=YAML(typ='safe')
    mainconfig_filepath = cmdargs['params_file']
    if not os.path.isabs(mainconfig_filepath):
        mainconfig_filepath = os.path.join(cmdargs['root_dir'], mainconfig_filepath)

    try:
        with open(mainconfig_filepath, 'r', encoding='UTF-8') as file:
            main_config = yaml.load(file)
    except:
        main_config = {}

    for argument in cmdargs:
        if cmdargs[argument]:
            main_config[argument] = cmdargs[argument]

    if main_config.get('no_book_scraper'):
        mandatory_args = ['scraper_output_file']
    else:
        mandatory_args = ['url']

    for argument in mandatory_args:
        if not main_config.get(argument):
            raise Exception(f'Mandatory argument not provided: <{argument}>')

    return main_config


def parse_config(main_config):
    yaml=YAML(typ='safe')
    config_dir = os.path.join(main_config['root_dir'], 'config')
    parser_config_filepath = os.path.join(config_dir, 'parser_config.yml')
    stylesheet_filepath = os.path.join(config_dir, 'stylesheet.css')
    stylesheet_mobile_filepath = os.path.join(config_dir, 'stylesheet_mobile.css')
    pdfkit_config_filepath = os.path.join(config_dir, 'pdfkit_config.yml')

    ## html parser config
    try:
        with open(parser_config_filepath, 'r', encoding='UTF-8') as file:
            main_config['parser_config'] = yaml.load(file)
    except:
        main_config['parser_config'] = {}
        print(f'WARNING! HTML parser configuration file not found at \'{parser_config_filepath}\'. Resulting .html file may not look pretty.')

    ## html stylesheet
    try:
        with open(stylesheet_filepath, 'r', encoding='UTF-8') as file:
            main_config['stylesheet'] = file.read()
            main_config['stylesheet_filepath'] = stylesheet_filepath
    except:
        main_config['stylesheet'] = main_config['stylesheet_filepath'] = None
        print(f'WARNING! Stylesheet file not found at \'{stylesheet_filepath}\'. Resulting .html/.pdf files may not look pretty.')

    ## html stylesheet (mobile)
    try:
        with open(stylesheet_mobile_filepath, 'r', encoding='UTF-8') as file:
            main_config['stylesheet_mobile'] = file.read()
            main_config['stylesheet_mobile_filepath'] = stylesheet_mobile_filepath
    except:
        main_config['stylesheet_mobile'] = main_config['stylesheet_mobile_filepath'] = None
        print(f'WARNING! Stylesheet file (mobile) not found at \'{stylesheet_mobile_filepath}\'. Resulting .html/.pdf files may not look pretty.')

    ## pdfkit confing
    try:
        with open(pdfkit_config_filepath, 'r', encoding='UTF-8') as file:
            main_config['pdfkit_config'] = yaml.load(file)
    except:
        main_config['pdfkit_config'] = {}
        print(f'WARNING! Failed to load PDF Kit configuration from file \'{pdfkit_config_filepath}\'. Resulting .pdf files may not look pretty.')

    ## scraper output file
    if main_config.get('scraper_output_file'):
        if not os.path.isfile(main_config['scraper_output_file']):
            raise Exception(f'Specified Book Scraper output file not found: \'{main_config["scraper_output_file"]}\'')

    return main_config



######## MAIN #############################################
if __name__ == '__main__':
    raise Exception('Module "config" is not intended to run as a standalone program')

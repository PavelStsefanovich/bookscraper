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

    try:
        with open(parser_config_filepath, 'r', encoding='UTF-8') as file:
            main_config['parser_config'] = yaml.load(file)
    except:
        main_config['parser_config'] = {}
        print(f'WARNING! HTML parser configuration file not found at \'{parser_config_filepath}\'. Resulting .html file may not look pretty.')

    try:
        with open(stylesheet_filepath, 'r', encoding='UTF-8') as file:
            main_config['stylesheet'] = file.read()
    except:
        main_config['stylesheet'] = None
        print(f'WARNING! HTML stylesheet file not found at \'{stylesheet_filepath}\'. Resulting .html file may not look pretty.')

    try:
        with open(stylesheet_mobile_filepath, 'r', encoding='UTF-8') as file:
            main_config['stylesheet_mobile'] = file.read()
    except:
        main_config['stylesheet_mobile'] = None
        print(f'WARNING! HTML stylesheet_mobile file not found at \'{stylesheet_mobile_filepath}\'. Resulting .html file may not look pretty.')

    return main_config



######## MAIN #############################################
if __name__ == '__main__':
    raise Exception('Module "config" is not intended to run as a standalone program')

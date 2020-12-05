import argparse
import config
import os
import sys
from book_scraper import book_scraper
from html_builder import html_builder
from pdf_builder import pdf_builder
from subprocess import Popen



######## USER INPUT #######################################
parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('-u','--url', dest='url', help='Target book URL')
#TODO implement title override from cmdargs
#parser.add_argument('-t','--title', dest='title', help='Book title (will also be optimized and used as output file name)')
parser.add_argument('-s','--start_page', dest='start_page', default='1', help='First page to be included into scraping')
parser.add_argument('-e','--end_page', dest='end_page', help='Last page to be included into scraping')
parser.add_argument('-p','--params_file', dest='params_file', default='params.yml', help='Path to YAML parameters file (to be used instead of command-line arguments; if both parameters file and cmd arguments specified, cmd arguments take priority)')
parser.add_argument('--no_book_scraper', action='store_true', help='If specified, book_scraper will be skipped (scraper output file must be specified explicitly usting \'--scraper_output_file\' argument)')
parser.add_argument('--scraper_output_file', help='Path to previously generated book scraper output file')
parser.add_argument('--no_pdf_builder', action='store_true', help='If specified, pdf_builder will be skipped')
cmdargs = vars(parser.parse_args())



######## ROOT DIRECTORY ###################################
if getattr(sys, 'frozen', False):
    cmdargs.update({'root_dir' : os.path.dirname(sys.executable)})
elif __file__:
    cmdargs.update({'root_dir' : sys.path[0]})



######## MAIN #############################################
if __name__ == '__main__':
    try:
        main_config = config.parse_cmdargs(cmdargs)
        main_config = config.parse_config(main_config)

        if not main_config.get('no_book_scraper'):
            main_config['scraper_output_file'] = book_scraper.main(main_config)

        main_config['html_builder_output_files'] = html_builder.main(main_config)

        ## pause before proceeding
        keyboard_input = input('\n>> Press <Enter> to proceed to pdf_builder (enter "stop" to exit): ')
        if keyboard_input == 'stop':
            main_config['no_pdf_builder'] = True

        if not main_config.get('no_pdf_builder'):
            main_config['pdf_builder_output_files'] = pdf_builder.main(main_config)

        ## display result
        print(f'\nFiles generated in directory \'{os.getcwd()}\'')
        print('\n>> Type "open" to open this directory in file explorer')
        keyboard_input = input('>> Press <Enter> to exit: ')
        if keyboard_input == 'open':
            proc = Popen(['explorer', '.'], shell=True, stdin=None, stdout=None, stderr=None, close_fds=True)

    except Exception as e:
        print('\n(!) ERROR:')
        print(e)
        keyboard_input = input('\n>> Press <Enter> to exit: ')

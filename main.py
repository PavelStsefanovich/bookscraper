import argparse
import config
import os
import sys
from book_scraper import book_scraper
from html_builder import html_builder



######## USER INPUT #######################################
parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('-u','--url', dest='url', help='Target book URL')
parser.add_argument('-t','--title', dest='title', help='Book title (will also be optimized and used as output file name)')
parser.add_argument('-s','--start_page', dest='start_page', default='1', help='First page to be included into scraping')
parser.add_argument('-e','--end_page', dest='end_page', help='Last page to be included into scraping')
parser.add_argument('-p','--params_file', dest='params_file', default='params.yml', help='Path to YAML parameters file (to be used instead of command-line arguments; if both parameters file and cmd arguments specified, cmd arguments take priority)')
cmdargs = vars(parser.parse_args())



######## ROOT DIRECTORY ###################################
if getattr(sys, 'frozen', False):
    cmdargs.update({'root_dir' : os.path.dirname(sys.executable)})
elif __file__:
    cmdargs.update({'root_dir' : sys.path[0]})



######## MAIN #############################################
if __name__ == '__main__':
    main_config = config.parse_cmdargs(cmdargs)
    main_config = config.parse_config(main_config)
    output_file = book_scraper.main(main_config)
    html_builder.main(output_file)

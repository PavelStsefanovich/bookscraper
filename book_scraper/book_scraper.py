from . import book_scraper_data as bdata



######## FUNCTIONS ########################################
def get_website_scraper_metadata(cmdargs):
    metadata = None
    for key in bdata.known_book_websites:
        if not cmdargs.get('url'):
            continue
        if cmdargs['url'].startswith(key):
            metadata = bdata.known_book_websites[key]

    if not metadata:
        raise Exception(f'Book website not supported: "{key}".')

    return metadata


def run_scraper(scraper_metadata, cmdargs):
    output_file = scraper_metadata["scraper_function"](scraper_metadata, cmdargs)
    return output_file


def main (cmdargs):
    scraper_metadata = get_website_scraper_metadata(cmdargs)
    output_file = run_scraper(scraper_metadata, cmdargs)
    return output_file



######## MAIN #############################################
if __name__ == '__main__':
    main({})

import os
import re
from . import book_scraper_helpers as helpers
from . import book_scraper_data as bdata



######## FUNCTIONS ########################################
def normalize(text):
    text = text.replace('\r','').replace('\n','').replace('\t','')
    # more normalization conventions go here
    return text


def scrape_loveread(metadata, cmdargs):
    ### set base URLs
    book_base_url = metadata["base_url"] + '/'
    try:
        book_base_url = book_base_url + re.search(metadata["url_book_regex"], cmdargs["url"])[0]
    except:
        print(f'ERROR: Failed to determine book base URL: user-provided URL does not match expected format.')
        raise
    try:
        page_base_url = book_base_url + re.search(metadata["url_page_novalue_regex"], cmdargs["url"])[0]
    except:
        print(f'ERROR: Failed to determine page base URL: user-provided URL does not match expected format.')
        raise

    ### author & title
    title_url = page_base_url + '1'
    soup = helpers.make_soup(title_url)
    if soup == -1:
        raise Exception(f'Failed to parse URL with BeautifulSoup: \'{title_url}\'')

    # parse html for author and title
    text = helpers.search_soup(
        soup=soup,
        search_tag=metadata["book_title_search_tag"],
        search_class=metadata["book_title_search_class"]
    )
    if text == -1:
        print(f'URL used: \'{title_url}\'')
        raise Exception('ERROR: Failed to find author or title in html.')

    # title
    try:
        title = normalize(text.strip().split('|')[0].split('-')[1].strip())
        print(f'TITLE: {title}')
    except:
        print('ERROR: Failed to determine title')
        print(f'Text used: \'{text}\'')
        raise

    # author
    try:
        author = normalize(text.strip().split('|')[1].split('-')[1].strip())
        print(f'AUTHOR: {author}')
    except:
        print('ERROR: Failed to determine author')
        print(f'Text used: \'{text}\'')
        raise

    ### pages range
    try:
        start_page = '1'
        start_page = str(int(cmdargs["start_page"]))
    except:
        pass

    try:
        end_page = None
        end_page = str(int(cmdargs["end_page"]))
    except:
        pass

    # parse html for end_page
    if not end_page:
        navigation_panel = helpers.search_soup(
            soup=soup,
            search_tag=metadata["book_navigation_panel_search_tag"],
            search_class=metadata["book_navigation_panel_search_class"],
            return_text=False
        )
        if navigation_panel == -1:
            print(f'URL used: \'{title_url}\'')
            raise Exception('ERROR: Failed to find navigation panael in html.')

        try:
            end_page = navigation_panel.find_all('a')[-2].text
        except:
            print('ERROR: Failed to determine end page')
            print(f'Text used: \'{text}\'')
            raise

    print(f'START PAGE: {start_page}')
    print(f'END PAGE: {end_page}')

    ### book header
    out_file = os.path.join(cmdargs["root_dir"], f'{author} @ {title}.txt')
    header = f'@@title:{title.upper()}\n@@author:{author}'
    with open(out_file,'w', encoding="utf-8") as book:
        book.write(header)

    ### book text
    page = int(start_page)

    while True:
        url = page_base_url + str(page)
        print(f' parsing: {url}')

        soup = helpers.make_soup(url)
        if soup == -1:
            print(f'(!) Failed to parse: {url}')
            text = f'\n!!!!! PAGE {str(page)} is skipped !!!!!\n'
        else:
            text = helpers.search_soup(
                soup=soup,
                search_tag=metadata["book_text_search_tag"],
                search_class=metadata["book_text_search_class"]
            )

        with open(out_file,'a', encoding="utf-8") as book:
            book.write(text)

        page += 1
        if page > int(end_page):
            break

    ### book notes (footnotes)
    footnote_url = book_base_url.replace('read_book','notes')
    soup = helpers.make_soup(footnote_url)
    # soup.find('div', class_='contents', text='Примечания')
    # if soup != -1:
    if re.match(rf'Примечания\sкниги\:\s+{title}', soup.text.split('|')[0].strip()):
        print('Notes found, parsing')

        notes_text = helpers.search_soup_all(
            soup=soup,
            search_tag=metadata["book_text_search_tag"],
            search_class=metadata["book_text_search_class"]
        )

        note_numbers = helpers.search_soup_all(
            soup=soup,
            search_tag=metadata["book_note_numbers_search_tag"],
            search_class=metadata["book_note_numbers_search_class"]
        )

        notes_zip = list(zip(note_numbers, notes_text))
        notes = '\n\n\n@@FOOTNOTES@@\n'

        for pair in notes_zip:
            notes += f'\n{pair[0]}\n{pair[1]}\n'

        with open(out_file,'a', encoding="utf-8") as book:
            book.write(notes)

    ### return output file path
    return out_file

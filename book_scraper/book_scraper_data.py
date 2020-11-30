from .book_website_scrapers import *

known_book_websites = {
    'http://loveread.ec': {
        'scraper_function': scrape_loveread,
        'base_url': 'http://loveread.ec',
        'url_book_regex': r'(?<=\/)read_book\.php\?id=\d+',
        'url_page_novalue_regex': r'\&p\=(?=\d)',
        'book_title_search_tag': 'h2',
        'book_title_search_class': None,
        'book_text_search_tag': 'p',
        'book_text_search_class': 'MsoNormal',
        'book_note_numbers_search_tag': 'p',
        'book_note_numbers_search_class': 'prm',
        'book_navigation_panel_search_tag': 'div',
        'book_navigation_panel_search_class': 'navigation'
    }
}

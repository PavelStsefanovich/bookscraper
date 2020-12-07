import requests
from bs4 import BeautifulSoup


def make_soup(url):
    http_headers = {'User-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0'}

    try:
        r = requests.get(url, headers=http_headers)
        c = r.content
        soup = BeautifulSoup(c, "html.parser")
    except:
        return -1

    return soup


def search_soup(soup=None, search_tag=None, search_class=None, return_text=True):
    try:
        if search_class:
            found = soup.find(search_tag, {"class" : search_class})
        else:
            found = soup.find(search_tag)

        if return_text:
            found = found.text

        return found

    except:
        print('ERROR: Searching soup failed.')
        print(f'Search tag used: \'{search_tag}\'')
        print(f'Search class used: \'{search_class}\'')
        return -1


def search_soup_complex(soup=None, search_tag=None, search_class=None, embedded_tags=None, return_text=True):
    try:
        if search_class:
            found = soup.find(search_tag, {"class" : search_class})
        else:
            found = soup.find(search_tag)

        if return_text:
            book_text = ''
            for item in found:
                try: 
                    text = item.text
                except:
                    continue

                if len(text) == 0:
                    continue

                if item.name == search_tag:
                    book_text += f'\n{text}'
                    continue

                for emb_tag in embedded_tags:
                    if emb_tag[0] == item.name and emb_tag[1] == item.attrs["class"][0]:
                        text = ' '.join((emb_tag[2], text))
                        book_text += f'\n{text}'
                        continue

            return book_text

        return found

    except:
        print('ERROR: Searching soup failed.')
        print(f'Search tag used: \'{search_tag}\'')
        print(f'Search class used: \'{search_class}\'')
        return -1


def search_soup_all(soup=None, search_tag=None, search_class=None, return_text=True):
    try:
        if search_class:
            found = soup.find_all(search_tag, {"class" : search_class})
        else:
            found = soup.find_all(search_tag)

        if return_text:
            found_text = []
            for element in found:
                found_text.append(element.text)
            found = found_text

        return found

    except:
        print('ERROR: Searching soup failed.')
        print(f'Search tag used: \'{search_tag}\'')
        print(f'Search class used: \'{search_class}\'')
        return -1
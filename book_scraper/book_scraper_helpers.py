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
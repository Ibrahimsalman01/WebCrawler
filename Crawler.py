import regex as reg
import requests as req
import math
import shutil
import os


def Crawl(seed: str) -> str:
    link_filter = {
        'queue':[seed],
        'uniques':set()
    }
    page_content = {

    }

    BASE_URL = seed.rsplit('N', 1)[0]

    while len(link_filter['queue']) > 0: 
        popped = link_filter['queue'].pop(0)

        initial_request = req.get(popped)
        save_data(initial_request.text, "data_parse.txt")
        page_grab = parse_data("data_parse.txt", BASE_URL)
        print(page_grab)

        for absolute in page_grab['filter_list']:
            if absolute not in link_filter['uniques']:
                link_filter['queue'].append(absolute)
                link_filter['uniques'].add(absolute)

    return f'The number of page(s) found: {str(len(link_filter["uniques"]))}'


def save_data(text: str, local_file: str):
    with open(local_file, "w") as data_w:
        data_w.write(text)


def parse_data(local_file: str, BASE_URL: str) -> list:
    page_grab = {
        'filter_list': [],
        'page_content': {
            'title': str(),
            'outgoing_links': list(),
            'words': dict()
        }
    }
    word_str = str()

    with open(local_file, "r") as data_r:
        for line in data_r:
            
            # create titles and add them to the words and outgoing_links dictionaries
            title = reg.search('<title>\w-\d+</title>', line)
            if title:
                page_title = title.group(0).lstrip('<title>').rsplit('</title>')[0]
                page_grab['page_content']['title'] = page_title
            
            # search for all absolutes in each page
            search_absolute = reg.search('\w-\d+.html', line)
            if search_absolute:
                ABSOLUTE = BASE_URL + search_absolute.group(0)
                page_grab['filter_list'].append(ABSOLUTE)
                page_grab['page_content']['outgoing_links'].append(ABSOLUTE)
            
            word_str += line
        # grab all the words between the p tags
        words = word_str[word_str.find('<p') + 3:word_str.find('</p>')].split()
        for word in words:
            if word not in page_grab['page_content']['words']:
                page_grab['page_content']['words'][word] = 1
            else:
                page_grab['page_content']['words'][word] += 1
    return page_grab
    

print(Crawl('http://people.scs.carleton.ca/~davidmckenney/tinyfruits/N-0.html'))
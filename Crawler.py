import regex as reg
import requests as req
import json
import math
import shutil
import os


def Crawl(seed: str) -> str:
    link_filter = {
        'queue':[seed],
        'uniques':set()
    }
    crawl_page_content = []
    
    BASE_URL = seed.rsplit('N', 1)[0]

    while len(link_filter['queue']) > 0: 
        popped = link_filter['queue'].pop(0)

        initial_request = req.get(popped)
        save_data(initial_request.text, "data_parse.txt", True)
        page_grab = parse_data("data_parse.txt", BASE_URL)
        if page_grab['parse_page_content'] not in crawl_page_content:
            crawl_page_content.append(page_grab['parse_page_content'])

        for absolute in page_grab['filter_list']:
            if absolute not in link_filter['uniques']:
                link_filter['queue'].append(absolute)
                link_filter['uniques'].add(absolute)
    
    # sort all the dictionaries based on title
    crawl_page_content = sorted(crawl_page_content, key=lambda t: int(t['title'].strip('N-')))
    # clear jsonData folder and make a new folder
    if os.path.exists('./jsonData'):
        shutil.rmtree('./jsonData')
    os.makedirs('./jsonData')
    # save all the json dumps to files in the jsonData folder
    for i in range(len(crawl_page_content)):
        content_dump = json.dumps(crawl_page_content[i], indent=3)
        if not os.path.exists(f'./jsonData/page_{i}.json'):
            with open(f'./jsonData/page_{i}.json', 'a+') as save_json:
                save_json.write(content_dump)

    return f'The number of page(s) found: {str(len(link_filter["uniques"]))}'


def save_data(text: str, local_file: str, rewrite: bool):
    if rewrite:
        file_mode = 'w'
    else:
        file_mode = 'a'
    with open(local_file, file_mode) as data_w:
        data_w.write(text)


def parse_data(local_file: str, BASE_URL: str) -> list:
    page_grab = {
        'filter_list': [],
        'parse_page_content': {
            'title': '',
            'native_link': '',
            'outgoing_links': [],
            'words': {}
        }
    }
    word_str = ''

    with open(local_file, "r") as data_r:
        for line in data_r:
            
            # create titles and add them to the words and outgoing_links dictionaries
            title = reg.search('<title>\w-\d+</title>', line)
            if title:
                page_title = title.group(0).lstrip('<title>').rsplit('</title>')[0]
                page_grab['parse_page_content']['title'] = page_title
                page_grab['parse_page_content']['native_link'] = BASE_URL + page_title + '.html'
                print(page_grab['parse_page_content']['native_link'])
            
            # search for all absolutes in each page
            search_absolute = reg.search('\w-\d+.html', line)
            if search_absolute:
                ABSOLUTE = BASE_URL + search_absolute.group(0)
                page_grab['filter_list'].append(ABSOLUTE)
                page_grab['parse_page_content']['outgoing_links'].append(ABSOLUTE)
            
            word_str += line
        # removing \n with a space instead to separate words
        word_str = word_str.replace('\n', ' ')
        if '<p' in word_str:
            # start by finding the first half of the start p tag in case of in-line css
            word_str = word_str[word_str.find('<p'):]
            # cut out all the in-line css if present and create a list of the words we want
            word_str = word_str[word_str.find('>') + 1:word_str.find('</p>')].split()
        
        # add the words to the dictionary
        for word in word_str:
            if word not in page_grab['parse_page_content']['words']:
                page_grab['parse_page_content']['words'][word] = 1
            else:
                page_grab['parse_page_content']['words'][word] += 1
    return page_grab
    

print(Crawl('http://people.scs.carleton.ca/~davidmckenney/tinyfruits/N-0.html'))
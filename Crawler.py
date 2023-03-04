import regex as reg
import requests as req
import math
import shutil
import os


def Crawl(seed: str) -> str:
    link_filter = {
        'queue':[seed],
        'duplicates':set()
    }
    BASE_URL = seed[:-8]

    while len(link_filter['queue']) > 0: 
        popped = link_filter['queue'].pop(0)

        initial_request = req.get(popped)
        save_data(initial_request.text, "initial_data.txt")
        absolute_grab = parse_data("initial_data.txt", BASE_URL)

        for absolute in absolute_grab:
            if absolute not in link_filter['duplicates']:
                link_filter['queue'].append(absolute)
                link_filter['duplicates'].add(absolute)
    return f'The number of page(s) found: {str(len(link_filter["duplicates"]))}'


def save_data(text: str, local_file: str):
    with open(local_file, "w") as initial_data_w:
        initial_data_w.write(text)


def parse_data(local_file: str, BASE_URL: str) -> list:
    absolutes = []

    with open(local_file, "r") as initial_data_r:
        for line in initial_data_r:
            search = reg.search('\w-\d+.html', line)
            if search:
                absolutes.append(BASE_URL + search.group(0))
    return absolutes


print(Crawl('http://people.scs.carleton.ca/~davidmckenney/tinyfruits/N-0.html'))
print(Crawl('http://people.scs.carleton.ca/~davidmckenney/fruits/N-0.html'))
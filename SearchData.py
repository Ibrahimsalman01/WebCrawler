import json
import regex as reg


def get_outgoing_links(URL: str) -> list:
    title_index = URL.rsplit('N-', 1)[1].replace('.html', '')
    with open(f'./jsonData/page_{title_index}.json', 'r') as out_going_links:
        page_content = json.load(out_going_links)
        return page_content['outgoing_links']
    

def get_incoming_links(URL: str) -> list:
    BASE_URL = URL.rsplit('N', 1)[0]
    url_list = []
    
    for i in range(len('./jasonData') - 1):
        with open(f'./jsonData/page_{i}.json', 'r') as incoming_check:
            dump_load = json.load(incoming_check)
            if URL in dump_load['outgoing_links']:
                url_list.append(BASE_URL + dump_load['title'] + '.html')
    return url_list

def get_page_rank(URL: str) -> int:
    pass

def get_idf(word: str) -> float:
    pass

def get_tf(URL: str, word: str) -> float:
    pass

def get_tf_idf(URL, word):
    pass

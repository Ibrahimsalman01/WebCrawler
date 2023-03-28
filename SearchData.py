import json
import regex as reg
import math
import numpy as np


def get_outgoing_links(URL: str) -> list:
    title_index = URL.rsplit('N-', 1)[1][:1]
    print(title_index)
    with open(f'./jsonData/page_{title_index}.json', 'r') as out_going_links:
        page_content = json.load(out_going_links)
        return page_content['outgoing_links']


def get_incoming_links(URL: str) -> list:
    BASE_URL = URL.rsplit('N', 1)[0]
    url_list = []
    
    for i in range(len('./jasonData') - 1):
        with open(f'./jsonData/page_{i}.json', 'r') as incoming_check:
            page_content = json.load(incoming_check)
            if URL in page_content['outgoing_links']:
                url_list.append(BASE_URL + page_content['title'] + '.html')
    return url_list


def get_page_rank(URL: str) -> int:
    BASE_URL = reg.split('\d+', URL)[0]
    # initialize adj and d matrix
    adj_matrix = [[0 for _ in range(len(f'./jsonData'))] for _ in range(len(f'./jsonData'))]
    d_matrix = [[0 for _ in range(len(f'./jsonData'))] for _ in range(len(f'./jsonData'))]

    for i in range(len(f'./jsonData')):
        in_links = get_incoming_links(BASE_URL + str(i) + '.html')
        # check if the row has all zeros
        for link in in_links:
            # add necessary 1s to match our in links
            int_split = int(reg.search('\d+', link).group(0))
            adj_matrix[i][int_split] = 1
        
        # find the 1s in each row in adj matrix and insert the values into the d matrix 
        row_sum = 0
        for row in range(len(adj_matrix[i])):
            if adj_matrix[i][row] == 1: row_sum += 1
        
        # if the row sum is 0, insert 1/(N - 1) into each elem in the row except for the i_th elem
        if row_sum == 0:
            for j in range(len(adj_matrix[i])):
                if j != i:
                    adj_matrix[i][j] = 1 / (len(f'.jsonData') - 1)
                    row_sum += adj_matrix[i][j]
        d_matrix[i][i] = 1 / row_sum
    # define our lists as real matricies and multiply to find our M matrix
    adj_matrix = np.array(adj_matrix)
    d_matrix = np.array(d_matrix)
    
    m = np.matmul(adj_matrix, d_matrix)
    v = np.array([(1 / (len(f'.jsonData') + 1)) for _ in range(len(f'.jsonData') + 1)])
    v_prev = np.array([0 for _ in range(len(f'.jsonData') + 1)])
    
    # stop iterations when distance between the current and the previous matrix is =< 0.0001
    while (v - v_prev).all() > 0.0001:
        v_prev = v
        v = np.matmul(m, v)
    # once the PR vector is complete, return the specific PR value for that page
    return v[int(reg.search('\d+', URL).group(0))]


def get_idf(word: str) -> float:
    doc_words = 0
    json_pages = len('./jsonData') - 1
    for i in range(len('./jsonData') - 1):
        with open(f'./jsonData/page_{i}.json', 'r') as page:
            page_content = json.load(page)
            if word in page_content['words']:
                doc_words += 1
    if doc_words == 0:
        return 0
    return math.log(json_pages / (1 + doc_words), 2)


def get_tf(URL: str, word: str) -> float:
    title_index = URL.rsplit('N-', 1)[1][:1]
    with open(f"./jsonData/page_{title_index}.json", "r") as tf:
        page_content = json.load(tf)
        try:
            num_word = page_content['words'][word]
            words_total = sum(page_content['words'].values())
            return num_word / words_total
        except:
            return -1


def get_tf_idf(URL, word):
    tf = get_tf(URL, word)
    idf = get_idf(word)
    return math.log(1 + tf, 2) * idf


from searchdata import get_tf_idf, get_page_rank
import json

def search(phrase: str, boost: bool) -> list:
    page_rankings = {}
    # initialize and find all unique words in the json data
    word_list = []
    for i in range(len(f'./jsonData')):
        with open(f'./jsonData/page_{i}.json', 'r') as page:
            page_content = json.load(page)
            for word in page_content['words']:
                if word not in word_list:
                    word_list.append(word)
    word_list.sort()
    
    # create a vector matrix for tf-idfs based on the words in word_list
    vector_matrix = [[0 for _ in range(len(word_list))] for _ in range(len(f'./jsonData'))]
    
    # inserting tf-idfs into the matrix
    for i in range(len(vector_matrix)):
        with open(f'./jsonData/page_{i}.json', 'r') as page:
            page_content = json.load(page)
            # vector matrix of tf-idfs
            for j in range(len(vector_matrix[i])):
                if word_list[j] in page_content['words']:
                    vector_matrix[i][j] = get_tf_idf(page_content['native_link'], word_list[j])
                    if boost:
                        vector_matrix[i][j] *= get_page_rank(page_content['native_link'])
            # page_rankings building
            page_rankings[page_content['title']] = dict()
            page_rankings[page_content['title']]['URL'] = page_content['native_link']
            page_rankings[page_content['title']]['score'] = 0
    print(page_rankings)

search('t', False)
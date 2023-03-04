import requests as req
import regex as reg

BASE_URL = 'http://people.scs.carleton.ca/~davidmckenney/tinyfruits/'

absolutes = []

with open("initial_data.txt", "r") as initial_data_r:
    for line in initial_data_r:
        m = reg.search(r'\w-\d.html', line)
        if m:
            absolutes.append(BASE_URL + m.group(0))

print(absolutes)

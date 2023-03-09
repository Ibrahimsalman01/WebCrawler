import regex

BASE = 'http://people.scs.carleton.ca/~davidmckenney/fruits/N-0.html'

ABSOLUTE = BASE.rsplit('/', 1)[1].rstrip('.html')
print(ABSOLUTE)
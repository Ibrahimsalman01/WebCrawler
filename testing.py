import requests

x = requests.get("http://people.scs.carleton.ca/~davidmckenney/tinyfruits/N-0.html")

# saving the data to a txt file
with open("initial_data.txt", "w") as initial_data_w:
    initial_data_w.write(x.text)

with open("initial_data.txt", "r") as initial_data_r:
    for line in initial_data_r:
        if "<html><head><title>" in line:
            print("title: ", line[19:22], "\n")
        elif "<a" in line:
            print(line[9:19])


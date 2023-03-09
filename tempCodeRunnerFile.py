for line in data_r:
            print("pre-replacement: ", title_list)
            # create titles and add them to the words and outgoing_links dictionaries
            title = reg.search('<title>\w-\d+</title>', line)
            if title:
                page_title = title.group(0).lstrip('<title>').rsplit('</title>')[0]
                # print(page_title)
                title_list.append(page_title)
                print("post-replacement: ", title_list, "\n")
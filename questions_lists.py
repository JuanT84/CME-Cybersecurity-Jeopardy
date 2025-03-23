def get_list(text_id):
    name = str(text_id) + ".txt"
    f = open(name, "r")

    raw_data = f.readlines()
    # print(list(data))
    f.close()

    cat_count = 0
    q_count = 0
    level = {}
    game = {}
    for i in range(len(raw_data)):
        data = raw_data[i].strip()
        if 'Q: ' not in data:
            level = {}
            cat_count += 1
            level['title'] = data
        else:
            q_count += 1
            start_ind = data.index('Q: ') + 3
            mid_ind = data.index('A: ')
            question = data[start_ind: mid_ind]
            answer = data[mid_ind + 3:]
            if cat_count < 7:
                dollars = 200 * q_count
                category = 'category 0' + str(cat_count)
                level[dollars] = [question, answer]
            elif cat_count < 13:
                dollars = 400 * q_count
                category = 'category 1' + str(cat_count - 6)
                level[dollars] = [question, answer]
            else:
                category = 'final'
                game['final'] = [question, answer, raw_data[i-1].strip()]
            if q_count >= 5:
                q_count = 0
                game[category] = level

    return game


# I built the level scraper after building the main.py playable game
# and I found the easiest way to scrape the levels and store the files
# needed some transformations before it could easily loaded into the game



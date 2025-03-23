import requests
from bs4 import BeautifulSoup
# this routine can take a # or series of numbers and see if the jeopardy archives has a game file for that number game


def get_categories(data):
    cats = []
    res = data.body.find_all('td', attrs={'class': 'category_name'})
    for ind in range(len(res)):
        cats.append(res[ind].text)
    return cats


def get_clues(data):
    cl = []
    results = data.body.find_all('td', attrs={'class': 'clue_text'})
    for ind in range(len(results)):
        try:
            cor_resp = results[ind].find('em', attrs={'class': 'correct_response'})
            cl[ind // 2].append(cor_resp.text)
        except:
            cl.append([results[ind]['id'], results[ind].text])
    return cl


def correlate(cl, cat):
    lst = []
    for ind in range(len(cat)):
        lst.append([cat[ind]])
        if ind < 6:
            for j in range(5):
                lst[ind].append(cl[ind + j * 6])
        elif ind < 12:
            for j in range(5):
                lst[ind].append(cl[ind + j * 6 + 24])
        else:
            lst[ind].append(cl[-1])
    return lst


# Making a GET request
id = 2721
for i in range(4):
    try:
        url = 'https://j-archive.com/showgame.php?game_id=' + str(id + i)
        r = requests.get(url)
        soup = BeautifulSoup(r.content, 'html.parser')
        parsed_html = soup

        categories = get_categories(parsed_html)
        clues = get_clues(parsed_html)
        game = correlate(clues, categories)

        name = str(id + i) + ".txt"
        f = open(name, "w")

        for item in range(len(game)):
            it = game[item]
            print(it[0])
            try:
                f.write(it[0] + '\n')
            except:
                f.write('problem with this category' + '\n')
            for i in range(len(it) - 1):
                print(it[i + 1])
                try:
                    f.write('Q: ' + it[i + 1][1])
                    f.write(' A: ' + it[i + 1][2] + '\n')
                except:
                    f.write('Q: Problem with this one')
                    f.write(' A: Problem with this one\n')
        f.close()
    except:
        pass

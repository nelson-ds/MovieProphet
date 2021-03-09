import urllib
import sys
import os
import json
import unicodedata
import time
import json
from multiprocessing import Pool


def _fetch(data, errorfile, args={}):
    url_base = 'http://www.omdbapi.com/'
    url_args = urllib.parse.urlencode(args)
    url = url_base + '?' + url_args
    # print url

    try:
        opener = urllib.request.build_opener()
        opener.addheaders = [('User-Agent', 'Chrome/55.0.2883.95')]
        response = opener.open(url)
        # time.sleep(1)

        movie = json.loads(response.read())

        if movie['Response'] and movie['Response'] == 'False':
            errorfile.write(args['y'] + "\t")
            errorfile.write('FALSE\t')
            errorfile.write(args['t'])
            errorfile.write('\n')
            return 0

        data['ratings'].append(movie)
        return 1
    except:
        errorfile.write(args['y'] + "\t")
        errorfile.write('ERROR\t')
        errorfile.write(args['t'])
        errorfile.write('\n')
    return 0


def getMovies(year, errorfile):
    count = 0
    titles_dict = {}

    data = {}
    data['year'] = str(year)
    data['ratings'] = []

    titles = open('year-wise/'+str(year)+'.txt', 'r')

    for title in titles:
        titles_dict[title] = year
        count += 1
    titles.close
    # print str(year) + " :: " + str(len(titles_dict))

    args = {}
    args['r'] = 'json'
    args['plot'] = 'short'
    args['y'] = str(year)

    title_cnt = 0

    for title in titles_dict:
        args['t'] = title.rstrip('\n')
        title_cnt += _fetch(data, errorfile, args)
        count -= 1

    error_count = len(titles_dict) - title_cnt
    # print str(year) + "\t" + str(count) + "\t" + str(title_cnt) + "\t" + str(error_count)
    with open('rating-json/'+str(year)+'-1.json', 'w') as outfile:
        json.dump(data, outfile)
    return title_cnt, error_count


def main(year):
    errorfile = open('errors/' + str(year) + '.txt', 'w')
    title_cnt, error_count = getMovies(year, errorfile)
    print(str(year) + "\t" + str(title_cnt) + "\t" + str(error_count))
    errorfile.close


if __name__ == '__main__':
    p = Pool(50)
    p.map(main, range(1900, 2018))
    p.close()

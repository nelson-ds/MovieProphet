from bs4 import BeautifulSoup  # import beautiful soup scraper
import urllib  # url library
import re  # regular expression package
import pandas as pd  # dataframe for final output
import time  # package for datetime

start_time = time.time()
print("Parsing Box Office Mojo for movie names and id's",
      time.strftime("%Y/%m/%d %H:%M:%S"), "\n")

# Setting up page links to be scraped
#page_names = ['A&p=.htm', 'A&page=2&p=.htm']
page_names = ['NUMB&p=.htm',
              'A&p=.htm', 'A&page=2&p=.htm', 'A&page=3&p=.htm', 'A&page=4&p=.htm', 'A&page=5&p=.htm', 'A&page=6&p=.htm', 'A&page=7&p=.htm', 'A&page=8&p=.htm', 'A&page=9&p=.htm', 'A&page=10&p=.htm',
              'B&p=.htm', 'B&page=2&p=.htm', 'B&page=3&p=.htm', 'B&page=4&p=.htm', 'B&page=5&p=.htm', 'B&page=6&p=.htm', 'B&page=7&p=.htm', 'B&page=8&p=.htm',
              'C&p=.htm', 'C&page=2&p=.htm', 'C&page=3&p=.htm', 'C&page=4&p=.htm', 'C&page=5&p=.htm', 'C&page=6&p=.htm', 'C&page=7&p=.htm',
              'D&p=.htm', 'D&page=2&p=.htm', 'D&page=3&p=.htm', 'D&page=4&p=.htm', 'D&page=5&p=.htm', 'D&page=6&p=.htm',
              'E&p=.htm', 'E&page=2&p=.htm', 'E&page=3&p=.htm', 'E&page=4&p=.htm', 'E&page=5&p=.htm', 'E&page=6&p=.htm', 'E&page=7&p=.htm',
              'F&p=.htm', 'F&page=2&p=.htm', 'F&page=3&p=.htm', 'F&page=4&p=.htm', 'F&page=5&p=.htm', 'F&page=6&p=.htm',
              'G&p=.htm', 'G&page=2&p=.htm', 'G&page=3&p=.htm', 'G&page=4&p=.htm', 'G&page=5&p=.htm', 'G&page=6&p=.htm', 'G&page=7&p=.htm',
              'H&p=.htm', 'H&page=2&p=.htm', 'H&page=3&p=.htm', 'H&page=4&p=.htm', 'H&page=5&p=.htm', 'H&page=6&p=.htm',
              'I&p=.htm', 'I&page=2&p=.htm', 'I&page=3&p=.htm', 'I&page=4&p=.htm', 'I&page=5&p=.htm', 'I&page=6&p=.htm',
              'J&p=.htm', 'J&page=2&p=.htm', 'J&page=3&p=.htm', 'J&page=4&p=.htm',
              'K&p=.htm', 'K&page=2&p=.htm', 'K&page=3&p=.htm', 'K&page=4&p=.htm',
              'L&p=.htm', 'L&page=2&p=.htm', 'L&page=3&p=.htm', 'L&page=4&p=.htm', 'L&page=5&p=.htm',
              'M&p=.htm', 'M&page=2&p=.htm', 'M&page=3&p=.htm', 'M&page=4&p=.htm', 'M&page=5&p=.htm', 'M&page=6&p=.htm', 'M&page=7&p=.htm',
              'N&p=.htm', 'N&page=2&p=.htm', 'N&page=3&p=.htm', 'N&page=4&p=.htm', 'N&page=5&p=.htm',
              'O&p=.htm', 'O&page=2&p=.htm', 'O&page=3&p=.htm', 'O&page=4&p=.htm', 'O&page=5&p=.htm',
              'P&p=.htm', 'P&page=2&p=.htm', 'P&page=3&p=.htm', 'P&page=4&p=.htm', 'P&page=5&p=.htm', 'P&page=6&p=.htm', 'P&page=7&p=.htm',
              'Q&p=.htm',
              'R&p=.htm', 'R&page=2&p=.htm', 'R&page=3&p=.htm', 'R&page=4&p=.htm', 'R&page=5&p=.htm', 'R&page=6&p=.htm',
              'S&p=.htm', 'S&page=2&p=.htm', 'S&page=3&p=.htm', 'S&page=4&p=.htm', 'S&page=5&p=.htm', 'S&page=6&p=.htm', 'S&page=7&p=.htm', 'S&page=8&p=.htm', 'S&page=9&p=.htm', 'S&page=10&p=.htm', 'S&page=11&p=.htm', 'S&page=12&p=.htm', 'S&page=13&p=.htm',
              'T&p=.htm', 'T&page=2&p=.htm', 'T&page=3&p=.htm', 'T&page=4&p=.htm', 'T&page=5&p=.htm', 'T&page=6&p=.htm', 'T&page=7&p=.htm', 'T&page=8&p=.htm',
              'U&p=.htm', 'U&page=2&p=.htm',
              'V&p=.htm', 'V&page=2&p=.htm', 'V&page=3&p=.htm',
              'W&p=.htm', 'W&page=2&p=.htm', 'W&page=3&p=.htm', 'W&page=4&p=.htm', 'W&page=5&p=.htm', 'W&page=6&p=.htm',
              'X&p=.htm',
              'Y&p=.htm', 'Y&page=2&p=.htm',
              'Z&p=.htm', 'Z&page=2&p=.htm']
links = ['http://www.boxofficemojo.com/movies/alphabetical.htm?letter=' +
         pn for pn in page_names]
print("Reading URLs...\n")
pages_search = list(map(urllib.request.urlopen, links))  # Open URL

soups_search, movie_tags, movie_list, merged_movie_list, counter = [
], [], {}, {}, 0  # Initialize variables

# Read all URLs in Beautiful Soup
for page in pages_search:
    print("Scraping page: ", page_names[counter])
    soups_search.append(BeautifulSoup(page.read(), "html.parser"))
    counter += 1

# Navigate soup to get content
print()
counter = 0
for soup in soups_search:
    # Extract only the blocks of HTML code containing the movie names and id by navigating through soup
    movie_tags = list(soup.find_all('a', href=re.compile(r"/movies/\?id=")))

    # Extract the movie names and id from blocks of HTML code
    name_id = {}
    for movies in movie_tags:
        m_id = re.search(r"<b>(.)*</b>", str(movies))
        if m_id:
            key = str(m_id.group())[3:-4]
            val = str(re.search(r"id=(.)*.htm|.HTM", str(movies)).group())[3:]
            name_id[key] = val
            # Writing all names and id to single dictionary
            merged_movie_list[key] = val

    # Writing names and id to single dictionary with reference of page name
    movie_list[page_names[counter]] = name_id
    print('Parsing page: ' + str(page_names[counter]) + '; Obtained '
          + str(len(movie_list[page_names[counter]])) + ' movies')
    counter += 1

print("Obtained a total of ", str(len(merged_movie_list)), " movies")
print("\nFinished parsing Box Office Mojo at",
      time.strftime("%Y/%m/%d %H:%M:%S"))
print("Total time taken: " + str(round(time.time() - start_time, 2)) + " seconds")

output1 = pd.DataFrame(movie_list)
output2 = pd.Series(merged_movie_list, name='MovieID')
output1.to_csv("bom_name_id1.csv")
output2.to_csv("bom_name_id2.csv")

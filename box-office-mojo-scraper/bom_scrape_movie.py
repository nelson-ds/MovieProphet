# Nelson Dsouza; Capstone Project - Movie Prophet; 1/5/2017; Box Office Mojo SCRAPER

from bs4 import BeautifulSoup;  # import beautiful soup scraper
import urllib.request as urllib2
import re  # regular expression package
import csv
import pandas as pd;  # dataframe for final output
import time  # package for datetime
import http.client
http.client.HTTPConnection._http_vsn = 10
http.client.HTTPConnection._http_vsn_str = 'HTTP/1.0'

start_time = time.time()
print("Parsing Box Office Mojo for movie metadata", time.strftime("%Y/%m/%d %H:%M:%S"), "\n")

# User input for movie index and loop increment; Retrieves movie from start_index to end_index-1
mov_str_ind, mov_end_ind, mov_inc_ind = 0, 16828, 50
counter = mov_str_ind+0

# Initializing global variables
movie_nm, movie_id, str_mov_at, mov_tot = [], [], mov_str_ind+0, mov_end_ind - mov_str_ind
summary, players, tlg, ds, awards, genre, fran, chart = [], [], [], [], [], [], [], []
output = pd.DataFrame(columns=['Link','Summary', 'Players', 'Total Lifetime Gross', 'Domestic Summary',
                               'Awards', 'Genre', 'Franchise', 'Chart'], index=movie_nm[mov_str_ind:mov_end_ind])

with open('name_id_bom.csv', newline='') as inputfile:  # Read movie names and corresponding bom id
    for row in csv.reader(inputfile):
        movie_nm.append(row[0])
        movie_id.append(row[1])
all_links_movies = ['http://www.boxofficemojo.com/movies/?id=' + m_id for m_id in movie_id]  # Convert id to link

# Iterate till user inputted end of movie is reached
while str_mov_at < mov_end_ind:
    end_ctr_at = counter + mov_inc_ind - 1  # Updating end index based on increment
    if (counter + mov_inc_ind) > mov_end_ind:  # Taking care of case when increment greater than total movie end index
        mov_inc_ind = mov_end_ind - str_mov_at  # Update counter accordingly
        end_ctr_at = str_mov_at + mov_inc_ind - 1  # Exit when no more movies left

    links_movies, soups_movies = all_links_movies[str_mov_at: str_mov_at + mov_inc_ind], []
    print('* Scraping', counter, 'to', end_ctr_at, 'web pages out of', mov_end_ind-1, '*\n',
          movie_nm[str_mov_at:str_mov_at + mov_inc_ind])

    i = 1
    while True and i < 6:
        try:
            pages_movies = list(map(urllib2.urlopen, links_movies))  # Open URL
        except Exception:
            print("Error faced. Retrying", i, "time")
            i+=1
            continue
        break

    for page in pages_movies:  # Read all URLs in Beautiful Soup
        soups_movies.append(BeautifulSoup(page.read(), "html.parser"))

    for idx, soup in enumerate(soups_movies):
        print('\t\t\tParsing movie:', movie_nm[str_mov_at + idx], '-', links_movies[idx])
        # Extract only the blocks of HTML code containing the summary by navigating through soup
        str_soup = str(soup)
        summary_tags = soup.find_all('table', bgcolor="#dcdcdc")
        summary_titles = re.compile(">([\w|\s|,|.|']*):").findall(str(summary_tags[0]))
        sm_vals = summary_tags[0].find_all('b')
        # Since we are pulling values in bold, domestic lifetime gross is in bold and will be pulled
        summary_values = [re.sub('Domestic Lifetime Gross','',
                                      sm_vals[x].get_text()) for x in range(len(sm_vals))]
        summary_dict = {}
        for i in range(len(summary_values)):  # Append summary values to main list
            summary_dict[summary_titles[i]] = summary_values[i]
        # The column 'Domestic Total as of' has date associated with it which we don't want so removing it
        dtao = {k: v for (k, v) in summary_dict.items()
                if any(k.startswith("Domestic Total as of") for k2 in summary_dict.keys())}
        if bool(dtao):
            for val in list(dtao.keys()):
                summary_dict['Domestic Total Gross'] = summary_dict.pop(val)
        summary.append(summary_dict)

        # Extract only the blocks of HTML code containing the players by navigating through soup
        player_tags = list(soup.find_all('a', href=re.compile(r"/people/\?view")))
        if player_tags:
            player_titles = [str(re.search(r"view=(.)*\&", str(x)).group())[5:-1] for x in player_tags]
            pl_vals = re.compile("</table></div></div></td>(.*)").findall(str_soup)
            pl_vals = pl_vals[0].split(':')
            players_dict, player_values = {}, []
            for i in range(1, len(pl_vals)):
                # Strip empty string and values which are not required
                player_values.append(list(filter(lambda name: name.strip() and name not in
                    ['Cinematographer','* Denotes minor role'], re.compile(">([\w|\s|.|*|-|']*)<").findall(pl_vals[i]))))
            for i in range(len(player_titles)):  # Append people values to main list
                players_dict[player_titles[i]] = player_values[i]
            players.append(players_dict)
        else: players.append({'Players': 'No Player Information'})

        # Extract only the blocks of HTML code containing the mp_box contents by navigating through soup
        mpb_tags = soup.findAll("div", {"class": "mp_box_content"})

        # If movie has Total Lifetime Gross information, it will be in first mp_box; retrieve it
        mpb_tags_pad = 0  # This will track the number of mbp_tags traversed
        if re.compile("Total Lifetime Grosses").findall(str_soup):
            str_mpb_tags0 = str(mpb_tags[mpb_tags_pad])
            tlg_titles = re.compile(">([\w]*):").findall(str_mpb_tags0)
            tlg_values = re.compile("[$|n/a][\w|\s|,|/]*<", ).findall(str_mpb_tags0)
            tlg_dict = {}
            for i in range(len(tlg_titles)):  # Append people values to main list
                tlg_dict[tlg_titles[i]] = tlg_values[i][0:-1]
            tlg.append(tlg_dict)
            mpb_tags_pad += 1
        else: tlg.append({'Total Lifetime Gross': 'No Total Lifetime Gross Information'})

        # If movie has Domestic Summary Information, it will be in second mp_box; retrieve it
        if re.compile("Domestic Summary").findall(str_soup):
            str_mpb_tags1 = str(mpb_tags[mpb_tags_pad])
            ds_titles_values = re.compile(">([\w|\s|%]*):([\w|\s|/|<|>|$|,|.|']*)</tr>").findall(str_mpb_tags1)
            # Below code will also extract live movie release date eg - la la land
            # ds_tv = re.compile(">([\w|\s|%]*):(.*?)</tr>", re.DOTALL).findall(str_mpb_tags1)
            ds_dict = {}
            for i in range(len(ds_titles_values)):  # Append people values to main list
                ds_dict[ds_titles_values[i][0].replace(u'\xa0', ' ')] = \
                    re.sub('</td>|<td>|</a>|\n|', '', ds_titles_values[i][1]).replace(u'\xa0', ' ')
            ds.append(ds_dict)
            mpb_tags_pad += 1
        else: ds.append({'Domestic Summary': 'No Domestic Summary Information'})

        # If movie has Award Information, it will be in third mp_box; retrieve it
        if len(mpb_tags) > mpb_tags_pad and len(str(mpb_tags[mpb_tags_pad])) == 51:
            mpb_tags_pad += 1 # In some pages, presence of extra empty tag (of length 51) is detected so we skip it
        if re.compile("Academy Awards®").findall(str_soup):
            awards.append(re.sub('</b>|<b>', '', str(mpb_tags[mpb_tags_pad].find_all('b')[0])))
            mpb_tags_pad += 1
        else: awards.append('No Academy Awards Information')

        # If movie has Genre Information, it will be in fourth mp_box; retrieve it
        if len(mpb_tags) > mpb_tags_pad and re.compile("Genre").findall(str(mpb_tags[mpb_tags_pad])):
            genre_titles_values = list(mpb_tags[mpb_tags_pad].find_all('tr', bgcolor = re.compile('#([\w|\s]*)')))
            genre_titles_values = [re.sub('<(.*?)>', '', str(item)) for item in genre_titles_values]
            genre_dict = {}
            for i in range(len(genre_titles_values)):
                genre_dict[genre_titles_values[i].rsplit('\n')[0]] = genre_titles_values[i].rsplit('\n')[1]
            genre.append(genre_dict)
            mpb_tags_pad += 1
        else: genre.append({'Genre': 'No Genre Information'})

        # If movie has Franchise Information, it will be in fifth mp_box; retrieve it
        if len(mpb_tags) > mpb_tags_pad and re.compile("Franchise").findall(str(mpb_tags[mpb_tags_pad])):
            fran_titles_values = list(mpb_tags[mpb_tags_pad].find_all('tr', bgcolor = re.compile('#([\w|\s]*)')))
            fran_titles_values = [re.sub('<(.*?)>', '', str(item)) for item in fran_titles_values]
            fran_dict = {}
            for i in range(len(fran_titles_values)):
                fran_dict[fran_titles_values[i].rsplit('\n')[0]] = fran_titles_values[i].rsplit('\n')[1]
            fran.append(fran_dict)
            mpb_tags_pad += 1
        else: fran.append({'Franchise': 'No Franchise Information'})

        # If movie has Chart Information, it will be in sixth mp_box; retrieve it
        if len(mpb_tags) > mpb_tags_pad and re.compile("Chart").findall(str(mpb_tags[mpb_tags_pad])):
            chart_titles_values = list(mpb_tags[mpb_tags_pad].find_all('tr', bgcolor = re.compile('#([\w|\s]*)')))
            chart_titles_values = [re.sub('<(.*?)>', '', str(item)) for item in chart_titles_values]
            chart_dict = {}
            for i in range(len(chart_titles_values)):
                chart_dict[chart_titles_values[i].rsplit('\n')[0]] = chart_titles_values[i].rsplit('\n')[1]
            # The column 'Highest All Time Rank' has date associated with it which we don't want so removing it
            hatr = {k: v for (k, v) in chart_dict.items()
                 if any(k.startswith("Highest All Time Rank") for k2 in chart_dict.keys())}
            if bool(hatr):
                for val in list(hatr.keys()):
                    chart_dict['Highest All Time Rank'] = chart_dict.pop(val)
            chart.append(chart_dict)
            mpb_tags_pad += 1
        else: chart.append({'Chart': 'No Chart Information'})

        # Adding movie information to dataframe
        output.loc[movie_nm[str_mov_at + idx]] = pd.Series({'Link': links_movies[idx],
                                                            'Summary': summary[-1], 'Players': players[-1],
                                                            'Total Lifetime Gross': tlg[-1], 'Domestic Summary': ds[-1],
                                                            'Awards': awards[-1], 'Genre': genre[-1],
                                                            'Franchise': fran[-1], 'Chart': chart[-1]})

    print('\t\tWriting output of movies from', counter, 'to', end_ctr_at, 'out of', mov_end_ind-1, '\n')
    output.to_csv('tab_all_bom.csv')
    counter += mov_inc_ind
    str_mov_at += mov_inc_ind

tab_summary = pd.DataFrame([sm for sm in summary])
tab_players = pd.DataFrame([pl for pl in players])
tab_tlg = pd.DataFrame([tl for tl in tlg])
tab_domsum = pd.DataFrame([d for d in ds])
tab_genre = pd.DataFrame([gn for gn in genre])
tab_franchise = pd.DataFrame([fr for fr in fran])
tab_chart = pd.DataFrame([ch for ch in chart])

lnk = all_links_movies[mov_str_ind: mov_end_ind]
mov = movie_nm[mov_str_ind: mov_end_ind]

tab_summary["Awards"] = awards
tab_summary["Link"] = lnk
tab_summary["Name"] = mov

tab_players["Link"] = lnk
tab_tlg["Link"] = lnk
tab_domsum["Link"] = lnk
tab_genre["Link"] = lnk
tab_franchise["Link"] = lnk
tab_chart["Link"] = lnk

tab_players["Name"] = mov
tab_tlg["Name"] = mov
tab_domsum["Name"] = mov
tab_genre["Name"] = mov
tab_franchise["Name"] = mov
tab_chart["Name"] = mov

tab_summary.to_csv('tab_summary.csv')
tab_players.to_csv('tab_players.csv')
tab_tlg.to_csv('tab_tlg.csv')
tab_domsum.to_csv('tab_domsum.csv')
tab_genre.to_csv('tab_genre.csv')
tab_franchise.to_csv('tab_franchise.csv')
tab_chart.to_csv('tab_chart.csv')

# print('\n* Retrieved Information is: *')
# movie_data, temp_ind, str_mov_at = [], 0, mov_str_ind+0
# for i in range(mov_tot):
#     movie_data.append([movie_nm[str_mov_at], all_links_movies[str_mov_at], summary[i], players[i], tlg[i], ds[i],
#                       awards[i], genre[i], fran[i], chart[i]])
#     temp_ind += 1
#     str_mov_at+=1
#     print(movie_data[-1])

print("\nFinished scraping Box Office Mojo at", time.strftime("%Y/%m/%d %H:%M:%S"))
print("Total movies scraped:", mov_tot)
print("Total time taken: " + str(round(time.time() - start_time,2)) + " seconds")
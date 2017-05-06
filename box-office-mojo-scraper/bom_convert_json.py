import pandas as pd
import csv
import re

df = pd.DataFrame.from_csv('bom.csv')

def split(i, ind):
    op = []
    if ind not in [2]:  # Splitting logic if data in Dictionary format
        m = [re.sub(r'[\'\"]', '', x.strip()) for x in re.sub(r'[{}]', '', df.ix[i, ind]).split("',")]
    else:  # Splitting logic if data in string format
        m = [re.sub(r'[\'\]\[\"]', '', x.strip()) for x in re.sub(r'[{}]', '', df.ix[i, ind]).split("'], ")]
    for item in m:
        sp = item.split(':')
        op.append(['\t\t\t\t\t"' + sp[0].replace(" ", "") + '": {"S":' + '"' +
                   str(sp[1].strip().encode('ascii', 'ignore')) + '"},'])
    return op


def write_data(i, set_end):
    print(df.index[i])
    if set_end: en_lst = '\t\t}'
    else: en_lst = '\t\t},'
    st = [
        ['\t\t{'],
        ['\t\t\t\"PutRequest\": {'],
        ['\t\t\t\t\"Item\": {'],
        ['\t\t\t\t\t\"Name\": {\"S\":\"' + re.sub(r'[\"]', '', str(df.index[i].encode('ascii', 'ignore'))) + '\"},'],
        ['\t\t\t\t\t\"Link\": {\"S\":\"' + df.ix[i, 0] + '\"},'],
    ]
    md = [
        ['\t\t\t\t\t\"Awards\": {\"S\":\"' + df.ix[i, 5] + '\"},'],
        ['\t\t\t\t\t\"GenreRank\": {\"S\":\"' + re.sub(r'[\"]', '', df.ix[i, 6]) + '\"},'],
        ['\t\t\t\t\t\"Franchise\": {\"S\":\"' + re.sub(r'[\"]', '', df.ix[i, 7]) + '\"},'],
        ['\t\t\t\t\t\"Chart\": {\"S\":\"' + re.sub(r'[\"]', '', df.ix[i, 8]) + '\"}'],
    ]
    en = [
        ['\t\t\t\t}'],
        ['\t\t\t}'],
        [en_lst]
    ]
    return [st, md, en]


mini, maxi, inc = 0, 16828, 25
for j in range(mini, maxi, inc):  # Writing data to json files with maximum 25 items per file
    set_end = False
    with open('bom/bom_' + str(j) + '.json', 'w', newline='') as fp:
        a = csv.writer(fp, delimiter='~', quoting=csv.QUOTE_NONE, quotechar="~")
        fst = [['{'], ['\t\"bom\":['], ]
        lst = [['\t]'], ['}']]
        a.writerows(fst)

        if j+inc > maxi: rng = maxi - j
        else: rng = 25

        for k in range(rng):
            if k == rng-1: set_end = True
            i = j+k
            dat = write_data(i, set_end)
            all_data = dat[0] + split(i, 1) + split(i, 2) + split(i, 3) + split(i, 4) + dat[1] + dat[2]
            a.writerows(all_data)
        a.writerows(lst)
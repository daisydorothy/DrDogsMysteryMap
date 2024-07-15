import re, csv, os, pprint as pp


# Get data of where StreetView has covered, according to Wikipedia
def get_wikipedia_SV_coverage_data():
    wikilist = read_wiki_csv()
    wikilist, sv_countries = clean_wiki_csv(wikilist)
    return wikilist, sv_countries

def read_wiki_csv(): # get csv
    wikilist = []
    with open('latlng/sources/wikipedia_list_of_coverage.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            wikilist.append(row)
    return(wikilist)

def clean_wiki_csv(wikilist): # clean csv (i copied and pasted straight from wiki into a csv hehe)
    countries = []
    footnote = '\[\d+\]'
    fakespace =  '\\xa0'

    for row in wikilist:
        row[0] = re.sub(footnote, '', row[0])
        row[0] = re.sub(fakespace, ' ', row[0])
        row[0] = row[0].strip()
        row[0] = row[0].replace('*', '').upper()
        countries.append(row[0])
    countries = countries[1:] # get rid of first entry - just col title
    return wikilist, countries


# Get list of world cities latitudes and longitudes, dl'd from Simplemaps.com (free version)
def get_worldcities_latlngs():
    latlngs = read_latlngs()
    latlng_cs = get_countries(latlngs)
    return latlngs, latlng_cs

def read_latlngs(): # read csv
    latlngs = []
    with open('latlng/sources/simplemaps/worldcities.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            latlngs.append(row)
    return(latlngs)

# get separate list of which countries are covered - for easy pruning in next step
def get_countries(latlngs):
    latlng_cs = []
    for row in latlngs:
        row[4] = row[4].upper()
        if row[4].upper() not in latlng_cs: # just get unique boys
            latlng_cs.append(row[4].upper()) # this it the country column
    latlng_cs = latlng_cs[1:]
    return latlng_cs


# remove all entries form worldcities list that we know we won't have SV entries for
def prune_latlngs(sv_countries, latlng_countries, latlngs):
    # get list of countries that are covered by SV, and we have lat lngs for
    list_same = [country for country in latlng_countries if country in sv_countries]
    #sense check -  get list of countries not covered by google street view
    #list_diff = [country for country in latlng_countries if country not in sv_countries]
    #print(list_diff) # yeah seems pretty reasonable - but S Korea is omitted by mistake

    # prune further
    # remove countries that we likely arent gonna get any data for bcos SV vv limited (according to wikipedia)
    ignore_list = ['IRAQ', 'PAKISTAN', 'NEPAL', 'MADAGASCAR', 'TANZANIA', 'EGYPT']
    cleaner_list = [country for country in list_same if country not in ignore_list]

    sv_covered_latlngs = [latlngs[0]] # get oriignal headings of latlngs

    for row in latlngs:
        if row[4] in cleaner_list:
            sv_covered_latlngs.append(row)

    #hand prune
    # clean it up one more time, based on SV wiki
    cleanest_list = []
    for row in sv_covered_latlngs:
        country = row[4]
        city = row[0]
        capital_status = row[8]
        if country == "BELARUS":
            if city == "Minsk":
                cleanest_list.append(row)
        elif country == "CHINA":
            if city in ["Beijing", "Shanghai", "Hangzhou", "Guilin", "Lhasa", "Guangzhou", "Chengdu", "Shenzen", "Xi An"]:
                cleanest_list.append(row) # wiki says only major tourist spots covered; chose top 10
        elif country == "INDIA":
            if capital_status != "":
                cleanest_list.append(row) # wiki says only major cities, so lets just use capital status
        elif country == "DOMINICAN REPUBLIC":
            if city == "Santo Domingo" or city == "Santiago":
                cleanest_list.append(row)
        else:
            cleanest_list.append(row)
    return(cleanest_list)



wikilist, sv_countries = get_wikipedia_SV_coverage_data()
latlngs, latlng_countries = get_worldcities_latlngs()
clean_latlng_list = prune_latlngs(sv_countries, latlng_countries, latlngs)


with open('latlng/sv_latlng_cities.csv', 'w') as csvfile:
    csvwriter = csv.writer(csvfile)
    for row in clean_latlng_list:
        csvwriter.writerow(row)




# # where is the bulk?
# country_count = {}
# for row in clean_latlng_list:
#         if row[4] not in country_count.keys():
#             country_count[row[4]] = 1
#         else:
#             country_count[row[4]] += 1
# pp.pprint(country_count)

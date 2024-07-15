import csv, requests, json, pprint as pp

# Check which of the latlngs in sv_latlng_cities.csv has street view data
# want to make sure there's a street view to serve our users! (/single user, lol)
# do so by asking the google streetview api for metadata assoc. with a given lat/lng (Free to do)

def get_latlng_data(): # get the data from the csv (yes i should pickle this)
    latlngs = []
    with open('latlng/sv_latlng_cities.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            city_ascii = row[1]
            country = row[4]
            lat = row[2]
            lng = row[3]
            id = row[-1]
            newrow = [lat, lng, city_ascii, country, id]
            latlngs.append(newrow)
    return(latlngs)

def make_latlngs_readable(latlngs): # format them for the API
    for row in latlngs:
        charstring = row[0]+ ', ' +row[1]
        row.append(charstring)


def identify_ok_latlngs(latlngs): # for each entry, ask API for metadata
    meta_base = 'https://maps.googleapis.com/maps/api/streetview/metadata?'
    key = 'INSERT KEY HERE'
    with open("latlng/latlng_metadata_test.csv", 'w') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(latlngs[0])
        for row in latlngs[1:]:
            params = {'key': key, 'location': row[-1]}
            meta_response = requests.get(meta_base, params = params)
            row.append(meta_response.json()["status"])
            csvwriter.writerow(row) # write out to file as running in case connection drops



latlngs = get_latlng_data()
make_latlngs_readable(latlngs)
identify_ok_latlngs(latlngs_test)

# # Oh dear! my connection dropped at around 28k requests.
# # lets figure out what we're missing, and get the rest of the metadata
#
# full_latlngs = latlngs
#
# processed_latlngs = []
# with open('latlng/latlng_metadata_p1.csv', 'r') as file:
#     reader = csv.reader(file)
#     for row in reader:
#         processed_latlngs.append(row[0:-1])
#
# latlngs_toprocess = [x for x in full_latlngs if x not in processed_latlngs]
#
# # sense check
# print(len(full_latlngs))
# print(len(processed_latlngs))
# print(len(latlngs_toprocess))
#
#
# #identify_ok_latlngs(latlngs_toprocess)
#
# processed_latlngs_v2 = []
# with open('latlng/latlng_metadata_p2.csv', 'r') as file:
#     reader = csv.reader(file)
#     for row in reader:
#         processed_latlngs_v2.append(row[0:-1])
#
# print(processed_latlngs_v2[2])
# latlngs_toprocess_v2 = [x for x in latlngs_toprocess if x not in processed_latlngs_v2]
# print(len(latlngs_toprocess_v2))
#
#
# #identify_ok_latlngs(latlngs_toprocess_v2)
#
#
# processed_latlngs_v3 = []
# with open('latlng/latlng_metadata_p3.csv', 'r') as file:
#     reader = csv.reader(file)
#     for row in reader:
#         processed_latlngs_v3.append(row[0:-1])
#
# print(processed_latlngs_v3[2])
# latlngs_toprocess_v3 = [x for x in latlngs_toprocess if x not in processed_latlngs_v3 and x not in processed_latlngs_v2]
# print(len(latlngs_toprocess_v3))
#
#
# identify_ok_latlngs(latlngs_toprocess_v3)
#
#
# # For reference:
# # metaparams = [{'key': key, 'location': testloc}]
# # testloc = '37.773972, -122.431297'

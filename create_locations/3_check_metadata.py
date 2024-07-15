import csv, json

# take the file annotated with metadata; keep those entries WITH, toss out those w.OUT

metadata = []
with open('latlng/latlng_metadata_full.csv', 'r') as file:
    reader = csv.reader(file)
    for row in reader:
        metadata.append(row)

ok_metadata = []
for m in metadata:
    if m[-1] == "OK" or m[-1] == 'status':
        ok_metadata.append(m)


country_count = {}
for m in ok_metadata:
    if m[3] not in country_count.keys():
        country_count[m[3]] = 1
    else:
        country_count[m[3]] += 1

with open('latlng/cities_checked.csv', 'w') as csvfile:
    csvwriter = csv.writer(csvfile)
    for row in ok_metadata:
        csvwriter.writerow(row)


import json
with open('cities_test.json', 'w') as f:
    json.dump(ok_metadata, f)
#json_string = json.dumps(ok_metadata)
#print(json_string)

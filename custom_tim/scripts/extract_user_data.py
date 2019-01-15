import csv

with open('../All_users_eternal_swolemates.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    user_list = []
    for row in csv_reader:
        if line_count == 0:
            print('Column names are:')
            print(", ".join(row))
            line_count += 1
        else:
            user_list.append(row)
            line_count += 1
    print('Processed ' + str(line_count) + ' lines.')

followers_list = []
followed_by_list = []
not_following_back = []
for row in user_list:
    if row[6] == 'TRUE':
        followed_by_list.append(row)
    if row[7] == 'TRUE':
        followers_list.append(row)
    if row[6] == 'TRUE' and row[7] == 'FALSE':
        not_following_back.append(row[1])
    if row[11] == 'TRUE':
        print row[11] + ' has blocked you'

print not_following_back
print str(len(not_following_back)) + ' users not following you back'

print '\nwriting not_following_back-ers to csv...'
with open('../not_following_back.csv', mode='w') as _file:
    _writer = csv.writer(_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    for row in not_following_back:
        _writer.writerow([row,])
        print row

with open('../not_following_back.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    for row in csv_reader:
        print row
print('\ndone')

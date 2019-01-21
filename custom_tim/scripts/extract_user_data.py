import csv

filename = '../data/All_users_eternal_swolemates_20190121_1639.csv'
with open(filename) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    user_list = []
    for row in csv_reader:
        if line_count == 0:
            print('Column names are:')
            print(", ".join(row))
            col_names = row
            line_count += 1
        else:
            user_list.append(row)
            line_count += 1
    print('Processed ' + str(line_count) + ' lines.')

followers_list = []
following_list = []
not_following_back = []

try:
    username_row = col_names.index('username')
    followers_row = col_names.index('user_followed_by')
    following_row = col_names.index('user_follows')
except ValueError:
    username_row = -1
    followers_row = -1
    following_row = -1

for row in user_list:
    if following_row != -1 and followers_row != -1:
        if row[following_row] == 'TRUE':
            following_list.append(row)
        if row[followers_row] == 'TRUE':
            followers_list.append(row)
        if row[following_row] == 'TRUE' and row[followers_row] == 'FALSE':
            not_following_back.append(row[username_row])

print '\nnum followers: ' + str(len(followers_list))
print 'num following: ' + str(len(following_list))
print str(len(not_following_back)) + ' users not following you back'

save_losers = True
if save_losers:
    print '\nwriting not_following_back-ers to csv...'
    with open('../data/not_following_back.csv', mode='w') as _file:
        _writer = csv.writer(_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for row in not_following_back:
            _writer.writerow([row,])

    with open('../data/not_following_back.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            print row
    print('\ndone')

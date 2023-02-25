import os

if os.path.exists('nick_usage.csv'):
    os.remove('nick_usage.csv')

file = open('nick_usage.csv', 'w')
file.write('pull_date,pull_time,location,update_time,pct_full,date,time,wday\n')

file.close()

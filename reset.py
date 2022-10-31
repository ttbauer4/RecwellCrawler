import os

os.remove('nick_usage.csv')

file = open('nick_usage.csv', 'w')
file.write('date,pull_time,wday,location,update_time,pct_full,time\n')

file.close()
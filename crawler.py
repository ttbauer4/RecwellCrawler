import csv
from array import array
from time import strftime
import time
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from datetime import datetime, timedelta

# Define tracker attributes
l1 = []
l2 = []
l3 = []
pHouse = []
track = []
aqCenter = []
trackerArrays = [l1, l2, l3, pHouse, track, aqCenter]

'''
write_to_csv writes arrays to a CSV file as rows

:param path: path to CSV file
:param delim: string delimiter for writing arrays to rows
:param *args: variable number of array arguments to be written to given CSV
'''
def write_to_csv(path: str, delim: str, arr: array):
    with open(path, 'a') as file:
        mywriter = csv.writer(file, delimiter=',')
        mywriter.writerows(arr)

options = Options()
options.headless = True
driver = webdriver.Chrome(options=options)

driver.set_page_load_timeout(60)

driver.get('https://recwell.wisc.edu/liveusage/')
time.sleep(5)

soup = bs(driver.page_source, 'html.parser')

i = 0
use = 0.0
cap = 0.0
now = datetime.now()
for x in soup.find_all('div', class_ = 'live-tracker')[:-6]:
    trackerArrays[i].append(strftime("%m-%d-%Y", now.timetuple()))
    trackerArrays[i].append(strftime("%H:%M", now.timetuple()))
    trackerArrays[i].append(x.find('p', class_ = 'tracker-location').text)
    updateTime = x.find('p', class_ = 'tracker-update-time').text
    trackerArrays[i].append(updateTime)
    
    use = float(x.find('span', class_ = 'tracker-current-count pending').text)
    cap = float(x.find('span', class_ = 'tracker-max-count').text)
    trackerArrays[i].append('%.2f' % (float(use / cap) * 100.0))

    if updateTime.strip() == "Currently closed" or updateTime.strip() == "Updated over an hour ago":
        actTime = "n/a"
        trackerArrays[i].append(actTime)
        trackerArrays[i].append(actTime)
        trackerArrays[i].append(actTime)
    elif updateTime.strip() == "Updated an hour ago":
        actTime = (now - timedelta(hours=1)).timetuple()
        trackerArrays[i].append(strftime("%m-%d-%Y", actTime))
        trackerArrays[i].append(strftime("%H:%M", actTime))
        trackerArrays[i].append(strftime("%A", actTime))
    elif updateTime.strip() == "Updated moments ago":
        actTime = (now - timedelta()).timetuple()
        trackerArrays[i].append(strftime("%m-%d-%Y", actTime))
        trackerArrays[i].append(strftime("%H:%M", actTime))
        trackerArrays[i].append(strftime("%A", actTime))
    else:
        strDiff = updateTime[updateTime.index("Updated")+7:updateTime.index("Updated")+10].strip()
        actTime = (now - timedelta(minutes=int(strDiff))).timetuple()
        trackerArrays[i].append(strftime("%m-%d-%Y", actTime))
        trackerArrays[i].append(strftime("%H:%M", actTime))
        trackerArrays[i].append(strftime("%A", actTime))

    i+=1

write_to_csv('/home/ttbauer/RecwellCrawler/nick_usage.csv', ',', trackerArrays)

driver.close()

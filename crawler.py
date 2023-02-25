import csv
from array import array
from time import strftime
import time
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from datetime import datetime, timedelta

rows = [[], [], [], [], [], [], [], [], []] # represents the rows in output table
outputFilePath = "/home/ttbauer/RecwellCrawler/nick_usage.csv" # an absolute or relative path to the output file

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

try:
    options = Options()
    options.add_argument('headless') # make headless
    driver = webdriver.Chrome(options=options) # apply options
    driver.set_page_load_timeout(60) # throw TimeouException if page is not loaded after 1 minute

    driver.get('https://recwell.wisc.edu/liveusage/')
    time.sleep(5) # wait for JS elements to load
    soup = bs(driver.page_source, 'html.parser') # retrieve page source

    now = datetime.now()
    locations = soup.find_all('div', class_ = 'live-tracker')[:-6] # tag containing info by location

    for i in range(len(rows)):
        rows[i].append(strftime("%m-%d-%Y", now.timetuple())) # append pull date as mm/dd/yy
        rows[i].append(strftime("%H:%M", now.timetuple())) # append pull time as hh:mm in 24-hr format
        rows[i].append(locations[i].find('p', class_ = 'tracker-location').text) # append location name
        updateTime = locations[i].find('p', class_ = 'tracker-update-time').text # "last updated" text
        rows[i].append(updateTime) # append "last updated" text
        use = float(locations[i].find('span', class_ = 'tracker-current-count pending').text)
        cap = float(locations[i].find('span', class_ = 'tracker-max-count').text)
        rows[i].append('%.2f' % (float(use / cap) * 100.0)) # calculate and append percentage full

        if updateTime.strip() == "Currently closed" or updateTime.strip() == "Updated over an hour ago":
            rows[i].append("n/a")
            rows[i].append("n/a")
            rows[i].append("n/a")
        elif updateTime.strip() == "Updated an hour ago":
            actTime = (now - timedelta(hours=1)).timetuple() # calculate actual updated time
            rows[i].append(strftime("%m-%d-%Y", actTime)) # append actual updated time in mm/dd/yy format
            rows[i].append(strftime("%H:%M", actTime)) # append actual updated time in hh:mm format
            rows[i].append(strftime("%A", actTime)) # append actual updated time in weekday format
        elif updateTime.strip() == "Updated moments ago":
            actTime = (now - timedelta()).timetuple() # calculate actual updated time
            rows[i].append(strftime("%m-%d-%Y", actTime)) # append actual updated time in mm/dd/yy format
            rows[i].append(strftime("%H:%M", actTime)) # append actual updated time in hh:mm format
            rows[i].append(strftime("%A", actTime)) # append actual updated time in weekday format
        else:
            strDiff = updateTime[updateTime.index("Updated")+7:updateTime.index("Updated")+10].strip()
            actTime = (now - timedelta(minutes=int(strDiff))).timetuple() # calculate actual updated time
            rows[i].append(strftime("%m-%d-%Y", actTime)) # append actual updated time in mm/dd/yy format
            rows[i].append(strftime("%H:%M", actTime)) # append actual updated time in hh:mm format
            rows[i].append(strftime("%A", actTime)) # append actual updated time in weekday format

except TimeoutException:
    for x in (rows):
        x[0] = strftime("%m-%d-%Y", now.timetuple()) # append pull date as mm/dd/yy
        x[1] = strftime("%H:%M", now.timetuple()) # append pull time as HH:MM in 24-hr format
        x[2] = "TIMEOUT ERROR"
        x[3] = "TIMEOUT ERROR"
        x[4] = "TIMEOUT ERROR"
        x[5] = "TIMEOUT ERROR"
        x[6] = "TIMEOUT ERROR"

except:
    for x in (rows):
        x[0] = strftime("%m-%d-%Y", now.timetuple()) # append pull date as mm/dd/yy
        x[1] = strftime("%H:%M", now.timetuple()) # append pull time as HH:MM in 24-hr format
        x[2] = "UNKNOWN ERROR"
        x[3] = "UNKNOWN ERROR"
        x[4] = "UNKNOWN ERROR"
        x[5] = "UNKNOWN ERROR"
        x[6] = "UNKNOWN ERROR"

finally:
    write_to_csv(outputFilePath, ',', rows)
    driver.close()

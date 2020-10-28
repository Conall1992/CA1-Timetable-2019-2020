from datetime import datetime, date, timedelta
import sys
import requests 
import json
from bs4 import BeautifulSoup
'''
Uses JSON requests to grab my timetable from opentimetables and outputs to the console.  
'''

current_date = datetime.today().strftime("%Y-%m-%d")
l_date = date(int(current_date.split("-")[0]), int(current_date.split("-")[1]), int(current_date.split("-")[2]))
f_date = date(2020, 10, 5)

delta = l_date - f_date
days_of_Week = {1: "Monday", 2: "Tuesday", 3: "Wednesday", 4: "Thursday", 5: "Friday", 6: "Saturday", 0: "Sunday"}
week, days = int(delta.days) // 7 + 1, int(delta.days + 1) % 7 # week and day, we add one becuase we want to start on week, day 1 not week, day 0
week_startDate = l_date - timedelta(days - 1 )


#headers needed
headers = {
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:76.0) Gecko/20100101 Firefox/76.0",
    "Accept": "application/json, text/plain, */*",
    "Accept-Encoding": "gzip, deflate, br",
    "Authorization": "basic T64Mdy7m[",
    "Content-Type": "application/json",
    "Content-Length": "45",
    "Origin": "https://opentimetable.dcu.ie",
    "Connection": "keep-alive",
    "Referer": "https://opentimetable.dcu.ie/"
}

payload =  {
  "ViewOptions": {
    "Days": [
      {
        "Name": days_of_Week[days],
        "DayOfWeek": days,
        "IsDefault": True
      }
     
    ],
    "Weeks": [
      {
        "WeekNumber": week,
        "WeekLabel": "Week " + str(week),
        "FirstDayInWeek": str(week_startDate) + "T00:00:00.000Z"
      }
    ],
    "TimePeriods": [
      {
        "Description": "All Day",
        "StartTime": "08:00",
        "EndTime": "22:00",
        "IsDefault": True
      }
    ],
    "DatePeriods": [
      {
        "Description": "This Week",
        "StartDateTime": "2020-10-05T00:00:00.000Z",
        "EndDateTime": "2021-10-03T00:00:00.000Z",
        "IsDefault": True,
        "IsThisWeek": True,
        "IsNextWeek": False,
        "Type": "ThisWeek"
      }
    ],
 "LegendItems": [],
    "InstitutionConfig": {},
    "DateConfig": {
      "FirstDayInWeek": "2020-10-05T00:00:00+00:00" + "T00:00:00.000Z",
      "StartDate": "2020-10-05T00:00:00+00:00",
      "EndDate": "2021-09-27T00:00:00+00:00"
    },
  
  },
  "CategoryIdentities": [
    "38b55ac0-a242-23d3-4a10-79f11bdd780c"
  ]
}

#url for timetable
my_url = "https://opentimetable.dcu.ie/broker/api/categoryTypes/241e4d36-60e0-49f8-b27e-99416745d98d/categories/events/filter"


#sends a post request with the json contents and the headers(these are both needed)
page_json = requests.post(my_url, json=payload, headers=headers).content

#used to the convert the JSON file to a python dictionary
data = (json.loads(page_json))

#grabs each product
a = []
order = {}
for i in data[0]['CategoryEvents'][:-1]:
    # checks if i is a dictionary
    if isinstance(i, dict):
        maxLen = len(max(i, key=lambda values: values[1]))
        j = 0
        for k, v in i.items():
            if (k == "Description" or k == "EventType" or k == "Location") and v != 'None':
    
                # print("{}: {}\n".format(k, v))
                j += 1
                a.append(v)
            elif k == "StartDateTime":
                
                j += 1
                a.append(v)
            if j == 4:               
                order["{} ({}) in {} at {}".format(a[0], a[1], a[2], a[3][11:-9])] = int(a[3][11:-9].split(":")[0])
                a = []
                j = 0

times = []

for (k, v) in (sorted(order.items(), key=lambda v: v[1])):
    if k[-5:] not in times: # because of covid the class was split into 5 different groups, stops it repeating 5 times
      print(k)
      times.append(k[-5:])
    

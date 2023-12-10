# Hindu Calendar Days Filter App

Tired of parents telling me when I should fast and when I shouldn't fast? 

So, I made two scripts that helps me **find out days and exact times I'm not required to fast**:

* **panchang-generator.py** - This fetches Tithi and Nakshatra timings from "https://www.drikpanchang.com/tamil/tamil-month-panchangam.html?geoname-id=2643741&date={}" and stores Nakshatra details in `nakshatra.csv` and tithi details in `tithi.csv`

* **find-days.py** - This reads both `nakshatra.csv` and `tithi.csv` and removes all the dates/times **when you should be fasting**. Then, it also removes certain week days as well as pradosh_dates.

## How to use this app?

1. Step 1: Generate the `tithis.csv` from scratch by running `python3 panchang-generator.py -t`. You may also add `-r` flag if you want to rewrite this file everytime you run this 
script. If this is not included, content will be appended to the `tithis.csv` not rewritten. This will take a long time as it fetches details from each these pages individually.

2. Step 2: Generate the `nakshatra.csv` from scratch by running `python3 panchang-generator.py -n`. You may also add `-r` flag if you want to rewrite this file everytime you run this script. If this is not included, content will be appended to the `nakshatra.csv` not rewritten. This will take a long time as it fetches details from each these pages individually.

3. Step 3: Filter the dates and find out when you are not required to fast by then, running `python3 find-days.py`. Filtered dates will then, be printed. 

## Note

If you want change the dates when tithis and nakshatras are generated, please change the dates on the following code which can be found in `panchang-generator.py`

```
start_date = datetime(year=2023, month=7, day=6)
stop_date = datetime(year=2023, month=12, day=31)
```

`nakshatra_exist.csv` and `tithi_old.csv` are examples of csvs that will be generated. 

## TASK:
1. ~~Get a list of Thitis for each date~~
2. ~~Get the CSV of all Tithis~~
3. ~~Deal with multiple Tithis in one day~~
4. ~~Add start and end date for each Tithi~~
5. ~~Remove tithis~~
6. ~~Remove nakshatras~~
7. ~~Remove days~~
8. ~~Find common timeslots~~
9. ~~Remove the Sundays before Sunrise and Sunset~~
10. ~~Create a remove function~~
~~11. Remove https://www.udayfoundation.org/shradh-pitru-paksha/~~
12. Remove https://www.drikpanchang.com/vrats/pradoshdates.html
~~13. Remove a range of multiple days~~


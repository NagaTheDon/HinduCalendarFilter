from datetime import date, timedelta, datetime
import requests
from bs4 import BeautifulSoup
import csv
import time

import argparse

def date_range_list(start_date, end_date):
    # Return generator for a list datetime.date objects (inclusive) between start_date and end_date (inclusive).
    curr_date = start_date
    while curr_date <= end_date:
        yield (curr_date, curr_date.strftime("%d/%m/%Y"))
        curr_date += timedelta(days=1)


def find_element(soup, search_str, current_type, prev_dates):
    return_fields = []

    start_date = min(prev_dates)

    results = soup.find_all(string=search_str, recursive=True)
    assert(len(results) > 0)

    for result in results:
        span_parent = result.parent

        if span_parent.name != "span":
            span_parent = span_parent.parent

        spans = span_parent.find_next_siblings("span")
        for span in spans:
            txt = span.text.replace("upto", "") # Remove upto since no one cares
            element,time_date = txt.split("  ")
            time_str, date_str = (time_date.split(", ") + [None])[:2]
            # Update time
            updated_date_type = datetime.min
            round_day = False
            if time_str != "Full Night" and time_str != "24:00":
                updated_date_type = updated_date_type.strptime(time_str, "%H:%M")
            else:
                # print("YOOOOOOOOOOOO: TIME STRING AT "+str(current_type)+" IS: "+time_str)
                round_day = True
                current_type += timedelta(days=1) # Move it to next day 00:00



            # Update date
            if date_str is not None and round_day is False:
                this_date_type = datetime.strptime(date_str, "%b %d")
                updated_date_type = updated_date_type.replace(
                                            year=current_type.year,
                                            month=this_date_type.month,
                                            day=this_date_type.day)
            else: # Use the current date
                updated_date_type = updated_date_type.replace(
                                            year=current_type.year,
                                            month=current_type.month,
                                            day=current_type.day)

            return_fields.append((element, updated_date_type, start_date))

    return return_fields


ArgsHandler = argparse.ArgumentParser()
ArgsHandler.add_argument("-n","--nakshatra", action="store_true")
ArgsHandler.add_argument("-t", "--tithi", action="store_true")
ArgsHandler.add_argument("-r", "--rewrite", action="store_true")
args = ArgsHandler.parse_args()
print(args)

if not (bool(args.nakshatra) ^ bool(args.tithi)):
    ArgsHandler.error('--nakshatra and --tithi are either both given or both absent. Either only nakshatra or only tithi should be given')


start_date = datetime(year=2023, month=7, day=6)
stop_date = datetime(year=2023, month=12, day=31)
date_list = date_range_list(start_date, stop_date)

file_name = None
file_name = "nakshatra.csv" if args.nakshatra else "tithi.csv"

element_name = "Nakshathram" if args.nakshatra else "Tithi"

writing_mode = "w+" if args.rewrite else "a+"

prev_dates = [datetime.min]
with open(file_name, writing_mode, encoding='UTF8', newline='') as f:
    writer = csv.writer(f)

    if f.readlines() == 0:
        writer.writerow(["Nakshatra", "Start Date", "Start Time", "End Date", "End time"])

    for date_type, date in date_list:
        URL = "https://www.drikpanchang.com/tamil/tamil-month-panchangam.html?geoname-id=2643741&date={}&time-format=24hour"
        print(URL.format(date))
        response = requests.get(URL.format(date))

        soup = BeautifulSoup(response.content, "html.parser")

        tithis = find_element(soup, element_name, date_type, prev_dates)
        prev_dates.clear()

        for tithi in tithis:
            writer.writerow([tithi[0],
                             tithi[2].strftime("%d-%m-%Y"),
                             tithi[2].strftime("%H:%M:%S"),
                             tithi[1].strftime("%d-%m-%Y"),
                             tithi[1].strftime("%H:%M:%S")])
            prev_dates.append(tithi[1])




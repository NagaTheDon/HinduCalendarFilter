import csv
from datetime import date, timedelta, datetime
from pprint import pprint
from suntime import Sun
import pytz
from functools import cmp_to_key

restricted_tithis = [
                        "Sathurthi",
                        "Shasti",
                        "Astami",
                        "Navami",
                        "Thasami",
                        "Egadashi",
                        "Duvadasi",
                        "Sathuradasi",
                        "Amavasai",
                        "Pournami"
]

restricted_naks = [
                    "Aswini",
                    "Bharani",
                    "Magam",
                    "Revathi",
                    "Moolam",
                    "Thiruvonam",
                    "Karthigai",
                    "Poorattathi"
]

restricted_days = [
                    "Tuesday",
                    "Wednesday",
                    "Thursday",
                    "Friday",
                    "Saturday",
]

pradosh_dates = [
    "03-01-2023",
    "19-01-2023",
    "02-02-2023",
    "17-02-2023",
    "04-03-2023",
    "19-03-2023",
    "03-04-2023",
    "17-04-2023",
    "02-05-2023",
    "16-05-2023",
    "01-06-2023",
    "15-06-2023",
    "30-06-2023",
    "14-07-2023",
    "30-07-2023",
    "13-08-2023",
    "28-08-2023",
    "12-09-2023",
    "27-09-2023",
    "11-10-2023",
    "26-10-2023",
    "10-11-2023",
    "24-11-2023",
    "10-12-2023",
    "24-12-2023"
]


tithis = []
with open("./tithi.csv", 'r') as file:
    csvreader = csv.reader(file)
    for row in csvreader:
        tithis.append(row)


tithis = [tithi for tithi in tithis if tithi[0] not in restricted_tithis]

nakshatras = []
with open("./nakshatra.csv", 'r') as file:
    csvreader = csv.reader(file)
    for row in csvreader:
        nakshatras.append(row)

nakshatras = [nakshatra for nakshatra in nakshatras if nakshatra[0] not in restricted_naks]

# Remove all the restricted days
def remove_restricted_days(times):

    accepted_times = []

    for time in times:
        # print(time)
        # Start date
        start_date = time[1]
        start_time = time[2]

        start_str = start_date+";"+start_time
        start_datetime_obj = datetime.strptime(start_str, "%d-%m-%Y;%H:%M:%S")

        # End date
        end_date = time[3]
        end_time = time[4]

        end_str = end_date+";"+end_time
        end_datetime_obj = datetime.strptime(end_str, "%d-%m-%Y;%H:%M:%S")


        # If the time starts in a restricted day, push the timings to the next day
        # print(f"Start day: {start_datetime_obj.strftime('%A')}")
        # print(f"End day: {end_datetime_obj.strftime('%A')}")
        while(start_datetime_obj.strftime('%A') in restricted_days):
            start_datetime_obj += timedelta(days=1)
            start_datetime_obj = start_datetime_obj.replace(hour=0, minute=0, second=0)
            # print(f"Changed start day to {start_datetime_obj}-{start_datetime_obj.strftime('%A')}")

        while(end_datetime_obj.strftime('%A') in restricted_days):
            end_datetime_obj -= timedelta(days=1)
            end_datetime_obj = end_datetime_obj.replace(hour=23, minute=59, second=0)
            # print(f"Changed end day to {end_datetime_obj}-{end_datetime_obj.strftime('%A')}")


        # # If the start time after roll-over has not exceeded the end time,
        if(start_datetime_obj < end_datetime_obj):
            accepted_times.append(
                                    {
                                        "name" : time[0],
                                        # "start_date_str" : start_datetime_obj.strftime("%d-%m-%Y"),
                                        # "start_time_str": start_datetime_obj.strftime("%H:%M:%S"),
                                        # "start_day": start_datetime_obj.strftime('%A'),
                                        # "end_date_str" : end_datetime_obj.strftime("%d-%m-%Y"),
                                        # "end_time_str": end_datetime_obj.strftime("%H:%M:%S"),
                                        # "end_day": end_datetime_obj.strftime('%A'),
                                        "start_obj" : start_datetime_obj,
                                        "end_obj" : end_datetime_obj,
                                    }
                                )
    return accepted_times

def join_any_times(elems):
    results = [elems[0]]
    # idx = 1
    elems_idx = 0

    while( elems_idx < len(elems)-1):
        elems_idx += 1
        results.append(elems[elems_idx])
        if( results[-2]["end_obj"] == results[-1]["start_obj"]):
            # print(f"Joining... {results[-2]} and {results[-1]}\n\n")
            if isinstance(results[-2]["name"], list):
                results[-2]["name"] = [*results[-2]["name"]]+ [results[-1]["name"]]
            else:
                results[-2]["name"] = [results[-2]["name"], results[-1]["name"]]

            # elems[-2]["end_date_str"] = ""
            # elems[-2]["end_time_str"] = ""
            # elems[-2]["end_day"] = ""
            results[-2]["end_obj"] = results[-1]["end_obj"]
            # Remove the last element
            del results[-1]
        # print("-----------------------\n\n\n")
    return results

def remove_times(times, removals):
    results = times
    elems_idx = 0
    removal_bool = True
    removed_this_range = False


    for remove_time in removals:
        # print(f"\n\nTrying to cut {remove_time}...")

        while len(results) > elems_idx:
            removal_key = 'start_obj' if removal_bool else 'end_obj'
            # print(f".. from {times[elems_idx]}->{times[elems_idx]['start_obj'].strftime('%A')} => {times[elems_idx]['end_obj'].strftime('%A')}, {removal_key}")
            if( remove_time['start_obj'] <= times[elems_idx]['start_obj'] and remove_time['end_obj'] >= times[elems_idx]['end_obj'] ):
                # print("Removing the entire day...")
                del results[elems_idx]
            elif( times[elems_idx]['start_obj'] <= remove_time[removal_key] and remove_time[removal_key] <= times[elems_idx]['end_obj'] ):
                # print("Cutting..")
                # Start time is in between this interval
                # print(f"Comparing {times[elems_idx][removal_key]} {remove_time[removal_key]}")
                update_time_start = min( times[elems_idx][removal_key], remove_time[removal_key] )
                update_time_end = max( times[elems_idx][removal_key], remove_time[removal_key] )
                # print(f"Start: {update_time_start} End: {update_time_end}")

                if update_time_start != update_time_end:
                    results.append(
                                        {
                                            # "start_obj" : times[elems_idx]['start_obj'],
                                            # "end_obj": removals[removal_key]
                                            'start_obj' : update_time_start,
                                            'end_obj': update_time_end
                                        }
                                    )
                    removed_this_range = True
                if not removal_bool: # If it is the end and it was found,
                    if removed_this_range: # Before you break it, remove this range too
                        del results[elems_idx]
                        removed_this_range = False
                    break # Break it
            else:

                # If it was removed from start but, end was not found in this range,
                if removed_this_range:
                    del results[elems_idx] # Remove it
                    removed_this_range = False
                # if removal_bool:
                #     results.append(times[elems_idx])
                # Only if it is end, add to the elements index
                # Only if it is the end, move on to the next index
                if not removal_bool:
                    elems_idx += 1

            removal_bool = not removal_bool

        elems_idx = 0
    return results




def find_common_times(times_a, times_b):
    results = []
    len_times_a = len(times_a)
    len_times_b = len(times_b)

    idx_times_a = 0
    idx_times_b = 0

    while ((idx_times_a < len_times_a) and (idx_times_b < len_times_b)):
        # Check if they overlap
        time_a = times_a[idx_times_a]
        time_b = times_b[idx_times_b]

        # print(f"Time A: {time_a['start_obj']}=>{time_a['end_obj']} Time B: {time_b['start_obj']}=>{time_b['end_obj']}")
        if( (time_b['start_obj'] <= time_a['end_obj']) and (time_a['start_obj'] <= time_b['end_obj']) ):
            overlap_start = max(time_a['start_obj'], time_b['start_obj'])
            overlap_end   = min(time_a['end_obj'], time_b['end_obj'])

            if(overlap_start != overlap_end):
                # print(f"Common times: {overlap_start}=>{overlap_end}")
                results.append(
                    {
                        # "name" : time_a['name']+time_b['name'],
                        "start_obj" : overlap_start,
                        "end_obj": overlap_end
                    }
                )

        if( time_a['end_obj'] > time_b['end_obj'] ):
            idx_times_b += 1
        else:
            idx_times_a += 1

    return results

allowed_tithis = remove_restricted_days(tithis)
allowed_joined_tithis = join_any_times(allowed_tithis)
# pprint(allowed_joined_tithis, sort_dicts=False)

allowed_nakshatras = remove_restricted_days(nakshatras)
allowed_joined_nakshatras = join_any_times(allowed_nakshatras)
# pprint(allowed_joined_nakshatras, sort_dicts=False)

allowed_times = find_common_times(allowed_joined_tithis, allowed_joined_nakshatras)
allowed_joined_times = join_any_times(allowed_times)
# pprint(allowed_joined_times, sort_dicts=False)

# Get Sun rises and when Sun sets on Sunday
latitude = 51.5553
longitude = 0.0589

sun = Sun(latitude, longitude)
curr_date = datetime(year=2023, month=3, day=27)
end_date = datetime(year=2023, month=12, day=31)

not_allowed_sunday_times = []

while curr_date <= end_date:
    if curr_date.strftime('%A') == "Sunday":
        sunrise_obj_aware = sun.get_local_sunrise_time(curr_date)
        sunrise_obj_naive = sunrise_obj_aware.replace(tzinfo=None)
        # # Allowed times are before Sunset
        # accepted_sunday_times.append(
        #     {
        #         "name" : "Sunday before Sunrise",
        #         "start_obj" : curr_date,
        #         "end_obj": sunrise_obj_naive
        #     }
        # )
        # # Allowed times are after Sunrise
        sunset_obj_aware = sun.get_local_sunset_time(curr_date)
        sunset_obj_naive = sunset_obj_aware.replace(tzinfo=None)
        # end_obj = curr_date.replace(hour=23, minute=59, second=0)
        # accepted_sunday_times.append(
        #     {
        #         "name": "Sunday after Sunset",
        #         "start_obj": sunset_obj_naive,
        #         "end_obj": end_obj,
        #     }
        # )

        not_allowed_sunday_times.append(
            {
                "name": "Sunday",
                "start_obj": sunrise_obj_naive,
                "end_obj": sunset_obj_naive
            }
        )
    curr_date += timedelta(days=1)







# print("\n\n\n\n\n\n\n")
sundays_removed = remove_times(allowed_times,not_allowed_sunday_times)


shradh_start = datetime(year=2023, month=9, day=29, hour=0, minute=0)
shradh_end = datetime(year=2023, month=10, day=14, hour=23, minute=59, second=59)
curr_date = shradh_start
shradh_days = []
while curr_date <= shradh_end:
    shradh_day_end = curr_date.replace(hour=23, minute=59, second=59)
    shradh_days.append(
        {
            "start_obj": curr_date,
            "end_obj": shradh_day_end
        }
    )
    curr_date += timedelta(days=1)

shradh_removed = remove_times(sundays_removed, shradh_days )

pradosh_days = []
start_object = datetime.min
for pdate in pradosh_dates:
    start_object = start_object.strptime(pdate, "%d-%m-%Y")
    end_object = start_object.replace(hour=23, minute=59, second=59)

    pradosh_days.append(
        {
            'start_obj': start_object,
            'end_obj': end_object,
        }
    )

pradosh_removed = remove_times( shradh_removed, pradosh_days )
pradosh_removed = sorted(pradosh_removed, key=lambda start: start['start_obj'])

print("======= DAYS YOU ARE NOT REQUIRED TO FAST ======")
for al in pradosh_removed:
    print(f"Between {al['start_obj'].strftime('%B %d, %Y, %A - %H:%M')} and {al['end_obj'].strftime('%B %d, %Y, %A - %H:%M')}")


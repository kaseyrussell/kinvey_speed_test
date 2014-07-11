import json
import datetime
import random

lowest_lux       = 2501  # always above lower limit of GoodLux, worst case because will check all records
highest_lux      = 15000

""" Make a series of datasets (each in a json file). Each dataset will have
*days* worth of data."""
for days in range(1,15):
    start = datetime.datetime(1980+days, 01, 01, 00, 00) # have each dataset come from a different year
    hours_per_day    = 24
    samples_per_hour = 60
    samples_per_day  = hours_per_day * samples_per_hour
    num_samples      = days * samples_per_day
    fname            = "datasets/fakedata_{0:02}day_{1}samples.json".format(days,num_samples)

    lux_records      = []
    daily_records    = []

    for day in range(days):
        time_stamps  = []
        lux_readings = []

        for sample in range(samples_per_day):
            time_stamps.append(start + sample*datetime.timedelta(minutes=1))
            if time_stamps[-1].hour in range(8,12):
                # have max goodlux in hours after waking
                lux_readings.append(10000 + random.randint(0,5000))
            else:
                lux_readings.append(random.randint(lowest_lux,highest_lux))

        for t,lux in zip(time_stamps, lux_readings):
            lux_records.append([lux, t.isoformat()])

        daily_records.append({
            "accumulatedLux": sum(lux_readings),
            "lastLuxRecordDate": time_stamps[int(samples_per_day*0.4)].isoformat(),
            "uid": "{:%Y-%m-%d}".format(time_stamps[0]),
            "date": time_stamps[int(samples_per_day*0.7)].isoformat()}) # how is "date" different than "uid" or "lastLuxRecordDate"?

    dailyRecords = json.dumps(daily_records)
    dailyRecords = "[{\n         ".join(dailyRecords.split("[{"))
    dailyRecords = "\n    }, {\n         ".join(dailyRecords.split("}, {"))
    dailyRecords = '",\n        '.join(dailyRecords.split('",'))
    dailyRecords = "\n    }]".join(dailyRecords.split("}]"))
    luxRecords   = json.dumps(lux_records)
    luxRecords   = "],\n    ".join(luxRecords.split("],"))

    with open(fname, 'wa') as fobj:
        fobj.write("{\n")
        fobj.write('  "dailyRecords": \n    ')
        fobj.write(dailyRecords)
        fobj.write(",\n")
        fobj.write('  "luxRecords": \n    ')
        fobj.write(luxRecords)
        fobj.write("\n}")



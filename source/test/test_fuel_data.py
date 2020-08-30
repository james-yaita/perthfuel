'''
Checks Fuel Data.py
'''
# Reload modules to get latest updates to other modules
import sys
import os
import importlib as imp
import pprint
sys.path.append(os.path.abspath('../'))
import fuel_data as  fd

#sys.path.append(os.path.abspath('../'))
#import fuel_data as  fd


imp.reload(fd)


def sanity():
    print("Check the Fuel data stuff")
    return None


def bySuburb():
    brentwoodList = fd.get_fuel_by_suburb("Brentwood")
    pprint.pprint(brentwoodList, indent=4)


def byWrongDay():
    wrongDay = fd.get_fuel_by_suburb("Brentwood", day="ashita")
    print(wrongDay)


def addingWrongStuff():
    # empty sett
    stations = {}
    filtered_data = fd.get_fuel_by_suburb("Brentwood")

    price_day = "price_" + "today"
    extraction_mapping = {

            "trading_name": "trading-name",
             "price_today": None

    }
    fd.add_to_dictionary(stations,
                         filtered_data,
                         "trading_name",
                         {**extraction_mapping,
                          **{price_day: "price"}})
    pprint.pprint(stations, indent=4)
    filtered_data_2 = fd.get_fuel_by_suburb("Brentwood", day="ashita")
    fd.add_to_dictionary(stations,
                         [],
                         "trading_name",
                         {**extraction_mapping,
                          **{price_day: "price"}})
    pprint.pprint(stations, indent=4)

"""
- When the station closed down yesterday
- When the station opens tomorrow

- when the price is below 1.00

check google map link works

check sorting

City Beach is a suburb that exists but has no petrol stations
Brentwood has 1
Ascot has many




"""



# If the file is not loaded as a module,
# call functions
if __name__ == '__main__':
    sanity()
    # bySuburb()
    # byWrongDay()
    addingWrongStuff()


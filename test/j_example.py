
# Import from a parent directory
import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 


import suburb as suburb_info
import importlib
import fuel_data as fd
import feedparser



print("lets see")
results = fd.get_fuel_by_suburb(suburb="Brentwood")
print(results)

for station in results:
    print(f"{station}\r\n\r\n")

print(type(results))

#a
import requests
import feedparser

# Fuel Data
'''

Code to extract information from the Fuel Watch RSS feed

See:
https://www.fuelwatch.wa.gov.au/fuelwatch/pages/public/contentholder.jspx?key=fuelwatchRSS.html
for full details



'''
__fuel_watch_rss_feed__ = 'http://www.fuelwatch.wa.gov.au/fuelwatch/fuelWatchRSS?'
__debugging__ = True


# === Sort Filter Functions ===


def by_price_today(item):
    '''
    Function to be passed to the the sorting function.

    As the price is stored as a text string, it needs
    to be converted to a floating point number.

    :item: dictionary : Supplies the station information
    :return: price : Today's price as a floating point number
   '''

    return float(item.get('price_today', 0.0))


def by_location(item):
    '''
    Function to be passed to the the sorting function.

    Parameters
    ----------
    item: dictionary
        Supplies the station information

    Returns
    -------
        Returns the location (usually suburb)

   '''
    return item.get('location', "")


def by_brand(item):
    '''
    Function to be passed to the the sorting function.

    Parameters
    ----------
    item: dictionary
        Supplies the station information

    Returns
    -------
        Returns the station brand

   '''
    return item.get('brand', "") 


# === END Sort Filter Functions ===   



def convert_to_list(stations):
    '''
    Converts a dictionary into a list

    Parameters
    ----------
    stations: dictionary
        The station information

    Returns
    -------
        Dictionary at top level is converted to a list

    '''

    new_area = []
    for station in stations:
        new_area.append(stations[station])

    return new_area


def add_to_dictionary(stations, fuel_watch_data, primary_key, mapping_keys):
    '''
    Add fuel watch data to the existing dictionary of information.

    Good for adding additional information (such as yesterday's price) 
    to already existing information.

    Parameters
    ----------
    stations: dictionary
        The station information

    fuel_watch_data: dictionary
        Extracted information from Fuel Watch

    primary_key: String
        The key name for getting station information

    mapping_keys: Dictionary
         Key-Value pair on how to extract information from the 
         Fuel Watch RSS feed and put it into our station 
         dictionary

    Returns
    -------
        Dictionary at top level is converted to a list
    '''

    for station in fuel_watch_data:

        station_info = {}
        # Go through the fuel watch data, extract infromation
        # and put it into the list using the desired key
        for key, value in mapping_keys.items():
            if isinstance(value, list):
                '''
                When we want to combine data from multiple entries
                into the one entry.
                Typically we do that by combining 
                latitude and longitude into co-ords
                '''
                first = True
                for component in value:
                    if first:
                        station_info[key] = station.get(component, None)
                        first = False
                    else:
                        station_info[key] = station_info[key] + "," + \
                                            station.get(component, None)
            else:
                station_info[key] = station.get(value, None)

        # Insert any additional or updated data into the existing data set.
        existing_info = stations.get(station_info[primary_key], {})
        stations[station_info[primary_key]] = {**existing_info, **station_info}
    return None


def __get_fuel(zone_info, product=None, day=None, brand=None):
    '''

    Gets the information from the Fuel Watch Website based on the
    supplied parameters
    
    Parameters
    ----------
    zone_info: String.
        Regions or suburb information

    product_id: Number. 
        Fuel type

    day: String. 
        Today, Tomorrow or Yesterday

    brand: Number. 
        Number ID for the brand.  See Fuel Watch for list.
    '''
   
    # Create the request URL
    # zone_info containing surrounding when a suburb
    feed_url = __fuel_watch_rss_feed__ + zone_info

    feed_url += get_field_value_product(product)
    feed_url += get_field_value_brand(brand)
    feed_url += get_field_value_day(day)


    if __debugging__:
        print(f"Request URL: {feed_url}")

    # Get the information
    data = feedparser.parse(feed_url)
    return data['entries']


def get_field_value_brand(brand=None):
    '''
    Adds brand key value pair ready for input into the URL request.  

    Returns an empty string when Brand is none.  Fuel watch then
    assumes all brands have been requested
    
    Parameters
    ----------
        brand: Number.
            ID for the brand.  See Fuel Watch for list.

    Returns
    -------
        String of key value pair for URL query. Or empty sting for None
    '''

    if brand == None or brand == 0 or brand =='0':
        print("removed brand of ", type(brand) )
        return ''
    else:
        return '&Brand=' + str(brand)


def get_field_value_day(day=None):
    '''
    Adds day key value pair ready for input into the URL request.  

    Returns an empty string when day is none.  Fuel watch
    will assume today is requested
    
    Parameters
    ----------
        day: String. Default is none and Fuel Watch treats as 
            today.  Options are: Today, Tomorrow, Yesterday

    Returns
    -------
        String of key value pair for URL query. Or empty sting for None
    '''
    if day == None:
        return ''
    else:
        return '&Day=' + day        


def get_field_value_product(product=None):
    '''
    Adds day key value pair ready for input into the URL request.  

    Returns an empty string when product is none.  Fuel watch
    will assume Unleaded is requested
    
    Parameters
    ----------
        product: Number, default is none.  See Fuel Watch for list

    Returns
    -------
        String of key value pair for URL query. Or empty sting for None
    '''
    if product  == None:
        return ''
    else:
        return '&Product=' + str(product)


def get_field_value_surrounding(surrounding=None):
    '''
    Return the key value pair for checking surround suburbs.
    When surrounding key is not supplied Fuel Watch 
    returns the surrounding suburbs

    Parameters
    ----------
        surrounding: Boolean, default is none.  By default
            Fuel watch will return surrounding suburbs.

    Returns
    -------
        String of key value pair for URL query. Or empty sting for None
    '''
    if surrounding is None:
        print("In Surrounding value is: None")
    else:
        print("In surrounding value is: ", surrounding)
    if surrounding == "no":
        return '&Surrounding=no'
    elif surrounding == "yes":
        return '&Surrounding=yes'
    else:
        return ''



def get_fuel_by_suburb(suburb, product=None, day=None, surrounding=None, brand=None):
    '''
    Request information for a suburb.  Other parameters can optionally
    supplied

    Parameters
    ----------
    suburb: String.  Suburb to lookup

    product_id: Number. Fuel type

    day: String. Today, Tomorrow or Yesterday

    surrounding: Boolean. Include surrounding suburbs.  

    brand: Number.  Number ID for the brand

    '''

    suburb = suburb.replace(' ', '%20')
    zone = 'Suburb=' + str(suburb) + get_field_value_surrounding(surrounding)
    return __get_fuel(zone, product = product, day = day, brand = brand)



def get_fuel_by_region(region, product=None, day=None, brand=None):
    '''
    Request information for a region.  Other parameters can optionally
    supplied

    Parameters
    ----------
    regions: Number.  Region to lookup

    product_id: Number. Fuel type

    day: String. Today, Tomorrow or Yesterday

    brand: Number.  Number ID for the brand

    Returns
    -------
    Data from the Fuel Watch website
    '''
    zone = 'Region=' + str(region)
    return __get_fuel(zone, product=product, day=day, brand=brand)



def get_fuel_by_division(state_region_code, product=None, day=None, brand=None):
    '''
    Request information for a division in the state. 
    Other parameters can optionally supplied

    Parameters
    ----------
    state_region_code: Number.  Division to lookup

    product_id: Number. Fuel type

    day: String. Today, Tomorrow or Yesterday

    brand: Number.  Number ID for the brand

    Returns
    -------
    Data from the Fuel Watch website
    '''

    zone = 'StateRegion=' + str(state_region_code)
    return __get_fuel(zone, product = product_id, day = day, brand = brand)

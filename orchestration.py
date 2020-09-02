import display
import fuel_data as fd

orchestration = [
    {
        "name": "price_yesterday",
        "fuelwatch_lookup": None,
        "data_sort_function": None,
        "display_in_html": {
            "col_title": "Yesterday",
            "col_number": 0,
            "data_set_key": "price_yesterday",
            "display_function": display.display_price,
            "html_sort_function": "sortNumerically",
            "html_name": "PRICE_YESTERDAY",
            "direction": "DIR_UNKNOWN",
            "element_root": "price_yesterday"
        }
    },
    {
        "name": "price_today",
        "fuelwatch_lookup": None,
        "data_sort_function": fd.by_price_today,
        "display_in_html": {
            "col_title": "Today",
            "col_number": 1,
            "data_set_key": "price_today",
            "display_function": display.display_price,
            "html_sort_function": "sortNumerically",
            "html_name": "PRICE_TODAY",
            "direction": "DIR_UP",
            "element_root": "price_today"
        }
    }, {
        "name": "price_tomorrow",
        "fuelwatch_lookup": None,
        "data_sort_function": None,
        "display_in_html": {
            "col_title": "Tomorrow",
            "col_number": 2,
            "data_set_key": "price_tomorrow",
            "display_function": display.display_price,
            "html_sort_function": "sortNumerically",
            "html_name": "PRICE_TOMORROW",
            "direction": "DIR_UNKNOWN",
            "element_root": "price_tomorrow"
        }
    }, {
        "name": "trading_name",
        "fuelwatch_lookup": "trading-name",
        "data_sort_function": None,
        "data_display_function": None,
        "display_in_html": None
    }, {
        "name": "brand",
        "fuelwatch_lookup": "brand",
        "data_sort_function": None,
        "data_display_function": None,
        "display_in_html": {
            "col_title": "Brand",
            "col_number": 3,
            "data_set_key": "brand",
            "display_function": display.display_as_is,
            "html_sort_function": "sortAlphabetically",
            "html_name": "BRAND",
            "direction": "DIR_UNKNOWN",
            "element_root": "brand"
        }
    }, {
        "name": "street_address",
        "fuelwatch_lookup": "address",
        "data_sort_function": None,
        "display_in_html": {
            "col_title": "Address",
            "col_number": 4,
            "data_set_key": "street_address",
            "display_function": display.display_as_is,
            "html_sort_function": None,
            "html_name": "STREET_ADDRESS",
            "direction": "DIR_UNKNOWN",
            "element_root": "streetAddress"
        }
    }, {
        "name": "locality",
        "fuelwatch_lookup": "location",
        "data_sort_function": None,
        "data_display_function": None,
        "display_in_html": {
            "col_title": "Locality",
            "col_number": 5,
            "data_set_key": "locality",
            "display_function": display.display_as_is,
            "html_sort_function": "sortAlphabetically",
            "html_name": "LOCALITY",
            "direction": "DIR_UNKNOWN",
            "element_root": "locality"
        }
    }, {
        "name": "co-ords",
        "fuelwatch_lookup": ['latitude', 'longitude'],
        "data_sort_function": None,
        "data_display_function": None,
        "display_in_html": {
            "col_title": "Co-Ords",
            "col_number": 6,
            "data_set_key": "co-ords",
            "display_function": display.display_co_ords,
            "html_sort_function": None,
            "html_name": "LOCALITY",
            "direction": "DIR_UNKNOWN",
            "element_root": "locality"
        }
    }

]
suburb_identifier = 'suburb'
product_identifier = 'product'
brand_identifier = 'brand'
surrounding_identifier = 'surrounding'

fuel_site_params = {
    surrounding_identifier: {
        "default": "yes",
        "required": False,
        "supplied_value": None},
    product_identifier: {
        "default": "",
        "required": True,
        "supplied_value": None
    },

    brand_identifier: {
        "default": 0,
        "required": False,
        "supplied_value": None
    },

    product_identifier: {
        "default": 1,
        "required": False,
        "supplied_value": None
    }
}

def get_instructions():
    fuel_watch_instructions = {}
    html_display_instruction = []

    for instrument in orchestration:

        # Get instructions for getting data
        key = instrument.get("name", None)
        value = instrument.get("fuelwatch_lookup", None)
        if key is not None and value is not None:
            fuel_watch_instructions[key] = value

        # Get instruction for displaying in html
        html_instructions = instrument.get("display_in_html", None)
        if html_instructions is not None:
            html_display_instruction .append(html_instructions)
    return fuel_watch_instructions, html_display_instruction

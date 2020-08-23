import suburb as suburb_info
import imp
import fuel_data as fd
import display
# import os.path

from markupsafe import escape
from flask import Flask, request
# from flask import Flask, redirect, url_for, request
app = Flask(__name__)

imp.reload(suburb_info)

# the last 12 months + 
# daily price of a product
# With Charts


INDEX_PAGE = "index.html"
DIV_MAIN_OPEN = '<div class="main">'
DIV_CLOSE = '</div>'
DIV_CONTENT_OPEN = '<div class="content">'

# Make this a Config to get rid of clutter

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
            "html_display": display.display_co_ords,
            "html_sort_function": None,
            "html_name": "LOCALITY",
            "direction": "DIR_UNKNOWN",
            "element_root": "locality"
        }
    }

]

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


@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r




@app.route('/')
@app.route('/index.html')
def hello_world():

    page_content = ""
    page_content = display.html_head("Fuel Prices")
    page_content += display.html_body_masthead("Fuel Prices", "")

    page_content += DIV_MAIN_OPEN
    page_content += DIV_CONTENT_OPEN

    page_content += display.display_form()
    page_content += '''
    <ul>
    <li><a href="region?id=18&name=Mandurah">Mandurah</a></li>
    <li><a href="region?id=26&name=South%20of%20River">South of River</a></li>
    <li><a href="region?id=27&name=Hills%20%26%20East Metro">Hills &amp; East Metro</a></li>
    <li><a href="region?id=25&name=North%20of%20River">North of River</a></li>
    </ul>
    '''

    page_content += DIV_CLOSE
    page_content += DIV_CLOSE
    page_content += display.html_body_footer()
    page_content += display.html_tail()

    return page_content

# app.route('region/)






@app.route('/results.html', methods=["POST"])
def display_result():
    page_content = ""
    fuel_type = {"id": 1, "name": "Unleaded Petrol"}

    expected_inputs = [
        {
            "name": "suburb",
            "default": "",
            "required": True,
            "supplied_value": None
        }, {
            "name": "brand",
            "default": None,
            "required": False,
            "supplied_value": None
        }, {
            "name": "product",
            "default": None,
            "required": False,
            "supplied_value": None
        }, {
            "name": "surrounding",
            "default": None,
            "required": False,
            "supplied_value": "no"
        }

    ]

    requested_suburb = ""

    for item in expected_inputs:
        if item["name"] in request.form:
            print(item["name"], " has value of ", request.form[item["name"]])
            item["supplied_value"] = request.form[item["name"]]
        else:
            print(item["name"], " not supplied")

        """
        if item["name"] == "surrounding":
            if item["supplied_value"] == None:
                item
        """

    if expected_inputs[0]["supplied_value"] is not None:
        requested_suburb = expected_inputs[0]["supplied_value"]
    else:
        # FIXME
        print("It will end in tears")




    query_params = {}
    [query_params.update({item["name"]: item["supplied_value"]}) for item in expected_inputs]

    # Assuming errors
    body_content = f"""<h2>Problem Encountered</h2>
    <p>Currently no data is available for '{requested_suburb}'</p>
    <p>Please check the supplied suburb. If the suburb exists, 
    there may not be any data for it as the moment.</p> 

    """

    title = "Fuel Price Search Results"
    page_heading = "Fuel Prices"
    breadcrumbs = "Search Results"
    js_params = None

    body_content, js_params = get_suburb_content(query_params)
    title = f"{requested_suburb.title()} Fuel Price"
    page_heading = "Fuel Prices"
    breadcrumbs = f"{requested_suburb.title()} Search Results"

    page_content = display.html_head(title)
    page_content += display.html_body_masthead(page_heading, breadcrumbs)

    page_content += DIV_MAIN_OPEN
    page_content += DIV_CONTENT_OPEN

    page_content += "<p>Results for: "
    for k, v in query_params.items():
        page_content += k + ": " + v + " "

    page_content += "</p>"

    page_content += display.display_form()


    page_content += body_content
    page_content += DIV_CLOSE
    page_content += DIV_CLOSE
    page_content += display.html_body_footer()
    # print(js_params)
    page_content += display.html_tail(js_params)

    return page_content


@app.route('/region')
def display_region():
    # ?id=<string:region_id>&name=<string:region_desc>
    region_id = request.args.get('id')
    region_desc = request.args.get('name')

    page_content = ""

    requested_region = "To Be Done"
    valid_region = True

    # Assuming errors
    body_content = f"""<h2>Problem Encountered</h2>
    <p>Currently no data is available for region'</p>


    """

    title = "Fuel Price Search Results"
    page_heading = "Fuel Prices"
    breadcrumbs = "Search Results"
    js_params = None
    if valid_region is True:
        requested_region = region_desc

        body_content, js_params = get_region_content(region_id)
        title = f"{requested_region.title()} Fuel Price"
        page_heading = "Fuel Prices"
        breadcrumbs = f"{requested_region.title()}"

    page_content = display.html_head(title)
    page_content += display.html_body_masthead(page_heading, breadcrumbs)

    page_content += DIV_MAIN_OPEN
    page_content += DIV_CONTENT_OPEN

    page_content += display.display_form()

    page_content += body_content
    page_content += DIV_CLOSE
    page_content += DIV_CLOSE
    page_content += display.html_body_footer()
    page_content += display.html_tail(js_params)

    return page_content


def get_sorted_data(get_data_function,
                    parameters,
                    extraction_mapping,
                    days):
    stations = {}
    # print("In get_sorted_data ", parameters, " \n\n")
    for day in days:
        # Creating a new key for price based on the day

        filtered_data = get_data_function(**parameters, day=day)
        '''
        if __debug__:
            print("\nfiltered data for  ", day, "\n", filtered_data, "\n")
        '''

        price_day = "price_" + day

        fd.add_to_dictionary(stations,
                             filtered_data,
                             "trading_name",
                             {**extraction_mapping,
                              **{price_day: "price"}})

    sorted_data = sorted(fd.convert_to_list(stations),
                         key=fd.by_price_today,
                         reverse=False)

    return sorted_data


def get_region_content(region_id, days=['yesterday', 'today', 'tomorrow']):

    extraction_mapping, items_to_display = get_instructions()

    # print("\n\n")
    sorted_data = get_sorted_data(fd.get_fuel_by_region,
                                  {"region": region_id},
                                  extraction_mapping,
                                  days=days)

    if len(sorted_data) == 0:
        error_text = f"<p>No data for the region.</p>"
        error_text += f"<p>Please check the regsion and try again.</p>"
        return error_text, None
    else:
        table_content = display.formatted_html_table(sorted_data,
                                                     items_to_display)
        return table_content, items_to_display


def get_suburb_content(query_request, days=['yesterday', 'today', 'tomorrow']):

    extraction_mapping, items_to_display = get_instructions()

    print("\n\n")
    sorted_data = get_sorted_data(fd.get_fuel_by_suburb,
                                  query_request,
                                  extraction_mapping,
                                  days=days)

    if len(sorted_data) == 0:
        error_text = f"<p>No data for suburb</p>"
        error_text += f"<p>Please check the suburb and try again.</p>"
        return error_text, None
    else:
        table_content = display.formatted_html_table(sorted_data,
                                                     items_to_display)
        return table_content, items_to_display


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

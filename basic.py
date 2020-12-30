import suburb as suburb_info
import imp
import fuel_data as fd
import display
import json




from orchestration import get_instructions
from orchestration import suburb_identifier
from orchestration import brand_identifier
from orchestration import product_identifier
from orchestration import surrounding_identifier
from orchestration import fuel_site_params



from markupsafe import escape
from flask import Flask, request
# from flask import Flask, redirect, url_for, request
app = Flask(__name__)

imp.reload(suburb_info)
imp.reload(display)
imp.reload(fd)




INDEX_PAGE = "index.html"
DIV_MAIN_OPEN = '<div class="main">'
DIV_CLOSE = '</div>'
DIV_CONTENT_OPEN = '<div class="content">'


@app.route('/')
@app.route('/index.html')
def hello_world():

    page_content = ""
    page_content = display.html_head("Fuel Prices")
    page_content += display.html_body_masthead("Fuel Prices", "")

    page_content += DIV_MAIN_OPEN
    page_content += DIV_CONTENT_OPEN

    page_content += display.display_locality_form()
    page_content += '''

<h3>Unleaded Prices</h3>
<ul>
  <li>
    <a href="region?id=18&name=Mandurah">Mandurah</a>
  </li><li>
    <a href="region?id=26&name=South%20of%20River">South of River</a>
  </li><li>
    <a href="region?id=27&name=Hills%20%26%20East Metro">
      Hills &amp; East Metro
    </a>
  </li><li>
    <a href="region?id=25&name=North%20of%20River">North of River</a>
  </li>
</ul>
    '''

    page_content += DIV_CLOSE
    page_content += DIV_CLOSE
    page_content += display.html_body_footer()
    page_content += display.html_tail()

    return page_content


@app.route('/prices.html')
def display_prices():
    supplied_suburb = request.args.get(suburb_identifier, "")
    supplied_product = request.args.get(product_identifier, 1)
    supplied_brand = request.args.get(brand_identifier, 0)
    supplied_surrounding = request.args.get(surrounding_identifier,
                           fuel_site_params["surrounding"]["default"])

    page_content = ""

    requested_suburb = ""
    body_content = f"""
        <h3 class="error">Problem Encountered</h3>

        <p>Please make sure you enter a suburb or town into the suburb field.</p>
        """
    js_params = None
    page_heading = "Fuel Prices"
    title = f"Fuel Price"
    breadcrumbs = f"Search Results"


    query_params = {
        suburb_identifier: supplied_suburb,
        product_identifier: supplied_product,
        brand_identifier: supplied_brand,
        surrounding_identifier: supplied_surrounding
    }

    if supplied_suburb is not None and supplied_suburb != "":
        supplied_suburb = supplied_suburb.title()
        body_content, js_params = get_suburb_content(query_params)
        title = f"{supplied_suburb} Fuel Price"
        breadcrumbs = f"{supplied_suburb} Search Results"

    else:
        supplied_suburb = ""

    page_content = display.html_head(title)
    page_content += display.html_body_masthead(page_heading, breadcrumbs)

    page_content += DIV_MAIN_OPEN
    page_content += DIV_CONTENT_OPEN
    for k, v in query_params.items():
        page_content += f"<!-- {k} : {v} -->"
    page_content += display.display_locality_form(suburb=supplied_suburb,
                        selected_product=supplied_product,
                        selected_brand=supplied_brand,
                        surrounding=supplied_surrounding)
    page_content += body_content
    page_content += DIV_CLOSE
    page_content += DIV_CLOSE
    page_content += display.html_body_footer()
    page_content += display.html_tail(js_params)

    return page_content


@app.route('/locality.html', methods=["GET", "POST"])
def display_result():
    page_content = ""

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
            "supplied_value": None
        }
    ]

    requested_suburb = ""
    body_content = f"""
        <h3 class="error">Problem Encountered</h3>

        <p>Please make sure you enter a suburb or town into the suburb field.</p>
        """
    js_params = None
    page_heading = "Fuel Prices"
    title = f"Fuel Price"
    breadcrumbs = f"Search Results"

    for item in expected_inputs:
        if item["name"] in request.form:
            print(item["name"], " has value of |", request.form[item["name"]], "|")
            item["supplied_value"] = request.form[item["name"]]

        else:
            print(item["name"], " not supplied")
            if item["name"] == "surrounding":
                item["supplied_value"] = "no"
            if item["name"] == "suburb":
                print(" we should fail")

    suburb_response = expected_inputs[0]["supplied_value"]

    query_params = {}
    [query_params.update({item["name"]: item["supplied_value"]})
        for item in expected_inputs]

    if suburb_response is not None and suburb_response != "":
        requested_suburb = expected_inputs[0]["supplied_value"]
        body_content, js_params = get_suburb_content(query_params)
        title = f"{requested_suburb.title()} Fuel Price"
        breadcrumbs = f"{requested_suburb.title()} Search Results"


    page_content = display.html_head(title)
    page_content += display.html_body_masthead(page_heading, breadcrumbs)

    page_content += DIV_MAIN_OPEN
    page_content += DIV_CONTENT_OPEN

    page_content += "<!-- <p>Results for: "
    for k, v in query_params.items():
        if v is None:
            v = "None"
        page_content += k + ": " + v + " "

    page_content += "</p> -->"

    page_content += display.display_locality_form(suburb=requested_suburb,
        selected_product=query_params["product"],
        selected_brand=query_params["brand"],
        surrounding=query_params["surrounding"])

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
    body_content = f"""<h3 class="error">Problem Encountered</h3>
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

    # FIXME add different forms
    page_content += display.display_locality_form()


    page_content += body_content
    page_content += DIV_CLOSE
    page_content += DIV_CLOSE
    page_content += display.html_body_footer()
    page_content += display.html_tail(js_params)

    return page_content


def get_sorted_data(get_data_function,
                    parameters,
                    extraction_mapping,
                    days=['yesterday', 'today', 'tomorrow']):
    '''
    Get the data and sort it.s

    '''
    stations = {}

    for day in days:
        # Creating a new key for price based on the day

        filtered_data = get_data_function(**parameters, day=day)

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
        error_text += f"<p>Please check the region and try again.</p>"
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
        error_text = f'<h3 class="error">No Data Exists for Suburb</h3>'
        error_text += f"<p>You may wish to include surrounding suburbs.</p>"
        error_text += f"""
        <p>Please check the suburb name.  If it is correct, 
        then use the surround suburbs option before trying again.</p>
        """
        return error_text, None
    else:
        table_content = display.formatted_html_table(sorted_data,
                                                     items_to_display)
        return table_content, items_to_display


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

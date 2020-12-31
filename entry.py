import data.suburb as suburb_info
import data.region as region_info
import imp
import data.fuel_data as fd

import view.display as display
import view.requests
import orchestration

# from orchestration import get_instructions
# from orchestration import suburb_identifier
# from orchestration import brand_identifier
# from orchestration import product_identifier
# from orchestration import surrounding_identifier
# from orchestration import fuel_site_params


from markupsafe import escape
from flask import Flask, request
# from flask import Flask, redirect, url_for, request
app = Flask(__name__)

imp.reload(suburb_info)
imp.reload(display)
imp.reload(fd)

DIV_MAIN_OPEN = '<div class="main">'
DIV_CLOSE = '</div>'
DIV_CONTENT_OPEN = '<div class="content">'


@app.route('/')
@app.route('/index.html')
@app.route('/index.htm')
def home_page():
    page_content = ""
    page_content = display.html_head("Fuel Prices")
    page_content += display.html_body_masthead("Fuel Prices", "")

    page_content += DIV_MAIN_OPEN
    page_content += DIV_CONTENT_OPEN

    page_content += display.display_locality_form(None)
    page_content += '''
<ul>
  <li>
    <a href="region?region_id=18&region_name=Mandurah">Mandurah</a>
  </li><li>
    <a href="region?region_id=26&region_name=South%20of%20River">South of River</a>
  </li><li>
    <a href="region?region_id=27&region_name=Hills%20%26%20East Metro">
      Hills &amp; East Metro
    </a>
  </li><li>
    <a href="region?region_id=25&region_name=North%20of%20River">North of River</a>
  </li>
</ul>

<p><a href="region.html">Search other regions.</a></p>
    '''

    page_content += DIV_CLOSE
    page_content += DIV_CLOSE
    page_content += display.html_body_footer()
    page_content += display.html_tail()

    return page_content


@app.route('/locality')
@app.route('/locality.html')
@app.route('/locality.htm')
def display_locality():
    query_request = view.requests.parse_locality_request()

    page_content = ""
    fuel_watch_instructions, html_display_instructions =\
        orchestration.get_instructions()

    title = "Fuel Price Search Results"
    page_heading = "Fuel Prices"
    breadcrumbs = "Search Results"

    if query_request is not None:
        parameters = {
            orchestration.suburb_identifier: query_request.get(
                orchestration.suburb_identifier, ""
            ),
            orchestration.surrounding_identifier: query_request.get(
                orchestration.surrounding_identifier,
                orchestration.fuel_site_params[
                    orchestration.surrounding_identifier
                ]["default"]
            ),
            orchestration.product_identifier: query_request.get(
                orchestration.product_identifier,
                orchestration.fuel_site_params[
                    orchestration.product_identifier
                ]["default"]
            ),
            orchestration.brand_identifier: query_request.get(
                orchestration.brand_identifier,
                orchestration.fuel_site_params[
                    orchestration.brand_identifier
                ]["default"]
            )
        }

        print("parameters are: ", parameters)

        title = f"""{query_request.get(
            orchestration.suburb_identifier, ""
        )} Fuel Price"""
        page_heading = "Fuel Prices"
        breadcrumbs = f"""{query_request.get(
            orchestration.suburb_identifier, ""
        )}"""

        sorted_data = fd.get_sorted_data(
            fd.get_fuel_by_suburb,
            parameters,
            fuel_watch_instructions)

        if sorted_data is None:
            body_content = display.get_connection_issue_message("suburb")
        elif len(sorted_data) < 1:
            body_content = display.get_no_data_available("suburb")
        else:
            body_content = display.formatted_html_table(
                sorted_data,
                html_display_instructions)
    else:
        body_content = display.get_initial_message("suburb")

    page_content = display.html_head(title)
    page_content += display.html_body_masthead(page_heading, breadcrumbs)

    page_content += DIV_MAIN_OPEN
    page_content += DIV_CONTENT_OPEN

    page_content += display.display_locality_form(query_request)

    page_content += body_content

    page_content += DIV_CLOSE
    page_content += DIV_CLOSE
    page_content += display.html_body_footer()
    page_content += display.html_tail(html_display_instructions)

    return page_content


@app.route('/region')
@app.route('/region.html')
@app.route('/region.htm')
def display_region():
    query_request = view.requests.parse_region_request()

    page_content = ""
    alt_content = ""  # <div>Pending</div>
    fuel_watch_instructions, html_display_instructions =\
        orchestration.get_instructions()

    title = "Fuel Price Search Results"
    page_heading = "Fuel Prices"
    breadcrumbs = "Search Results"

    if query_request is not None:
        parameters = {
            "region": query_request.get('region_id', None),
            "product": query_request.get('product', 1),
            "brand": query_request.get('brand', 0)
        }

        print("parameters are: ", parameters)
        # TODO escape characters
        title = f"{query_request['region_name']} Fuel Price"
        page_heading = "Fuel Prices"
        breadcrumbs = f"{query_request['region_name']}"

        sorted_data = fd.get_sorted_data(
            fd.get_fuel_by_region,
            parameters,
            fuel_watch_instructions)

        if sorted_data is None:
            body_content = display.get_connection_issue_message("region")
        elif len(sorted_data) < 1:
            body_content = display.get_no_data_available("region")
        else:
            body_content = display.formatted_html_table(
                sorted_data,
                html_display_instructions)
            # alt_content = display.enclose_in_div(
            #    display.html_div(sorted_data),
            #    element_class="different",
            #    element_id="asjson"
            # )
    else:
        body_content = display.get_initial_message("region")

    page_content = display.html_head(title)
    page_content += display.html_body_masthead(page_heading, breadcrumbs)

    page_content += DIV_MAIN_OPEN
    page_content += DIV_CONTENT_OPEN

    page_content += display.display_region_form(query_request)

    page_content += body_content
    page_content += alt_content

    page_content += DIV_CLOSE
    page_content += DIV_CLOSE
    page_content += display.html_body_footer()
    page_content += display.html_tail(html_display_instructions)

    return page_content


if __name__ == '__main__':
    app.run(debug=True, host='localhost')

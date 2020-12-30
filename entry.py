import data.suburb as suburb_info
import data.region as region_info
import imp
import fuel_data as fd
import json
import view.display as display

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

    page_content += display.display_locality_form()
    page_content += '''
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


@app.route('/region')
@app.route('/region.html')
@app.route('/region.htm')
def display_region():
    # ?id=<string:region_id>&name=<string:region_desc>
    # TODO sanitise !!!

    region_desc = request.args.get('regions', None)
    region_id = request.args.get('id', None)
    supplied_product = request.args.get(product_identifier, 1)
    supplied_brand = request.args.get(brand_identifier, 0)

    if (region_id is None and region_desc is not None):
        region_id = region_info.find_id(region_desc)


    print(region_desc)
    print(region_id)
    #TODO add look up region based on id

    page_content = ""

    # Assuming errors
    body_content = f"""<h3 class="error">Problem Encountered</h3>
    <p>Currently no data is available for region</p>

    """

    title = "Fuel Price Search Results"
    page_heading = "Fuel Prices"
    breadcrumbs = "Search Results"
    js_params = None
    if region_id:
        body_content, js_params = display.get_region_content({"region": region_id,
         "product" : supplied_product, "brand": supplied_brand})
        # TODO escape characters
        title = f"{region_desc} Fuel Price"
        page_heading = "Fuel Prices"
        breadcrumbs = f"{region_desc}"

    page_content = display.html_head(title)
    page_content += display.html_body_masthead(page_heading, breadcrumbs)

    page_content += DIV_MAIN_OPEN
    page_content += DIV_CONTENT_OPEN

    page_content += display.display_region_form(region_desc,
                        selected_product=supplied_product,
                        selected_brand=supplied_brand)

    extraction_mapping, items_to_display = get_instructions()

    sorted_data = fd.get_sorted_data(fd.get_fuel_by_region,
                                  {"region": region_id},
                                  extraction_mapping,
                                   days=['yesterday', 'today', 'tomorrow'])
    page_content += body_content

    page_content += "<div class+\"different\">"
    page_content += display.html_div(sorted_data)
    page_content += "</div>"
    page_content += DIV_CLOSE
    page_content += DIV_CLOSE
    page_content += display.html_body_footer()
    page_content += display.html_tail(js_params)

    return page_content    



if __name__ == '__main__':
    app.run(debug=True, host='localhost')

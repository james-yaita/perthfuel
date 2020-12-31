'''
display.py

Code to generate HTML content
'''
import os.path
import os
import urllib.parse

import data.suburb as list_of_suburbs
import data.region as list_of_regions
import data.product as product
import data.brand as brand
import imp

import data.fuel_data as fd

imp.reload(list_of_suburbs)
imp.reload(product)
imp.reload(brand)


INDEX_PAGE = "index.html"
DIV_MAIN_OPEN = '<div class="main">'
DIV_MAIN_CLOSE = '</div>'


def html_div(filtered_data):
  the_content = ""
  for station in filtered_data:
    the_content += f"<div class=\"station\" style=\"border: solid 2px #ffcccc;\" id=\"{station['trading_name']}\">"

    for item in station:

      the_content += f"<div class=\"{item}\">{station[item]}</div>"
    the_content += "</div>"
  return the_content


def formatted_html_table(filtered_data, cols):
  """


  Args:
    filtered_data (list): The sorted data set of prices
      and petrol station details
    cols (list): Column header information

  Returns:
    string: HTML table element

  """

  thead = '<table>\n'
  tbody = '<tbody id="info">\n'

  row_data = ["<thead>\n<tr>"]
  for col in cols:
    element_root = col['element_root']
    col_title = col['col_title']
    th_content = f"""
        <th id=\"{element_root}\">{col_title}</th>"""
    row_data.append(th_content)

  row_data.append("\n</tr>\n</thead>\n")
  thead += ' '.join(row_data)

  for row in filtered_data:
    tbody += "<tr>"
    for col in cols:

      # Put - when there is no data
      cell = row.get(col.get('data_set_key', None), '-')

      # Place data in td cell.
      # Uses a function to convert data to an appropriate format
      # eg. number of decimal points
      if 'display_function' in col.keys():
        cell_func = col.get('display_function')
        tbody += f"<td>{cell_func(cell)}</td>"
      else:
        tbody += f"<td>{cell}</td>"
    tbody += "</tr>\n"

  tbody += '</tbody>\n'
  tend = '\n</table>'

  return thead + tbody + tend


def html_head(title="Fuel Watch"):
  '''
  Returns the output for the HEAD section of a HTML page


  Args:
    title (string): For use in HTML title (default is 'Fuel Watch')

  Returns
  -------

  String for the Head element plus opening doctype element

  '''
  head = f'''<!DOCTYPE html>
<html lang="en-AU">
<head>
<meta charset="utf-8">
<title>{title}</title>
<link rel="stylesheet" href="static/style/desktop.css">
<link rel="stylesheet" href="static/style/mobile.css" media="only screen and (min-device-width: 320px) and (max-device-width: 500px)">
</head>
    '''
  return head


def enclose_in_div(content, element_class=None, element_id=None):
  '''
  Enclose content in a div tag

  Args:

  '''
  open_tag = "<div"

  if element_class:
    open_tag += f" class=\"{element_class}\""

  if element_id:
    open_tag += f" id=\"{element_id}\""

  open_tag += ">"
  close_tag = "</div>" + os.linesep

  update_content = open_tag + content + close_tag
  return update_content


def html_body_masthead(title, breadcrumb=""):
  '''
Returns the output for 'masthead' of a HTML page.
It included the opening <body> tag and is the first div in
the page.  It designed to included the page name


Parameters
----------

title: String.
        Text for the main heading

Returns
-------

String for the page masthead

  '''
  masthead = f'''
<body>
<a name="top"></a>
<div id="masthead">
<h1><a href="./index.html">{title}</a></h1>
<div class="breadcrumbs">
<a href="{INDEX_PAGE}">Home</a> &#x22EE {breadcrumb}</div>
</div>
'''
  return masthead


def display_region_form(request=None):
  Region = None
  selected_product = 1
  selected_brand = 0

  if request is not None:
    Region = request.get('region_name', None)
    selected_product = request.get('product', 1)
    selected_brand = request.get('brand', 0)

  print(f"""
      Regions {Region}
      product {selected_product}
      brand {selected_brand}

    """)

  region_combo = region_combo_box(list_of_regions.region_list,
                                  region_entered=Region)
  product_dropdown = create_dropdown(data_list=product.pl,
                                     data_option_value_key=product.item_id,
                                     date_option_name_key=product.item_name,
                                     default_selection=selected_product,
                                     html_name="product",
                                     html_id="product_dd")
  brand_dropdown = create_dropdown(data_list=brand.bl,
                                   data_option_value_key=brand.item_id,
                                   date_option_name_key=brand.item_name,
                                   default_selection=selected_brand,
                                   html_name="brand",
                                   html_id="brand_dd")

  form_info = f'''
    <h2>Search by Regions</h2>

    <div class="tab_container">

    <form method="GET" action="/region.html">
    <div class="form_group">
    <label for="region">Region:</label> {region_combo}
    </div>

    <div class="form_group">
    <label for="product">Fuel Type:</label> {product_dropdown}
    </div>

    <div class="form_group">
    <label for="brand_dd">Brand:</label> {brand_dropdown}
    </div>

    <div class="form_group">
    <input type="submit" value="Search">
    </div>
    </form>
    </div>

    '''
  return form_info


def display_locality_form(request=None):
  suburb = None
  selected_product = 1
  selected_brand = 0
  surrounding = "yes"

  if request is not None:
    suburb = request.get('suburb', None)
    selected_product = request.get('product', 1)
    selected_brand = request.get('brand', 0)
    surrounding = request.get('surrounding', None)

  print(f"""
      suburb {suburb}
      surrounding {surrounding}
      product {selected_product}
      brand {selected_brand}

    """)

  suburb_combo = suburb_combo_box(list_of_suburbs.sl, suburb_entered=suburb)
  product_dropdown = create_dropdown(data_list=product.pl,
                                     data_option_value_key=product.item_id,
                                     date_option_name_key=product.item_name,
                                     default_selection=selected_product,
                                     html_name="product",
                                     html_id="product_dd")
  brand_dropdown = create_dropdown(data_list=brand.bl,
                                   data_option_value_key=brand.item_id,
                                   date_option_name_key=brand.item_name,
                                   default_selection=selected_brand,
                                   html_name="brand",
                                   html_id="brand_dd")

  # Created the checkbox for surronding suburbs
  # and decide if is checked.
  surrounding_status = ""
  if surrounding == "yes":
    surrounding_status = 'checked="checked"'

  surrounding_suburbs_input = f'''
    <input type="checkbox" id="surrounding" name="surrounding"
     value="yes" {surrounding_status}>
    '''

  form_info = f'''
    <h2>Search by Locality</h2>

    <div class="tab_container">

    <form method="GET" action="/locality.html">
    <div class="form_group">
    <label for="suburb">Suburb:</label> {suburb_combo}
    </div>

    <div class="form_group">
    <label for="surround">Include Surrounding Suburbs:</label> {surrounding_suburbs_input}
    </div>

    <div class="form_group">
    <label for="product">Fuel Type:</label> {product_dropdown}
    </div>

    <div class="form_group">
    <label for="brand_dd">Brand:</label> {brand_dropdown}
    </div>

    <div class="form_group">
    <input type="submit" value="Search">
    </div>
    </form>
    </div>

    '''
  return form_info


def create_dropdown(data_list,
                    data_option_value_key,
                    date_option_name_key,
                    html_name,
                    html_id,
                    default_selection=None,
                    css_class=None):

  css_class_text = ""

  if css_class is not None:
    css_class_text = f' class="{css_class}"'

  html_code = f'''
    <select name="{html_name}" id="{html_id}"{css_class_text}>
'''
  # check that data_list is a list

  for item in data_list:
    if data_option_value_key in item:
      html_code += f'<option value="{item[data_option_value_key]}"'

      if default_selection is not None:

        if str(default_selection) == str(item[data_option_value_key]):
          html_code += ' selected="selected"'
      html_code += f'''>
              {item.get(date_option_name_key,"&nbsp;")}</option>\n'''

  html_code += '</select>'
  return html_code


def suburb_combo_box(suburb_list, suburb_entered=None):

  current_value = ""
  if suburb_entered is not None:
    current_value = f'value="{suburb_entered}"'
  '''
    Produce a drop down but editable text
    '''
  html_text = f'''
<input type="text" list="suburbs" id="suburb"
{current_value} name="suburb">
<datalist id="suburbs">'''

  for suburb_name in suburb_list:
    html_text += f"<option>{suburb_name}</option>\n"

  html_text += "</datalist>"
  return html_text


def region_combo_box(region_list, region_entered=None):
  current_value = ""
  if region_entered is not None:
    current_value = f' value="{region_entered}"'
  '''
    Produce a drop down but editable text
    '''
  html_text = f'''
<input type="text" list="regions" id="region"
{current_value} name="region_name">
<datalist id="regions">'''

  for region in region_list:
    #        html_text += f"""<option data-region=\"{region['region_id']}\"
    # value=\"{region['region_name']}\"/>"""
    html_text += f"""<option value=\"{urllib.parse.unquote_plus(region['region_name'])}\">
 {region['region_name']}</option>"""

  html_text += "</datalist>"
  return html_text


def get_initial_message(requested_zone):
  message = f"""
<p>Use the search options above to find prices for a {requested_zone}.
    """
  return message


def get_connection_issue_message(requested_zone):
  message = f"<h3 class=\"error\">Problem Encountered.</h3>"
  message += f"""
<p>Currently no data is available
 for the {requested_zone}.</p>

<p>Please try again later.</p>
"""

  return message


def get_no_data_available(requested_zone):
  message = f"<p>No data for the requested {requested_zone}.</p>"
  message += f"<p>Please check the {requested_zone} and try again.</p>"

  return message


# TODO deprecate
def get_suburb_content(query_request, days=['yesterday', 'today', 'tomorrow']):

  extraction_mapping, items_to_display = get_instructions()

  sorted_data = fd.get_sorted_data(fd.get_fuel_by_suburb,
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


def html_body_footer():
  """
Returns the output for footer of a HTML page.
Typically it will be the footer navigation and copyright
notices

Parameters
----------
None

Returns
-------

String containing content for page footer in the HTML body

  """

  footer = f'''
<div id="footer">
<p>
Data derived from the <a href="https://www.fuelwatch.wa.gov.au">Fuel Watch website</a>. Instructions for using this data feed are at <a href="https://www.fuelwatch.wa.gov.au/fuelwatch/pages/public/contentholder.jspx?key=fuelwatchRSS.html">
Fuel Watch RSS</a>
</p>
</div>
'''
  return footer


def html_tail(items_to_display=None):
  '''
  Returns the dynamic javascript code to be inserted once table has been displayed.


  Parameters
  ----------
  None

  Returns
  -------
  Close the HTML tags


col_title : Co-Ords
col_number : 5
html_display : <function display_co_ords at 0x7fe3d0cb67b8>
html_sort_function : None
html_name : LOCALITY
direction : DIR_UNKNOWN
element_root : locality


  '''
  script_text = ""

  if items_to_display is not None:
    script_text += '''
<script type="text/javascript" src="static/scripts/sort.js"></script>
<script>
    var sorter = new SortData("info", [
            '''
    sorter_array = []

    for group in items_to_display:
      # Pass the information to a Javascript quasi class object
      # to allow the right type of sorting
      if group["html_sort_function"] is not None:
        ele = f'''
        {{
        "name": "{group['html_name']}",
          "td_element_id": "{group['element_root']}",
          "col_number": {group['col_number']},
          "direction": {group['direction']},
          "img_element_id": "{group['element_root']}_image",
          "sort_cat_function": "{group['html_sort_function']}"
        }}'''
        sorter_array.append(ele)

    script_text += ','.join(sorter_array)
    script_text += '])'
    script_text += '\n</script>'
  # end if for script_text

  tail = f'''
<div class="tail">
    <a href="{INDEX_PAGE}">Home</a> | <a href="#top">Page Top</a>
</div>
{script_text}

</body>
</html>
  '''
  return tail

# These are the Cell Functions

# ===========================================================


def cents_to_dollar(price):
  return "$" + format((float(price) / 100), '4.2f')


def display_price(data):
  answer = '-'
  try:
    if data:
      price = float(data)
      answer = f"{price:.1f}"
  except:
    print("data wrong", "type is ", type(data))
  return answer


def display_co_ords(data):
  '''
  Create link to google maps
          https://www.google.com/maps/dir/?api=1&parameters
  https://www.google.com/maps/search/?api=1&query=47.5951518,-122.3316393
  '''
  google_query = "https://www.google.com/maps/search/?api=1&query="
  co_ords = data.split(',')
  lat_str = f"{float(co_ords[0]):.3f}"
  lon_str = f"{float(co_ords[1]):.3f}"
  inner_html = f"<a href=\"{google_query}{data}\""
  inner_html += " title=\"Google Maps link for latitude "
  inner_html += f"{lat_str}, longitude {lon_str}\">"
  inner_html += f"Google Maps"
  inner_html += "</a>"

  return inner_html


def display_as_is(data):
  return data

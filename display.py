'''
display.py

Code to generate HTML content
'''
import os.path
import suburb as list_of_suburbs
import product
import brand
import imp

imp.reload(list_of_suburbs)
imp.reload(product)
imp.reload(brand)


INDEX_PAGE = "index.html"
DIV_MAIN_OPEN = '<div class="main">'
DIV_MAIN_CLOSE = '</div>'


def generate_file(data_set,
                  file_name,
                  page_title="Fuel Watch",
                  h1_title="Fuel Watch Prices",
                  breadcrumb="Prices",
                  column_info=None
                  ):
    """
        Writes a HTML page utilising the dataset to the supplied location.

        Options exist to change page titles.

    Exceptions
    ----------

    Throws a general exception when it cannot write to file


    Parameters
    ----------

    data_set: List.
            Data used to create page contents
    file_name: String.
            Location to save HTML content
    page_title: String, default.
            Text to population HTML <title> tag
    h1_title: String, default.
            Text to populate HTML H1 tag in page masthead
    column_info: String, default is None
            Information to make the page sortable using JavaScript.
            Will refer to content in other folders for
            JavaScript and Images


    Returns
    -------
    None

    """

    try:
        print(f"Attempting to generate HTML file")
        base_dir = os.path.dirname(os.path.abspath(__file__))
        fn = os.path.join(base_dir, "html", "dynamic", file_name)

        f = open(fn, 'w')

        f.write(
            html_head(page_title),
            html_body_masthead(h1_title, breadcrumb),
            DIV_MAIN_OPEN,
            formatted_html_table(data_set, column_info),
            DIV_MAIN_CLOSE,
            html_body_footer(),
            html_tail(column_info)
        )
        f.close()
        print(f"File Printed to {fn}")

    except Exception as iso_ex:
        print("Could not write to file: ", file_name)
        print(iso_ex)

    return None


def formatted_html_table(filtered_data, cols):
    """
    Returns the closing body and html tags for a HTML page.

  Parameters
  ----------
  filtered_data : List
          The sorted data set of prices and petrol station details
  cols : Tuple of dictionary
          The set of column title and data access keys to use


  Returns
  -------
  The HTML table text


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

            # By getting the column data to be the key,
            # try and find it in the row
            cell = row.get(col.get('data_set_key', None), '-')

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


    Parameters
    ----------

    title: String, default Fuel Watch.
            Text for the HTML title tag

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


def display_locality_form(suburb=None,
                          selected_product=1,
                          selected_brand=0,
                          surrounding="yes"):
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
    # adn decide if is checked.
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

    <form method="GET" action="/prices.html">
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


# ===========================================================
def cents_to_dollar(price):
    return "$" + format((float(price) / 100), '4.2f')


def display_price(data):
    answer = '-'
    try:
      price = float(data)
      answer = f"{price:.1f}"
    except:
      answer = '&nbsp;'

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

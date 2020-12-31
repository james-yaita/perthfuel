import json
from flask import Flask
from flask import request
from flask import Response


from markupsafe import escape
# import json
# from flask import Flask, request

import orchestration
import data.suburb as list_of_suburbs
import data.region as list_of_regions
import data.product as product
import data.brand as brand
import imp

import data.fuel_data as fd


imp.reload(list_of_suburbs)
imp.reload(product)
imp.reload(brand)

# http://blog.luisrei.com/articles/flaskrest.html


def localityJson(info):
    print(info)

    # default to unleaded
    product = request.args.get('product', 1)

    # default to all brands
    brand = request.args.get('brand', 0)

    # default to surrounding suburbs
    surrounding = request.args.get('surrounding', "yes")

    parameters = {"suburb": info,
                  "product": product,
                  "brand": brand,
                  "surrounding": surrounding
                  }

    extract = {
        "trading_name": "trading-name",
        "brand": "brand",
        "street_address": "address",
        "locality": "location",
        "co-ords": ['latitude', 'longitude']
    }

    sorted_data = fd.get_sorted_data(
        fd.get_fuel_by_suburb,
        parameters,
        extract
    )

    js = json.dumps(sorted_data)

    resp = Response(js, status=200, mimetype='application/json')

    print("return a JSON")

    return resp

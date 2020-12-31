from markupsafe import escape
import json
from flask import Flask, request

import orchestration
import data.suburb as list_of_suburbs
import data.region as list_of_regions
import data.product as product
import data.brand as brand
import imp


imp.reload(list_of_suburbs)
imp.reload(product)
imp.reload(brand)


def parse_region_request():
    print("Is it global?")
    region_desc = request.args.get('region_name', None)
    region_id = request.args.get('region_id', None)

    product = orchestration.product_identifier
    supplied_product = request.args.get(
        product,
        orchestration.fuel_site_params[product]["default"]
    )

    brand = orchestration.brand_identifier
    supplied_brand = request.args.get(
        brand,
        orchestration.fuel_site_params[brand]["default"]
    )

    request.args.get(orchestration.brand_identifier, 0)
    print("product is ",supplied_product)
    print("brand is ", supplied_brand)

    if (region_id is None and region_desc is not None):
        region_id = list_of_regions.find_id(region_desc)
    elif (region_id is not None and region_desc is None):
        region_desc = list_of_regions.find_desc(region_id)
    else:
        return None

    query_params = {
        product: supplied_product,
        brand: supplied_brand,
        'region_name': region_desc,
        'region_id': region_id
    }

    print("Query params are ", query_params)

    return query_params

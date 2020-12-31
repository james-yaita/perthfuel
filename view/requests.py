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


def parse_locality_request():
    suburb = orchestration.suburb_identifier

    supplied_suburb = request.args.get(suburb, "")

    surrounding_info = orchestration.surrounding_identifier
    supplied_surrounding = request.args.get(
        surrounding_info, "no"
    )

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

    query_params = {
        product: supplied_product,
        brand: supplied_brand,
        suburb: supplied_suburb,
        surrounding_info: supplied_surrounding
    }

    print("Query params are ", query_params)

    return query_params


def parse_region_request():

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

    if (region_id is None and region_desc is not None):
        region_id = list_of_regions.find_id(region_desc)
    elif (region_id is not None and region_desc is None):
        region_desc = list_of_regions.find_desc(region_id)
    elif (region_id is None and region_desc is None):
        return None

    query_params = {
        product: supplied_product,
        brand: supplied_brand,
        'region_name': region_desc,
        'region_id': region_id
    }

    print("Query params are ", query_params)

    return query_params

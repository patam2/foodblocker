"""
"""


import requests
import re


class Selver:
    def __init__(self) -> None:
        self.session = requests.Session()

    def get_product_categories(self) -> dict:
        output = {}
        for product_id in range(50):
            vue_query = '{"query":{"bool":{"filter":{"bool":{"must":[{"terms":{"level":[%d]}},{"terms":{"is_active":[true]}}]}}}}}&size=4000&sort=position:asc' % product_id
            req = self.session.get('https://www.selver.ee/api/catalog/vue_storefront_catalog_et/category/_search?from=0&request=' + vue_query).json()
            if req['hits']['total']['value'] == 0:
                continue
            for raw_product_data in req['hits']['hits']:                
                output[raw_product_data['_source']['id']] = raw_product_data['_source']['url_path']
        return output

    def get_products_by_category(self, catid: str) -> dict: #Todo -> recursion
        product_query = open(r'C:\Users\patri\Desktop\Praktiline töö\epoe_moodulid\selver_page_get_query.txt', 'r').read().replace('PRODUCTID', catid)

        page, remaining, output = 0, 0, {}

        req = self.session.get(product_query).json()

        for raw_product_data in req['hits']['hits']:
            if 'product_ingrediens' in raw_product_data['_source']:
                output[raw_product_data['_source']['url_path']] = {'ingrediens': raw_product_data['_source']['product_ingrediens']}
        return output



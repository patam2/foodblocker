"""
"""


from collections import defaultdict
import os
import re
import requests


class Selver:
    def __init__(self) -> None:
        self.session = requests.Session()

    def get_product_categories(self) -> dict:
        """
        Loopib Selveri vue apist product numbritega 2-5,
        dict {
            selver_id: selver_name
        }
        """

        output = {}
        for product_id in range(2, 6):
            vue_query = '{"query":{"bool":{"filter":{"bool":{"must":[{"terms":{"level":[%d]}},{"terms":{"is_active":[true]}}]}}}}}&size=4000&sort=position:asc' % product_id
            req = self.session.get('https://www.selver.ee/api/catalog/vue_storefront_catalog_et/category/_search?from=0&request=' + vue_query).json()
            if req['hits']['total']['value'] == 0:
                continue
            for raw_product_data in req['hits']['hits']:                
                output[raw_product_data['_source']['id']] = raw_product_data['_source']['url_path']
        return output

    def get_incrediens_by_category(self, catid: str) -> dict:
        """
        Võtab vastu selveri kategooria numbri, annab tagasi tooted ja nende allergeenid, koostisosad,
        dict {
            product_url {
                incrediens: str
                allergens: str
            }
        }
        """
        product_query = open(fr'{os.getcwd()}\epoe_moodulid\selver_page_get_query.txt', 'r').read().replace('PRODUCTID', catid)

        page, remaining, output = 0, 0, defaultdict(dict)

        req = self.session.get(product_query).json()
        for raw_product_data in req['hits']['hits']:
            url_path = raw_product_data['_source']['url_path']
            if 'product_ingrediens' in raw_product_data['_source']:
                output[url_path]['ingrediens'] = raw_product_data['_source']['product_ingrediens']
            if 'product_allergens' in raw_product_data['_source']:
                output[url_path]['allergens'] = raw_product_data['_source']['product_allergens']
        return output

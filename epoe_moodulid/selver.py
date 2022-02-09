"""
"""


import os
import requests


class Selver:
    def __init__(self) -> None:
        self.session = requests.Session()
        self.product_query = open(
            rf"{os.getcwd()}\epoe_moodulid\selver_page_get_query.txt", "r"
        ).read()

    def get_product_categories(self) -> dict:
        """
        Loopib Selveri vue apist product numbritega 2-5,
        dict {
            selver_id: selver_name
        }
        """

        output = {}
        for product_id in range(2, 6):
            vue_query = (
                '{"query":{"bool":{"filter":{"bool":{"must":[{"terms":{"level":[%d]}},{"terms":{"is_active":[true]}}]}}}}}&size=150&sort='
                % product_id
            )
            req = self.session.get(
                "https://www.selver.ee/api/catalog/vue_storefront_catalog_et/category/_search?from=0&request="
                + vue_query
            ).json()
            if req["hits"]["total"]["value"] == 0:
                continue
            for raw_product_data in req["hits"]["hits"]:
                output[str(raw_product_data["_source"]["id"])] = raw_product_data[
                    "_source"
                ]["url_path"]
        return output

    def get_incrediens_by_category(self, catid: str, page=0, output=[]) -> list:
        """
        Võtab vastu selveri kategooria numbri, annab tagasi tooted ja nende allergeenid, koostisosad,
        [{
            product_url: str,
            incrediens: str,
            allergens: str
        }, ... ]
        """
        product_query = self.product_query.replace("PRODUCTID", catid)

        if page > 0:
            product_query = product_query.replace(f"from=0", f"from={page*96}")
        req = self.session.get(product_query).json()
        hits = req["hits"]["total"]["value"]

        for raw_product_data in req["hits"]["hits"]:
            to_add = {"allergens": "", "ingrediens": ""}
            to_add["url_path"] = raw_product_data["_source"]["url_path"]
            if "product_ingrediens" in raw_product_data["_source"]:
                to_add["ingrediens"] = raw_product_data["_source"][
                    "product_ingrediens"
                ].lower()
            if "product_allergens" in raw_product_data["_source"]:
                to_add["allergens"] = raw_product_data["_source"][
                    "product_allergens"
                ].lower()
            output.append(to_add)
        if hits - (page + 1) * 96 > 0:
            return self.get_incrediens_by_category(catid, page + 1, output)
        return output
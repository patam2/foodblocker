import re
import os
from pymongo import MongoClient
from epoe_moodulid import selver


MONGODB_PORT = 27017  # TODO: env

selver_client = selver.Selver()
mongo_client = MongoClient(host=os.environ.get('MONGODB_IP'), port=MONGODB_PORT)
selver_db = mongo_client["filter"]["selver_products"]


def format_ingrediens(raw: str) -> list:
    """
    Eemaldab ebavajalised stringid, võib sisaldada, jne.
    """

    if match := re.search(pattern="(toode)* võib (sisaldada)*", string=raw, flags=re.I):
        if match.groups() != (None, None):
            raw = raw[: match.start()]
    return raw


for cat_id, cat_name in selver_client.get_product_categories().items():
    try:
        gathered_incrediens = selver_client.get_incrediens_by_category(cat_id, output=[])

        if gathered_incrediens == []:
            continue
        for enum, incredient in enumerate(gathered_incrediens):
            gathered_incrediens[enum]["ingrediens"] = format_ingrediens(
                incredient["ingrediens"]
            )
            gathered_incrediens[enum]["allergens"] = format_ingrediens(
                incredient["allergens"]
            )

            selver_db.update_one({'url_path': gathered_incrediens[enum]['url_path']}, {"$set": gathered_incrediens[enum]}, upsert=True)
    except Exception as E:
        print(E)
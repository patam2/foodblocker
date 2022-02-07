import re
from pymongo import MongoClient
from epoe_moodulid import selver


MONGODB_IP = '127.0.0.1'
MONGODB_PORT = 27017 #TODO: env

selver_client = selver.Selver()
mongo_client = MongoClient(host=MONGODB_IP, port=MONGODB_PORT)
selver_db = mongo_client['filter']['selver_products']

def format_ingrediens(raw: str) -> list:
    """
    Eemaldab ebavajalised stringid, võib sisaldada, jne.
    """
    print(raw)
    remove_strings = []
  
    if match := re.search(
        pattern = '(toode)* võib (sisaldada)*',
        string = raw, 
        flags = re.I
    ):
        if match.groups() != (None, None):
            raw = raw[:match.start()]

    return raw


for cat_id, cat_name in selver_client.get_product_categories().items():
    gathered_incrediens = selver_client.get_incrediens_by_category(
        cat_id, 
        output = []
    ) 

    if gathered_incrediens == []:
        continue
    
    try:
        status = selver_db.insert_many(
            gathered_incrediens
        )
        print(cat_id, len(status.inserted_ids), 'added') 
    except:
        pass
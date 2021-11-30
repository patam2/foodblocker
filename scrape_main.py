import re
from pymongo import MongoClient
from epoe_moodulid import selver


MONGODB_IP = '127.0.0.1'
MONGODB_PORT = 27017

selver_client = selver.Selver()
mongo_client = MongoClient(host=MONGODB_IP, port=MONGODB_PORT)
selver_db = mongo_client['filter']['selver_products']

def format_ingrediens(raw: str) -> list:
    """
    Eemaldab ebavajalised stringid, võib sisaldada, jne.
    """
    print(raw)
    remove_strings = []
  
    if match := re.search('(toode)* võib (sisaldada)*', raw, flags=re.I): #Eemaldab "toode v6ib sisaldada" asjad
        if match.groups() != (None, None):
            raw = raw[:match.start()] #Kuna need marked on lopus ss saab votta alguse

    return raw


for cat_id, cat_name in selver_client.get_product_categories().items():
    gathered_incrediens = selver_client.get_incrediens_by_category(
        cat_id, 
        output = [] #ma ei tea miks, aga kui seda parami ei ole siis tulevad mongodb id-d peale ??? miks????
    ) 
    
    if gathered_incrediens == []:
        continue
    
    status = selver_db.insert_many(
        gathered_incrediens #Todo: ükshaaval et vältida duplikaate?
    )
    print(cat_id, len(status.inserted_ids), 'added') #
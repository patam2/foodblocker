import pymongo
import re


MONGODB_IP = '127.0.0.1'
MONGODB_PORT = '27001'


def format_ingrediens(raw: str) -> list:
    """
    Cleans the ingrediens string by splitting commas, removing information that may not be needed.
    """
    output = [] 
    if match := re.search('(toode)* võib (sisaldada)*', raw, flags=re.IGNORECASE): #Eemaldab "toode v6ib sisaldada" asjad
        raw = raw[:match.start()] #Kuna need marked on lopus ss saab votta alguse

    for item in raw.split(','):
        if '(' in item:
            output.append(
                item.split('(', 1)[1].rstrip(')-')
            )

            if ' '

            continue
        output.append(item)

    return output


format_ingrediens("""
Suhkur, vahvel 17% (NISUJAHU, rapsiõli, emulgaator (letsitiin), sool, kergitusaine E500, MUNAPULBER, stabilisaator E414), kakaomass, MANDEL, kakaovõi, taimsed rasvad (palmi-, võiseemnikutuumaõli), emulgaator (letsitiin), lõhna- ja maitseaine, vanilliin. Šokolaadi min. 40%. Säilitusaineteta. Võib sisaldada vähesel määral pähkleid, maapähklit, piimatooteid ja seesamiseemneid.
""")
import re


MONGODB_IP = '127.0.0.1'
MONGODB_PORT = '27001'


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

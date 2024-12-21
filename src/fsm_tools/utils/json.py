import os
import locale
import json
from .common import generate_code

json_data = {}

def seek_json_message(msg_id:str, domain: str, lang:str = None) -> str:
    """

    """
    if len(json_data) == 0 or domain not in json_data.keys():
        json_file = open(os.path.join(os.path.dirname(__file__), "../locales", domain+".json"), "r")
        json_data[domain] = json.load(json_file)

    if lang is None:
        lang = str(locale.getdefaultlocale()[0])
        if lang not in json_data[domain].keys():
            lang = "en-US"

    if msg_id not in json_data[domain][lang].keys():
        raise KeyError(msg_id)
    else:
        return json_data[domain][lang][msg_id]

def generate_json_message(grammar:str, component: str, action:str, lang:str = None) -> str:
    """

    """
    return seek_json_message(generate_code(grammar, component, action), "automata", lang)

def get_json_message(msg_id:str, lang:str = None) -> str:
    """

    """
    return seek_json_message(msg_id, "automata", lang)
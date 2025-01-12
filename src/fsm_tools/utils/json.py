import os
import locale
import json
from typing import Union, Dict, Any
from pathlib import Path
from .common import generate_code

path = Path(os.path.dirname(__file__))
localized_messages = {}


def load_message(domain: str) -> None:
    """
    Charge ou met à jour le dictionnaire pour un domaine donné.

    :param domain: Domaine correspondant au fichier JSON
    :type domain: str
    """
    global localized_messages
    json_file_path = os.path.join(path.parent.absolute(), "locales", domain + ".json")

    if not os.path.isfile(json_file_path):
        raise FileNotFoundError(f"The JSON file for domain '{domain}' was not found.")

    with open(json_file_path, "r", encoding="utf-8") as json_file:
        localized_messages[domain] = json.load(json_file)


def seek_message(msg_id: str, domain: str, lang: str = None) -> str:
    """
    Recherche un message localisé dans un domaine donné.

    :param msg_id: Identifiant du message
    :type msg_id: str
    :param domain: Domaine du message
    :type domain: str
    :param lang: Langue (ex: 'fr-FR', 'en-US'). Si None, utilise la langue par défaut
    :type lang: str
    :return: Message localisé
    :rtype: str
    """
    if domain not in localized_messages:
        load_message(domain)

    messages = localized_messages[domain]

    if lang is None:
        lang = str(locale.getdefaultlocale()[0])

    if lang not in messages:
        lang = "en-US"

    if msg_id not in messages[lang]:
        raise KeyError(f"The message with ID '{msg_id}' was not found for language '{lang}'.")

    return messages[lang][msg_id]


def format_message(template: str, **kwargs) -> str:
    """
    Formate un message en injectant des paramètres dynamiques.

    :param template: Modèle de message avec des espaces réservés (ex: "Bonjour, {nom} !")
    :type template: str
    :param kwargs: Paramètres à injecter dans le message
    :return: Message formaté
    :rtype: str
    """
    try:
        return template.format(**kwargs)
    except KeyError as e:
        raise ValueError(f"The parameter '{e.args[0]}' is missing for formatting the message.")


def get_message(msg_id: str, domain: str, lang: str = None, **kwargs) -> str:
    """
    Génère un message formaté en recherchant le modèle et en injectant des paramètres.

    :param msg_id: Identifiant du message
    :type msg_id: str
    :param domain: Domaine du message
    :type domain: str
    :param lang: Langue (optionnel)
    :type lang: str
    :param kwargs: Paramètres dynamiques pour formater le message
    :return: Message formaté
    :rtype: str
    """
    raw_message = seek_message(msg_id, domain, lang)
    return format_message(raw_message, **kwargs)


def generate_message(grammar: str, component: str, action: str, domain: str, lang: str = None, **kwargs) -> str:
    """

    """
    msg_id = generate_code(grammar, component, action)
    raw_msg = seek_message(msg_id, domain, lang)
    return format_message(raw_msg, **kwargs)


def json_to_po(json_domain: Union[Dict[str, any], str], output_dir: str, **kwargs):
    """
    Transposes a dictionary of localized messages in JSON format or loads a dictionary from a file of localized messages
    in JSON format to convert it into an i18n file structure compatible with gettext after transformation.

    This function relies on non-significant 'msgid' keys in the JSON dictionary and multiple 'msgstr' entries in a list.

    **Note:** It does not currently handle plurals.

    The language description uses IETF language tags commonly found in locales. These tags are broken down into sub-tags:
        - The first sub-tag, in lowercase, refers to the language
        - The subsequent sub-tags are extensions.

    The primary language tag is used to ensure the consistency of the messages.

    Actions
    -------

    This function performs several checks:

        - Verifies that each language has the same number of messages.
        - Ensures that the sets of IDs across languages overlap (i.e., the pairwise difference between the sets is zero).
        - If there is a difference, it checks for the existence of a complete set of messages for the language, which will
          be used to fill in the missing 'msgid' entries before constructing the portable file (.po).
        - Ensures that the cardinality of each 'msgstr' list is identical.

    Notes
    -----

    This function only raises alerts and does not modify the input contents. It prepares the i18n architecture based on
    the following structure:

       | base_path
       |- locales
       |-- lang_tag
       |---- LC_MESSAGES
       |----- domain.po


    :param json_domain: a dictionary containing localized messages or the name of a file containing messages in JSON format.
    :type json_domain: Union[Dict[str, Any], str]
    :param output_dir: the output directory where the i18n file structure will be generated.
    :type output_dir: str
    :param kwargs: see below
    :return: None
    :rtype: None
    :keyword arguments:
        source (``str``) : The source language for the translation (used as a reference).
        languages (``list``) : A list of target languages to handle the completeness of extensions for certain languages.
        authors (``list``) : A list of authors.
    """
    def check_lang_cardinality(cardinality, lang) -> bool:
        lang_cardinality = len(set(json_data[lang].keys()))
        return lang_cardinality == cardinality

    def check_lang_keys(source_lang, dest_lang) -> set:
        source_keys = set(json_data[source_lang].keys())
        dest_keys = set(json_data[dest_lang].keys())
        return source_keys - dest_keys

    source = ""
    languages = []
    authors = []
    json_data = {}
    if kwargs:
        try:
            source = kwargs.pop("source")
            languages = kwargs.pop("languages")
            authors = kwargs.pop("authors")
        except KeyError:
            pass
    if isinstance(json_domain, dict):
        json_data = json_domain
    else:
        load_message(json_domain)
        json_data = localized_messages[json_domain]

    if source:
        print("Checking with source language...")
        keys_card = len(set(json_data[source].keys()))
        for key, lang in json_data.items():
            print("Checking language '{lang}' with source '{source}'...".format(lang=key, source=source))
            if check_lang_cardinality(keys_card, key):
                print("Check is True.")
            else:
                print("Check is False.")
                language = key[:2]
                if len(languages) > 0 and language in languages:
                    print("Filling missing keys")
                    mkeys = check_lang_keys(source, key)
                    print("Set difference is '{set}".format(set=mkeys))
                    for mkey in mkeys:
                        json_data[key][mkey] = json_data[language][mkey]
            print("Number of keys is {keys}".format(keys=len(set(json_data[key].keys()))))
            print("Set difference is : {set}".format(set=check_lang_keys(source, key)))
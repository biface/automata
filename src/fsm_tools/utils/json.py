import os
import locale
import json
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

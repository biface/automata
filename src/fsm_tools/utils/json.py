import json
import os
from pathlib import Path

from .common import generate_code

path = Path(os.path.dirname(__file__))
localized_messages = {}

_DEFAULT_LANG = "en-US"


def load_message(domain: str) -> None:
    """
    Load or refresh the message dictionary for a given domain.

    Looks for a JSON file named ``<domain>-ng.json`` in the ``locales/`` directory
    adjacent to the ``fsm_tools`` package root.

    :param domain: Domain name corresponding to the JSON file (without suffix).
    :type domain: str
    :raises FileNotFoundError: If the JSON file for the domain does not exist.
    """
    global localized_messages
    json_file_path = os.path.join(
        path.parent.absolute(), "locales", domain + ".json"
    )

    if not os.path.isfile(json_file_path):
        raise FileNotFoundError(f"The JSON file for domain '{domain}' was not found.")

    with open(json_file_path, "r", encoding="utf-8") as json_file:
        localized_messages[domain] = json.load(json_file)


def seek_message(msg_id: str, domain: str, lang: str = None) -> str:
    """
    Look up a message by ID in a given domain.

    The ``lang`` parameter is accepted for future ``i18n-tools`` compatibility
    but has no effect in this version — the language is fixed to ``en-US``.

    :param msg_id: Message identifier (numeric string matching a key in the JSON file).
    :type msg_id: str
    :param domain: Message domain (``"automata"`` or ``"errors"``).
    :type domain: str
    :param lang: Reserved for future use. Has no effect until ``i18n-tools`` is integrated.
    :type lang: str
    :return: Raw message template string.
    :rtype: str
    :raises KeyError: If ``msg_id`` is not found for the active language.
    """
    if domain not in localized_messages:
        load_message(domain)

    messages = localized_messages[domain]
    active_lang = _DEFAULT_LANG

    if active_lang not in messages:
        raise KeyError(
            f"Language '{active_lang}' is not available in domain '{domain}'."
        )

    if msg_id not in messages[active_lang]:
        raise KeyError(
            f"The message with ID '{msg_id}' was not found for language '{active_lang}'."
        )

    return messages[active_lang][msg_id]


def format_message(template: str, **kwargs) -> str:
    """
    Inject dynamic parameters into a message template.

    :param template: Message template with placeholders (e.g. ``"Symbol '{symbol}' is invalid."``).
    :type template: str
    :param kwargs: Named parameters to inject.
    :return: Formatted message.
    :rtype: str
    :raises ValueError: If a required placeholder parameter is missing from ``kwargs``.
    """
    try:
        return template.format(**kwargs)
    except KeyError as e:
        raise ValueError(
            f"The parameter '{e.args[0]}' is missing for formatting the message."
        )


def get_message(msg_id: str, domain: str, lang: str = None, **kwargs) -> str:
    """
    Fetch and format a message by ID.

    The ``lang`` parameter is accepted for future ``i18n-tools`` compatibility
    but has no effect in this version — the language is fixed to ``en-US``.

    :param msg_id: Message identifier.
    :type msg_id: str
    :param domain: Message domain (``"automata"`` or ``"errors"``).
    :type domain: str
    :param lang: Reserved for future use. Has no effect until ``i18n-tools`` is integrated.
    :type lang: str
    :param kwargs: Named parameters to inject into the message template.
    :return: Formatted message.
    :rtype: str
    """
    raw_message = seek_message(msg_id, domain, lang)
    return format_message(raw_message, **kwargs)


def generate_message(
    grammar: str, component: str, action: str, domain: str, lang: str = None, **kwargs
) -> str:
    """
    Compute the error code from ``(grammar, component, action)`` and return the
    corresponding formatted message.

    The ``lang`` parameter is accepted for future ``i18n-tools`` compatibility
    but has no effect in this version — the language is fixed to ``en-US``.

    :param grammar: Chomsky grammar level name (e.g. ``"Regular"``).
    :type grammar: str
    :param component: Grammar component name (e.g. ``"alphabet"``).
    :type component: str
    :param action: Action name (e.g. ``"add"``).
    :type action: str
    :param domain: Message domain (``"automata"`` or ``"errors"``).
    :type domain: str
    :param lang: Reserved for future use. Has no effect until ``i18n-tools`` is integrated.
    :type lang: str
    :param kwargs: Named parameters to inject into the message template.
    :return: Formatted message.
    :rtype: str
    """
    msg_id = generate_code(grammar, component, action)
    raw_msg = seek_message(msg_id, domain, lang)
    return format_message(raw_msg, **kwargs)

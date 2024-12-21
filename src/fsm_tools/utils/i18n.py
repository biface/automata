import locale
import os
import gettext

from fsm_tools.utils.common import generate_code


def seek_message(msg_id:str, domain:str, lang:str = None) -> str:
    """

    """
    if lang is None:
        lang = str(locale.getdefaultlocale()[0])

    locale_dir = os.path.join(os.path.dirname(__file__), "locales")
    error_translation = gettext.translation(domain, localedir=locale_dir, languages=[lang], fallback=True)

    return error_translation.gettext(msg_id)


def generate_message(grammar:str, component: str, action:str, lang:str = None) -> str:
    """

    """
    return seek_message(generate_code(grammar, component, action), "errors", lang)


def get_message(msg_id:str, lang:str = None) -> str:
    """

    """
    return seek_message(str(msg_id), "errors", lang)

"""
This module provides exception classes for Finite State Machines and Automata.
"""

from typing import List
from .constants import CHOMSKY_GRAMMARS, COMPONENTS, ACTIONS
from .utils.json import generate_message, get_message


class AutomatonGroup:
    """
    This class implements the automaton group for automata. This will be used with pythion versions upper 3.11.

    """

    def __init__(self):
        self.exceptions: List[Exception] = []

    def add_exception(self, exception: Exception) -> None:
        self.exceptions.append(exception)


class AutomatonException(Exception):
    """
        Generic exception for errors in formal automata.
        Computes a unique error code based on the Chomsky grammar hierarchy level,
        the component, and the action.

        Localized error codes are fetched from `errors.mo`.
        General exception messages are fetched from `exception_msg.mo`.
    """

    def __init__(self, grammar: str, component: str, action: str, locale: str = None, **event) -> None:
        """
        This class implements the exception basis for formal grammar automata.

        :param grammar: name of the formal grammar hierarchy level.
        :type grammar: str
        :param component: name of a formal grammar's component .
        :type component: str
        :param action: name of an action on a formal grammar's component.
        :type action: str
        :param locale: name of the locale if not the environment locale will be used.
        :type locale: str
        :return: None
        :rtype: None
        :raises: ValueError.
        """

        if not grammar in CHOMSKY_GRAMMARS.keys():
            raise ValueError("Unknown grammar hierarchy name.")
        else:
            self.grammar = grammar

        if not component in COMPONENTS.keys():
            raise ValueError("Unknown component name.")
        else:
            self.component = component

        if not action in ACTIONS.keys():
            raise ValueError("Unknown action name.")
        else:
            self.action = action

        self.value = 1000 * CHOMSKY_GRAMMARS[self.grammar] + 100 * COMPONENTS[self.component] + ACTIONS[self.action]
        self.locale = locale
        self.domains = ["automata"]
        self.message = generate_message(self.grammar, self.component, self.action, self.domains[0], self.locale)
        self.group = AutomatonGroup()
        super().__init__(self.message)
        self.group.add_exception(self)

    def set_locale(self, new_locale: str) -> None:
        self.locale = new_locale
        self.message = self.generate_message(self.locale)

    def generate_message(self, locale: str) -> str:
        """

        """
        return generate_message(self.grammar, self.component, self.action, self.domains[0], locale)

    def __str__(self):
        return self.message


# Specialized exceptions

class AutomatonError(AutomatonException):
    event = {}
    def __init__(self, grammar: str, component: str, action: str, locale: str = None, **event) -> None:
        super().__init__(grammar, component, action, locale)
        self.domains.append("errors")
        if event:
            self.event['format'] = event
        self.message = self.generate_message(self.locale)

    def generate_message(self, locale: str) -> str:
        automaton_msg = super().generate_message(locale)
        if len(self.event) > 0:
            try:
                error_msg = generate_message(self.grammar, self.component, self.action, self.domains[1], self.locale,
                                             **self.event['format'])
                for exc in self.group.exceptions:
                    if type(exc) is self.event['cls']:
                        self.group.exceptions.remove(exc)
                self.group.add_exception(self.event['cls'](error_msg))
                automaton_msg += "\n" + error_msg
            except KeyError as e:
                raise e
        return automaton_msg


class ReadError(AutomatonError):
    """Error raised for reading actions (01, AttributeError)."""

    def __init__(self, grammar_level, component, locale=None, **event):
        if event:
            self.event['cls'] = AttributeError
        super().__init__(grammar_level, component, 'read', locale, **event)



class AddError(AutomatonError):
    """Error raised for addition actions (02, ValueError)."""

    def __init__(self, grammar_level, component, locale=None, **event):
        if event:
            self.event['cls'] = ValueError
        super().__init__(grammar_level, component, 'add', locale, **event)


class RemoveError(AutomatonError):
    """Error raised for removal actions (03, KeyError)."""

    def __init__(self, grammar_level, component, locale=None, **event):
        if event:
            self.event['cls'] = KeyError
        super().__init__(grammar_level, component, 'remove', locale, **event)


class ModifyError(AutomatonError):
    """Error raised for modification actions (04, ValueError)."""

    def __init__(self, grammar_level, component, locale=None, **event):
        if event:
            self.event['cls'] = ValueError
        super().__init__(grammar_level, component, 'modify', locale, **event)


class ValidationError(AutomatonError):
    """Error raised for validation actions (05, AssertionError)."""

    def __init__(self, grammar_level, component, locale=None, **event):
        if event:
            self.event['cls'] = AssertionError
        super().__init__(grammar_level, component, 'validate', locale, **event)


class SearchError(AutomatonError):
    """Error raised for search actions (06, KeyError)."""

    def __init__(self, grammar_level, component, locale=None, **event):
        if event:
            self.event['cls'] = KeyError
        super().__init__(grammar_level, component, 'search', locale, **event)


class RemoveComponentError(AutomatonError):
    """Error raised for component withdrawal actions (19, RuntimeError)."""

    def __init__(self, grammar_level, component, locale=None, **event):
        if event:
            self.event['cls'] = RuntimeError
        super().__init__(grammar_level, component, 'withdraw', locale, **event)
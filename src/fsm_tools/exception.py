"""
This module provides exception classes for Finite State Machines and Automata.
"""

from .constants import CHOMSKY_GRAMMARS, COMPONENTS, ACTIONS
from .utils.i18n import generate_message, get_message


class StateMachineException(Exception):
    """
    This basic class implements generic exception for finite-state machines or automata. All classes will derive from it.

    :param message: human-readable description of the exception.
    :type message: str
    :param code: internal code of the exception for future uses.
    :type code: int
    """

    def __init__(self, message: str = None, code: int = None) -> None:
        """
        This function instantiates the fundamental elements for exception handling in finite-state machines and automata.

        Parameters

        :param message: Message to show in the exception.
        :type message: str
        :param code: Error code.
        :type code: int
        :raises: None

        :return: None.
        :rtype: None
        """
        super().__init__(message)
        self.code = code


class StateMachineTypeError(TypeError):
    """
    This basic class implements specific type error types for finite-state machines and automata.

    :param message: human-readable description of the exception.
    :type message: str
    :param code: internal code of the exception for future uses. Type Error code will be between 1001 an 1999
    :type code: int
    """

    def __init__(self, message: str = None, code: int = 0) -> None:
        """
        This class implements the exception basis for finite-state machines and automata.

        :param message: human-readable description of the exception.
        :type message: str
        :param code: Error code. This error code must be between 1 an 999 otherwise a ValueError exception is raised.
        :type code: int
        :raises: ValueError

        :return: None.
        :rtype: None
        """
        super().__init__(message)
        if code / 1000 > 1:
            raise ValueError("State machine type error: Code must be between 1 and 999.")
        else:
            self.code = 1000 + code


class StateMachineValueError(ValueError):
    """
    This basic class implements specific value error types for finite-state machines and automata.

    :param message: human-readable description of the exception.
    :type message: str
    :param code: internal code of the exception for future uses. Type Error code will be between 1001 an 1999
    :type code: int
    """

    def __init__(self, message: str = None, code: int = 0) -> None:
        """
        This class implements the exception basis for finite-state machines and automata.

        :param message: human-readable description of the exception.
        :type message: str
        :param code: Error code. This error code must be between 1 an 999 otherwise a ValueError exception is raised.
        :type code: int
        :raises: ValueError

        :return: None.
        :rtype: None
        """
        super().__init__(message)
        if code / 1000 > 1:
            raise ValueError("State machine value error: Code must be between 1 and 999.")
        else:
            self.code = 2000 + code


class InvalidStateTransitionError(StateMachineValueError):
    """
    This exception is raised if the requested transition event already exists.
    """

    def __init__(self, message: str = None, code: int = 0) -> None:
        """
        This class implements the transition exception basis for finite-state machines and automata.

        :param message: handle event that cause the exception to be raised.
        :type message: str
        :param code: internal code of the exception for future uses.
        :type code: int
        :return: None.
        :rtype: None
        """
        msg = "The requested transition event already exists. The event " + message + " is already registered."
        super().__init__(msg, code)


class InvalidStateTriggerError(StateMachineValueError):
    """
    This exception is raised if the requested trigger event is not registered.
    """

    def __init__(self, message: str = None, code: int = 0) -> None:
        """
        This class implements the trigger exception basis for finite-state machines and automata.

        :param message: handle event that cause the exception to be raised.
        :type message: str
        :param code: internal code of the exception for future uses.
        :type code: int
        :return: None.
        :rtype: None
        """
        msg = "The requested trigger event is not registered. The event " + message + " is not registered in transitions dictionary."
        super().__init__(msg, code)


class AutomatonException(Exception):
    """
        Generic exception for errors in formal automata.
        Computes a unique error code based on the Chomsky grammar hierarchy level,
        the component, and the action.

        Localized error codes are fetched from `errors.mo`.
        General exception messages are fetched from `exception_msg.mo`.
    """

    def __init__(self, grammar: str, component: str, action: str, locale: str = None) -> None:
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
        self.message = get_message(str(self.value), self.locale)
        super().__init__(self.message)

    def set_locale(self, new_locale: str) -> None:
        self.locale = new_locale
        self.message = self.generate_message(self.locale)

    def generate_message(self, locale:str) -> str:
        """

        """
        return generate_message(self.grammar, self.component, self.action, locale)

    def __str__(self):
        return self.message

# Specialized exceptions
class ReadException(AutomatonException, AttributeError):
    """Error raised for reading actions (01, AttributeError)."""
    def __init__(self, grammar_level, component, locale=None):
        super().__init__(grammar_level, component, 'read', locale)


class AddError(AutomatonException, ValueError):
    """Error raised for addition actions (02, ValueError)."""
    def __init__(self, grammar_level, component, locale=None):
        super().__init__(grammar_level, component, 'add', locale)


class RemoveError(AutomatonException, KeyError):
    """Error raised for removal actions (03, KeyError)."""
    def __init__(self, grammar_level, component, locale=None):
        super().__init__(grammar_level, component, 'remove', locale)


class ModifyError(AutomatonException, ValueError):
    """Error raised for modification actions (04, ValueError)."""
    def __init__(self, grammar_level, component, locale=None):
        super().__init__(grammar_level, component, 'modify', locale)


class ValidationError(AutomatonException, AssertionError):
    """Error raised for validation actions (05, AssertionError)."""
    def __init__(self, grammar_level, component, locale=None):
        super().__init__(grammar_level, component, 'validate', locale)


class SearchError(AutomatonException, KeyError):
    """Error raised for search actions (06, KeyError)."""
    def __init__(self, grammar_level, component, locale=None):
        super().__init__(grammar_level, component, 'search', locale)


class RemoveComponentError(AutomatonException, RuntimeError):
    """Error raised for component withdrawal actions (19, RuntimeError)."""
    def __init__(self, grammar_level, component, locale=None):
        super().__init__(grammar_level, component, 'withdraw', locale)
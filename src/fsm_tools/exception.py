"""
This module provides exception classes for Finite State Machines and Automata.
"""


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
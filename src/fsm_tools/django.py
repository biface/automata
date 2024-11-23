from typing import Any
from .lightweight import ExtFSM

class ContextFSM(ExtFSM):
    """
    This class implements a Finite State Machine to be used in Django contexts. It inherits from ExtFSM class.
    """
    def __init__(self, initial_state: Any):
        """
        This initializing method sets an instance ContextFSM and helps a Finite State Machine to be used in a Django
        contexts.

        :param initial_state: The initial state of the FSM.
        :type initial_state: Any
        :return: None
        :rtype: None
        """
        super().__init__(initial_state)


    def as_dict(self) -> dict:
        """
        This method returns a dictionary representation of the FSM.

        :return: A dictionary representation of the FSM.
        :rtype: dict
        """
        return dict([('current', self.current), ('previous', self.previous), ('transitions', self.transitions)])

    def add_to_context(self, context:dict, key:str) -> None:
        """
        This method adds the given key to the given context from a defined Django's view function.

        :param context: The context dictionary to add the key to.
        :type context: dict
        :param key: The key to fill. The content will be wiped out.
        :type key: str
        :return: None
        :rtype: None
        """
        context[key] = self.as_dict()
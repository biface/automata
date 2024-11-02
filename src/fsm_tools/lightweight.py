class FSM:
    """
    Finite State Machine light (FSM) class

    Description
    ===========

    This class is a lightweight implementation of the finite state machine. It simply uses a dictionary to store state
    transitions, and the current state is stored in a variable.

    The data model associated with this class resides mainly in the transition dictionary. Each machine state has a
    dictionary whose key is the state. Each of these dictionaries is described by the event that constitutes the
    dictionary key, and the value is the state after the transition.

    Example
    =======


    """

    def __init__(self, initial_states):
        """
        This function initializes the FSM class. It requires to define the initial states as a string. it also
        initializes the ``transitions`` dictionary.

        :param initial_states: initial states
        :return: None
        """

        self.initial = initial_states
        self.current = initial_states
        self.transitions = {}

    def add_transition(self, from_state, to_state, event):
        """
        This function adds a state transition to the finite-state automaton. The transition consists in adding the
        transition event to the transition dictionary for a given state. If the original state does not exist, it is
        created in the transition dictionary.

        :param from_state: initial state
        :param to_state: final state
        :param event: transition event
        """
        if from_state not in self.transitions:
            self.transitions[from_state] = {}
        self.transitions[from_state][event] = to_state

    def get_state(self):
        """
        This function returns the current state of the FSM.

        :return: the current state of the FSM.
        """
        return self.current

    def reset(self):
        """
        This function resets the FSM to its initial state.
        """
        self.current = self.initial

    def trigger(self, event):
        """
        This function triggers the event on the FSM. It sets the current state of the FSM to the state
        defined by the event.

        :param event: the event to trigger
        """
        if event in self.transitions.get(self.current, {}):
            self.current = self.transitions[self.current][event]


class ExtFSM(FSM):
    """
    This class extends simple FSM with memory of previous state
    """

    def __init__(self, initial_states):
        """
        This function initializes the ExtFSM class.

        :param initial_states: initial states
        :return: None
        """
        super().__init__(initial_states)
        self.previous = None

    def reset(self):
        """
        This function reset to initial state ExtFSM instance.
        """
        super().reset()
        self.previous = None

    def get_previous(self):
        """
        This function returns the previous state of the ExtFSM.

        :return: the previous state of the ExtFSM.
        """
        return self.previous

    def trigger(self, event):
        """
        This function triggers the event on the ExtFSM.
        :param event: the event to trigger
        """
        self.previous = self.get_state()
        super().trigger(event)
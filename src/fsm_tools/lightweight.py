class FSMlight:
    """
    The FSMlight class implements a lightweight Finite State Machine.

    Description
    ===========


    """

    def __init__(self, initial_states):
        self.initial = initial_states
        self.current = initial_states
        self.transitions = {}

    def add_transition(self, from_state, to_state, event):
        if from_state not in self.transitions:
            self.transitions[from_state] = {}
        self.transitions[from_state][event] = to_state

    def get_state(self):
        return self.current

    def reset(self):
        self.current = self.initial

    def trigger(self, event):
        if event in self.transitions.get(self.current, {}):
            self.current = self.transitions[self.current][event]


class ExtFSM(FSMlight):
    """
    This class extends simple FSM with memory of previous state
    """

    def __init__(self, initial_states):
        super().__init__(initial_states)
        self.previous = None

    def reset(self):
        super().reset()
        self.previous = None

    def get_previous(self):
        return self.previous

    def trigger(self, event):
        if event in self.transitions.get(self.current, {}):
            self.previous = self.current
            self.current = self.transitions[self.current][event]
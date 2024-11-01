from .lightweight import ExtFSM

class ContextFSM(ExtFSM):
    """
    This class implements a Finite State Machine to be used in Django contexts.
    """
    def __init__(self, initial_state):
        super().__init__(initial_state)


    def as_dict(self):
        return dict([('current', self.current), ('previous', self.previous), ('transitions', self.transitions)])
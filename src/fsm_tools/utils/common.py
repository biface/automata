from fsm_tools.constants import CHOMSKY_GRAMMARS, COMPONENTS, ACTIONS

def generate_code(grammar:str, component: str, action:str) -> str:
    """
    This function generates a code for a given grammar, component and action.

    :param grammar: grammar key
    :type grammar: str
    :param component: component key
    :type component: str
    :param action: action key
    :type action: str
    :return: str
    :raise ValueError: If keys are not defined in grammar, component, action dictionaries
    """
    if not grammar in CHOMSKY_GRAMMARS.keys():
        raise KeyError("Unknown grammar name")
    if not component in COMPONENTS.keys():
        raise KeyError("Unknown component name")
    if not action in ACTIONS.keys():
        raise KeyError("Unknown action name")

    return str(1000*CHOMSKY_GRAMMARS[grammar] + 100*COMPONENTS[component] + ACTIONS[action])

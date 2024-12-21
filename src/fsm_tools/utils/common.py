from fsm_tools.constants import CHOMSKY_GRAMMARS, COMPONENTS, ACTIONS

def generate_code(grammar:str, component: str, action:str) -> str:
    """

    """
    if not grammar in CHOMSKY_GRAMMARS.keys():
        raise KeyError("Unknown grammar name")
    if not component in COMPONENTS.keys():
        raise KeyError("Unknown component name")
    if not action in ACTIONS.keys():
        raise KeyError("Unknown action name")

    return str(1000*CHOMSKY_GRAMMARS[grammar] + 100*COMPONENTS[component] + ACTIONS[action])

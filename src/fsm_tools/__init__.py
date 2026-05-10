import os
from pathlib import Path

from .advanced import (
    Grammar as Grammar,
    Automaton as Automaton,
    TuringMachine as TuringMachine,
    LinearBoundedAutomaton as LinearBoundedAutomaton,
)
from .extended import (
    ExtendedTuringMachine as ExtendedTuringMachine,
    ExtendedLBA as ExtendedLBA,
)
from .exception import (
    AutomatonException as AutomatonException,
    AutomatonError as AutomatonError,
    AutomatonGroup as AutomatonGroup,
    ReadError as ReadError,
    AddError as AddError,
    RemoveError as RemoveError,
    ModifyError as ModifyError,
    ValidationError as ValidationError,
    SearchError as SearchError,
    RemoveComponentError as RemoveComponentError,
)

base_path = Path(os.path.abspath(__file__))
__VERSION__ = "0.0.3"

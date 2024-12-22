import os
from pathlib import Path

from .exception import InvalidStateTransitionError, InvalidStateTriggerError
from .lightweight import FSM, ExtFSM
from .django import ContextFSM

base_path = Path(os.path.abspath(__file__))
__VERSION__ = '0.0.1-3'

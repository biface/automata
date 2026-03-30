import os
from pathlib import Path

from .django import ContextFSM
from .exception import AddError, ReadError, RemoveError
from .lightweight import FSM, ExtFSM

base_path = Path(os.path.abspath(__file__))
__VERSION__ = "0.0.1-3"

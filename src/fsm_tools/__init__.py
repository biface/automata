import os
from pathlib import Path


from .exception import AddError, ReadError, RemoveError

base_path = Path(os.path.abspath(__file__))
__VERSION__ = "0.0.1-3"

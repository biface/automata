import os
from pathlib import Path


from .exception import (AddError as AddError,
                        ReadError as ReadError,
                        RemoveError as RemoveError)

base_path = Path(os.path.abspath(__file__))
__VERSION__ = "0.0.1-3"

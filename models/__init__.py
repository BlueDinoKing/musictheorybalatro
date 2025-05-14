from .note import Pitch, Interval
from .key import Key
# from .hand import Hand
# from .deck import Deck
# from .player import Player
# from .round import Round
# from .game import Game
# from .modifier import Modifier
import os
__all__ = ["Pitch", "Interval", "Key"]

directory = os.path.dirname(__file__)

# Create each file
for name in __all__:
    filename = f"{name.lower()}.py"
    filepath = os.path.join(directory, filename)
    if not os.path.exists(filepath):
        with open(filepath, "w") as file:
            # Optionally, add a docstring or placeholder content
            file.write(f'"""{name} module."""\n')
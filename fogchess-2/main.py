from __future__ import annotations
from typing import Callable, Optional, List, Any, Dict


def main() -> int:
    print("Hello World!")
    piece: Piece = Pawn()
    piece.render()
    return 0

def evaluate(piece: Piece):
    pass

class Piece:
    def __init__(self):
        pass
    @classmethod
    def render(cls):
        print(f"Hello World! by {cls}")
        pass

class Pawn(Piece):
    pass

class King(Piece):
    pass

if __name__ == "__main__":
    main()

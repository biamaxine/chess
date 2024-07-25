from .....Shared import Shared

pieces = {
  'king': ('♔', '♚'),
  'queen': ('♕', '♛'),
  'rook': ('♖', '♜'),
  'bishop': ('♗', '♝'),
  'knight': ('♘', '♞'),
  'pawn': ('♙', '♟'),
}

class Piece(Shared):
  def __init__(self, name: str, color: str, position: tuple[int, int]) -> None:
    super().__init__()
    self.__color = color
    if (name in list(pieces.keys())):
      self.__name = name
      self.__ico = pieces[name][1] if color == 'white' else pieces[name][0]
    else:
      raise ValueError('This name does not correspond to that of a chess piece.')

  # Access Methods
  def get_position(self) -> tuple[int, int]:
    return self.__position

  def set_position(self, position: tuple[int, int]) -> None:
    self.__position = position

  def get_color(self) -> str:
    return self.__color

  def get_name(self) -> str:
    return self.__name

  def get_ico(self) -> str:
    return self.__ico

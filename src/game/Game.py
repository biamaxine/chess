from ..Shared import Shared
from .board.Board import Board

class Game(Shared):
  def __init__(self) -> None:
    super().__init__()
    self.__board = Board()

  def start(self) -> None:
    print('GAME START!\n')

    self.__board.display()

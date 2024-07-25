from typing import Optional

from ....Shared import Shared
from .piece.Piece import Piece

class Square(Shared):
  def __init__(
    self,
    position: tuple[int, int],
    content: Optional[Piece] = None,
  ) -> None:
    super().__init__()
    self.__content = content
    self.__position = position

  # Access Methods
  def get_content(self) -> Optional[Piece]:
    return self.__content

  def set_content(self, content: Optional[Piece] = None) -> None:
    self.__content = content
    if (content):
      content.set_position(self.__position)

  def get_position(self) -> tuple[int, int]:
    return self.__position

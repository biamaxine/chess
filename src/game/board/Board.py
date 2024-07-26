from ...Shared import Shared
from .square.Square import Square
from .square.piece.Piece import Piece

class Board(Shared):
  def __init__(self) -> None:
    super().__init__()
    self.__this = [[Square((x, y)) for x in range(8)] for y in range(8)]
    pieces = ['rook', 'knight', 'bishop', 'king', 'queen', 'bishop', 'knight', 'rook']
    for i, piece in enumerate(pieces):
      self.get_position((i, 0)).set_content(Piece(piece, 'white', (i, 0)))
      self.get_position((i, 1)).set_content(Piece('pawn', 'white', (i, 1)))
      self.get_position((i, 6)).set_content(Piece('pawn', 'black', (i, 6)))
      self.get_position((i, 7)).set_content(Piece(piece, 'black', (i, 7)))

  # Action Methods
  def display(self) -> None:
    headers = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
    table = self.create_table(headers=headers, show_header=False, show_lines=True)

    for y in range(8):
      row = []
      for x in range(8):
        piece = self.get_position((x, 7-y)).get_content()
        if piece:
          ico = piece.get_ico()
          color = 'bold red' if piece.get_color() == 'black' else 'bold yellow'
          row.append(self.color(ico, color))
        else:
          row.append(' ')
      table.add_row(f'{y + 1}', *row)

    table.add_row('', *headers)

    self.log(table)

  # Access Methods
  def get_position(self, position: tuple[int, int]) -> Square:
    (x, y) = position
    return self.__this[y][x]

  def get_matrix(self) -> list[list[tuple[str, str, bool]]]:
    matrix = [[('', '') for _ in range(8)] for _ in range(8)]
    for y in range(8):
      for x in range(8):
        piece = self.get_position((x, y)).get_content()
        if (piece):
          matrix[y][x] = (piece.get_color(), piece.get_name(), piece.was_moved())

    return matrix

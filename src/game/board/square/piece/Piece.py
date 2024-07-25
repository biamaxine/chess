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

  # Action Methods
  def check_moves(
    self,
    name: str,
    board: list[list[tuple[str, str]]],
    last: tuple[int, int],
  ) -> tuple[str, str, str]:
    if (name == 'pawn'):
      return self.__check_pawn_moves(board, last)
    return []

  def __check_pawn_moves(
    self,
    board: list[list[tuple[str, str]]],
    last: tuple[int, int],
  ) -> list[tuple[str, str, str]]:
    moves = []
    color = self.__color
    enemy = 'black' if color == 'white' else 'white'
    id = 1 if color == 'white' else -1

    # normal
    y = self.__y() + 1 * id
    if (board[y][self.__x()][0] == ''):
      normal = True
      moves.append((
        self.position_to_coordinate((self.__x(), y)),
        'normal', '',
      ))

      # doble
      is_white = self.__y() == 1 and color == 'white'
      is_black = self.__y() == 6 and color == 'black'
      if (is_white or is_black):

        doble = board[y + 1 * id][self.__x()][0]
        if (doble == ''):
          moves.append((
            self.position_to_coordinate((self.__x(), y + 1 * id)),
            'doble', '',
          ))

    # atack
    for id in [-1, 1]:
      x = self.__x() + id

      if (board[y][x][0] == enemy):
        moves.append((
          self.position_to_coordinate((x, y)),
          'atack', board[y][x][1],
        ))

      # en passant
      else:
        check_white = color == 'white' and self.__y() == 4
        check_black = color == 'black' and self.__y() == 3

        if (check_white or check_black):
          if (board[y][x][0] == ''):
            is_enemy = board[self.__y()][x][0] == enemy
            is_pawn = board[self.__y()][x][1] == 'pawn'
            is_last = (x, self.__y()) == last

            if (is_enemy and is_pawn and is_last):
              moves.append((
                self.position_to_coordinate((x, y)),
                'en passant',
                self.position_to_coordinate((x, self.__y())),
              ))

    return moves

  # Access Methods
  def __x(self) -> int:
    return self.get_position()[0]

  def __y(self) -> int:
    return self.get_position()[1]

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

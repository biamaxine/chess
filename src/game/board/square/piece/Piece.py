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
    self.__position = position
    self.__was_moved = False
    if (name in list(pieces.keys())):
      self.__name = name
      self.__ico = pieces[name][1] if color == 'white' else pieces[name][0]
    else:
      raise ValueError('This name does not correspond to that of a chess piece.')

  # Action Methods
  def check_moves(
    self,
    name: str,
    board: list[list[tuple[str, str, bool]]],
    last: tuple[int, int],
  ) -> tuple[str, str, str]:
    print(name)

    if (name == 'king'):
      return self.__check_king_moves(board)
    if (name == 'queen'):
      return self.__check_queen_moves(board)
    if (name == 'bishop'):
      return self.__check_bishop_moves(board)
    if (name == 'knight'):
      return self.__check_knight_moves(board)
    if (name == 'rook'):
      return self.__check_rook_moves(board)
    if (name == 'pawn'):
      return self.__check_pawn_moves(board, last)
    return []

  def __check_king_moves(
    self,
    board: list[list[tuple[str, str, bool]]],
  ) -> list[tuple[str, str, str]]:
    moves = []

    enemy = 'black' if self.__color == 'white' else 'white'

    for id_x in [1, 0, -1]:
      for id_y in [1, 0, -1]:
        if (id_x == 0 and id_y == 0):
          continue
        x = self.__x() + id_x
        y = self.__y() + id_y
        if (0 <= x < 8 and 0 <= y < 8):

          position = board[y][x]
          if (position[0] == ''):
            moves.append((
              self.position_to_coordinate((x, y)),
              'normal', ''
            ))

          elif (position[0] == enemy):
            moves.append((
              self.position_to_coordinate((x, y)),
              'attack', position[1]
            ))

    # Castling
    if not (self.__was_moved):
      y = self.__y()
      line = board[y]

      # King-side Castling
      if not (line[7][2]): # Rook on king's side has not moved
        if (line[5][0] and line[6][0]):
          moves.append((
            self.position_to_coordinate((6, y)),
            'castle', '',
          ))

      # Queen-side Castling
      if not (line[0][2]): # Rook on queen's side has not moved
        if (line[1][0] and line[2][0] and line[3][0]):
          moves.append((
            self.position_to_coordinate((2, y)),
            'castle', '',
          ))

    return moves

  def __check_queen_moves(
    self,
    board: list[list[tuple[str, str, bool]]],
  ) -> list[tuple[str, str, str]]:
    moves = []
    moves += self.__check_bishop_moves(board)
    moves += self.__check_rook_moves(board)
    return moves

  def __check_bishop_moves(
    self,
    board: list[list[tuple[str, str, bool]]],
  ) -> list[tuple[str, str, str]]:
    moves = []

    color = self.get_color()
    enemy = 'black' if color == 'white' else 'white'

    for id_x in [-1, 1]:
      for id_y in [-1, 1]:
        x = self.__x()
        y = self.__y()
        is_empty = True

        while(0 <= x < 8 and 0 <= y < 8 and is_empty):
          x += 1 * id_x
          y += 1 * id_y

          try:
            self.validate_position((x, y))
          except:
            break

          position = board[y][x]
          if (position[0] == ''):
            moves.append((
              self.position_to_coordinate((x, y)),
              'normal', ''
            ))

          elif (position[0] == enemy):
            moves.append((
              self.position_to_coordinate((x, y)),
              'attack', position[1],
            ))
            is_empty = False

          else: is_empty = False

    return moves

  def __check_knight_moves(
    self,
    board: list[list[tuple[str, str, bool]]],
  ) -> list[tuple[str, str, str]]:
    moves = []

    enemy = 'black' if self.__color == 'white' else 'white'

    for id_x in [-2, -1, 1, 2]:
      for id_y in [-2, -1, 1, 2]:
        if (id_x == id_y):
          continue

        x = self.__x() + id_x
        y = self.__y() + id_y
        if (0 <= x < 8 and 0 <= y < 8):

          position = board[y][x]
          if not (position[0]):
            moves.append((
              self.position_to_coordinate((x, y)),
              'normal', '',
            ))

          elif (position[0] == enemy):
            moves.append((
              self.position_to_coordinate((x, y)),
              'attack', '',
            ))

    return moves

  def __check_rook_moves(
    self,
    board: list[list[tuple[str, str, bool]]],
  ) -> list[tuple[str, str, str]]:
    moves = []

    color = self.get_color()
    enemy = 'black' if color == 'white' else 'white'

    for id in [-1, 1]:
      x = self.__x()
      is_empty = True
      while (0 <= x < 8 and is_empty):
        x += 1 * id

        try:
          self.validate_position((x, self.__y()))
        except:
          break

        position = board[self.__y()][x]
        if (position[0] == ''):
          moves.append((
            self.position_to_coordinate((x, self.__y())),
            'normal', ''
          ))

        elif (position[0] == enemy):
          moves.append((
            self.position_to_coordinate((x, self.__y())),
            'attack', position[1]
          ))
          is_empty = False

        else: is_empty = False

    for id in [-1, 1]:
      y = self.__y()
      is_empty = True
      while (0 <= y < 8 and is_empty):
        y += 1 * id

        try:
          self.validate_position((self.__x(), y))
        except:
          break

        position = board[y][self.__x()]
        if (position[0] == ''):
          moves.append((
            self.position_to_coordinate((self.__x(), y)),
            'normal', ''
          ))

        elif (position[0] == enemy):
          moves.append((
            self.position_to_coordinate((self.__x(), y)),
            'attack', ''
          ))
          is_empty = False

        else: is_empty = False

    return moves

  def __check_pawn_moves(
    self,
    board: list[list[tuple[str, str, bool]]],
    last: tuple[int, int],
  ) -> list[tuple[str, str, str]]:
    moves = []
    color = self.__color
    enemy = 'black' if color == 'white' else 'white'
    id = 1 if color == 'white' else -1

    # normal
    y = self.__y() + 1 * id
    if (board[y][self.__x()][0] == ''):
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

    # attack
    for id in [-1, 1]:
      x = self.__x() + id

      if (0 <= x < 8):
        if (board[y][x][0] == enemy):
          moves.append((
            self.position_to_coordinate((x, y)),
            'attack', board[y][x][1],
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
    self.__was_moved = True

  def was_moved(self) -> bool:
    return self.__was_moved

  def get_color(self) -> str:
    return self.__color

  def get_name(self) -> str:
    return self.__name

  def get_ico(self) -> str:
    return self.__ico

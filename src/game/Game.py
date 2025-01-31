from ..Shared import Shared
from .board.Board import Board
from .board.square.piece.Piece import Piece

class Game(Shared):
  def __init__(self) -> None:
    super().__init__()
    self.__board = Board()
    # Resetable Variables
    self.__is_started: bool = False
    self.__turn: str = 'white'
    self.__moves: list[tuple[int, int]] = [(-1, -1)]

  def start(self) -> None:
    self.__reset()

    self.log(self.color('GAME START!\n', 'bold green'))

    while (self.__is_started):
      self.log(self.background(
        f'\nIts the turn of the {self.__turn.upper()} pieces\n',
        'blue',
      ), style='bold')
      (position_i, piece, moves) = self.__select_piece()
      (position_f, movement_name, dead_enemy) = self.__select_movement(moves)
      self.__move(piece, position_i, position_f, movement_name, dead_enemy)
      self.__turn = 'black' if self.__turn == 'white' else 'white'

  def __select_piece(
    self,
    reload: bool = False,
  ) -> tuple[tuple[int, int], Piece, list[tuple[str, str, str]]]:
    # If the player chooses a wrong piece.
    if not (reload):
      self.__board.display()

    # Receives a position and checks if it is valid.
    key = True
    while(key):
      self.log(self.color('\nWhich piece do you want move?', 'bold yellow'))
      try:
        coordinate = input(': ')
        position_i = self.coordinate_to_position(coordinate)
        key = False
      except ValueError as e:
        self.log(self.color(f'<<< {e} >>>', 'bold red'))

    # Get the contents in position and check if it is a piece.
    piece = self.__board.get_position(position_i).get_content()

    # If it is not a piece.
    if not (piece):
      self.log(self.color(
        f'\n<<< Oops! The coordinate "{coordinate.upper()}" is empty >>>\n',
        'bold red',
      ))
      return self.__select_piece(reload=True)

    # If it is an enemy piece.
    if not (piece.get_color() == self.__turn):
      self.log(self.color(
        '\n<<< Oops! This piece is not yours. >>>\n',
        'bold red',
      ))
      return self.__select_piece(reload=True)

    # Get the possible moves for this piece.
    moves = piece.check_moves(
      piece.get_name(),
      self.__board.get_matrix(),
      self.__moves[-1],
    )

    # If it is a valid piece but cannot move.
    if (len(moves) == 0):
      self.log(self.color(
        '\n<<< This piece cannot currently move. >>>\n',
        'bold red',
      ))
      return self.__select_piece(reload=True)

    return (position_i, piece, moves)

  def __select_movement(
    self,
    moves: list[tuple[str, str, str]],
    options: list[str] = None,
  ) -> tuple[tuple[int, int], str, str]:
    if not (options):
      options = []
      for movement in moves:
        options.append(movement[0].upper())

    self.log(self.color(f'\nYour options: {options}\n', 'bold green'))

    key = True
    while (key):
      self.log(self.color(
        'Where do you want to move your piece?',
        'bold yellow',
      ))
      try:
        coordinate = input(': ').upper()
        position_f = self.coordinate_to_position(coordinate)
        if not (coordinate in options):
          self.log(self.color(
            '<<< This piece does not reach that position. >>>',
            'bold red',
          ))
          return self.__select_movement(moves, options)
        key = False
      except ValueError as e:
        self.log(self.color(f'<<< {e} >>>', 'bold red'))

    (_, movement_name, dead_enemy) = moves[options.index(coordinate)]

    return (position_f, movement_name, dead_enemy)

  def __move(
    self,
    piece: str,
    position_i: tuple[int, int],
    position_f: tuple[int, int],
    movement_name: str,
    dead_enemy: str,
  ):
    content_f = self.__board.get_position(position_f).get_content()
    self.__board.get_position(position_f).set_content(piece)
    self.__board.get_position(position_i).set_content()
    self.__moves.append(position_f)

    if (movement_name == 'attack'):
      self.log(self.color('\nAttack:', 'bold blue'))
      self.log(self.color(
        f'{piece.get_name()} kill {dead_enemy}\n'.upper(),
        'bold red',
      ))

    if (movement_name == 'en passant'):
      enemy_position = self.coordinate_to_position(dead_enemy)
      self.__board.get_position(enemy_position).set_content()

      self.log(self.color('\nEn Passant:', 'bold blue'))
      self.log(self.color(
        f'pawn kill pawn\n'.upper(),
        'bold red',
      ))

    if (movement_name == 'castle'):
      if (content_f):
        self.__board.get_position(position_i).set_content(content_f)

        self.log(self.color('\nCastle:', 'bold blue'))
        self.log(self.color(
          f'king swap rook\n'.upper(),
          'bold blue',
        ))

  # Access Methods
  def __reset(self) -> None:
    self.__is_started = True
    self.__turn = 'white'
    self.__moves = [(-1, -1)]

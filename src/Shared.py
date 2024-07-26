# This class share the same methods with all classes
import re

from rich.console import Console
from rich.table import Table
from rich import box
class Shared:
  def __init__(self) -> None:
    self.log = Console().print

  # Convertion Methods
  def x_axis_to_letter(self, x: int) -> str:
    if (self.validate_x_axis(x)):
      return chr(ord('a') + x)

  def y_axis_to_number(self, y: int) -> str:
    if (self.validate_y_axis(y)):
      return str(y + 1)

  def position_to_coordinate(self, position: tuple[int, int]) -> str:
    (x, y) = position
    if (self.validate_position(position)):
      return self.x_axis_to_letter(x) + self.y_axis_to_number(y)

  def letter_to_x_axis(self, letter: str) -> int:
    if (self.validate_coordinate_letter(letter)):
      return ord(letter.lower()) - ord('a')

  def number_to_y_axis(self, number: str) -> int:
    if (self.validate_coordinate_number(number)):
      return int(number) - 1

  def coordinate_to_position(self, coordinate: str) -> tuple[int, int]:
    if (self.validate_coordinate(coordinate)):
      (letter, number) = coordinate[0], coordinate[1]
      return (self.letter_to_x_axis(letter), self.number_to_y_axis(number))

  # Validation Methods
  def validate_x_axis(self, axis: int) -> bool:
    if not ((0 <= axis) and (axis < 8)):
      raise ValueError("X axis value must be between 0 and 7.")
    return True

  def validate_y_axis(self, axis: int) -> bool:
    if not ((0 <= axis) and (axis < 8)):
        raise ValueError("Y axis value must be between 0 and 7.")
    return True

  def validate_position(self, position: tuple[int, int]) -> bool:
    (x, y) = position
    if not (self.validate_x_axis(x) and self.validate_y_axis(y)):
      raise ValueError("Position values must be between 0 and 7 for both x and y axes.")
    return True

  def validate_coordinate_letter(self, letter: str) -> bool:
    regex = '^([a-h]|[A-H])$'
    if not re.match(regex, letter):
      raise ValueError("Coordinate letter must be between 'a' and 'h' or 'A' and 'H'.")
    return True

  def validate_coordinate_number(self, number: str) -> bool:
    regex = '^[1-8]$'
    if not re.match(regex, number):
      raise ValueError("Coordinate number must be between '1' and '8'.")
    return True

  def validate_coordinate(self, coordinate: str) -> bool:
    regex = r'^([a-h]|[A-H])[1-8]$'
    if not re.match(regex, coordinate):
      raise ValueError("Coordinate must be in the format 'a1' to 'h8' or 'A1' to 'H8'.")
    return True

  # Console
  def color(self, text: str, color: str) -> str:
    return f'[{color}]{text}[/{color}]'

  def background(self, text: str, color: str) -> str:
    return f'[on {color}]{text}[/on {color}]'

  def create_table(
    self,
    headers: list[str] = None,
    show_header: bool = True,
    show_lines: bool = True,
  ) -> Table:
    if headers is None:
      headers = []
    table = Table(show_header=show_header, show_lines=show_lines, box=box.SQUARE)
    for header in headers:
      table.add_column(header, justify="center")
    return table

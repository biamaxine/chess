# INIT PROJECT: Chess
from src.game.Game import Game

class Main:
  def __init__(self) -> None:
    pass

  def run(self):
    game = Game()
    game.start()

if __name__ == '__main__':
  main_instance = Main()
  main_instance.run()

# INIT PROJECT: Chess
import argparse

class Main:
  def __init__(self) -> None:
    self.dev_mode = False

  def run(self):
    from src.game.Game import Game

    game = Game()
    game.start()

if (__name__ == '__main__'):
  parser = argparse.ArgumentParser(description="Run the chess game.")
  parser.add_argument('--dev', action='store_true', help='Run in development mode')
  args = parser.parse_args()

  main_instance = Main()
  main_instance.dev_mode = args.dev

  if main_instance.dev_mode:
    from dev import run_dev

    run_dev(main_instance.run)
  else:
    main_instance.run()

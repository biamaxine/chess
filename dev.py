import sys
import subprocess
import time

from typing import Callable

from rich.console import Console
from rich.traceback import install
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

def run_dev(run: Callable[..., None]):
  console = Console()
  install(show_locals=True)

  def color(color: str, text: str) -> str:
    return f'[bold {color}]{text}[/bold {color}]'

  console.print(color('green', 'Running in development mode\n'))

  class ChangeHandler(FileSystemEventHandler):
    def __init__(self, script_path):
      self.script_path = script_path

    def on_modified(self, event):
      if event.src_path.endswith('.py'):
        console.print(
          color('yellow', event.src_path) + ' has been modified.\nRestarting...',
          highlight=False,
        )
        subprocess.run([sys.executable, self.script_path, '--dev'])

  # Main Path
  script_path = sys.argv[0]
  event_handler = ChangeHandler(script_path)
  observer = Observer()
  observer.schedule(event_handler, path='.', recursive=True)
  observer.start()

  # Run Project in Develompent Mode
  run()

  try:
    while True:
      time.sleep(1)
  except KeyboardInterrupt:
    observer.stop()
    console.print(color('red', 'Stopping the watcher...'))

  observer.join()

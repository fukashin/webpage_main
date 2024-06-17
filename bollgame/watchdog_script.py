import os
import sys
import time
import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class ReloadHandler(FileSystemEventHandler):
    def __init__(self, process):
        self.process = process

    def on_modified(self, event):
        if event.src_path.endswith('.py'):
            print(f'File changed: {event.src_path}')
            self.process.terminate()
            self.process = subprocess.Popen([sys.executable, 'main.py'])

if __name__ == "__main__":
    process = subprocess.Popen([sys.executable, 'main.py'])
    event_handler = ReloadHandler(process)
    observer = Observer()
    observer.schedule(event_handler, path='.', recursive=True)
    observer.start()
    print("Watching for file changes...")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
    process.terminate()

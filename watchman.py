import time
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from fileProcessing import fileProcessing   # process the file, another python code

WATCH_FOLDER = r"C:\flask_upload\uploads"

class FileHandler(FileSystemEventHandler):
    def on_created(self, event):
        # ignore folder
        if event.is_directory:
            return

        filepath = os.path.normpath(event.src_path)

        print(f"New file detected: {filepath}")

        try:
            # wait until upload completely(!)
            time.sleep(1)  

            print(f"Running fileProcessing on {filepath}")
            fileProcessing(filepath)
            time.sleep(1)

        except Exception as e:
            print("Error while processing:", e)


def start_watcher():
    print("Starting folder watcher...")
    print("Watching:", WATCH_FOLDER)

    event_handler = FileHandler()
    observer = Observer()
    observer.schedule(event_handler, WATCH_FOLDER, recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()


if __name__ == "__main__":
    start_watcher()

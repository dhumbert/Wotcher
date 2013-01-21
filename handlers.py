from watchdog.events import FileSystemEventHandler

class WotcherEventHandler(FileSystemEventHandler):
	def __init__(self, modified_callback):
		self.modified_callback = modified_callback

	def on_modified(self, event):
		self.modified_callback(event.src_path)
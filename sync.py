import os.path
import paramiko

class SFTPSync:
	def __init__(self, host, username, password, port=22):
		self.host = host
		self.username = username
		self.password = password
		self.port = port
		self.dirs = []
		self.connection = None

	def add_dir(self, local, remote):
		local = os.path.abspath(local)
		self.dirs.append((local, remote))

	def modified(self, path):
		remote_paths = self.get_remote_paths(path)

		print "MODIFIED: {0}".format(path)

		for remote_path in remote_paths:
			print "    > Sync to {0}".format(remote_path),
			connection = self.connect()

			directory = os.path.dirname(remote_path)
			self.build_remote_tree(directory)

			connection.put(path, remote_path)
			print "Done!"

		print ""

	def build_remote_tree(self, path):
		parts = path.split('/')
		connection = self.connect()

		for n in range(2, len(parts) + 1):
			path = '/'.join(parts[:n])
			try:
				connection.stat(path)
			except IOError: # remote dir doesn't exist
				print "    > Creating directory {0}".format(path)
				connection.mkdir(path)

	def get_remote_paths(self, path):
		directory = os.path.dirname(path)

		remote_paths = []

		for dirToCheck in self.dirs:
			found = directory.find(dirToCheck[0])
			if found >= 0:
				mod_file = os.path.basename(path)
				mirror = self.path_for_nix(dirToCheck[1])

				# if directory isn't the same as dirToCheck, file is in a subdirectory
				if (directory != dirToCheck[0]):
					subdir = directory[(found + len(dirToCheck[0]) + 1):]
					subdir = self.path_for_nix('/' + os.path.normpath(subdir))
				else:
					subdir = ''

				remote_paths.append(mirror + subdir + '/' + mod_file)
		return remote_paths

	def path_for_nix(self, path):
		return path.replace('\\', '/');

	def connect(self):
		if self.connection is None:
			print "Connecting to {0}:{1}...".format(self.host, self.port)
			t = paramiko.Transport((self.host, self.port))
			t.connect(username=self.username, password=self.password)
			self.connection = paramiko.SFTPClient.from_transport(t)
			print "Connected!"
			print ""

		return self.connection

	def close(self):
		print "Closing connection..."
		self.connection.close()

import socket

class ChatServer():
	def __init__(self, port) -> None:
		self.port = port
		socketsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		socket.bind(('localhost', port))
		socket.listen(10)
		self.socket = socket

		self.clients = {}
	
print(ChatServer(56232))

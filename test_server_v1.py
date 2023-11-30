import unittest
from unittest.mock import patch, MagicMock
from server import get_time, get_hour_minute, broadcast, setup_server

from datetime import datetime

class TestServer(unittest.TestCase):
	def test_get_time(self):
		time_now = get_time()
		current_time = datetime.now()
		# Format the output
		formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
		
		self.assertIsInstance(time_now, str)
		self.assertRegex(time_now, r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}")
		self.assertEqual(time_now, formatted_time)

	def test_get_hour_minute(self):
		time_now = get_hour_minute()

		current_time = datetime.now()
		# Format the output
		formatted_time = current_time.strftime("%H:%M:%S")
		
		self.assertIsInstance(time_now, str)
		self.assertRegex(time_now, r"\d{2}:\d{2}:\d{2}")
		self.assertEqual(time_now, formatted_time)
	
	@patch('socket.socket')
	def test_setup_server(self, mock_socket):
		mock_socket.return_value.bind.return_value = None
		mock_socket.return_value.listen.return_value = None
		server_socket, clients = setup_server(54332)
		self.assertEqual(clients, {})
		#mock_socket.assert_called_once_with(socket.AF_INET, socket.SOCK_STREAM)
		mock_socket.return_value.bind.assert_called_once_with(('localhost', 54332))
		mock_socket.return_value.listen.assert_called_once_with(5)

	# @patch('server.clients', {"user1": MagicMock(), "user2": MagicMock()})
	# def test_broadcast(self):
	# 	message = "Hello, world!"
	# 	username = "user1"
	# 	sending_client = MagicMock()

	# 	broadcast(message, username, sending_client)

	# 	# Check that the message was sent to all clients except the sender
	# 	for client in server.clients.values():
	# 		if client != sending_client:
	# 			client.send.assert_called_once()

if __name__ == '__main__':
	unittest.main()

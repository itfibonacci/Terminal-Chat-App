import unittest
import socket
import threading
import time
from datetime import datetime
from unittest.mock import patch

PORT = 54332

# import functions from the server.py
from server import setup_server, handle_client, broadcast, get_time, get_hour_minute, cleanup, get_clients

class TestServerFunctionality(unittest.TestCase):
	def setUp(self) -> None:
		# Start a thread for the server
		server_thread = threading.Thread(target=setup_server)
		server_thread.start()
	
	def tearDown(self) -> None:
		cleanup()

	def test_client_connection(self):
		# Create a test socket
		test_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

		# Start a thread for the server
		# server_thread = threading.Thread(target=setup_server)
		# server_thread.start()

		try:
			# Simulate the client socket connecting to the server
			test_socket.connect(('localhost', PORT))

			# Wait for the server to handle the connection
			time.sleep(1)

			# Check if the test client is in the clients dictionary on the server side
			self.assertIn(test_socket, get_clients().values())

		except Exception as e:
			print(f"Error in receive_message: {e}")
		finally:
			# Close the simulated client socket
			test_socket.close()

if __name__ == '__main__':
    unittest.main()
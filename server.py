from datetime import datetime
import socket
import threading
import signal
# 1. consider adding a functionality where each socket is related to a username.. so the server has a dictionary where each username points to the socket --- done
# 2. add functionality to not allow joining if the username already exists
# 3. replace even the client that sends the message with the same message that the server broadcasts to others

# idea is to trap control c and exit gracefully
def signal_handler(sig, frame):
	print("\nCtrl-c detected. Exiting gracefully.")
	cleanup()

def cleanup():
	# Additional cleanup or exit actions can be added here
	print(f'{get_time()}: Server is shutting down')
	#shutdown_event.set()
	for client in clients.values():
		client.close()
	server_socket.close()
	#sys.exit(0)

# Register the signal handler for Ctrl+C
signal.signal(signal.SIGINT, signal_handler)

def setup_server():

	global PORT
	PORT = 54332
	
	global server_socket

	server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	server_socket.bind(('localhost', PORT))

	server_socket.listen(5)

	# List to store all the connected clients
	global clients
	clients = {}

def tearDown():
	for client_socket in get_clients().values():
		client_socket.close()
	server_thread.join()

def get_clients():
	return clients

def get_time():
	current_time = datetime.now()
	# Format the output
	formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")

	# return the formatted time
	return formatted_time

def get_hour_minute():
	current_time = datetime.now()
	# Format the output
	formatted_time = current_time.strftime("%H:%M:%S")

	# return the formatted time
	return formatted_time

def handle_client(client_socket):
	# send a message to the client saying you have been connected and the current time
	# Get the current date and time
	print('{}: Established a connection with socket: {}'.format(get_time(),client_socket))

	client_socket.send("Please type your username".encode('utf-8'))

	username = client_socket.recv(1024).decode('utf-8')
	clients[username] = client_socket
	print('{}: User {} has joined the chat.'.format(get_time(), username))
	client_socket.send("{}: Welcome to the chat {}".format(get_time(), username).encode('utf-8'))
	
	broadcast(f"{username} has joined the chat. There are {len(clients)} ppl in the chat.", username, client_socket)

	try:
		while True:
			data = client_socket.recv(1024).decode('utf-8')

			if (data.lower() == 'quit'):
				break

			broadcast(data, username, client_socket)
	except (ConnectionResetError, BrokenPipeError):
		pass
	finally:
		#clients.remove(client_socket)
		# let other users know that {username} has left the chat		
		client_socket.close()
		del clients[username]
		print(f'{get_time()}: User {username} has left the chat. Number of total users is {len(clients)}.')

	return

def broadcast(message, username, sending_client):
	# add time to the message
	for client in clients.values():
		if (client != sending_client):
			client.send(('\n{} - {}: {}').format(get_hour_minute(), username, message).encode('utf-8'))

if __name__ == "__main__":
	# Start a thread for the server
	#server_thread = threading.Thread(target=setup_server)
	#server_thread.start()
	
	setup_server()
	while True:
		client_socket, address = server_socket.accept()

		handle_client_thread = threading.Thread(target=handle_client, args=(client_socket,))
		handle_client_thread.start()

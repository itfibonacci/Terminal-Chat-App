#### finish up the tasks below
### create a threads list that holds all the threads

from datetime import datetime
import socket
import threading
import signal
# 1. consider adding a functionality where each socket is related to a username.. so the server has a dictionary where each username points to the socket --- done
# 2. add functionality to not allow joining if the username already exists
# 3. replace even the client that sends the message with the same message that the server broadcasts to others
# 4 make sure to join all the threads at the end
# idea is to trap control c and exit gracefully

def signal_handler(sig, frame, cleanup, clients, server_socket):
	print("\nCtrl-c detected. Exiting gracefully.")
	cleanup(clients, server_socket)

def cleanup(clients, server_socket):
	# Additional cleanup or exit actions can be added here
	print(f'{get_time()}: Server is shutting down')
	#shutdown_event.set()
	for client in clients.values():
		print(f'{get_time()}: Closing client connection {client}')
		client.close()
	print(f'{get_time()}: Closing server socket {server_socket}')
	server_socket.close()
	#sys.exit(0)

def setup_server(PORT):
	print(f'{get_time()}: Server is starting up...')
	server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server_socket.bind(('localhost', PORT))
	server_socket.listen(5)
	clients = {}
	print(f'{get_time()}: Server is ready.')
	return server_socket, clients

def tearDown(clients, server_thread):
	for client_socket in clients.values():
		client_socket.close()
	server_thread.join()

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

def valid_username(username, clients):
	if (username in clients.keys()):
		return False
	else:
		return True
	
def handle_client(client_socket, clients):
	# send a message to the client saying you have been connected and the current time
	# Get the current date and time
	print('{}: Established a connection with socket: {}'.format(get_time(),client_socket))
	
	while True:
		client_socket.send("Please type your username: ".encode('utf-8'))
		username = client_socket.recv(1024).decode('utf-8')
		if (valid_username(username, clients)):
			break
		client_socket.send(f'Username {username} is taken. '.encode('utf-8'))

	clients[username] = client_socket
	print(f'{get_time()}: User {username} has joined the chat. There are {len(clients)} ppl in the chat.')
	client_socket.send(f'{get_time()}: User {username} has joined the chat. There are {len(clients)} ppl in the chat.'.encode('utf-8'))
	
	broadcast(f"{username} has joined the chat. There are {len(clients)} ppl in the chat.", username, client_socket, clients)

	try:
		while True:
			data = client_socket.recv(1024).decode('utf-8')

			if (data.lower() == 'quit'):
				break

			broadcast(data, username, client_socket, clients)
	except (ConnectionResetError, BrokenPipeError):
		pass
	finally:
		#clients.remove(client_socket)
		# let other users know that {username} has left the chat		
		client_socket.close()
		del clients[username]
		print(f'{get_time()}: User {username} has left the chat. Number of total users is {len(clients)}.')

		broadcast(f'{get_time()}: User {username} has left the chat. Number of total users is {len(clients)}.', username, client_socket, clients)

def broadcast(message, username, sending_client, clients):
	# add time to the message
	for client in clients.values():
		if (client != sending_client):
			client.send(('\n{} - {}: {}').format(get_hour_minute(), username, message).encode('utf-8'))

if __name__ == "__main__":
	# Start a thread for the server
	PORT = 54332
	server_socket, clients = setup_server(PORT)
	
	# Register the signal handler for Ctrl+C
	signal.signal(signal.SIGINT, lambda sig, frame: signal_handler(sig, frame, cleanup, clients, server_socket))

	threads = []
	
	while True:
		# change this because on control c, it gets called - maybe without even a try statement
		try:
			client_socket, address = server_socket.accept()
		except socket.error:
			break
		handle_client_thread = threading.Thread(target=handle_client, args=(client_socket,clients))
		handle_client_thread.start()
		threads.append(handle_client_thread)
	
	for thread in threads:
		print(f'{get_time()}: Waiting for thread {thread.ident} to close.')
		thread.join()

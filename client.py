import socket
import threading
import sys
import signal

def initial_setup():
	PORT = 54332

	global client_socket

	client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	client_socket.connect(('localhost', PORT))

	welcome_message = client_socket.recv(1024).decode('utf-8')
	print(welcome_message + ": ", end="")

	global username
	username = input()

	client_socket.send(username.encode('utf-8'))

	welcome_message_username = client_socket.recv(1024).decode('utf-8')
	print(welcome_message_username)

# idea is to trap control c and exit gracefully
def signal_handler(sig, frame):
	print("\nCtrl-c detected. Exiting gracefully.")
	cleanup()

def cleanup():
	# Additional cleanup or exit actions can be added here
	try:
		client_socket.send('quit'.encode('utf-8'))
	except Exception as e:
		print(f"Error closing client socket: {e}")
	shutdown_event.set()
	try:
		# Close the client socket
		client_socket.close()
	except Exception as e:
		print(f"Error closing client socket: {e}")
	print("\nExiting gracefully.")
	#sys.exit(0)

# Register the signal handler for Ctrl+C
signal.signal(signal.SIGINT, signal_handler)

def replace_line(new_text):
	# Move the cursor to the beginning of the line
	sys.stdout.write('\r')
	# Clear the line
	sys.stdout.write('\033[K')
	# Print the new text
	sys.stdout.write(new_text + '\n' + username + ": ")
	# Flush the output to update the display
	sys.stdout.flush()

def send_message():
	try:
		while not shutdown_event.is_set():
			print("{}: ".format(username), end="")
			
			message = input()
			if (message.lower() == 'quit'):
				cleanup()
				break
			try:
				client_socket.send(message.encode('utf-8'))
			except Exception as e:
				print(f"Error in receive_message: {e}")
	except Exception as e:
		print(f"Error in send_message: {e}")
        #cleanup()

	return

def receive_message():
	try:
		while not shutdown_event.is_set():
			user_message = client_socket.recv(1024).decode('utf-8')
			#print(user_message)
			replace_line(user_message)
	except Exception as e:
		print(f"Error in receive_message: {e}")
	return

send_message_thread = threading.Thread(target=send_message)
receive_message_thread = threading.Thread(target=receive_message)

if __name__ == "__main__":
	# Create an Event object to signal the shutdown
	shutdown_event = threading.Event()

	initial_setup()

	send_message_thread.start()
	receive_message_thread.start()

	try:
		send_message_thread.join()
		receive_message_thread.join()
	except KeyboardInterrupt:
		print("\nCtrl+C detected. Cleaning up and exiting, thread join block.")
	#client_socket.close()

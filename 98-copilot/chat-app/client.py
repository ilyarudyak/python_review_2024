import socket
import threading

# Create a socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Define the server address and port
server_address = ('localhost', 3000)

# Connect to the server
client_socket.connect(server_address)

def send_message():
    while True:
        message = input("Enter a message to send to the server: ")
        client_socket.send(message.encode())

def receive_response():
    while True:
        response = client_socket.recv(1024)
        print("Received response from server:", response.decode())

# Create two threads for sending and receiving messages
send_thread = threading.Thread(target=send_message)
receive_thread = threading.Thread(target=receive_response)

# Start the threads
send_thread.start()
receive_thread.start()

# Wait for the threads to finish
send_thread.join()
receive_thread.join()

# Close the socket when you're done
client_socket.close()
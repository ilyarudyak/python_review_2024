import socket
import threading

connected_clients = []

def handle_client(client_socket):
    # Add the client to the list of connected clients
    connected_clients.append(client_socket)

    while True:
        # Receive data from the client
        message = client_socket.recv(1024)
        if not message:
            break

        # Print the received data
        print(f"Received message: {message.decode('utf-8')}")

        # Broadcast the message to all connected clients
        for client in connected_clients:
            if client != client_socket:
                client.send(message)

def start_server():
    # 1) Create a socket object
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # 2) Bind the socket to a specific address and port
    server_address = ('localhost', 3000)
    server_socket.bind(server_address)

    # 3) Listen for incoming connections
    server_socket.listen(5)
    print("Server listening on {}:{}".format(*server_address))

    # 4) Run an infinite loop to accept incoming connections
    while True:
        # Accept a client connection
        client_socket, client_address = server_socket.accept()
        print("Accepted connection from {}:{}".format(*client_address))

        # Start a new thread to handle the client connection
        client_thread = threading.Thread(target=handle_client, args=(client_socket,))
        client_thread.start()


if __name__ == "__main__":
    start_server()
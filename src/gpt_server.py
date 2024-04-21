import socket

# Server address and port
server_host = '128.110.217.156'
server_port = 12345

# Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the server address and port
server_socket.bind((server_host, server_port))

# Listen for incoming connections
server_socket.listen(1)

print("Server listening on {}:{}".format(server_host, server_port))

while True:
    # Accept a connection from the proxy
    proxy_socket, proxy_address = server_socket.accept()
    print("Accepted connection from proxy:", proxy_address)

    while True:
        # Receive data from the proxy
        data = proxy_socket.recv(1024).decode()

        if data:
            print("Received data from proxy:", data)

            # Process the data (e.g., perform calculations, handle requests)

            # Send a response back to the proxy
            response = "Response from server: {}".format(data.upper())
            proxy_socket.sendall(response.encode())

            # Check if the connection should be closed
            if data.lower() == 'bye':
                break

    # Close the proxy socket
    proxy_socket.close()

# Close the server socket
server_socket.close()
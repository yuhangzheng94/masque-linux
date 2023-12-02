import socket

# Proxy address and port
proxy_host = '128.110.217.132'
proxy_port = 4433

# Server address and port
server_host = '128.110.217.156'
server_port = 12345

# Create a socket object
proxy_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the proxy address and port
proxy_socket.bind((proxy_host, proxy_port))

# Listen for incoming connections
proxy_socket.listen(1)

print("Proxy listening on {}:{}".format(proxy_host, proxy_port))

while True:
    # Accept a connection from the client
    client_socket, client_address = proxy_socket.accept()
    print("Accepted connection from:", client_address)
    
    # Create a socket object to connect to the server
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect to the server
    server_socket.connect((server_host, server_port))

    while True:
        # Receive data from the client
        data = client_socket.recv(1024).decode()

        if data:
            print("Received data from client:", data)

            # Send data to the server
            server_socket.sendall(data.encode())

            # Receive response from the server
            response = server_socket.recv(1024).decode()
            print("Received response from server:", response)

            # Send the response back to the client
            client_socket.sendall(response.encode())

            # Check if the connection should be closed
            if data.lower() == 'bye':
                break

    # Close the server socket
    server_socket.close()
 
    # Close the client socket
    client_socket.close()

# Close the proxy socket
proxy_socket.close()
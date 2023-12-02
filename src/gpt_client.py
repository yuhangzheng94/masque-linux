import socket

# Proxy address and port
proxy_host = '128.110.217.132'
proxy_port = 12343

# Server address and port
server_host = '128.110.217.156'
server_port = 54321

# Create a socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the proxy
client_socket.connect((proxy_host, proxy_port))

while True:
    # Receive data from the user
    data = input("Enter data to send: ")

    # Send data to the proxy
    client_socket.sendall(data.encode())

    # Receive response from the proxy
    response = client_socket.recv(1024).decode()

    # Print the response
    print("Response from proxy:", response)

    # Check if the connection should be closed
    if data.lower() == 'bye':
        break

# Close the socket
client_socket.close()
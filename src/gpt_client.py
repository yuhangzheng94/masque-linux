import socket

# Proxy address and port
proxy_host = '128.110.217.132'
proxy_port = 4433

# Server address and port
server_host = '128.110.217.156'
server_port = 12345

client_host = '128.110.217.119'
client_port = 8989

# Create a socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the proxy
client_socket.connect((proxy_host, proxy_port))

# Connect to the end port that sends request and measure RTTs
listening_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Bind the socket to the proxy address and port
listening_socket.bind((client_host, client_port))
# Listen for incoming connections
listening_socket.listen(1)
# Accept a connection from the client
request_socket, request_address = listening_socket.accept()
print("Accepted connection from:", request_address)


while True:
    # Receive data from the user
    # data = input("Enter data to send: ")
    data = request_socket.recv(1024).decode()

    if not data:
        continue

    # Send data to the proxy
    client_socket.sendall(data.encode())

    # Receive response from the proxy
    response = client_socket.recv(1024)

    # # Print the response
    # print("Response from proxy:", response)

    request_socket.sendall(response)

    # Check if the connection should be closed
    if data.lower() == 'bye':
        break

# Close the socket
client_socket.close()
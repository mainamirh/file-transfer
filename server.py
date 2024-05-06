import socket
import threading
import time


# Function to handle file transfer and saving
def runService(connection_socket, filename, filedata):
    try:
        with open(f"savedByServer/{filename}", "wb") as file:
            file.write(filedata)

        time.sleep(1)
        # Send a confirmation message back to the client
        connection_socket.send(
            "\n   📡 Message from Server: 💾 File saved successfully.\n".encode()
        )

    except IOError as e:
        # Handle file IO errors
        connection_socket.send(f"Error saving file: {e}".encode())
    except Exception as e:
        # Handle other exceptions
        connection_socket.send(f"An error occurred: {e}".encode())


def handle_client(connection_socket, client_address):
    print(f"Client {client_address} connected.")

    connection_socket.settimeout(60)  # Disconnect after being idle for 60 seconds

    try:
        while True:
            message = connection_socket.recv(1024)

            if message.decode() == "exit":
                connection_socket.close()
                print(f"{connection_socket} Disconnected by Client {client_address}")
                break

            else:
                filename, filedata = message.split(b"\n", 1)  # Receive file

                time.sleep(1)
                connection_socket.send(
                    "\n   📡 Message from Server: 📥 File received successfully.".encode()
                )

                runService(connection_socket, filename.decode(), filedata)

    except ValueError:
        print(f"{client_address} disconnected.")

    except socket.timeout:
        print(f"Connection of {client_address} timed out.")
        connection_socket.close()


# Configure server
host = "localhost"
port = 12000
# params ipv4, tcp
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((host, port))
server_socket.listen(1)
print("Server listening on port:", port)

# Serve the clients
while True:
    # Accept a new connection
    connection_socket, client_address = server_socket.accept()

    # Create a new thread to handle the client
    client_thread = threading.Thread(
        target=handle_client, args=(connection_socket, client_address)
    )
    client_thread.start()

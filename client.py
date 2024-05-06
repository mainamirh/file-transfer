import socket
import os
import time

client_socket = None


# Function to establish connection with the server
def establishConnection():
    global client_socket
    serverHost = "localhost"
    serverPort = 12000
    # params ipv4, tcp
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    print(f"Connecting to {serverHost}:{serverPort} ...")

    time.sleep(1)

    try:
        client_socket.connect((serverHost, serverPort))
        print("Client Socket: ", client_socket.getsockname())
        print("\n   🛜  Connection established successfully.\n")
        time.sleep(1)

    except ConnectionRefusedError:
        print(
            "\n   ❗ Connection refused. Make sure the server is running and listening.\n"
        )
        disconnect()
    except Exception as e:
        print(f"\n    ❗ An error occurred: {e}\n")
        disconnect()


# Function to read selected file
def readSelectedFile(selectedFile):
    file_path = os.path.join("files", selectedFile)
    try:
        with open(file_path, "rb") as file:
            file_data = file.read()
        return file_data

    except FileNotFoundError:
        print(f"\n❌ File '{selectedFile}' not found.")
        return None
    except Exception as e:
        print(f"\n❌ Error reading file '{selectedFile}': {e}")
        return None


# Function to handle response from server
def responseFromServer():
    global client_socket

    client_socket.settimeout(60)  # Disconnect after being idle for 60 seconds

    try:
        while True:
            # Receive a confirmation message from the server
            receiveMessage = client_socket.recv(1024).decode()
            if receiveMessage:
                print(receiveMessage)
                if (
                    receiveMessage
                    == "\n   📡 Message from Server: 💾 File saved successfully.\n"
                ):
                    break

    except ConnectionAbortedError:
        print("Server closed the connection.")
        disconnect()
    except socket.timeout:
        print(f"Connection of {client_socket} timed out.")
        disconnect()


# Function to send file to server
def sendFileToServer(filename, filedata):
    global client_socket
    if client_socket is None:
        return
    client_socket.sendall(f"{filename}\n".encode() + filedata)
    responseFromServer()


def disconnect():
    global client_socket
    print("\nDisconnecting...")
    client_socket.close()  # Close connection
    time.sleep(1)
    exit(1)  # Exit the program


def sendExitMessage():
    global client_socket
    client_socket.send("exit".encode())


# Function to clear the screen
def clear_screen():
    # For Windows
    if os.name == "nt":
        _ = os.system("cls")
    # For Mac and Linux
    else:
        _ = os.system("clear")


clear_screen()

# Try to connect to the server
establishConnection()

# Get list of files
files = os.listdir("files")

# Show menu to the user
while True:
    print("\n❔ Which file do you want to send?")

    for index, file in enumerate(files, 1):
        print(f"    {index}. {file}")

    print(f"\n{len(files) + 1}. Exit")

    choice = input("\nSelect your file: ")

    if choice.isdigit():  # Check if input is a number
        choice = int(choice)
        if 1 <= choice <= len(files):
            clear_screen()  # Clear screen after sending file
            selected_file = files[choice - 1]  # Get the selected file
            print(f"\n✅ You selected: {selected_file}")
            file_data = readSelectedFile(selected_file)
            time.sleep(1)
            if file_data:
                print(f"📨 Sending {selected_file} to the server...")
                time.sleep(1)

                sendFileToServer(selected_file, file_data)

        elif choice == len(files) + 1:
            sendExitMessage()
            disconnect()
            break
        else:
            clear_screen()
            print("\n❌ Invalid choice. Please select a valid file number.")
    else:
        clear_screen()
        print("\n❌ Invalid input. Please enter a number corresponding to the file.")

import socket

HOST = 'localhost'  # Replace with server IP or hostname
PORT = 65432        # Replace with server port

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))

    while True:
        message = input("Enter the data to hash (or 'quit' to quit): ")
        if message:
            # Encode data for reliable transmission
            s.sendall(message.encode())
            print("///////////////////////////////////////////")
            print(f"\n\nSent message: {message}\n")

            # Receive response and extract status code and phrase
            received_data = s.recv(1024).decode()
            print(f"Server replied:")
            if received_data:
                status_line = received_data.split("\r\n")[0]  # Extract first line
                status_code, status_phrase = status_line.split()[1:3]
                # print(f"Status code: {status_code}, Status phrase: {status_phrase}")
                print(f"Remaining response: {received_data}\n")
                print("///////////////////////////////////////////")

            else:
                print("Server disconnected without reply.")

            # Check for closure message from server
            if received_data and received_data.endswith("\r\nServer shutting down...\r\n"):
                print("Server initiated closure. Closing client.")
                break

        else:
            break  # Exit loop if empty input

    # Gracefully close the connection
    s.shutdown(socket.SHUT_RDWR)  # Bidirectional close
    print("Connection closed.")

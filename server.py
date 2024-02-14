import socket
import threading
import hashlib

HOST = 'localhost'  # Replace with your server's IP or hostname
PORT = 65432        # Choose an available port number

def sha256_hash(data):
    """Hashes the given data using SHA-256 and returns the hexadecimal digest."""
    hasher = hashlib.sha256()
    hasher.update(data.encode())
    return hasher.hexdigest()

def handle_client(conn, addr):
    """Handles a connected client, receiving and processing data."""
    with conn:  # Ensures socket closure even with exceptions
        print(f"Connected by {addr}")
        try:
            while True:
                data = conn.recv(1024).decode()
                if not data:
                    break

                # Print and process data (convert to uppercase)
                processed_data = data
                print(f"{addr} sent: {data}")

                # Check for quit message
                if processed_data == "quit":
                    print(f"Client {addr} requested closure.")
                    conn.sendall(f"HTTP/1.1 200 OK\r\n\r\nServer shutting down...\r\n".encode())
                    print("Server shutdown")
                    server_socket.close()
                    break

                # Send response
                processed_data = sha256_hash(processed_data)
                print("Status: 200 OK")
                response = f"HTTP/1.1 200 OK\r\n\r\nOutput:\n{processed_data}\r\n"
                conn.sendall(response.encode())
            # print("Server shutdown.")
            # server_socket.close()

        except ConnectionError:
            print(f"Client {addr} abruptly disconnected.")

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    server_socket.bind((HOST, PORT))
    server_socket.listen()
    print(f"Server listening on {HOST}:{PORT}")

    while True:
        conn, addr = server_socket.accept()
        client_thread = threading.Thread(target=handle_client, args=(conn, addr))
        client_thread.start()
import socket
import threading

# Server configuration
HOST = '127.0.0.1'  # The IP address for localhost; this means the server will only listen on the local machine
PORT = 8080         # The port number the server will use to listen for incoming connections

# Function: handle_client
# Input: client_socket - the socket object representing the client connection
# Output: None
# Purpose: Handle individual client HTTP requests in a separate thread
def handle_client(client_socket):
    try:
        # Receive the client's request (up to 1024 bytes) and decode it from bytes to a UTF-8 string
        request = client_socket.recv(1024).decode('utf-8')
        print(f"Received request: {request}")  # Debugging: Output the client's request to the console

        # Parse the HTTP request by splitting it into lines
        lines = request.splitlines()
        if len(lines) > 0:  # Ensure there is at least one line in the request
            first_line = lines[0]  # The first line typically contains the HTTP method and resource path
            parts = first_line.split()  # Split the line into its components (e.g., ["GET", "/index.html", "HTTP/1.1"])
            # Check if the request is a 'GET' method and contains a resource path
            if len(parts) > 1 and parts[0] == 'GET':
                requested_file = parts[1]  # Extract the requested resource path (e.g., "/index.html")

                # Handle HTTP 301 redirect: Redirect "/page1.html" to "/page2.html"
                if requested_file == '/page1.html':
                    # Construct a 301 Moved Permanently response header with "Location" to redirect to "/page2.html"
                    response = (
                        "HTTP/1.1 301 Moved Permanently\r\n"
                        "Location: /page2.html\r\n"  # Redirect location
                        "Content-Length: 0\r\n"  # No content in the response body
                        "Connection: close\r\n"  # Indicate that the server will close the connection
                        "\r\n"
                    )
                    client_socket.sendall(response.encode())  # Send the response back to the client
                    client_socket.close()  # Close the socket for this client
                    return  # Exit the function since the response has been sent

                # Default to serving "index.html" if the root ("/") is requested
                if requested_file == '/':
                    requested_file = '/index.html'

                try:
                    # Construct the file path by appending the requested file to the current directory (.)
                    file_path = '.' + requested_file
                    with open(file_path, 'rb') as f:  # Open the requested file in binary read mode
                        content = f.read()  # Read the file's content

                    # Determine the content type based on the file extension (default to 'text/html')
                    content_type = 'text/html'
                    if file_path.endswith('.jpg') or file_path.endswith('.jpeg'):
                        content_type = 'image/jpeg'  # Set content type for JPEG images

                    # Construct a 200 OK HTTP response header with appropriate headers
                    response = (
                        "HTTP/1.1 200 OK\r\n"
                        f"Content-Type: {content_type}\r\n"  # Set the content type
                        f"Content-Length: {len(content)}\r\n"  # Set the content length
                        "Connection: close\r\n"  # Indicate that the server will close the connection
                        "\r\n"
                    )
                    client_socket.sendall(response.encode() + content)  # Send the response header and file content

                except FileNotFoundError:
                    # Handle 404 Not Found: The requested file does not exist
                    with open('./404.html', 'rb') as f:  # Open the custom 404 error page
                        content = f.read()  # Read the content of the 404 error page

                    # Construct a 404 Not Found HTTP response header
                    response = (
                        "HTTP/1.1 404 Not Found\r\n"
                        "Content-Type: text/html\r\n"  # Set content type to HTML
                        f"Content-Length: {len(content)}\r\n"  # Set content length
                        "Connection: close\r\n"  # Indicate that the server will close the connection
                        "\r\n"
                    )
                    client_socket.sendall(response.encode() + content)  # Send the response header and content

    except Exception as e:
        print(f"Error: {e}")  # Debugging: Print any exceptions that occur
    finally:
        client_socket.close()  # Ensure the client socket is closed to free up resources

# Function: start_server
# Input: None
# Output: None
# Purpose: Initialize and start the multi-threaded web server
def start_server():
    # Create a TCP socket using IPv4 (AF_INET) and a streaming socket (SOCK_STREAM)
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Bind the socket to the specified host (localhost) and port
    server_socket.bind((HOST, PORT))
    # Listen for incoming connections, with a backlog of 5 (maximum number of queued connections)
    server_socket.listen(5)
    print(f"Server started on {HOST}:{PORT}")  # Debugging: Output the server's start message

    try:
        while True:  # Continuously listen for incoming connections
            # Accept a new connection from a client
            client_socket, addr = server_socket.accept()
            print(f"Connection from {addr}")  # Debugging: Output the client's address
            # Create a new thread to handle the client's request
            client_handler = threading.Thread(target=handle_client, args=(client_socket,))
            client_handler.start()  # Start the thread to handle the client
    except KeyboardInterrupt:
        print("\nShutting down the server.")  # Gracefully handle a keyboard interrupt (Ctrl+C)
    finally:
        server_socket.close()  # Close the server socket to free up resources

# Entry point of the script
if __name__ == '__main__':
    start_server()  # Call the function to start the server

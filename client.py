"""
Smart TV Remote Control (TCP Client)
====================================

This script implements a simple command-line "Smart Remote"
for the Smart TV server. It connects to the server over TCP,
sends user-typed commands, and displays the server responses.

Usage:
    python3 client.py [host] [port]

Examples:
    python3 client.py
        # connects to localhost:1238
    
    python3 client.py 192.168.1.20 5555
        # connects to a Smart TV server on another machine

Support commands (handled by server):
    - help
    - version
    - on
    - off
    - status
    - get_c
    - get_ch
    - set_ch <n>
    - quit

Author: dotDennis
Course: IDATA2304
"""

import socket
import threading
from config import DEFAULT_HOST, DEFAULT_PORT

def create_client_socket() -> socket.socket:
    """
    Creates a TCP client socket
    """
    return socket.socket(socket.AF_INET,socket.SOCK_STREAM)


def connect_to_server(sock: socket.socket, host: str, port: int) -> None:
    """
    Establish a TCP connection to the Smart TV server.

    Args:
        sock (socket.socket): The client socket.
        host (str): The server hostname or IP address.
        port (int): The TCP port number for the server.

    Returns:
        socket.socket: An active socket connection.
    """
    sock.connect((host,port))
    print('Connected to server')

def _receiver(sock: socket.socket) -> None:
    """
    Background receiver that continuously prints server messages
    (welcome, command responses, and asynchronous notifications).
    """
    try:
        while True:
            data = sock.recv(1024)
            if not data:
                break
            msg = data.decode(errors='ignore').strip()
            if msg:
                print(msg)
    except Exception:
        # Socket likely closed or interrupted; exit quietly
        pass

def read_send_command(sock: socket.socket) -> None:
    """
    Reads commands from the user input, sends to server,
    and prints the server reponses. Ends when user types 'quit'.
    """
    while True:
        command = input('SmartTV>> ').strip()
        if not command:
            print('No command entered (type \'help\' for options).')
            continue

        sock.sendall((command).encode())

        if command.lower() == 'quit':
            break

def main() -> None:
    """
    Main entry point of the Smart TV remote client.

    Behavior:
        - Creates a TCP client socket.
        - Connects to the Smart TV server (default from config.py)
        - Receives and prints the welcome message from server.
        - Enters interactive command loop:
            * Reads user input
            * Sends command to server
            * Prints server response
        - Exits when the user types 'quit' or if an error occurs.
        - Ensures socket closing before shutdown.

    Returns:
        None
    """
    host = DEFAULT_HOST
    port = DEFAULT_PORT
    sock = create_client_socket()
    try:
        connect_to_server(sock,host,port)
        # Start background receiver to handle both responses and notifications
        recv_thread = threading.Thread(target=_receiver, args=(sock,), daemon=True)
        recv_thread.start()
        read_send_command(sock)
    except Exception as e:
        print(f'An error occured: {e}\n')
    finally:
        sock.close()
        print('Disconnected from server')

if __name__=='__main__':
    main()

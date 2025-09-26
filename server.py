"""
Smart TV (TCP Server)
=====================

This server simulates a "Smart TV" that accepts simple text commands
from a remote client over TCP sockets.

Usage:
    python3 server.py

Behavior:
    - Binds to 127.0.0.1:1238 (change in code if needed)
    - Accepts a single client connection
    - Processes commands until the client disconnects or sends 'quit'

Notes:
    - The server delegates command parsing/logic to 'handle_command()' in handler.py
    - The server is restart-friendly via SO_REUSEADDR.
    - Multi-client support are planned for a later part (threads?)

Author: dotDennis
Course: IDATA2304
"""

import socket
from config import DEFAULT_HOST, DEFAULT_PORT
from handler import handle_command


def create_socket() -> socket.socket:
    """
    Create a TCP/IP socket with IPv4 addressing.

    Returns:
        socket.socket: A TCP socket with SO_REUSEADDR set for restart-friendly behavior.
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
    return s


def bind_socket(sock: socket.socket, host: str, port: int) -> None:
    """
    Bind the socket to a host and port.

    Args:
        sock (socket.socket): The server socket.
        host (str): The hostname or IP address to bind.
        port (int): The port number to bind.

    Returns:
        None
    """
    sock.bind((host, port))


def listen_for_connection(sock: socket.socket) -> None:
    """
    Set the socket into listening mode.

    Args:
        sock (socket.socket): The server socket.

    Returns:
        None

    """
    sock.listen()
    print(f'Server listening on {sock.getsockname()}')


def accept_connection(sock: socket.socket) -> tuple[socket.socket, tuple [str, int]]:
    """
    Wait for a client to connect.

    Args:
        sock (socket.socket): The listening socket.

    Returns:
        tuple:
            - conn (socket.socket): Connection socket and client address tuple.
            - addr (tuple[str, int]): The client (IP address, port).
    """
    return sock.accept()


def receive_command(conn) -> str | None:
    """
    Receive a command from the connected client.

    Args:
        conn (socket.socket): Active client connection.

    Returns:
        str | None: The decoded command string, or None if client closed.
    """
    try:
        data = conn.recv(1024)
        if not data:
            return None
        return data.decode(errors='replace').strip()
    except Exception as e:
        print(f'Server Error: {e!r}')
        return None


def close_socket(sock: socket.socket) -> None:
    """
    Close the socket and logs it.

    Args:
        sock (socket.socket): The socket to close

    Returns:
        None
    """
    sock.close()
    print('Server closed')


def main() -> None:
    """
    Main entry point of the Smart TV server.

    Behavior:
        - Creates a socket
        - Binds to host/port (from config.py)
        - Accepts a single client connection
        - Receives and processes commands until the client disconnects or sends 'quit'
        - Delegates command handling/parsing to handle_command() (from handle_command.py)
        - Ensures proper closing of sockets on shutdown

    Returns:
        None
    """
    host = DEFAULT_HOST
    port = DEFAULT_PORT
    server_socket = create_socket()
    conn = None

    try:
        bind_socket(server_socket, host, port)
        listen_for_connection(server_socket)
        conn, addr = accept_connection(server_socket)
        print(f'Server connection established with {addr}')
        conn.sendall(b'Welcome to the Smart TV server. Type \'ON\' to begin.\n')

        while True:
            command = receive_command(conn)
            if command is None:
                break
            if command.lower() == 'quit':
                conn.sendall(b'Until next time!\n')
                break

            response = handle_command(command)

            if not isinstance(response, str):
                response = 'ERROR: Internal handler bug (no response)'

            conn.sendall(response.encode())

    except Exception as e:
        print(f'Server encountered an error & shut down: {e!r}')

    finally:
        try:
            if conn:
                conn.close()
        except Exception as e:
            print(f'Error closing connection: {e!r}')
        try:
            close_socket(server_socket)
        except Exception as e:
            print(f'Error closing server socket: {e!r}')


if __name__ == '__main__':
    main()
import sys
import os
import random
import string
from socket import *
import socket
import threading
import socket
import threading

def background(client_socket):
    while True:
        try:
            server_message = client_socket.recv(1024).decode()
            if not server_message:
                print("\nServer disconnected.")
                break

            print(f"\nReceived from server: {server_message}")
        except:
            break

def main():
    host = '127.0.0.1'
    port = 65432

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client_socket.connect((host, port))
        print(f"Connected to server at {host}:{port}")

        # 1. Wait for greeting from server
        server_greeting = client_socket.recv(1024).decode()
        print(server_greeting)

        # Get username
        username = input("Enter your username: ")
        client_socket.send(username.encode())

        # Start background listener thread
        background_thread = threading.Thread(
            target=background, 
            args=(client_socket,), 
            daemon=True
        )
        background_thread.start()

        while True:
            message = input("Enter a message: ")

            if message.lower() == "quit":
                print("Disconnecting")
                break

            client_socket.send(message.encode())

    except ConnectionRefusedError:
        print(f"Connection refused — is the server running on {host}:{port}?")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        client_socket.close()
        print("Connection closed.")

if __name__ == "__main__":
    main()
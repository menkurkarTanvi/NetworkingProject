import sys
import os
import random
import string
from socket import *
import threading

#store clients
clients = {}
def client_handler(client_socket, client_address, username):
    print(f"Handling client {client_address}")
    try:
        while True:
            data = client_socket.recv(1024)
            data_string = data.decode('utf-8').strip()
            if len(data_string) > 1 and data_string.startswith("@"):
                username_message = data_string.split(" ", 1)
                if len(username_message) < 2:
                   client_socket.sendall(b"Incorrect format. Use: @username message\n")
                   continue
                target_username = username_message[0][1:]
                message = username_message[1]
                if target_username in clients:
                  target_socket = clients[target_username]
                  send_text = f"[{username}]{message}"
                  target_socket.sendall(message.encode('utf-8'))
                else:
                  client_socket.sendall(
                        f"User '{target_username}' not found.\n".encode('utf-8')
                    )
            else:
              client_socket.sendall(b"Incorrect format. Use: @username message\n")
    except Exception as e:
        print(f"Error handling client {client_address}: {e}")
    finally:
        client_socket.close()
        print(f"Client {client_address} disconnected.")

def main():
    HOST = '127.0.0.1' 
    PORT = 65432        

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen()

    print(f"Server listening on {HOST}:{PORT}")
    while True:
      client_socket, client_address = server_socket.accept()
      print(f"Accepted connection from {client_address}")
      message_to_client = "Hello, please send your username"
      client_socket.sendall(message_to_client.encode('utf-8'))
      username = client_socket.recv(1024).decode('utf-8').strip()
      #Add the (username, socket) to the dictionary
      clients[username] = client_socket
      client_socket.sendall(
        b"Welcome! Send messages using: @username message\n"
      )
      #Start the thread for the client
      client_thread = threading.Thread(target=client_handler, args=(client_socket, client_address, username))
      client_thread.start()
   

if __name__ == "__main__":
    main()

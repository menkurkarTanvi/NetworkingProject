import sys
import os
import random
import string
from socket import *
import threading
import socket
#store clients
clients = {} 
def client_handler(client_socket, client_address, username):
    print(f"Handling client {client_address}")
    try:
        while True:
            #receive the message from the client socket
            message = client_socket.recv(1024)
            message_string = message.decode('utf-8').strip()
            #Send the message to all clients except the client that sent the message
            for client_username in clients:
               if client_username != username:
                socket = clients[client_username]
                socket.sendall(message_string.encode('utf-8'))
        
    except Exception as e:
        print(f"Error handling client {client_address}: {e}")
    finally:
        # Remove the client from the dictionary
        if username in clients:
            del clients[username]
        #Close the client socket as wel will no longer need to communicate with that client
        client_socket.close()
        print(f"Client {client_address} ({username}) disconnected.")

def main():
    HOST = '192.168.1.40' 
    PORT = 65432        
    #Bind server to IP and Port
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen()

    print(f"Server listening on {HOST}:{PORT}")
    try:
      while True:
        #Accept connection from client
        client_socket, client_address = server_socket.accept()
        print(f"Accepted connection from {client_address}")
        message_to_client = "Hello, please send your username\n"
        client_socket.sendall(message_to_client.encode('utf-8'))
        username = client_socket.recv(1024).decode('utf-8').strip()

        #Check if the username is already in the dictionary
        if username in clients:
          client_socket.sendall(b"Username already taken. Disconnecting.\n")
          client_socket.close()
          continue

        #Add the (username, socket) to the dictionary
        clients[username] = client_socket
        client_socket.sendall(
          b"Welcome! Send messages\n"
        )
        #Start the thread for the client
        client_thread = threading.Thread(target=client_handler, args=(client_socket, client_address, username))
        client_thread.start()
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        server_socket.close()
        print("Connection closed.")
       
   

if __name__ == "__main__":
    main()

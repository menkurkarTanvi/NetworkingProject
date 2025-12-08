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
            data = client_socket.recv(1024)
            #Decode the message
            data_string = data.decode('utf-8').strip()
            #Check if the message is in the correct format
            if len(data_string) > 1 and data_string.startswith("@"):
                #Extract the target username and message
                username_message = data_string.split(" ", 1)
                #Validate the format
                if len(username_message) < 2:
                   client_socket.sendall(b"Incorrect format. Use: @username message\n")
                   continue
                #Get target username and message
                target_username = username_message[0][1:]
                message = username_message[1]
                #Check if the target username exists
                if target_username in clients:
                  #Send the message to the target user
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
        # Remove the client from the dictionary
        if username in clients:
            del clients[username]
        #Close the client socket as wel will no longer need to communicate with that client
        client_socket.close()
        print(f"Client {client_address} ({username}) disconnected.")

def main():
    HOST = '192.168.1.40' 
    PORT = 65432        

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
          b"Welcome! Send messages using: @username message\n"
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

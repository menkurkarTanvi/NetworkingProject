import socket
import threading
import tkinter as tk
from tkinter import simpledialog, scrolledtext, messagebox

class Chat_GUI:
    def __init__(self):
        self.host = '127.0.0.1'
        #self.host = '192.168.1.40'
        self.port = 65432
        
        #Create TCP/IP socket
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        #Connect to server using provided host and port
        try:
            self.client_socket.connect((self.host, self.port))
            print(f"Connected to server at {self.host}:{self.port}")
        except Exception as e:
            messagebox.showerror("Connection Error", f"Could not connect to server: {e}")
            return
        
        #Request the username from user
        self.username = simpledialog.askstring("Username", "Enter your username:")
        if not self.username:
            messagebox.showwarning("Input Error", "Username cannot be empty.")
            return
        
        #Send the username to the server
        try:
            self.client_socket.send(self.username.encode())
        except:
            messagebox.showerror("Send Error", "Could not send username to server.")
            return
        
        #Setup GUI
        self.setup_gui()
        
        #Start background thread to listen for messages from server
        self.running = True
        self.background_thread = threading.Thread(target=self.receive_message, daemon=True)
        self.background_thread.start()
        
        #Start the Tkinter main loop
        self.root.mainloop()
        
    #Build the GUI components    
    def setup_gui(self):
        self.root = tk.Tk()
        self.root.title("Chat Client")
        
        # Chat display area (messages received)
        self.chat_area = scrolledtext.ScrolledText(
            self.root, wrap=tk.WORD, state=tk.DISABLED, height=20, width=60
            )
        self.chat_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        
        # Message entry area (to send messages)
        self.message_entry = tk.Entry(self.root, width=60)
        self.message_entry.pack(padx=10, pady=(0, 10), fill=tk.X)
        self.message_entry.bind("<Return>", self.send_message)
        
        #Send Button
        self.send_button = tk.Button(self.root, text="Send", command=self.send_message)
        self.send_button.pack(padx=10, pady=(0, 10))
            
        #Handle window closing
        self.root.protocol("WM_DELETE_WINDOW", self.close_connection)
        
    #Send message from GUI input    
    def send_message(self, event=None):
        message = self.message_entry.get()
        if message.strip() != "":
            try:
                self.client_socket.send(message.encode())
            except:
                messagebox.showerror("Send Error", "Could not send message to server.")
                self.close_connection()
                
        self.message_entry.delete(0, tk.END)
    
    #Background listener for incoming messages
    def receive_message(self):
        while self.running:
            try:
                server_message = self.client_socket.recv(1024).decode()
                if not server_message:
                    self.display_message("Server disconnected.")
                    break
                self.display_message(server_message)
            except:
                break
            
        self.close_connection()
        
    #Display message in chat area
    def display_message(self, message):
        self.chat_area.config(state=tk.NORMAL)
        self.chat_area.insert(tk.END, message + "\n")
        self.chat_area.config(state=tk.DISABLED)
        self.chat_area.see(tk.END)
        
    #Close connection 
    def close_connection(self):
        self.running = False
        try:
            self.client_socket.close()
        except:
            pass
        self.root.destroy()
        
if __name__ == "__main__":
    Chat_GUI()
        
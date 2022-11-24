import socket
import threading

HEADER_LENGTH = 10
IP = "127.0.0.1"
PORT = 1234

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_socket.bind((IP, PORT))

server_socket.listen()

clients = []
pseudo=[]

def broadcast(message):
    for client in clients:
        client.send(message)

def handle(client):
    while True :
        try:
            message = client.recv(1024)
            print(f"{message}") #message in the server
            broadcast(message)

        except: #if the user crash or exit or crashed  we should remove it from the pseudo and clients
            index=clients.index(client)
            clients.remove(client)
            client.close()
            nickname=pseudo[index]
            pseudo.remove(nickname)
            break




def receive():
    while True:
        client, adress = server_socket.accept()   # to receive a new connexion and the socket of the client
        print(f"conneted with {str(adress)} !")
        client.send("PSEUDO".encode('utf-8')) #ask  for the nickname
        nickname=client.recv(1024)
        pseudo.append(nickname)
        clients.append(client)
        print(str(nickname) + " joined the server")
        broadcast(f"{nickname} is connected to the server! \n".encode("utf-8")) #broadcast the new client to all users
        client.send("You are connected to the server".encode("utf-8"))

        thread=threading.Thread(target =handle, args=(client,))  #virgule to pass the client as tuple to the handle function
        thread.start()


print("Server is running ")
receive()
import random
import socket
import time
from threading import Lock
from threading import Thread


class ChatServer:

    def __init__(self, port):
        self.port = port
        self.lock = Lock()
        self.clients = {}

    def handle_client(self, client_socket):
        user = "unknown"

        while True:
            data = client_socket.recv(4096).decode()

            command, param = data.split(",")

            # register handler
            if command == "register":
                print("\n{0} registered\n".format(param))
                with self.lock:
                    self.clients[param] = client_socket
                user = param
                client_socket.send("ack".encode())

            # list handler
            if command == "list":
                with self.lock:
                    names = self.clients.keys()

                names = ",".join(names)
                client_socket.send(names.encode())

            # chat handler
            if command == "chat":
                to_socket = None
                with self.lock:
                    if param in self.clients:
                        to_socket = self.clients[param]

                if to_socket is not None:
                    to_socket.send(("{0} says hi\n".format(user)).encode())
                else:
                    print("\nNo user by the name <{0}>\n".format(param))

    def run_server(self):

        # networking stuff to setup the connection, that the
        # can ignore
        socket_connection = socket.socket()
        socket_connection.bind(('', self.port))
        socket_connection.listen(5)

        # perpetually listen for new connections
        while True:
            client_socket, addr = socket_connection.accept()

            # spawn a thread to deal with a new client and immediately go back to
            # listening for new incoming connections
            Thread(target=self.handle_client, args=(client_socket,), daemon=True).start()


class User:

    def __init__(self, name, server_host, server_port):
        self.name = name
        self.server_port = server_port
        self.server_host = server_host

    def receive_messages(self, server_socket):
        while True:
            print("\n{0} received: {1}\n".format(self.name, server_socket.recv(4096).decode()))

    def run_client(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.connect((self.server_host, self.server_port))

        # register and receive ack
        server_socket.send("register,{0}".format(self.name).encode())
        server_socket.recv(4096).decode()

        # wait for friends to join
        time.sleep(3)

        # get list of friends
        server_socket.send("list,friends".encode())
        list_of_friends = server_socket.recv(4096).decode().split(",")
        num_friends = len(list_of_friends)

        # start listening for incoming messages
        Thread(target=self.receive_messages, args=(server_socket,), daemon=True).start()

        while True:
            # randomly select a friend and send a message
            friend = list_of_friends[random.randint(0, num_friends - 1)]
            server_socket.send("chat,{0}".format(friend).encode())

            time.sleep(random.randint(2, 6))


if __name__ == "__main__":
    server_port = random.randint(10000, 65000)
    server_host = "127.0.0.1"
    server = ChatServer(server_port)

    # start server
    Thread(target=server.run_server, daemon=True).start()
    time.sleep(1)

    # jane gets online
    jane = User("Jane", server_host, server_port)
    Thread(target=jane.run_client, daemon=True).start()

    zak = User("Zak", server_host, server_port)
    Thread(target=zak.run_client, daemon=True).start()

    abhishek = User("Abhishek", server_host, server_port)
    Thread(target=abhishek.run_client, daemon=True).start()

    igor = User("Natasha", server_host, server_port)
    Thread(target=igor.run_client, daemon=True).start()

    time.sleep(30)

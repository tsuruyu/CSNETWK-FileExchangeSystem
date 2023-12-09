import socket
import threading

host = '127.0.0.1'
port = 12345

registered = None

rgrClients = []
fileList = []

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def clientConnection(conn, addr):
    
    global registered
    connected = True
    
    while connected:
        fileRequest = None
        command = conn.recv(1024).decode()
        #print(f"Received command: {command}")
        
        if command == "register":
            name = conn.recv(1024).decode()
            if name not in rgrClients:
                rgrClients.append(name)
                conn.send("Registered!".encode())
                registered = True
            else:
                conn.send("Already registered!".encode())
            continue
        
        if registered == True:
            if command == "store":
                fileRequest = conn.recv(1024).decode()
                fileList.append(fileRequest)
                print(f"File {fileRequest} stored to directory by {name}.")
                continue
                
            elif command == "get":
                fileRequest = conn.recv(1024).decode()
                if fileRequest not in fileList:
                    conn.send("FDNE".encode())
                else:
                    with open(fileRequest, 'r'):
                        pass
                    conn.send(fileRequest.encode())
                    print(f"File {fileRequest} requested by {name} and successfully delivered.")
                continue
                    
            elif command == "dir":
                for file in fileList:
                    conn.send(file.encode())
                conn.send("Directory done!".encode())
                continue
                
            elif command == "register":
                name = conn.recv(1024).decode()
                if name not in rgrClients:
                    rgrClients.append(name)
                    conn.send("Registered!".encode())
                else:
                    conn.send("Already registered!".encode())
                continue
                    
            elif command == "leave":
                if name in rgrClients:
                    print(f"Client {name} disconnected.")
                else:
                    print("An unregistered user disconnected.")
                break
            
            elif command == "shutdown":
                server.close()
                print("Server stopped.")
                break
            
            else:
                break
        
        if not command:
            break

    conn.close()
    print(f"Current Connections: {threading.active_count() - 2 if threading.active_count() > 1 else threading.active_count() - 1}")
                

def main():
    print("Server is starting...")
    server.bind((host, port))
    server.listen()
    print(f"Server listening on {host}:{port}")
    
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=clientConnection, args=(conn, addr))
        thread.start()
        print(f"Current Connections: {threading.active_count() - 1}")

if __name__ == "__main__":
    main()

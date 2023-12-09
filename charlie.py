import socket

name = "Charlie"
syntax = ""

Running = True

joined = None
registered = None

fileList = []
cmdList = ["join <ip_address> <port>", "leave", "register <username>", "store <filename>", "dir", "get <filename>", "?"]

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def join(parsed):
    global joined
    if parsed[1] == "127.0.0.1" and parsed[2] == "12345":
        client.connect(("127.0.0.1", 12345))
        print(f"Connection to the Local File Exchange Server is successful.")
        joined = True
    else:
        print("Connection to the Server has failed! Please check IP Address and Port Number.")

def leave():
    print("Connection closed. Thank you for using the Local File Exchange System!")
    client.close()
    
def register(parsed):
    global registered
    name = parsed[1]
    client.send(name.encode())
    
    if client.recv(1024).decode() == "Registered!":
        print("Registered")
        registered = True
    else:
        print("Not registered")
    
def store(parsed):
    fileName = parsed[1]
    with open(fileName, 'w'):
        pass
    client.send(fileName.encode())
    fileList.append(fileName)
    
def dir():
    print("File directory:")
    while True:
        response = client.recv(1024).decode()
        print("\n")
        if response == "Directory done!":
            break
        elif not response:
            print("The server connection is closed.")
            break
        print(response)
        
def get(parsed):
    fileName = parsed[1]
    client.send(fileName.encode())
    
    fileRequest = client.recv(1024).decode()
    
    if fileRequest in fileList:
        print("The requested file is already at the user's folder, but it has been downloaded anyway.")
    elif fileRequest == "FDNE":
        print("The requested file does not exist!")
    else:
        fileList.append(fileRequest)

def question():
    print("List of commands:")
    for cmd in cmdList:
        print(f"/{cmd}")

def main():
    global Running, registered, joined
    
    print("Welcome to the Local File Exchange System.")
    
    while Running:
        print("----------------------")
        syntax = input("Enter a command: ")
        if syntax[0] != '/' :
            print("Command parameters do not match or is not allowed.")
        else:
            parsedInput = syntax.split()
            command = parsedInput[0][1:]
            print(f"Input is {parsedInput}")
            print(f"Command: {command}")
            
            if command == "join":
                if len(parsedInput) != 3:
                    print("Input syntax is invalid.")
                elif joined:
                    print("User is already in the server.")
                else:
                    join(parsedInput)
            
            elif command == "register":
                if len(parsedInput) != 2:
                    print("Input syntax is wrong!")
                elif registered:
                    print("User is already registered.")
                elif not joined:
                    print("User has not connected to any server.")
                else:
                    client.send(command.encode())
                    register(parsedInput)
                    
            elif command == "leave":
                if not joined:
                    print("User has not connected to the server yet.")
                else:
                    client.send(command.encode())
                    leave()
                    print("Exiting client application...")
                    Running = False
                
            elif command == "dir":
                if not joined:
                    print("User has not connected to the server yet.")
                elif not registered:
                    print("User has not registered to the server yet.")
                else:
                    client.send(command.encode())
                    dir()
                
            elif command == "?":
                question()
                
            elif command == "store":
                if len(parsedInput) != 2:
                    print("Input syntax is wrong!")
                elif not joined:
                    print("User has not connected to the server yet.")
                elif not registered:
                    print("User has not registered to the server yet.")
                else:
                    client.send(command.encode())
                    store(parsedInput)
                
            elif command == "get":
                if len(parsedInput) != 2:
                    print("Input syntax is wrong!")
                elif not joined:
                    print("User has not connected to the server yet.")
                elif not registered:
                    print("User has not registered to the server yet.")
                else:
                    client.send(command.encode())
                    get(parsedInput)
                    
            elif command == "shutdown":
                client.send(command.encode())
                    
            else:
                print("Command not found.")
        
if __name__ == "__main__":
    main()
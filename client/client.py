import socket 

sck = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sck.connect(('172.21.72.112', 8887))

print("Connected")

while True : 
    to_send = input("What do you want to send : ?")

    if(to_send == ""):
        break
    to_send += "\0"
    sck.send(to_send.encode())
    print("ok sended well !")

print("Done")
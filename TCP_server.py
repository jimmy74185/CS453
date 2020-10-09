import sys
from socket import *
import time
import threading

def main():
    #Take arguments from command lines
    Server_IP = sys.argv[1]
    Server_Port = sys.argv[2]
    port = int(Server_Port)
    vistorList = dict() #Stores the ConnectionID and Time

    server = socket(AF_INET, SOCK_STREAM) #Initial Socket interface.
    server.bind(('',port))
    server.listen(1)

    server.settimeout(300)

    print("The server is ready")

    while True:
        try:

            connectionSocket, clientAddress = server.accept()
            received = connectionSocket.recv(2048)
            visitID = received.decode('gbk').split()[1]
            if visitID in vistorList.keys(): #If connectionID exist 
                if ( time.time() - (vistorList[visitID]) ) >= 60: #Check ConntectID exist Time >60 or not
                    vistorList[visitID] = time.time()
                    msg = "OK "+visitID+" "+str(clientAddress[0])+" "+str(clientAddress[1])
                else:    # If not reply with RESET message
                    msg = "RESET "+str(visitID)

            else:
                vistorList[visitID] = time.time() #Record the time when connected
                msg = "OK "+visitID+" "+str(clientAddress[0])+" "+str(clientAddress[1])
            #↓ reply message to client
            connectionSocket.send(msg.encode())
            connectionSocket.close()
        except: #TIME OUT HANDLE 5MINUTES
            server.close()
            print("Server time out after 5mins")
            break
        else:
            continue

if __name__ == "__main__":
    main()
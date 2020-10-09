import sys
from socket import *
import time
def main():
    string = sys.argv[1]
    ip = sys.argv[2]            # Received input from command
    port = int(sys.argv[3])     # Turn the string into int for port number
    cID = sys.argv[4]
    
    cSocket = socket(AF_INET, SOCK_DGRAM)       #Making socket interface

    msg = string+" "+cID
    cSocket.sendto(msg.encode(), (ip, port))    #send message to the server in
    count = 0                                   # "StringTypedIn ConnectionID" format

    cSocket.settimeout(60)                      #Timeout for 60secs
    try:
        while count <= 3 :                     # Maximum 3 tries
            received, serverAddress = cSocket.recvfrom(2048)
            recvMsg = received.decode()

            if recvMsg.split()[0] == "OK":
                print("Connection established "+recvMsg[2:])
                break

            if recvMsg.split()[0] == "RESET":       
            #If received RESET, ask for new Connection ID and send the message again.
                if count == 2 : 
                    print("Connection Failure")
                    break
                print("Connection Error "+recvMsg.split()[1])
                cID = input("New Connection ID:")
                msg = string+" "+cID
                cSocket.sendto(msg.encode(), (ip, port))
            count+=1

    except:
        print("Time Out")

    cSocket.close()

if __name__ == "__main__":
    main()
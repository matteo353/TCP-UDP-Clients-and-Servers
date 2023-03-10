import datetime
from socket import *
import sys


def main():

    message = sys.argv[1]
    server_IP = sys.argv[2]
    server_port = int(sys.argv[3])
    connectionID = sys.argv[4]

    address = (server_IP, server_port)


    tries = 0

    while tries < 3:

        client_socket = socket(AF_INET, SOCK_STREAM)


        client_socket.settimeout(15)
        final_message = message + ' ' + connectionID

        try:
            client_socket.connect(address)
            client_socket.send(final_message.encode())

            # script is not receiving the response
            response = client_socket.recv(1024)
            words = response.decode().split()

            if 'OK' == words[0]:
                # response = “OK ConnectionID Client_IP Client_Port”

                # PRINT “Connection established 2876 192.168.0.10 12345 on 2023-01-16 06:06:06.123456”
                print('Connection established ' + words[1] + ' ' + words[2] + ' ' + words[3] + ' on ' + str(datetime.datetime.now()))
                client_socket.close()
                return

            elif 'RESET' == words[0]:
                print('Connection Error ' + connectionID + ' on ' + str(datetime.datetime.now()))
                connectionID = input('Enter new connection id: ')
                tries += 1
                client_socket.close()
                continue

        except Exception as e:
            # response =  “RESET ConnectionID”.
            # PRINT “Connection Error 2678 on 2023-01-16 06:06:06.123456”
            print('Connection Failure on ' + str(datetime.datetime.now()))
            client_socket.close()
            return
    return


if __name__ == '__main__':
    main()





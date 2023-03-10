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

    # is the timeout in the while loop or outside of it
    client_socket = socket(AF_INET, SOCK_DGRAM)

    while (tries < 3):
        client_socket.settimeout(15)

        final_message = message + ' ' + connectionID

        try:
            client_socket.sendto(final_message.encode(), address)
            response = client_socket.recv(2048)

            words = response.decode().split()

            if 'OK' == words[0]:
                # response = “OK ConnectionID Client_IP Client_Port”

                # PRINT “Connection established 2876 192.168.0.10 12345 on 2023-01-16 06:06:06.123456”
                print('Connection established ' + words[1] + ' ' + words[2] + ' ' + words[3] + ' on ' + str(datetime.datetime.now()))
                client_socket.close()
                return
            elif 'RESET' == words[0]:
                raise Exception()
                # throw an exception for a reset so that the except block will hit it

        #

        except Exception as e:
            # response =  “RESET ConnectionID”.
            # PRINT “Connection Error 2678 on 2023-01-16 06:06:06.123456”
            if tries < 2:
                print('Connection Error ' + connectionID + ' on ' + str(datetime.datetime.now()))
                connectionID = input('Enter new connection id: ')
                tries += 1
                continue
            else:
                break

    print('Connection Failure on ' + str(datetime.datetime.now()))
    client_socket.close()
    return


if __name__ == '__main__':
    main()
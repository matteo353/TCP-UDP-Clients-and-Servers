from socket import *
import sys
import time


def main():

    server_ip = sys.argv[1]
    server_port = int(sys.argv[2])
    address = (server_ip, server_port)

    connection_ids = {}

    server_socket = socket(AF_INET, SOCK_STREAM)
    server_socket.bind(address)
    server_socket.listen(1)

    while True:
        connection_socket, client_address = server_socket.accept()
        try:
            server_socket.settimeout(120)
            message, client_address = connection_socket.recvfrom(2048)
            words = message.decode().split()
            current_id = words[1]

            for key in connection_ids:
                if time.time() - connection_ids[key] > 30:
                    del connection_ids[key]

            if current_id not in connection_ids:
                connection_ids[current_id] = time.time()
                message = 'OK ' + str(current_id) + ' ' + str(server_ip) + ' ' + str(server_port)
                connection_socket.send(message.encode())
                continue

            elif current_id in connection_ids:
                message = 'RESET ' + current_id
                connection_socket.send(message.encode())
                connection_socket.close()
                continue

        except Exception as e:
            server_socket.close()
            return


if __name__ == '__main__':
    main()










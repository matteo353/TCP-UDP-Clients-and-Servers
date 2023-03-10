from socket import *
import sys
import time


def main():

    server_ip = sys.argv[1]
    server_port = int(sys.argv[2])
    address = (server_ip, server_port)

    connection_ids = {}

    server_socket = socket(AF_INET, SOCK_DGRAM)
    server_socket.bind(address)
    # when do you set the timeout

    while True:
        print('connection IDs: ' + str(connection_ids))
        try:
            server_socket.settimeout(120)
            print('waiting for connection...')
            message, client_address = server_socket.recvfrom(2048)
            words = message.decode().split()
            current_id = words[1]
            # how to handle the current id timing out after 30 seconds

            for key in connection_ids:
                if time.time() - connection_ids[key] > 30:
                    del connection_ids[key]
                    # remove id

            if current_id not in connection_ids:
                connection_ids[current_id] = time.time()
                message = 'OK ' + str(current_id) + ' ' + str(server_ip) + ' ' + str(server_port)
                server_socket.sendto(message.encode(), client_address)
                continue

            elif current_id in connection_ids:
                message = 'RESET ' + current_id
                server_socket.sendto(message.encode(), client_address)
                continue

        # if there have been no requests in 2 minutes
        except Exception:
            server_socket.close()
            return


if __name__ == '__main__':
    main()

import socket

def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(("127.0.0.1", 9999))

    try:
        for i in range(10):
            message = "Message {}".format(i + 1)
            client_socket.send(message)
            response = client_socket.recv(1024)
            print "Server response:", response
    except socket.error as e:
        print "Socket error:", e
    finally:
        client_socket.close()

if __name__ == "__main__":
    start_client()

import socket
import threading
import time

# Rate Limiter
class RateLimiter(object):
    def __init__(self, max_requests, time_window):
        self.max_requests = max_requests
        self.time_window = time_window
        self.client_data = {}

    def is_allowed(self, client_ip):
        current_time = time.time()
        if client_ip not in self.client_data:
            self.client_data[client_ip] = []
        self.client_data[client_ip] = [
            timestamp for timestamp in self.client_data[client_ip]
            if current_time - timestamp <= self.time_window
        ]
        if len(self.client_data[client_ip]) < self.max_requests:
            self.client_data[client_ip].append(current_time)
            return True
        return False

def handle_client(client_socket, client_address, rate_limiter):
    client_ip = client_address[0]
    print "Connection from:", client_ip

    while True:
        try:
            data = client_socket.recv(1024)
            if not data:
                break
            if rate_limiter.is_allowed(client_ip):
                response = "Request accepted: {}".format(data)
            else:
                response = "Rate limit exceeded. Try again later."
            client_socket.send(response)
        except socket.error:
            break

    print "Connection closed:", client_ip
    client_socket.close()

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("0.0.0.0", 9999))
    server_socket.listen(5)
    print "Server started on port 9999..."

    rate_limiter = RateLimiter(max_requests=5, time_window=10)

    while True:
        client_socket, client_address = server_socket.accept()
        client_handler = threading.Thread(
            target=handle_client,
            args=(client_socket, client_address, rate_limiter)
        )
        client_handler.start()

if __name__ == "__main__":
    start_server()

#How It Works:

Server:
* The RateLimiter class keeps track of the timestamps of requests from each client IP.
* If a client's requests exceed the allowed limit within the time window, further requests are rejected.

Client:
* Sends a series of messages to the server.
* Prints the server's response for each message.

#Run Instructions:
* Start the server by running the server script.
* Run the client script to simulate requests.

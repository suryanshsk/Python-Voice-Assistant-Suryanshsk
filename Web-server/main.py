import socket
# import time

# Define the host and port
SERVER_HOST = '0.0.0.0'
SERVER_PORT = 8080

# ---------- CREATE SOCKET ----------
# The first step is to create and initialise our socket. What is a socket?
# A socket is an endpoint in a network communication system. They are 
# the most important tool in creating our own server as they allow for 
# data to be sent and received over the network. They facilitate the 
# connection between the client and the server and enable the server 
# to handle multiple client connections simultaneously. Without sockets, 
# the data communication needed for the operation of a server would not 
# be possible. 
# You might be thinking, what's http then? HTTP, short for Hyper Text Transfer Protocol,
# is the protocol that's being used when data is sent or received through 
# the sockets. Keep this in mind as it'll be useful when we write our own HTTP
# response.

# socket.socket() -> initializes a new socket.

# The first argument we want to pass in is AddressFamily. For this,
# we will pass in an IP.
# You might ask, what is an IP?
# Internet Protocol (IP) are rules for routing or sending packets of 
# data across networks between devices. Basically, when data or information 
# travels over the Internet or web, it travels in small packets. 
# IP addresses ensure that devices like computers, servers etc.
# route those data packets to the correct place.

# socket.AF_INET specifies the Internet Protocol v4 addresses, the first 
# stable version of IP and also the most used protocol. You could use v6
# addresses, the newer version if you want. If you're wondering the main
# reason why ipv6 came out, it is because ipv4 could generate 
# around 4 billion addresses and the number of devices were exceeding.
# ipv6 supports around three hundred forty quindecillion addresses.
# Ofcourse, there are other improvements in performance but the number
# of addresses supported were the biggest problem that led to ipv6.

# socket.SOCK_STREAM means it is a TCP socket. TCP establishes 
# a connection between the sender and receiver and ensures that the 
# data, once it arrives, is complete, in order, and error-free.
# This connection is established using a handshake process in 3 steps (open up the image):
# 1. SYN (Synchronize): The client wants to establish a connection with 
# the server, so it sends a packet with the SYN (synchronize) flag set 
# to the server. This packet includes a sequence number, which is a 
# random number that initiates the sequence numbers for the data 
# packets that the client will send.
# 2. SYN-ACK (Synchronize-Acknowledgment): Upon receiving the SYN packet, 
# the server responds with a SYN-ACK packet. This packet acknowledges 
# the client's SYN packet (using the ACK flag) and includes the 
# server's own sequence number for the data packets it will send 
# to the client.
# 3. ACK (Acknowledgment): The client receives the server's SYN-ACK
# packet and responds with an ACK packet. This packet acknowledges 
# the server's SYN packet. At this point, the handshake is complete, 
# and both the client and server have established a reliable connection. 
# They can now start exchanging data. 
# If you have difficulty understanding this process, think of it this way - someone knocks at your door, 
# you open the door, then they say HI and your communication begins. 

# Instead of using SOCK_STREAM, you can use SOCK_DGRAM which specifies
# socket to use the UDP socket.
# UDP stands for User Datagram Protocol. UDP sends packets, 
# called datagrams, directly to the recipient without verifying 
# whether the recipient is ready to receive or not.
# So, at first glance UDP and TCP might seem like the same thing
# but they're actually quite different. 
# TCP ensures reliable transmission through error checking, 
# retransmissions when the packets are corrupted and congestion 
# control to reduce traffic load, meaning if the network condition
# is bad, it will alter the rate of transfer of data. Because of 
# this, TCP is used where reliability and data integrity are 
# critical, such as web browsing (HTTP/HTTPS) and email (SMTP, IMAP/POP3). 
# UDP doesn’t do all of this. It does not establish a connection/handshake before sending data. 
# It sends packets without verifying whether the recipient is ready to receive. 
# The benefit of this is that, UDP is faster than TCP as it doesn’t have
# to do error checking. The tradeoff is there’s no guarantee that the packets 
# will arrive in order, or in fact even arrive. This is why UDP is 
# generally used in applications such as live video or audio streaming, 
# online games, and broadcasting services.
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# server_socket.setblocking(False)
# After creating the socket, we can add optional settings to change
# the default behaviour of sockets.
# the first thing setsockopt takes in is -> level, meaning 
# the protocol level for which the configuration is happening in.
# For socket-level options, use socket.SOL_SOCKET. For TCP options, 
# can use socket.IPPROTO_TCP
# Next, we need to pass in the option name, meaning the feature we
# need to enable. We will use SO_REUSEADDR. SO stands for
# socket and REUSEADDR means Reuseaddress. This specific option tells the 
# kernel to allow this endpoint (IP address and port) to be 
# reused immediately after the socket is closed. Normally, there is 
# a delay before an endpoint can be reused, to ensure that any 
# delayed packets in the network are not mistakenly delivered to 
# the wrong application.
# finally, we pass in the value which is usually either 1 or 0; 1
# means on and 0 means off.
# Simply, this line allows the server socket to reuse a 
# local address immediately after the socket is closed, 
# instead of waiting for the default timeout.
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Till now, with our 2 lines, great progress btw, we have created
# and initialised a socket along with an option to improve
# performance. Next, we need to connect, or more specifically bind 
# our socket to our computer to tell it where our server should listen 
# for incoming network requests. This is done using the IP Address
# and port. What is an IP Address? Just a bunch of unique numbers 
# and letters that identifies and locates a device on a network.
# We can access each and every website through an IP address,
# for example google website can be reached by typing 142.250.189.206 (show it)
# DNS or the Domain Name System is used to map a proper string to this
# IP Address so that we, humans type only google.com to reach the website
# instead of a confusing number.
# Now what is a port? Basically, port helps differentiate 
# between multiple services running on the same computer. 
# It allows computers and servers to route the incoming network 
# traffic to the correct application or service. 
# For example, web servers usually listen on port 80 for HTTP traffic 
# and port 443 for HTTPS traffic. By using different port numbers, 
# a single server can host multiple services, each listening on its
# unique port, ensuring that all the http calls go to port 80 and
# https go to 443. Think of this way - If an IP address is like a 
# company's phone number, then a port number is like an extension.
# Since, we want this server to be accessible from any device, we can
# pass in 0.0.0.0. If you only want this computer to access the
# server, you can pass 127.0.0.1.
# For port, you can pass in any number in the range 0-65535 but remember, that Ports 
# 0-1023 are reserved for the operating system's use so don't use that.
# You won't get any error but your web server will not show up.
# I'll pass 8080 because it is similar to 80 and as i said 
# before, web servers typically listen on port 80 for HTTP request
server_socket.bind((SERVER_HOST, SERVER_PORT))

# The final step in socket creation is making socket listen to 
# the incoming connection requests using server_socket.listen().
# How this works internally is that the operating system takes
# note that this particular socket is now ready to accept incoming 
# connections. It creates a queue for these connections, handling 
# the initial handshake required. To specify, the size of this
# queue, we can pass the backlog value to the listen function
# To be clearer, the backlog parameter tells the maximum 
# number of fully established connections that can wait in the queue.
# But wait, what if the queue is full, what will happen to the new connection request?
# The new connection will either be refused or ignored (depending on the operating 
# system and its configuration), causing the client to retry later.
server_socket.listen(5)

print(f'Listening on port {SERVER_PORT} ...') # if all goes well, we will print that we have started listening on a specific port

while True: # so that we continuously keep listening to new client connections
    
    # Now, remember that our new connections get piled up in the queue? 
    # How do I take the front element of that queue? Using server_socket.accept()
    # This will give us a tuple with the socket and address of the client.
    # The socket object is specifically for communication with the newly accepted connection, 
    # don't confuse it with the server socket. The listening socket will continue to 
    # listen for other incoming connections, while the new socket is used to send 
    # and receive data on the connection just accepted. The address we receive 
    # is again a tuple of (host, port), where the host client's IP address
    # and port is the port used by client's machine for the connection.
    # By the way, what do you think will happen if there are no connections in the queue?
    # accept() will block the code until a connection becomes available (unless the socket 
    # is configured to be non-blocking). You can set it to be non blocking by doing
    # server_socket.setblocking(False) on top of the file (do it, get an error)
    # The error comes in because we told the socket to never block the execution
    # and when it tried to get a connection request from queue, the queue was empty
    # To resolve this, we can use the try..except block and catch the BlockingIOError
    # An important thing to mention is that BlockingIOError isn't just given
    # when we call the accept function, it can also be thrown when we send or
    # receive the HTTP request.
    # I'll be using the blocked version for the rest of the tutorial but
    # feel free to follow along with non blocked version.
    
    # try:
    print('ran') # <----- add print statement to explain the blocking
    client_socket, client_address = server_socket.accept()
    print('ran2')  # <----- add print statement to explain the blocking
    # except BlockingIOError:
    #     time.sleep(1)
    #     continue

    # Next, we need to get the data or in our case, the http request from the client so that we can give
    # an appropriate response. To do that, we use the client_socket and call
    # the recv function on it. We can specify the maximum amount of data 
    # we can handle in bytes. The most widely used networks limit packets 
    # to approximately 1500 bytes so we can pass in something like that.
    # The recv function returns bytes, obviously something we can't understand
    # So, we can convert it to string using the decode function.
    request = client_socket.recv(1500).decode()
    print(request)

    # This request is composed of a request line, headers, and 
    # an optional message body.
    
    # The first line of the http request is the request line.
    # It contains 3 elements - the http method, in our case it is 
    # GET but it can also be POST, UPDATE, DELETE, HEAD & OPTIONS.
    # GET, as the name suggests, tells/implies that some 
    # resource should be fetched. POST suggests that some data is 
    # created and pushed to the server. UPDATE and DELETE mean what
    # the name suggests. HEAD is similar to the **`GET`** method, 
    # except that it requests the server to respond with the headers 
    # only and not the actual body of the response. Where is that useful?
    # If a URL produces a large download, a `HEAD` request could read its 
    # Content-Length header to check the filesize without actually downloading the 
    # file. OPTIONS list out the HTTP methods and other options supported by 
    # a web server without performing any action or transferring a 
    # resource's data. The next part of the first line is usually 
    # the URL but in our case, the path is mentioned, meaning what route of the 
    # site is called. For example, if I go to YouTube.com/@RivaanRanawat, /@RivaanRanawat 
    # is the path. So, in our case since we just passed localhost:8080, it went 
    # to /, the default home path for most websites. I’m not going into 
    # much detail for this, you can look at this structure to understand more 
    # about URL if you want to. (insert image)

    # The final part of the first line is the HTTP version that was used to send 
    # this request. It is 1.1 but there are various versions of http - 0.9, the 
    # first official version, 1.0, 1.1, 2 and 3. This versioning might 
    # not seem important but it is actually pretty important! The http 
    # version used here determines the structure of the rest of this 
    # http request. In version 0.9, request only specified the first 
    # two parts of the first line - http method and the path. What about 
    # the version? It was the first version so ofcourse the concept of http 
    # versions didn’t exist back then. The response was simply an HTML 
    # file, no other type of file or message could be sent. In version 
    # 1.0, version was added to the first line, headers were attached 
    # in both requests and responses, more about that in some time. 
    # Things like status code and the ability to send files other than 
    # just HTML were also added to the response. The biggest problem with 
    # version 1.0 was Interoperability, meaning different browsers and
    # servers communicating with each other. Why did this issue exist? 
    # That’s because many people tried to improve the 1.0 version by 
    # adding new features, that’s good but there wasn't a good way to
    # make sure all browsers and servers understood these new features. 
    # Imagine the issue if I talk to you in English and suddenly say 
    # some important information in Hindi. All of this was fixed in 
    # the 1.1 version, the first standardised protocol. Along with 
    # this, multiple new things were added like cache control, pipelining
    # meaning the ability to send a second request before the first one 
    # is completed. In prior versions, a new TCP connection was created 
    # for each http call. As you can imagine, this was inefficient as a 
    # web page generally required multiple resources such as images, 
    # scripts, and stylesheets. The overhead of establishing and tearing 
    # down TCP connections for each resource increased the page load 
    # times and put more load on the servers. In 1.1, a connection can 
    # be/is reused. We will understand how this connection can be reused
    # in a couple of minutes. HTTP 2 was introduced 15 years later which 
    # focused on improving the performance. HTTP 3 was soon introduced 
    # which focused on changing TCP to QUIC, short for Quick UDP Internet 
    # Connection. You can think of QUIC as a protocol built on top of 
    # UDP providing the reliability and ordering of TCP but with reduced 
    # latency and improved performance. How does this happen? **Remember, 
    # TCP** requires a three-way handshake to establish a connection? This
    # adds latency. Additionally, if encryption is done (as in HTTPS), 
    # there is an additional handshake process. **QUIC** combines the 
    # connection and security handshakes, reducing the initial setup time.
    # How is performance improved? We know **TCP** connections are identified 
    # by IP addresses and port numbers, we did that in our code too. But 
    # what if a user's IP address changes (like when switching from Wi-Fi
    # to mobile data)? Then the TCP connection must be reestablished. 
    # In QUIC, connections are identified by connection IDs rather than 
    # IP addresses so it doesn’t matter if the network or IP changes.
    # All this information is good but the main question is Why are we 
    # getting HTTP 1.1 request, not HTTP 2 or 3? Simple, we have created a
    # basic server that depends on TCP because of which HTTP 3 isn’t used. 
    # In order to run HTTP 3 server, we need to depend on QUIC. To use 
    # HTTP 2, we need to implement some other protocols that allow 
    # features like multiplexing, the ability to run multiple requests 
    # at once. The interesting thing we notice here is the ability of 
    # browsers to use http 1.1 to send a request if the server it is 
    # interacting with, doesn’t use http 2/3. Alright, enough about 
    # the first line, I promise we’ll go over the next lines quicker. 
    # To remind you, the lines and structure we will see next are 
    # only present in HTTP 1.1.

    # The next line, Host: [localhost:8080](http://localhost:8080)
    # specifies the domain name and if you use IP address, that along 
    # with the port of the server from which the resource was requested.
    # The next line, Connection: keep-alive tells the server that the 
    # client wants to keep the connection open for further requests 
    # rather than closing it right after this request is fulfilled.
    # Remember, I had told in 1.1, a connection can be/is reused.
    # If this line says keep-alive, the connection is reused
    # User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)
    # AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36: 
    # This line provides detailed information about the client's browser,
    # operating system, and rendering engine.
    # sec-ch-ua-platform: "macOS": This line specifies the operating 
    # system the browser is running on.
    # Accept: image/avif,image/webp,image/apng,image/svg+xml,image/,*/;q=0.8: 
    # This header specifies the media types that the client can process,
    # prioritized from left to right. The **`q`** parameter indicates 
    # the quality factor for each type.
    # Sec-Fetch-Site: same-origin: lets us know if the request is being 
    # made from the same origin as the destination.
    # Sec-Fetch-Mode: no-cors: Specifies the mode for how the request 
    # should be made regarding CORS (Cross-Origin Resource Sharing) 
    # policies. What is CORS? A security mechanism implemented by 
    # web browsers to protect users from certain types of cyber attacks, 
    # like cross-site request forgery. What on earth does that mean? 
    # Let’s use an analogy. 
    # Imagine you have a blog hosted at `www.myawesomeblog.com`, and 
    # you want to embed a YouTube video within one of your blog posts.
    # The same-origin policy is a security measure implemented in
    # web browsers. It ensures that scripts running on pages from
    # your blog can only request data from `www.myawesomeblog.com`
    # and not from other sites directly, like `www.youtube.com`. 
    # This rule helps protect your blog's visitors from potential 
    # malicious scripts and data theft. What do you do in that case, 
    # you still want to display YouTube videos? Enter CORS 
    # (Cross-Origin Resource Sharing), a mechanism that allows 
    # restricted resources on a web page to be requested from another 
    # domain outside the domain from which the first resource was served. 
    # So, if YouTube sets up its servers to include specific CORS headers
    # in responses, it can allow your blog to embed its videos. 
    # Essentially, YouTube is telling the browser, "It's safe to 
    # display our videos on `www.myawesomeblog.com`". So, 
    # behind the scenes, when you embed a YouTube video on your blog, your 
    # blog's page makes a request to `www.youtube.com` to fetch the video. 
    # YouTube's servers respond with the video along with headers that say, 
    # "We permit `www.myawesomeblog.com` to display this content." The 
    # browser checks these permissions (the CORS headers) and decides 
    # it's okay to show the YouTube video on your blog. Understood, 
    # but what is the no-cors that's mentioned? The "no-cors" mode is 
    # generally used when you don't need to read the content from 
    # the other site but just need to include it or refer to it.
    # Sec-Fetch-Dest: navigate - tells the type of content the client 
    # expects to receive as a response - in our case, the request is 
    # to navigate the browser to a new document.
    # Referer: http://localhost:8080/ - tells the address of the web 
    # page that initiated the request. 
    # Accept-Encoding: gzip, deflate, br, zstd - Tells the server 
    # which encoding algorithms the client can understand for 
    # compressing the response. This supports gzip, deflate, 
    # Brotli (br), and Zstandard (zstd).
    # Accept-Language: en-IN,en-GB;q=0.9,en-US;q=0.8,en;q=0.7: 
    # Specifies the client's preferred languages, ordered by preference
    # using **`q`** values. In my case, English as used in India is
    # preferred, followed by British English, American English, and
    # then any other type of English.
    # All of these were headers.

    # The third thing in this request is an optional message body. 
    # You might wonder there's no optional message body? And that's
    # right. No message body is present in GET requests. However,
    # if it was a post request, we would have a message body.
    # Let me show it to you! (Notice one line is left between
    # headers and the message body)

    # That’s all about HTTP request format! This was very important
    # to understand as based on the request, we can frame our response
    # and this is going to be a piece of cake!

    # Returns HTTP response
    headers = request.split('\n')
    first_header_components = headers[0].split()

    http_method = first_header_components[0]
    path = first_header_components[1]

    if http_method == 'GET':
        if path == '/':
            fin = open('index.html')
        elif path == '/book':
            fin = open('book.json')
        else:
            # handle the edge case
            pass
        
        content = fin.read()
        fin.close()
        response = 'HTTP/1.1 200 OK\n\n' + content
    else:
        response = 'HTTP/1.1 405 Method Not Allowed\n\nAllow: GET'

    # You have the response created, you only want to send it back to
    # the client. To do that, there are multiple functions on client_socket
    # We'll be using sendall so that all the data is sent to the client.
    # sendall accepts ReadableBuffer but we have a response in string format
    # what do we do? we will encode the response so that it's converted
    # into bytes.
    # We could have also used the send function but the problem with it
    # is that there's no guarantee send() will send all the data in one
    # call, especially if the message is large or the network is busy.
    # sendall on the other hand continues sending data from the buffer 
    # until either all data has been sent or an error occurs. 
    # basically, sendall handles the re-sending of data that was not 
    # successfully sent in one go.
    client_socket.sendall(response.encode())

    # Close connection - show what happens if the client socket
    # is not closed.
    client_socket.close()

# Close socket
server_socket.close()
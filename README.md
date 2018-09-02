# p2p-chat
Version: 1.0
Author: Rylov Georgy

# Description
Decentralized chat, with 4-connectivity
* you can change the nickname at any time
* send multi-line messages 
* send private messages 
* encryption.

# Requirements
* Python 3.7
* PyQt5

# Directory tree
```
├── main.py
├── README.md
├── logs
|   └── ...
├── source
|   ├── chat_window.py
|   ├── connection_window
|   ├── server.py
|   ├── peermanager.py
|   ├── client.py
|   ├── client_info.py
|   ├── file_worker.py
|   ├── message.py
|   └── cryptographer.py
└── tests
    ├── server_tests.py
    ├── peer_manager_tests.py
    ├── client_tests.py
    └── client_info_tests.py
    
__Summary__: 3 directories, 15 files
```
### logs 
Here are stored the logs of chat

### source
```chat_window.py``` ─ Main app window\
```connection_window.py```\
```server.py``` ─ Receives messages from other chat participants and decides on further forwarding\
```peermanager.py``` ─ Keep number of connections equal to 4(if it is possible)\
```client.py``` ─ Send messages to chat\
```client_info.py``` ─ Info about client\
```file_worker.py```─ Keep files\
```message.py```\
```cryptographer.py``` ─ Encode and decode messages

# Run by terminal
./main.py

# Implementation details
First, the connection Manager sets the required number of connections, and then
the server is responsible for communication with all clients. Clients are responsible for sending messages.

# How to use
1. Enter the ip address and port you want to connect to
(Right now it works only in the local network, maybe once I'll learn how to remap ip addresess to router by NAT and it will work with Internet)
also ip field can contain wrong string, it will be ignored and your app will wait when someone connect to you
2. Enter a non-empty nick
3. Press ok
4. Start to chat(also you can change your nickname)

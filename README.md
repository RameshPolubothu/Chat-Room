# Chat-Room
Client-Server Secure Communication and Video Streaming System

Overview

This project implements a socket programming system where a server manages client connections, 
maintains client information securely, 
and facilitates secure communication and video streaming among clients

Features

Client Connection Management:

Clients can connect to the server, providing their name and generated public key.
The server maintains a dictionary mapping client names to their public keys and broadcasts this information to all connected clients.
Clients can disconnect by sending a 'QUIT' message to the server, which removes their entry from the dictionary and notifies other clients.


Secure Communication Management:

Clients can securely communicate with each other using public-key cryptography.
The server broadcasts encrypted messages among clients, ensuring only the intended recipient can decrypt and read the message.


Video Streaming Management:

The server streams video files to clients without saving them locally.
Clients can request a list of available videos and play a selected video file


used libraries

OpenCV (for video streaming)
PyCryptoDome (for RSA encryption)

Usage
-----------------------------------
Start the server:
python 210010039_server.py

Start the client(s):
python 210010039_client.py

---------------------------------
I have implemented the steps as asked in the problem statement.

client side 
-----------
1)first the name of the client will be asked.
Enter Your name:ramesh

2)The generated public will be sent to server and the dictionary named clientsdata will store 
the name and corresponding public key in the dictionary

3)This dictionary will be brodacasted to the every client in the connection.

4)I have provided the following options for the client as asked in problem statement

Options:

1. To Know Available clients
2. Send Message
3. Video Playback
4. Quit

when the client type 1 he will be knowing the available clients

when the client type 2 he will be able to send messages to the available clients if he types wrong name 
then the he will asked to enter the name of reciever again.

when the client type 3 he will be given the list of possible videos 

video_1 video_2
Enter the video you want to watch:

if he types 1 the vedio 1 will be played and if he types 2 the video 2 will be played as asked in problem statement 1/3 part with different resolutions.

when the client type 4 he will removed from the list of dictionary clients data at the server and at client level now his name will not be present in the available clients.


There is one exception that when the vedio is playing if the other client try to join the chat this 
will cause thread error so please donot join when the vedio is being played after vedio completion 
the clients will be able to join the chat.

the format of videos are video_1_240p video_1_720p video_1_1080p

demo video link

https://drive.google.com/file/d/1ByKZ4qXtee7x4EPXhWmQhAmADQinKwxx/view?usp=drive_link

Thankyou

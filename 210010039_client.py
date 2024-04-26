import socket
import json
import cv2
import numpy as np
import threading
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
FORMAT = 'utf-8'
SERVER = socket.gethostbyname(socket.gethostname())
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((SERVER, 7777))
clientsdata={}
complete = False
name = input("Enter Your name:")
def generate_key_pair():
    key = RSA.generate(1024)
    return key.publickey(), key  

public_key, private_key = generate_key_pair()
public_key_str = public_key.export_key().decode()

def receive():
    global clientsdata
    try:
        while True:
            msg = client.recv(2048).decode(FORMAT)
            if not msg:
                break
            if msg=='NAME':
                client.send(name.encode(FORMAT))
            elif msg=='Enter the public key:':
                print("sending generated the public key:")
                client.send(public_key_str.encode(FORMAT))  
            elif msg[0]=='@':
                print('\n')
                print(msg)
                # print('\n')
            elif msg[0]=='{':
                json_data = json.loads(msg)
                clientsdata = json_data
            elif msg[0]=='#':
                parts = msg.split( )
                value = parts[1] if len(parts) >= 2 else None
                del clientsdata[value]
                print('\n')
                print(msg)
            elif msg=='.':
                data = client.recv(2048)
                decrypted_message = decrypt_message(data, private_key)
                if decrypted_message is not None:
                    decrypted_message_extracted=decrypted_message.decode()
                    name_extracted = decrypted_message_extracted.split('$')[0]
                    msg_extracted = decrypted_message_extracted.split('$')[1]
                    print("\nFrom:"+name_extracted)
                    print()
                    print("Received Message:", msg_extracted)   
            elif msg=='%':
                data = client.recv(4096).decode()
                receive_video(data)           
    except ConnectionAbortedError as e:
        print("Connection closed")

      
def receive_video(data):
    global complete
    print(data)
    user_video = input("Enter the video you want to watch: ")
    client.send(user_video.encode())
    response = client.recv(4096).decode()
    print(response)
    while True:
        frame_size_data = client.recv(16)
        if not frame_size_data:
            break
        frame_size = int(frame_size_data.strip())
        if frame_size == 0:
            break
        frame_data = b''
        while len(frame_data) < frame_size:
            remaining_bytes = frame_size - len(frame_data)
            frame_data += client.recv(remaining_bytes)
        frame_np = np.frombuffer(frame_data, dtype=np.uint8)
        frame = cv2.imdecode(frame_np, cv2.IMREAD_COLOR)
        frame = cv2.resize(frame, (1080, 720))
        cv2.imshow('Video Stream', frame)
        key = cv2.waitKey(1)
    cv2.destroyAllWindows()
    complete=True

def encrypt_message(public_key_str, message):
    public_key = RSA.import_key(public_key_str)
    cipher = PKCS1_OAEP.new(public_key)
    encrypted_message = cipher.encrypt(message)
    return encrypted_message    

def decrypt_message(encrypted_message, private_key):
    try:
        cipher = PKCS1_OAEP.new(private_key)
        decrypted_message = cipher.decrypt(encrypted_message)
        return decrypted_message
    except ValueError as e:
        return None

receive_thread = threading.Thread(target=receive)
receive_thread.start()

def start():
    global complete
    while True:
        print("\nOptions:\n")
        print("1. To Know Available clients")
        print("2. Send Message")
        print("3. Video Playback")
        print("4. Quit")
        choice = input("Enter your choice:\n")
        if choice == "1":
            print("Availble Clients:")
            for x in clientsdata:
                if x != name:
                    print(x)
        elif choice == "2":
            while True:
                receiver = input("Enter receiver name: ")
                if receiver not in clientsdata:
                    print("Error: Receiver not found. Please enter a valid receiver name.")
                else:
                    break  
            message = input("Enter your message: ")
            message = name+"$"+message
            message = message.encode()
            encrypted_message = encrypt_message(clientsdata[receiver], message)
            client.send("chat".encode())
            client.send(encrypted_message)
        elif choice == "3":
            client.send("VIDEO".encode())
            while not complete:
                pass
            complete = False
        elif choice == "4":
            client.send('QUIT'.encode())
            break
        else:
            print("Error: Invalid choice. Please enter 1, 2, 3, or 4.")
    client.close()

start()
import socket
import cv2
import threading
import json

SERVER=socket.gethostbyname(socket.gethostname())
myserver=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
myserver.bind((SERVER,7777))
clientsockets=[]    #to store the sockets.
clients={}          #to store socketnumber:name
clientsdata={}  
FORMAT= 'utf-8'
videos = ["video_1", "video_2"]

def handle_client(conn,addr,name,pk):
    clientsockets.append(conn)
    clients[addr[1]]=name
    clientsdata[name]=pk
    tempmsg1 = "@New client "+name+" joined."
    broadcast(tempmsg1,conn)
    json_data = json.dumps(clientsdata)        
    broadcast(json_data,None)
    while True:
        msg=conn.recv(2048).decode(FORMAT)
        if msg=='QUIT':
            v=clients[addr[1]]
            tempmsg2="#client "+v+" left."
            broadcast(tempmsg2,conn)
            del clients[addr[1]]
            del clientsdata[name]
            clientsockets.remove(conn)    
            print(f"[ACTIVE CONNECTIONS]: {len(clients)}") 
            conn.close()
            break
        elif msg == 'VIDEO':
            global videos
            video_list=""
            for mv in videos:
                video_list+=mv + " "
            print(video_list)
            set="%"
            set=set.encode()
            conn.send(set)
            send_video(conn,video_list)
        elif msg=='chat':
            msg1=conn.recv(2048)
            msgtwo=msg1
            broadcast_msg(msgtwo,conn)
            
def broadcast(msg,conn):
    for client_conn in clientsockets:
        if client_conn!=conn:
            client_conn.send(msg.encode(FORMAT))
def broadcast_msg(msg,conn):
     for client_conn in clientsockets:
        if client_conn!=conn:
            client_conn.send(".".encode(FORMAT))
            client_conn.send(msg)   
              
def send_video(conn, v_files):
    global videos
    conn.send(v_files.encode())
    v_num = int(conn.recv(4096).decode())
    conn.send(f"Playing Video: video_{v_num}.mp4".encode())
    try:
        v_files = [f"video_{v_num}_240p.mp4", f"video_{v_num}_720p.mp4", f"video_{v_num}_1080p.mp4"]
        frame_num = 0
        while frame_num < len(v_files):
            cap = cv2.VideoCapture(v_files[frame_num])
            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            segment_size = total_frames // 3
            start_frame = segment_size * frame_num
            end_frame = segment_size * (frame_num + 1)
            cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)
            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break
                current_frame = int(cap.get(cv2.CAP_PROP_POS_FRAMES))
                frame_data = cv2.imencode('.jpg', frame)[1].tobytes()
                conn.sendall((str(len(frame_data))).encode().ljust(16) + frame_data)
                if  current_frame >= end_frame:
                    frame_num += 1
                    if frame_num == 3:
                        conn.send(b'0')
                    break
            cap.release()
    except Exception as e:
        print(f"Error: {e}")
    
def start_server():
    myserver.listen()
    print(f"server is listening on {SERVER}")
    while True:
        conn,addr=myserver.accept()
        conn.send('NAME'.encode(FORMAT))
        name=conn.recv(2048).decode(FORMAT)
        conn.send('Enter the public key:'.encode(FORMAT))
        pk=conn.recv(2048).decode(FORMAT)
        thread=threading.Thread(target=handle_client,args=(conn,addr,name,pk))
        thread.start()
        print(f"[ACTIVE CONNECTIONS]{threading.active_count()-1}")
   
print("starting server...")
start_server()
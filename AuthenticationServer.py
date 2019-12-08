import socket
import sqlite3
from _thread import *
import hashlib
import time

def register_account(username,password_hashed,email):
    conn = sqlite3.connect('accounts.db')
    c = conn.cursor()
    #c.execute('''CREATE TABLE accounts(uid, username, password, email)''')
    try:
        c.execute("INSERT INTO accounts (username, password, email) VALUES (?,?,?)",
                  (username,password_hashed,email))
        conn.commit()
        conn.close()
        return "Registraion Successfull"
    except sqlite3.Error as e:
        return e

def authenticate_account(username,password_hashed):
    conn = sqlite3.connect('accounts.db')
    c = conn.cursor()
    record = c.execute("SELECT * FROM accounts WHERE username=?", (username,)).fetchone()
    stored_hash = record[2]
    if stored_hash == password_hashed:
        token = hashlib.sha256()
        token.update(record[1].encode('utf-8') + str(time.time()).encode('utf-8'))
        c.execute("UPDATE accounts SET token = ? WHERE uid=?", (token.hexdigest(), record[0]))
        conn.commit()
        return ["Authenticated",record[1],token.hexdigest()]
    else:
        return ["Authentication Failure",]

def threaded_client(conn,addr):
    conn.send(b'Connected to server')
    reply = ""
    while True:
        try:
            username = ""
            password_hashed = ""
            email = ""
            data = conn.recv(1024)
            reply = ""

            if not data:
                print(str(addr) + " Disconnected")
                break
            else:
                decoded_data = data.decode("utf-8").split(",")
                if decoded_data[0] == "registration":
                    reply = register_account(decoded_data[1], decoded_data[2], decoded_data[3])
                elif decoded_data[0] == "authentication":
                    # print(decoded_data[1],decoded_data[2])
                    reply = authenticate_account(decoded_data[1], decoded_data[2])
                else:
                    reply = "Unknown Action"
                conn.sendall(str(reply).encode("utf-8"))
        except:
            print("Lost Connection To " + str(addr))
            break
    conn.close()

HOST = "shittyrunescape.thomassomerville.com"
PORT = 1337
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    s.bind((HOST,PORT))
except socket.error as e:
    str(e)

s.listen()
print("Server Started")

while True:
    conn, addr = s.accept()
    print("Connected to:", addr)
    start_new_thread(threaded_client, (conn,addr))

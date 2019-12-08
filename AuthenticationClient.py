import socket
import hashlib
from network import Network
import ast

def send_data(data):
    HOST = "shittyrunescape.thomassomerville.com"
    PORT = 1337

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    response = s.recv(1024)
    #print('Received', repr(response))
    s.sendall(data.encode("utf-8"))
    response = s.recv(1024)
    #print('Received', response)
    return response

def register_accout(username, password_raw, email):
    username = username
    password_raw = password_raw
    email = email
    salt = "shittyrunescape"
    password_hashed = hashlib.sha512(password_raw.encode() + salt.encode()).hexdigest()
    data = "registration" + "," + username + "," + password_hashed + "," + email
    result = send_data(data)
    print(result)

def authenticate_account(username, password_raw):
    username = username
    password_raw = password_raw
    salt = "shittyrunescape"
    password_hashed = hashlib.sha512(password_raw.encode() + salt.encode()).hexdigest()
    data = "authentication" + "," + username + "," + password_hashed
    result = send_data(data).decode("utf-8")
    result = ast.literal_eval(result)
    if result[0] == "Authenticated":
        return result[0], result[1], result[2]
    elif result[0] == "Authentication Failure":
        return result
    else:
        return "Unkown Authentication Result: " + str(result)

#register_accout("Admin4","Admin","Admin@gmail.com")
#print(authenticate_account("Admin","Admin"))

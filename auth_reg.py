import socket
from cfg import address_to_server
def reg(username, password):

    message = "REG-" + username + "-" + password
    response = _server_request(message)
    return response

def auth(username, password):
    message = "AUTH-" + username + "-" + password
    response = _server_request(message)
    return response

def _server_request(message):


    BUFFER_SIZE = 1024
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(address_to_server)
        message = message.encode("utf-8")
        client.send(message)
        data = client.recv(BUFFER_SIZE)
        data = data.decode('utf-8')
        client.close()
        return data
    except socket.error:
        return "ERR"
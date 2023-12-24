from django.shortcuts import render
import socket
import json
import struct
from django.http import HttpResponse
import logging

logger = logging.getLogger(__name__)


# Create your views here.

def index(request):
    # Your view logic here
    return render(request, 'room_reservation_app/index.html')



def send_command_to_phase2_server(command, token):
    # Replace these with the actual Phase 2 server host and port
    phase2_server_host = 'localhost'
    phase2_server_port = 1423

    try:
        # Establish a socket connection to the Phase 2 server
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((phase2_server_host, phase2_server_port))

            logger.debug(f"Connected to {host} on port {port}")

            # Prepare the command dictionary, including the token
            command_dict = {"command": command, "token": token}
            command_json = json.dumps(command_dict)
            command_bytes = command_json.encode('utf-8')

            # Send the length of the command JSON string followed by the string itself
            sock.sendall(struct.pack('!I', len(command_bytes)))
            sock.sendall(command_bytes)

            # Wait for the response (first the length, then the message)
            raw_response_size = sock.recv(4)
            if not raw_response_size:
                return "Error: Server did not send a response size."

            response_size = struct.unpack('!I', raw_response_size)[0]
            response = sock.recv(response_size).decode('utf-8')

            return response
    except ConnectionError as e:
        return f"Connection error: {e}"
    except struct.error as e:
        return f"Pack/Unpack error: {e}"
    except Exception as e:
        return f"An error occurred: {e}"


def command_view(request):
    print("command view")
    if request.method == 'POST':
        command = request.POST.get('command')
        token = request.COOKIES.get('token')  # Retrieve the token from cookies
        print(token)
        
        # Send the command to the Phase 2 server and get the response
        response = send_command_to_phase2_server(command, token)
        
        # Render the response in your HTML template
        return render(request, 'index.html', {'response': response, 'token': token})
    else:
        # Handle GET request
        return render(request, 'index.html')
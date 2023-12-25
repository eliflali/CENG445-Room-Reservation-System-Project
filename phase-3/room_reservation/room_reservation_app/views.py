from django.shortcuts import render
import socket
import json
import struct
from django.http import JsonResponse
from django.http import HttpResponse
import logging

logger = logging.getLogger(__name__)

def index(request):
    return render(request, 'room_reservation_app/index.html')

def send_command_to_phase2_server(command, token):
    phase2_server_host = 'localhost'
    phase2_server_port = 1423

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((phase2_server_host, phase2_server_port))
            logger.debug(f"Connected to {phase2_server_host} on port {phase2_server_port}")

            command_dict = {"command": command, "token": token}
            command_json = json.dumps(command_dict)
            command_bytes = command_json.encode('utf-8')

            sock.sendall(struct.pack('!I', len(command_bytes)))
            sock.sendall(command_bytes)
            print(f"Command sent: {command_json}")

            raw_response_size = sock.recv(4)
            if not raw_response_size:
                print("Error: Server did not send a response size.")
                return "Error: Server did not send a response size."

            response_size = struct.unpack('!I', raw_response_size)[0]
            response = sock.recv(response_size).decode('utf-8')
            print(f"Response received: {response}")

            return response
    except ConnectionError as e:
        return f"Connection error: {e}"
    except struct.error as e:
        return f"Pack/Unpack error: {e}"
    except Exception as e:
        return f"An error occurred: {e}"

def command_view(request):
    if request.method == 'POST':
        command = request.POST.get('command')
        token = request.COOKIES.get('token')

        response_json_string = send_command_to_phase2_server(command, token)
        print(response_json_string)
        try:
            # Parse the JSON response
            response_data = json.loads(response_json_string)
        except json.JSONDecodeError:
            # If response is not in JSON format, create a default response
            response_data = {'response': 'Invalid response from server'}

        # Return a JsonResponse to the AJAX request
        return JsonResponse(response_data)
    else:
        # For non-POST requests, just render the empty form
        return render(request, 'room_reservation_app/index.html')

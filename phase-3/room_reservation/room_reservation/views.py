from django.shortcuts import render
import socket
import json
import struct
from django.http import JsonResponse
from django.http import HttpResponse
import logging
from django.shortcuts import redirect
import requests
from django.views.decorators.csrf import csrf_exempt
from .decorators import login_required  # Import the decorator

logger = logging.getLogger(__name__)


def index(request):
    return render(request, 'index.html')


def send_command_to_phase2_server(command, token):
    phase2_server_host = 'localhost'
    phase2_server_port = 12345

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
            response = '{"re' + response
            print(f"Response received: {response}")

            return response
    except ConnectionError as e:
        return f"Connection error: {e}"
    except struct.error as e:
        return f"Pack/Unpack error: {e}"
    except Exception as e:
        return f"An error occurred: {e}"


def login_view(request):
    return render(request, 'login.html')


@csrf_exempt
def execute_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Prepare the command to send to the phase2 server
        command = {
            "action": "login",
            "username": username,
            "password": password
        }

        # Send the command to the phase2 server
        response = send_command_to_phase2_server(json.dumps(command), None)

        try:
            response_data = json.loads(response)
            if 'response' in response_data and 'token' in response_data:
                # Store the token in the user's session
                request.session['token'] = response_data['token']

                # Instead of redirecting, return a JSON response with the redirect URL
                return JsonResponse({'redirect': '/command-center/'})
            else:
                # Return a JSON response indicating invalid credentials
                return JsonResponse({'error': 'Invalid credentials'}, status=401)
        except json.JSONDecodeError:
            # Return a JSON response indicating failure to decode server response
            return JsonResponse({'error': 'Failed to decode response from server'}, status=500)

    # Return a JSON response for invalid requests
    return JsonResponse({'error': 'Invalid request'}, status=400)


@csrf_exempt  # Be mindful of CSRF in production
def register_view(request):
    # Handle GET request to serve the registration page
    if request.method == 'GET':
        return render(request, 'register.html')

    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')  # If you're including email in the registration process
        password = request.POST.get('password')
        fullname = request.POST.get('fullname')

        # Prepare the command to send to the phase2 server
        command = {
            "action": "register",
            "username": username,
            "email": email,  # Include this if your backend expects it
            "password": password,
            "fullname": fullname
        }

        # Send the command to the phase2 server
        response = send_command_to_phase2_server(json.dumps(command), None)

        try:
            response_data = json.loads(response)
            # Assuming the phase2 server returns a JSON response
            return JsonResponse(response_data)
        except json.JSONDecodeError:
            # Error handling if the response is not JSON or is malformed
            return JsonResponse({'error': 'Failed to decode response from server'}, status=500)

    # Handle non-POST requests or other errors
    return JsonResponse({'error': 'Invalid request'}, status=400)


def combined_view(request):
    objects = [
        {'name': 'Object1', 'x': 100, 'y': 150, 'color': 'red'},
        {'name': 'Object2', 'x': 200, 'y': 50, 'color': 'blue'},
        {'name': 'Object3', 'x': 150, 'y': 100, 'color': 'green'},
        # ... more objects ...
    ]
    response_message = ""
    token = request.COOKIES.get('token', '')

    if request.method == 'POST':
        command = request.POST.get('command')
        response_json_string = send_command_to_phase2_server(command, token)
        try:
            response_data = json.loads(response_json_string)
            response_message = response_data.get('response', 'Invalid response from server')
            token = response_data.get('token', token)
        except json.JSONDecodeError:
            response_message = 'Invalid response from server'

    context = {
        'objects': objects,
        'response_message': response_message,
        'token': token
    }
    return render(request, 'index.html', context)


@csrf_exempt  # To bypass CSRF token verification for demonstration purposes
@login_required  # Apply the decorator to the view
def command_center(request):
    if request.method == 'POST':
        action = request.POST.get('command')

        # Constructing the data to be sent based on the action
        data = {'action': action}
        if action == 'login':
            data['username'] = request.POST.get('username')
            data['password'] = request.POST.get('password')
        elif action == 'create_organization':
            data['token'] = request.POST.get('token')
            data['org_name'] = request.POST.get('org_name')
            data['description'] = request.POST.get('description')

        # Sending the request to the backend server
        response = requests.post('http://127.0.0.1:12345', json=data)

        # Process the response (assuming it's JSON)
        if response.ok:
            response_data = response.json()
            # You can process and visualize the response data as needed
            return render(request, 'response_template.html', {'response_data': response_data})
        else:
            return render(request, 'error_template.html', {'error': 'Error communicating with the backend server'})

    # For GET requests, or if the form is not submitted
    return render(request, 'command_center.html')


@csrf_exempt  # If CSRF protection is enabled, you'll need to handle CSRF token.
def execute_command(request):
    if request.method == 'POST':
        # Extract data from the form
        action = request.POST.get('command')
        data = {'action': action}

        # Additional data based on action
        if action in ['login', 'register']:
            data['username'] = request.POST.get('username')
            data['password'] = request.POST.get('password')
        elif action in ['create_organization', 'update_organization']:
            data['token'] = request.POST.get('token')
            data['org_name'] = request.POST.get('org_name')
            data['description'] = request.POST.get('description')

        # Send data to the backend server
        try:
            response = requests.post('http://127.0.0.1:12345', json=data)
            response.raise_for_status()
            return render(request, 'response_template.html', {'response_data': response.json()})
        except requests.RequestException as e:
            return render(request, 'error_template.html', {'error': str(e)})

    return render(request, 'command_center.html')


"""
def command_view(request):
    if request.method == 'POST':
        command = request.POST.get('command')
        token = request.COOKIES.get('token')

        response_json_string = send_command_to_phase2_server(command, token)
        
        response_json_string = '{"re'+response_json_string
        try:
            # Parse the JSON response
            response_data = json.loads(response_json_string)
            print(response_data)
        except json.JSONDecodeError:
            # If response is not in JSON format, create a default response
            response_data = {'response': 'Invalid response from server'}

        # Return a JsonResponse to the AJAX request
        return JsonResponse(response_data)
    else:
        # For non-POST requests, just render the empty form
        return render(request, 'index.html')


#for SVG map to render:
def map_view(request):
    objects = [
        {'name': 'Object1', 'x': 100, 'y': 150, 'color': 'red'},
        {'name': 'Object2', 'x': 200, 'y': 50, 'color': 'blue'},
        {'name': 'Object2', 'x': 150, 'y': 100, 'color': 'green'},
        # ... more objects ...
    ]
    context = {
        'objects': objects,
        # ... other context variables ...
    }
    return render(request, 'index.html', context)
"""

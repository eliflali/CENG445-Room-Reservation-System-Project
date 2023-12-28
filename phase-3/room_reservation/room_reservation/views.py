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
PERMISSIONS = [
    'access',
    'delete',
    'list',
    'add'
]


def index(request):
    return render(request, 'index.html')


@csrf_exempt
def send_command_to_phase2_server(command: dict, token: str = None):
    phase2_server_host = 'localhost'
    phase2_server_port = 12345

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((phase2_server_host, phase2_server_port))
            logger.debug(f"Connected to {phase2_server_host} on port {phase2_server_port}")

            if token is not None:
                command['token'] = token

            print(f"sending command: {command}")
            command = json.dumps(command)
            command_dict = {"command": command}
            command_json = json.dumps(command_dict)
            command_bytes = command_json.encode('utf-8')

            print(f"Command sent: {command_json}")
            sock.sendall(struct.pack('!I', len(command_bytes)))
            sock.sendall(command_bytes)

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
        response = send_command_to_phase2_server(command)

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
            return JsonResponse({'error': 'Failed to decode response from server in login'}, status=500)

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
        response = send_command_to_phase2_server(command)

        try:
            response_data = json.loads(response)
            # Assuming the phase2 server returns a JSON response
            return JsonResponse(response_data)
        except json.JSONDecodeError:
            # Error handling if the response is not JSON or is malformed
            return JsonResponse({'error': 'Failed to decode response from server in register view'}, status=500)

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


# TODO: make all of the command operations.
@csrf_exempt
def create_organization(request):
    """
    This function called by command-center.
    It will create an organization.

    First it will create permissions for that organization.
    Permission options:
        'add', 'delete', 'access', 'list', 'update'
    """
    token = request.session['token']

    permissions = request.POST.getlist('permissions')
    permission_request = {'action': 'create_organization_permissions'}
    for permission in permissions:
        permission_request[permission + "_permission"] = 'true'

    permission_request['org_name'] = request.POST.get('org_name')
    permission_response = send_command_to_phase2_server(permission_request, token)


    data = {'action': 'create_organization'}
    data['org_name'] = request.POST.get('org_name')
    data['description'] = request.POST.get('description')

    response = send_command_to_phase2_server(data, token)
    try:
        response = json.loads(response)
        response_message = response.get('response', 'Invalid response from server')

        permission_response = (json.loads(permission_response).
                               get('response', 'Invalid response from server in permissions'))

        # Prepare the context for rendering
        context = {'response_message': response_message,
                   'permission_response': permission_response,
                   'title': 'Create Organization Response'}

        # Check various conditions and modify context as needed
        if response_message == "Organization already exists.":
            context['error'] = 'The organization already exists.'
        elif response_message == "You don't have permission.":
            context['error'] = "You don't have permission to create an organization."
        elif response_message == "Invalid response from server":
            context['error'] = "Invalid response from server."

        # Render the response_template.html with the context
        return render(request, 'response_template.html', context)

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Failed to decode response from server in create organization'}, status=500)

@csrf_exempt
def update_organization(request):
    """
    This endpoint will update the organization.
    """
    token = request.session['token']

    data = {'action': 'update_organization'}
    data['org_name'] = request.POST.get('org_name')
    data['field'] = request.POST.get('field')
    data['value'] = request.POST.get('value')

    response = send_command_to_phase2_server(data, token)

    try:
        response = json.loads(response)
        response_message = response.get('response', 'Invalid response from')
        context = {'response_message': response_message, 'title': 'Update Organization'}

        return render(request, 'response_template.html', context)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid field name or something went wrong in phase-2 server while updating organization.'}, status=500)



@csrf_exempt
def process_request(request):
    """
    Process the request and returns back from the deep backend server.

    Returns:
        response (json): Response from the deep backend server
    """

    command = request.POST.get('command')

    if command == 'create_organization':
        return create_organization(request)
    elif command == 'update_organization':
        return update_organization(request)
    else:
        return JsonResponse({'error': ''})


@csrf_exempt  # To bypass CSRF token verification for demonstration purposes
@login_required  # Apply the decorator to the view
def command_center(request):
    if request.method == 'POST':
        print(f"REQUEST: {request.POST}")
        return process_request(request)

    # For GET requests, or if the form is not submitted
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

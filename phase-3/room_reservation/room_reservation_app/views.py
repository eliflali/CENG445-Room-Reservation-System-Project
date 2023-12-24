from django.shortcuts import render

# Create your views here.

def index(request):
    # Your view logic here
    return render(request, 'room_reservation_app/index.html')


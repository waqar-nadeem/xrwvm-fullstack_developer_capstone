# Uncomment the required imports before adding the code

# from django.shortcuts import render
# from django.http import HttpResponseRedirect, HttpResponse
# from django.contrib.auth.models import User
# from django.shortcuts import get_object_or_404, render, redirect
# from django.contrib.auth import logout
# from django.contrib import messages
# from datetime import datetime

from django.http import JsonResponse
from django.contrib.auth import login, authenticate
import logging
import json
from django.views.decorators.csrf import csrf_exempt
from .populate import initiate # <--- UNCOMMENTED: Needed for initial data load
from .models import CarMake, CarModel # <--- NEW: Imports Car models

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.

# Create a `login_request` view to handle sign in request
@csrf_exempt
def login_user(request):
    # Get username and password from request.POST dictionary
    data = json.loads(request.body)
    username = data['userName']
    password = data['password']
    # Try to check if provide credential can be authenticated
    user = authenticate(username=username, password=password)
    data = {"userName": username}
    if user is not None:
        # If user is valid, call login method to login current user
        login(request, user)
        data = {"userName": username, "status": "Authenticated"}
    return JsonResponse(data)


# <HINT> Add a method to get the list of cars
def get_cars(request):
    """
    Retrieves all car models and their associated car make details.
    Initializes car data if the CarMake collection is empty.
    """
    # Check if CarMake data exists
    count = CarMake.objects.filter().count()
    print(f"Car Make Count: {count}")
    if(count == 0):
        # Populate the database if empty
        initiate()
        
    # Retrieve CarModel objects, using select_related for efficient fetching of related CarMake data
    car_models = CarModel.objects.select_related('car_make').all()
    
    cars = []
    # Structure the data into a list of dictionaries for JSON response
    for car_model in car_models:
        cars.append({
            "CarModel": car_model.name, 
            "CarMake": car_model.car_make.name,
            "ID": car_model.id,
            "Type": car_model.type,
            "Year": car_model.year
        })
    
    return JsonResponse({"CarModels": cars})


# Create a `logout_request` view to handle sign out request
# def logout_request(request):
# ...

# Create a `registration` view to handle sign up request
# @csrf_exempt
# def registration(request):
# ...

# # Update the `get_dealerships` view to render the index page with
# a list of dealerships
# def get_dealerships(request):
# ...

# Create a `get_dealer_reviews` view to render the reviews of a dealer
# def get_dealer_reviews(request,dealer_id):
# ...

# Create a `get_dealer_details` view to render the dealer details
# def get_dealer_details(request, dealer_id):
# ...

# Create a `add_review` view to submit a review
# def add_review(request):
# ...   
# Required imports
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import logout, login, authenticate
from django.contrib import messages
from datetime import datetime

from django.http import JsonResponse
import logging
import json
from django.views.decorators.csrf import csrf_exempt
from .populate import initiate 
from .models import CarMake, CarModel 
from .restapis import get_request, analyze_review_sentiments, post_review

logger = logging.getLogger(__name__)

# ----------------------------
# LOGIN VIEW
# ----------------------------
@csrf_exempt
def login_user(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            username = data.get('userName')
            password = data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return JsonResponse({"userName": username, "status": "Authenticated"})
            else:
                return JsonResponse({"userName": username, "error": "Invalid Credentials"})
        except Exception as e:
            logger.error(f"Login failed: {e}")
            return JsonResponse({"error": "Server error", "details": str(e)}, status=500)
    else:
        return JsonResponse({"error": "Invalid request method"}, status=400)


# ----------------------------
# REGISTRATION VIEW
# ----------------------------
@csrf_exempt
def registration(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            username = data.get('userName')
            password = data.get('password')
            first_name = data.get('firstName')
            last_name = data.get('lastName')
            email = data.get('email')

            if User.objects.filter(username=username).exists():
                return JsonResponse({"userName": username, "error": "Already Registered"})

            user = User.objects.create_user(
                username=username,
                password=password,
                first_name=first_name,
                last_name=last_name,
                email=email
            )
            login(request, user)
            return JsonResponse({"userName": username, "status": "Authenticated"})
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        except Exception as e:
            logger.error(f"Registration failed: {e}")
            return JsonResponse({"error": "Server error", "details": str(e)}, status=500)
    else:
        return JsonResponse({"error": "Invalid request method"}, status=400)


# ----------------------------
# LOGOUT VIEW
# ----------------------------
@csrf_exempt
def logout_request(request):
    try:
        logout(request)
        return JsonResponse({"userName": ""})
    except Exception as e:
        logger.error(f"Logout failed: {e}")
        return JsonResponse({"error": "Server error", "details": str(e)}, status=500)


# ----------------------------
# GET CARS VIEW
# ----------------------------
def get_cars(request):
    count = CarMake.objects.count()
    if count == 0:
        initiate()
    car_models = CarModel.objects.select_related('car_make').all()
    cars = [
        {
            "CarModel": car_model.name,
            "CarMake": car_model.car_make.name,
            "ID": car_model.id,
            "Type": car_model.type,
            "Year": car_model.year
        }
        for car_model in car_models
    ]
    return JsonResponse({"CarModels": cars})


# ----------------------------
# GET DEALERSHIPS VIEW
# ----------------------------
def get_dealerships(request, state="All"):
    endpoint = "/fetchDealers" if state == "All" else f"/fetchDealers/{state}"
    dealerships = get_request(endpoint)
    return JsonResponse({"status": 200, "dealers": dealerships})


# ----------------------------
# GET DEALER DETAILS VIEW
# ----------------------------
def get_dealer_details(request, dealer_id):
    if dealer_id:
        endpoint = f"/fetchDealer/{dealer_id}"
        dealership = get_request(endpoint)
        return JsonResponse({"status": 200, "dealer": dealership})
    else:
        return JsonResponse({"status": 400, "message": "Bad Request"})


# ----------------------------
# GET DEALER REVIEWS VIEW
# ----------------------------
def get_dealer_reviews(request, dealer_id):
    if dealer_id:
        endpoint = f"/fetchReviews/dealer/{dealer_id}"
        reviews = get_request(endpoint)
        for review_detail in reviews:
            try:
                response = analyze_review_sentiments(review_detail.get('review', ''))
                review_detail['sentiment'] = response.get('sentiment', 'neutral')
            except Exception as e:
                logger.error(f"Sentiment analysis failed: {e}")
                review_detail['sentiment'] = 'neutral'
        return JsonResponse({"status": 200, "reviews": reviews})
    else:
        return JsonResponse({"status": 400, "message": "Bad Request"})


# ----------------------------
# ADD REVIEW VIEW
# ----------------------------
@csrf_exempt
def add_review(request):
    if not request.user.is_anonymous:
        try:
            data = json.loads(request.body)
            post_review(data)
            return JsonResponse({"status": 200})
        except Exception as e:
            logger.error(f"Add review failed: {e}")
            return JsonResponse({"status": 401, "message": "Error in posting review"})
    else:
        return JsonResponse({"status": 403, "message": "Unauthorized"})

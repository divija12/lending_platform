from django.views.generic import ListView
from .models import IndividualBorrower, BusinessBorrower
from django.shortcuts import render
from django.http import JsonResponse
from .utils import *
import json
import pandas as pd
from sklearn.preprocessing import LabelEncoder

# Create a LabelEncoder for categorical features
label_encoder = LabelEncoder()

def predict_individual_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        print(data)
        goal = data.get("goal")  
        print(goal)

        features = handle_dataset_individuals(data)
        
        default_probability = predict_default_probability(features, borrower_type="individual")
        print(default_probability)
        recommend_loan_boolean = recommend_loan(default_probability, "individual", goal)
        return JsonResponse({
            "default_probability": float(default_probability) * 100,
            "recommendation": recommend_loan_boolean
        })

def predict_business_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        print(data)
        goal = data.get("goal")  
        features = handle_dataset_business(data)
        print("final shape ", features.shape, type(features))
        default_probability = predict_default_probability(features, borrower_type="business")
        print(default_probability)
        
        recommend_loan_boolean = recommend_loan(default_probability, "business", goal)
        
        return JsonResponse({
            "default_probability": float(default_probability) * 100,
            "recommendation": recommend_loan_boolean
        })

# List views
class IndividualBorrowerListView(ListView):
    model = IndividualBorrower
    template_name = 'individual_borrower_list.html'
    context_object_name = 'borrowers'
    paginate_by = 50 

class BusinessBorrowerListView(ListView):
    model = BusinessBorrower
    template_name = 'business_borrower_list.html'
    context_object_name = 'borrowers'
    paginate_by = 50 

def home_view(request):
    return render(request, 'home.html')

def individual_form_view(request):
    return render(request, 'individual_form.html')

def business_form_view(request):
    return render(request, 'business_form.html')
# risk_assessment/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('individual/predict/', views.predict_individual_view, name='predict_individual'),
    path('business/predict/', views.predict_business_view, name='predict_business'),
    path('individuals/', views.IndividualBorrowerListView.as_view(), name='individual_borrower_list'),
    path('businesses/', views.BusinessBorrowerListView.as_view(), name='business_borrower_list'),
     # Form Views for Individual and Business Borrowers
    path('individual/form/', views.individual_form_view, name='individual_form'),
    path('business/form/', views.business_form_view, name='business_form'),
    path('', views.home_view, name='home')
]

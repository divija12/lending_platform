# risk_assessment/forms.py

from django import forms
from .models import IndividualBorrower, BusinessBorrower

class IndividualBorrowerForm(forms.ModelForm):
    class Meta:
        model = IndividualBorrower
        fields = ['name', 'income', 'credit_score', 'debt_to_income_ratio']

class BusinessBorrowerForm(forms.ModelForm):
    class Meta:
        model = BusinessBorrower
        fields = ['business_name', 'annual_revenue', 'business_credit_score', 'debt_coverage_ratio']

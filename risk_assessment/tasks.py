# risk_assessment/tasks.py
from celery import shared_task
from .models import IndividualBorrower, BusinessBorrower
from .utils import predict_default_probability

@shared_task
def periodic_individual_risk_assessment():
    borrowers = IndividualBorrower.objects.all()
    for borrower in borrowers:
        features = [borrower.income, borrower.credit_score, borrower.debt_to_income_ratio]
        default_probability = predict_default_probability(features, borrower_type="individual")
        borrower.default_probability = default_probability
        borrower.save()

@shared_task
def periodic_business_risk_assessment():
    borrowers = BusinessBorrower.objects.all()
    for borrower in borrowers:
        features = [borrower.annual_revenue, borrower.business_credit_score, borrower.debt_coverage_ratio]
        default_probability = predict_default_probability(features, borrower_type="business")
        borrower.default_probability = default_probability
        borrower.save()

from django.test import TestCase
from .models import IndividualBorrower, BusinessBorrower
from .utils import predict_default_probability, recommend_loan

class IndividualBorrowerTest(TestCase):
    def test_default_probability(self):
        features = [50000, 700, 0.3]
        probability = predict_default_probability(features, borrower_type="individual")
        self.assertTrue(0 <= probability <= 1)

class BusinessBorrowerTest(TestCase):
    def test_default_probability(self):
        features = [1000000, 650, 1.2]
        probability = predict_default_probability(features, borrower_type="business")
        self.assertTrue(0 <= probability <= 1)

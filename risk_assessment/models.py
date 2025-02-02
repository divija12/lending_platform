# risk_assessment/models.py

from django.db import models

class IndividualBorrower(models.Model):
    member_id = models.AutoField(primary_key=True)
    
    # Applicant Demographics
    #emp_title = models.CharField(max_length=100, null=True, blank=True)
    emp_length = models.IntegerField(null=True, blank=True)  # Consider storing in years
    home_ownership = models.CharField(max_length=50, null=True, blank=True)
    income = models.FloatField()
    verification_status = models.CharField(max_length=50, null=True, blank=True)
    #zip_code = models.CharField(max_length=10, null=True, blank=True)
    addr_state = models.CharField(max_length=10, null=True, blank=True)
    application_type = models.CharField(max_length=50, null=True, blank=True)

    # Financial History
    dti = models.FloatField()  # Debt-to-Income Ratio
    delinq_2yrs = models.IntegerField(null=True, blank=True)
    inq_last_6mths = models.IntegerField(null=True, blank=True)
    open_acc = models.IntegerField(null=True, blank=True)
    pub_rec = models.IntegerField(null=True, blank=True)
    revol_bal = models.FloatField(null=True, blank=True)
    total_acc = models.IntegerField(null=True, blank=True)
    collections_12_mths_ex_med = models.IntegerField(null=True, blank=True)

    # Loan Characteristics
    loan_amnt = models.FloatField()
    term = models.CharField(max_length=20)
    int_rate = models.FloatField()
    installment = models.FloatField(null=True, blank=True)
    grade = models.CharField(max_length=5, null=True, blank=True)
    sub_grade = models.CharField(max_length=5, null=True, blank=True)
    purpose = models.CharField(max_length=100, null=True, blank=True)
    
    # Prediction and other metadata
    default_probability = models.FloatField(default=0.0)
    default_ind = models.BooleanField(default=False)  # Target Variable for whether the user defaults
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.member_id}"


class BusinessBorrower(models.Model):
    # Basic details
    loan_number = models.CharField(max_length=20, unique=True, default=12345)  # LoanNr_Chkdgt
    name = models.CharField(max_length=255, default="Unknown Borrower")  # Name
    city = models.CharField(max_length=100, default="Unknown City")  # City
    state = models.CharField(max_length=2, default="CA")  # State (defaulted to CA)
    zip_code = models.CharField(max_length=10, default="00000")  # Zip (defaulted to "00000")
    bank = models.CharField(max_length=255, default="Unknown Bank")  # Bank
    bank_state = models.CharField(max_length=2, default="CA")  # BankState (defaulted to CA)
    naics_code = models.CharField(max_length=6, default="000000")  # NAICS (defaulted to an arbitrary code)

    # Loan approval details
    approval_date = models.DateField(null=True, blank=True)  # ApprovalDate
    approval_fy = models.CharField(max_length=4, default="2020")  # ApprovalFY (defaulted to "2020")
    term = models.IntegerField(default=120)  # Term (defaulted to 120 months, i.e., 10 years)
    no_of_employees = models.IntegerField(default=1)  # NoEmp (defaulted to 1 employee)
    business_type = models.CharField(max_length=1, default="1")  # NewExist (default to 1 = Existing)
    jobs_created = models.IntegerField(default=0)  # CreateJob (defaulted to 0 jobs created)
    jobs_retained = models.IntegerField(default=0)  # RetainedJob (defaulted to 0 jobs retained)
    franchise_code = models.CharField(max_length=6, default="00000", null=True, blank=True)  # FranchiseCode

    # Geographic and loan type information
    urban_rural = models.CharField(max_length=1, default="1")  # UrbanRural (defaulted to "1" = Urban)
    revolving_credit = models.CharField(max_length=1, default="N")  # RevLineCr (defaulted to "N" = No)
    low_doc_program = models.CharField(max_length=1, default="N")  # LowDoc (defaulted to "N" = No)

    # Charge-off and disbursement details
    charge_off_date = models.DateField(null=True, blank=True)  # ChgOffDate
    disbursement_date = models.DateField(null=True, blank=True)  # DisbursementDate
    disbursement_gross = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)  # DisbursementGross
    balance_gross = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)  # BalanceGross
    mis_status = models.CharField(max_length=10, default="PIF")  # MIS_Status (default to "PIF" = Paid in Full)

    # Financials
    charge_off_principal = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True, default=0.00)  # ChgOffPrinGr
    gross_approved = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)  # GrAppv
    sba_approved = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)  # SBA_Appv

    def __str__(self):
        return f"{self.name} ({self.loan_number})"

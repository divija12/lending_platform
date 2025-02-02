# import_business_borrowers.py
from django.core.management.base import BaseCommand
from risk_assessment.models import BusinessBorrower
import pandas as pd
from datetime import datetime

class Command(BaseCommand):
    help = 'Import business borrower data from a CSV file'

   # def add_arguments(self, parser):
    #    parser.add_argument('csv_file', type=str, help='Path to the CSV file to import')

    def handle(self, *args, **kwargs):
        csv_file = '/Users/divijakejriwal/Desktop/project 1/SBAnational.csv'
        #kwargs['csv_file']
        
        # Load CSV into a DataFrame
        df = pd.read_csv(csv_file, low_memory=False)
        
        # List of columns needed for the model
        required_columns = [
            'LoanNr_ChkDgt', 'Name', 'City', 'State', 'Zip', 'Bank', 'BankState', 'NAICS',
            'ApprovalDate', 'ApprovalFY', 'Term', 'NoEmp', 'NewExist', 'CreateJob', 'RetainedJob',
            'FranchiseCode', 'UrbanRural', 'RevLineCr', 'LowDoc', 'ChgOffDate', 'DisbursementDate',
            'DisbursementGross', 'BalanceGross', 'MIS_Status', 'ChgOffPrinGr', 'GrAppv', 'SBA_Appv'
        ]
        
        # Filter columns and drop rows with missing required fields
        df = df[required_columns].dropna(subset=['LoanNr_ChkDgt', 'Name', 'DisbursementGross', 'GrAppv', 'SBA_Appv'])
        
        borrowers_to_create = []
        for _, row in df.iterrows():
            # Convert date fields
            approval_date = self.parse_date(row['ApprovalDate'])
            charge_off_date = self.parse_date(row['ChgOffDate'])
            disbursement_date = self.parse_date(row['DisbursementDate'])
            
            borrower = BusinessBorrower(
                loan_number=row['LoanNr_ChkDgt'],
                name=row['Name'],
                city=row['City'],
                state=row['State'],
                zip_code=row['Zip'],
                bank=row['Bank'],
                bank_state=row['BankState'],
                naics_code=row['NAICS'],
                approval_date=approval_date,
                approval_fy=row['ApprovalFY'],
                term=row['Term'],
                no_of_employees=row['NoEmp'],
                business_type=row['NewExist'],
                jobs_created=row['CreateJob'],
                jobs_retained=row['RetainedJob'],
                franchise_code=row['FranchiseCode'],
                urban_rural=row['UrbanRural'],
                revolving_credit=row['RevLineCr'],
                low_doc_program=row['LowDoc'],
                charge_off_date=charge_off_date,
                disbursement_date=disbursement_date,
                disbursement_gross=row['DisbursementGross'],
                balance_gross=row['BalanceGross'],
                mis_status=row['MIS_Status'],
                charge_off_principal=row['ChgOffPrinGr'] if pd.notnull(row['ChgOffPrinGr']) else None,
                gross_approved=row['GrAppv'],
                sba_approved=row['SBA_Appv']
            )
            borrowers_to_create.append(borrower)

        # Bulk create for efficiency
        BusinessBorrower.objects.bulk_create(borrowers_to_create)
        self.stdout.write(self.style.SUCCESS(f"Successfully imported {len(borrowers_to_create)} borrowers"))
    
    def parse_date(self, date_str):
        """Utility to parse dates, assuming format is MM/DD/YYYY"""
        if pd.isna(date_str):
            return None
        try:
            return datetime.strptime(date_str, '%m/%d/%Y').date()
        except ValueError:
            return None

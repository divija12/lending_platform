# import_individual_borrowers.py
from django.core.management.base import BaseCommand
from risk_assessment.models import IndividualBorrower
import pandas as pd
from datetime import datetime

class Command(BaseCommand):
    help = 'Import individual borrower data from a CSV file'

    #def add_arguments(self, parser):
    #    parser.add_argument('csv_file', type=str, help='Path to the CSV file')

    def handle(self, *args, **kwargs):
        csv_file = '/Users/divijakejriwal/Desktop/project 1/updated_data.csv'
        #kwargs['csv_file']
        
        # Read the CSV file into a DataFrame
        df = pd.read_csv(csv_file)
        
        # Select only the columns that match the IndividualBorrower model
        required_columns = [ 'member_id', 'emp_length', 'annual_inc', 
                            'verification_status', 'addr_state', 'dti', 
                            'delinq_2yrs', 'inq_last_6mths', 'open_acc', 'pub_rec', 'revol_bal', 'total_acc', 
                            'collections_12_mths_ex_med', 'loan_amnt', 'term', 'int_rate', 'installment', 'grade', 
                            'sub_grade', 'default_probability', 'default_ind', 'last_updated']
        df = df[required_columns]
        
        # Iterate over the rows and create IndividualBorrower instances
        borrowers_to_create = []
        for _, row in df.iterrows():
            borrower = IndividualBorrower(
                member_id=row['member_id'],
                income=row['annual_inc'],  # Assuming 'income' maps to 'annual_inc'
                emp_length=row['emp_length'],
                verification_status=row['verification_status'],
                addr_state=row['addr_state'],
                dti=row['dti'],
                delinq_2yrs=row['delinq_2yrs'],
                inq_last_6mths=row['inq_last_6mths'],
                open_acc=row['open_acc'],
                pub_rec=row['pub_rec'],
                revol_bal=row['revol_bal'],
                total_acc=row['total_acc'],
                collections_12_mths_ex_med=row['collections_12_mths_ex_med'],
                loan_amnt=row['loan_amnt'],
                term=row['term'],
                int_rate=row['int_rate'],
                installment=row['installment'],
                grade=row['grade'],
                sub_grade=row['sub_grade'],
                default_probability=row['default_probability'],
                default_ind=row['default_ind'],
                last_updated=row['last_updated'] if isinstance(row['last_updated'], datetime) else datetime.now()  # Ensuring datetime format
            )
            borrowers_to_create.append(borrower)
        
        # Bulk create to save all borrowers at once (more efficient)
        IndividualBorrower.objects.bulk_create(borrowers_to_create)
        
        self.stdout.write(self.style.SUCCESS(f"Successfully imported {len(borrowers_to_create)} borrowers from {csv_file}"))

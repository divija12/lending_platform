from datetime import datetime
import joblib
import numpy as np
from sklearn.preprocessing import LabelEncoder
import pandas as pd

# Load individual models
individual_logistic_model = joblib.load("ml_models/individual_logistic_model.pkl")
individual_xgboost_model = joblib.load("ml_models/individual_xgboost_model.pkl")

# Load business models
business_logistic_model = joblib.load("ml_models/business_logistic_model.pkl")
business_xgboost_model = joblib.load("ml_models/business_xgboost_model.pkl")

def predict_default_probability(features, borrower_type="individual", model_type="xgboost"):
    if borrower_type == "individual":
        if model_type == "logistic":
            return individual_logistic_model.predict_proba([features])[0][1]
        elif model_type == "xgboost":
            model_feature_names = individual_xgboost_model.get_booster().feature_names
            print(model_feature_names)
            print(features.shape)
            features_array = np.array(features).reshape(1, -1)  # Reshape to 2D array
            return individual_xgboost_model.predict_proba(features_array)[0][1]
    elif borrower_type == "business":
        if model_type == "logistic":
            return business_logistic_model.predict_proba([features])[0][1]
        elif model_type == "xgboost":
            model_feature_names = business_xgboost_model.get_booster().feature_names
            print("Required Features: ", model_feature_names)
            features_array = np.array(features).reshape(1, -1)  # Reshape to 2D array
            return business_xgboost_model.predict_proba(features_array)[0][1]
        
def recommend_loan(default_probability, borrower_type="individual", lender_goal="profit_maximization"):
    thresholds = {
        "individual": {"profit_maximization": 0.41, "risk_minimization": 0.21, "market_expansion": 0.5},
        "business": {"profit_maximization": 0.35, "risk_minimization": 0.15, "market_expansion": 0.45},
    }
    print(thresholds[borrower_type].get(lender_goal, 0.5))
    threshold = thresholds[borrower_type].get(lender_goal, 0.5)
    return "Approve" if default_probability < threshold else "Deny"

def handle_dataset_individuals(data):
    
    label_encoder = LabelEncoder()

    required_features = [
        'months_since_credit_pull', 'policy_code', 'months_since_last_pymnt',
        'initial_list_status', 'term', 'recoveries',
        'collection_recovery_fee', 'verification_status_encoded', 'out_prncp',
        'out_prncp_inv', 'grade_ordinal', 'last_pymnt_amnt', 'int_rate',
        'total_rec_prncp', 'member_id', 'inq_last_6mths', 'installment',
        'sub_grade', 'emp_length_encoded', 'total_pymnt', 'addr_state',
        'total_pymnt_inv', 'Repayment_Progress'
    ]

    features = {feature: data.get(feature) for feature in required_features}
    # If data.get() returns None for missing features, you can handle it like this:
    features = {feature: data.get(feature, None) for feature in required_features}
    df = pd.DataFrame([features])
    df['Repayment_Progress'] = 100
    grade_mapping = {'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5, 'F': 6, 'G': 7}
    df['grade_ordinal'] = df['grade_ordinal'].map(grade_mapping)
    initial_status_mapping = {'f': 1, 'w': 0}
    df['initial_list_status'] = df['initial_list_status'].map(initial_status_mapping)
    print(len(df['sub_grade'].value_counts().unique()))
    # As each sub_grade has different frequency and there are 35 sub_grades we use Count or Frequency Encoding
    subgrade_mapping=df['sub_grade'].value_counts().to_dict()
    df['sub_grade']=df['sub_grade'].map(subgrade_mapping)
    # Ordinal Number Encoding
    df['term_months'] = df['term'].str.split().str[0].astype(int)
    df = df.drop(columns='term')
    subgrade_mapping=df['addr_state'].value_counts().to_dict()
    df['addr_state']=df['addr_state'].map(subgrade_mapping)
    df['verification_status_encoded'] = label_encoder.fit_transform(df['verification_status_encoded'])
    print("DF: ", df)
    print("Input shape: ", df.shape)  # Should print (1, 23), meaning 1 row and 23 columns
    df_transposed = df.T  # This transposes the DataFrame
    # Print the new shape
    print("Transposed DataFrame shape:", df_transposed)  # (23, 1)
    
    return df_transposed

def handle_dataset_business(data):
    """
    Processes JSON data specific to business borrowers and extracts features needed for prediction.
    
    Args:
        data (dict): JSON data from the request containing business borrower information.

    Returns:
        dict: A dictionary containing processed features for the prediction model.

       'NoEmp', 'NewExist', 'UrbanRural', 'RevLineCr', 'DisbursementGross',
       'ChgOffPrinGr', 'IsFranchise', 'DaysToDisbursement', 'DisbursementFY',
       'SBA_AppvPct', 'AppvDisbursed', 'RealEstate', 'TotalJobs', 'TermYears',
       'DisbGrossRatio'
    """
    
    features = {
        "NoEmp": int(data.get("no_emp", 10)),
        "NewExist": int(data.get("new_exist", 1)),
        "UrbanRural": int(data.get("urban_rural", 1)),
        "RevLineCr": 1 if data.get("rev_line_cr", "N") == "Y" else 0,
        "DisbursementGross": float(data.get("disbursement_gross", 100000.00)),
        "ChgOffPrinGr": float(data.get("chg_off_prin_gr", 0.00)),
        "IsFranchise": 1 if data.get("franchise_code", "00000") == "00001" else 0,
        "SBA_AppvPct": (float(data.get("sba_appv", 120000.00)) / float(data.get("gr_appv", 150000.00))) * 100,
        "AppvDisbursed": float(data.get("disbursement_gross", 100000.00)) / float(data.get("gr_appv", 150000.00)),
        "TotalJobs": int(data.get("create_job", 5)) + int(data.get("retained_job", 3)),
        "TermYears": int(data.get("term", 36)) / 12,
        "DisbGrossRatio": float(data.get("balance_gross", 50000.00)) / float(data.get("disbursement_gross", 100000.00)),
    }

    # Calculate `DaysToDisbursement`
    approval_date = data.get("approval_date")
    disbursement_date = data.get("disbursement_date")
    if approval_date and disbursement_date:
        approval_date = datetime.strptime(approval_date, "%Y-%m-%d")
        disbursement_date = datetime.strptime(disbursement_date, "%Y-%m-%d")
        features["DaysToDisbursement"] = (disbursement_date - approval_date).days
    else:
        features["DaysToDisbursement"] = 0  # Default or handle missing dates

    # Calculate `DisbursementFY`
    if disbursement_date:
        features["DisbursementFY"] = disbursement_date.year
    else:
        features["DisbursementFY"] = datetime.now().year  # Default to current year

    # RealEstate (Assuming there's a "purpose" field indicating real estate purpose)
    purpose = data.get("purpose", "").lower()
    features["RealEstate"] = 1 if "real estate" in purpose else 0

    df = pd.DataFrame([features])
    print("DF: ", df)
    print("Input shape: ", df.shape)  
    df_transposed = df.T  # This transposes the DataFrame
    # Print the new shape
    print("Transposed DataFrame shape:", df_transposed) 
    
    # Additional processing can be done here if needed for more complex transformations

    return df_transposed

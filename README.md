## Final-Project Credit Risk Evaluation System
The project aims to automate the credit risk assessment process through a web-based application that integrates machine learning for real-time decision-making. 
It follows a two-phase structure:
Machine Learning Model Development: Focused on building reliable, predictive models to assess credit risk using various borrower-specific features.
Django-based UI Integration: The trained model is embedded in a Django web application, allowing users to input borrower details and receive automated, model-driven decisions.
This end-to-end functionality enables lenders to access automated loan decisions quickly and accurately.

## Table of Contents 
- [Frontend](#frontend)
- [Results](#results)
- [Installation](#installation)
- [Run the application](#run-the-application)
- [View the application](#view-the-application)

## Frontend
<img width="673" alt="home page image" src="https://github.com/user-attachments/assets/e57c06f3-7c1f-464c-83dd-fd93b04a6282" />
Home page

## Results
<img width="550" alt="image" src="https://github.com/user-attachments/assets/134b2257-4e43-4223-8cdf-2bd1c5d62b6e" />
ML models comparison for Individual Borrowers

<img width="761" alt="image" src="https://github.com/user-attachments/assets/8bf7cb05-124e-4048-9fd2-d6331fd7dd93" />

<img width="586" alt="image" src="https://github.com/user-attachments/assets/6ef9d3d1-7a1f-4761-b105-33c43b4df634" />
ML models comparison for Business Borrowers

<img width="761" alt="image" src="https://github.com/user-attachments/assets/7db96da1-be4e-4286-b8c0-f20db9c70ea8" />


## Installation

### 1. Create a virtual environment

From the **root** directory run:

```bash
python -m venv venv
```

### 2. Activate the virtual environment

From the **root** directory run:

On macOS:

```bash
source venv/bin/activate
```

On Windows:

```bash
venv\scripts\activate
```

### 3. Install required dependencies

From the **root** directory run:

```bash
pip install -r requirements.txt
```

### 4. Run migrations

From the **root** directory run:

```bash
python manage.py makemigrations
```
```bash
python manage.py migrate
```

## Run the application

From the **root** directory run:

```bash
python manage.py runserver
```

## View the application

Go to http://127.0.0.1:8000/ to view the application.

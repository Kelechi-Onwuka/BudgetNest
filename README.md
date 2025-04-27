# BudgetNest – A Smart Monthly Budget Planner

## Overview
BudgetNest is a web application designed to help users create and manage a realistic monthly budget. The platform aims to provide insights into income and spending, empowering users to make informed financial decisions.

## Features
- **User Authentication:** Secure sign-up and login processes.
- **Income & Expense Tracking:** Easily add, edit, and manage financial transactions.
- **Budget Management:** Set monthly budgets and get recommendations.
- **Visual Insights:** Graphical representation of spending vs. income.
- **Database Integration:** Uses SQLite (via SQLAlchemy) for storing data.

## Technologies Used
- **Backend:** Python, Flask, Flask-SQLAlchemy
- **Database:** SQLite
- **Frontend:** HTML, CSS, JavaScript (further developed as needed)
- **Version Control:** Git

## Project Structure
BudgetNest/
├── venv/                  ← Virtual environment folder
├── app/                   ← Application package
│   ├── __init__.py        ← Initializes Flask app and contains create_app()
│   ├── routes.py          ← Defines application routes (blueprints)
│   └── models.py          ← Placeholder for database models
├── config.py              ← Application configuration (SECRET_KEY, etc.)
├── requirements.txt       ← Project dependencies list
└── run.py                 ← Entry point to run the Flask app



## Setup Instructions

1. **Clone the Repository:**
   ```bash
   git clone <repository_url>
   cd BudgetNest


2. Set Up Virtual Environment:

bash

python3 -m venv venv
source venv/bin/activate

3. Install Dependencies:


pip install -r requirements.txt

4. Run the Application:

python run.py
Then, open your browser and navigate to http://127.0.0.1:5000/ to see the application in action.


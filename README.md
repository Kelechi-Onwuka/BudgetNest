# BudgetNest – A Smart Monthly Budget Planner

## Overview
BudgetNest is a web application designed to help users create and manage a realistic monthly budget. The platform aims to provide insights into income and spending, empowering users to make informed financial decisions.

## Features
- **User Authentication:** Secure sign-up and login processes.
- **Income & Expense Tracking:** Easily add, edit, and manage financial transactions.
- **Visual Dashboard:** Summarizes income, expenses, and remaining balance.
- **Database Integration:** Uses SQLite (via SQLAlchemy) for storing data.

## Technologies Used
- **Backend:** Python, Flask, Flask-SQLAlchemy
- **Database:** SQLite
- **Frontend:** HTML, CSS, JavaScript
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

## Acknowledgments
Developed as part of a collaborative group project.  
I took the lead on front-end development, designing and building the user interface using HTML, CSS, and JavaScript.  
I also finalized the income and expense tracking functionality, organized front-end assets, and helped define the overall technical structure of the project.




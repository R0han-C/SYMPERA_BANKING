# Banking API

## Overview

This project is a RESTful Banking API built with Django and Django REST Framework. It provides endpoints for managing customer accounts, handling transactions, and viewing account details. The API supports operations such as creating accounts, depositing and withdrawing funds, transferring money between accounts, and viewing transaction history.

## Features

- Create customer accounts
- Deposit funds
- Withdraw funds
- Transfer funds between accounts
- View account balance and transaction history
- JWT-based authentication

## Technology Stack

- Python 3.x
- Django 4.2
- Django REST Framework 3.14.0
- PostgreSQL (psycopg2-binary 2.9.5)
- JWT Authentication (djangorestframework-simplejwt 5.3.1)

## Setup and Installation

1. Clone the repository:
```
git clone <repository-url>
cd <project-directory>
```

2.Create a virtual environment and activate it:
```
python3 -m venv venv
source venv/bin/activate
```
3.Install the required dependencies:
```
pip install -r requirements.txt
```
4. Set up your PostgreSQL database and update the `.env` file with your database credentials:
   - In this case I am using a docker container of Postgres 16.3 (This can be changed as per requirements)
5.Run migrations:
```
python manage.py migrate
```
6.Start the development server:
```
python manage.py runserver
```
7. docker-compose.yml is also included and has a set of simple commands to run. All the commands are included in the notes.txt file. Feel free to contact anytime if you face any issue.

## API Endpoints

- `POST /accounts/`: Create a new customer account
- `GET /accounts/<int:pk>/`: Retrieve account details
- `POST /deposit/`: Deposit funds into an account
- `POST /withdraw/`: Withdraw funds from an account
- `POST /transfer/`: Transfer funds between accounts
- `GET /transactions/`: View transaction history

For detailed API documentation and curl, refer to api-curl-commands.txt. Have also attached Postman Collection

## Authentication

This API uses JWT (JSON Web Token) for authentication. To obtain a token:

1. Send a POST request to `/api/token/` with valid user credentials.
2. Use the returned access token in the Authorization header for subsequent requests:

## ENHANCEMENTS TODO:

1. Logging
2. Security Layers
3. Encryption
4. OTP
5. Expire Session
6. Limits and restrictions
7. Fraudulent Activity metrics
8. Data Masking
9. MultiFactor Auth 
10. Pentesting

## SCREENSHOTS
Detailed Postman screenshots are in the SCREENSHOTS folder.

## Contact

If you have any concern reach out to me at rcviit4196@gmail.com


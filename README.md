# 🏦 CapitalBank
Online Banking Management System (Django Project)

CapitalBank is a simple online banking web application that allows users to manage their bank accounts digitally.
Users can create accounts, deposit and withdraw money, transfer funds to other users, and request loans—all from a secure web interface.

This project was built as a learning and practice project to understand how real-world banking systems work using Django.

## 🌟 What Can This Application Do?
### 👤 User Features

Register a new user account

Login and logout securely

View and update user profile

Change account password

### 💳 Bank Account Features

Each user has a personal bank account

Account balance is automatically calculated

Full transaction history is maintained

### 🔄 Transaction Features

Users can perform the following banking operations:

✅ Deposit Money – Add money to their account

✅ Withdraw Money – Withdraw money with validation rules

✅ Transfer Money – Send money to another user’s account

✅ Loan Request – Request loans (with approval system)

✅ Transaction Report – View transaction history with date filters

Each transaction generates an email notification (displayed in logs during development).

### 🛠️ Admin Features

Manage users and bank accounts

View and monitor all transactions

Approve or reject loan requests

Full control through Django Admin Dashboard

### 🧰 Technologies Used

Backend: Django (Python Web Framework)

Frontend: HTML, Bootstrap 5

Database:

SQLite (Development)

PostgreSQL (Production-ready)

Authentication: Django built-in authentication system

Email System: SMTP / Console Email Backend

Deployment Platform: Render.com

## 🧠 What I Did in This Project

In this project, I:

Designed a complete banking workflow

Implemented user authentication and authorization

Created bank account and transaction logic

Applied business rules for deposits, withdrawals, transfers, and loans

Built transaction history and reporting system

Implemented email notifications for transactions

Used Django Class-Based Views and Forms

Managed database relationships and migrations

Secured sensitive data using environment variables

Deployed the application to a live server (Render)

## 🚀 How to Run the Project (For Developers)
```bash pip install -r requirements.txt 
python manage.py migrate
python manage.py runserver
```

Then open your browser and visit:
👉 http://127.0.0.1:8000/

## 🎯 Project Purpose

This project was created to:

Practice Django backend development

Understand real-world banking system logic

Learn transaction handling and validations

Gain experience with deployment and environment configuration

This is an educational and practice project, not a real banking system.

## 📄 License

This project is free to use for learning and educational purposes.

## 🙌 Thank You

Happy Banking! 🏦

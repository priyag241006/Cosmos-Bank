Cosmos Bank 🏦
A desktop banking application built with Python and Tkinter that simulates real banking operations with a clean dark-themed UI.
---
📸 Screenshots
(![](<screenshots/Screenshot 2026-04-01 185759.png>))
(![](<screenshots/Screenshot 2026-04-01 185641.png>))
(![](<screenshots/Screenshot 2026-04-01 185624.png>))
(![](<screenshots/Screenshot 2026-04-01 185600.png>))
(![](<screenshots/Screenshot 2026-04-01 185500.png>))
---
📌 About
Cosmos Bank is a simple desktop banking app that simulates real banking operations like account creation, login, deposits, withdrawals and fund transfers — all with a clean dark-themed UI. Built purely with Python's built-in libraries, no external installations required.
---
✨ Features
🔐 Secure account creation with Aadhaar & mobile number validation
🔑 Password hashing using SHA-256
💰 Deposit & Withdraw money instantly
🔄 Fund transfer between accounts
📊 Live balance update after every transaction
🧾 Mini statement showing last 5 transactions
📋 Copy account number to clipboard on registration
🌙 Dark themed modern UI
🔔 Toast notifications for every action
---
🛠️ Tech Stack
Technology	Purpose
Python 3.x	Core language
Tkinter	GUI framework (built-in)
Hashlib	SHA-256 password hashing (built-in)
Random	Account number generation (built-in)
Datetime	Transaction timestamps (built-in)
> No external libraries needed — runs out of the box!
---
▶️ How to Run
Step 1 — Make sure Python is installed:
```bash
python --version
```
If not installed, download from python.org
Step 2 — Clone this repository:
```bash
git clone https://github.com/priyag241006/cosmos-bank.git
cd cosmos-bank
```
Step 3 — Run the app:
```bash
python cosmos_bank.py
```
That's it! No pip install needed. 🎉
---
📖 How to Use
🆕 Creating an Account
Click "Create New Account" on the login screen
Fill in your details:
Full Name
Aadhaar Number (exactly 12 digits)
Mobile Number (exactly 10 digits)
Password (minimum 8 characters)
Confirm Password
Click "Create Account"
Your unique 10-digit Account Number will be shown — save it!
🔑 Login
Enter your 10-digit Account Number
Enter your Password
Click "Login"
💰 Deposit
Click the "Deposit" tab on the dashboard
Enter the amount
Click "Deposit"
Balance updates instantly
💸 Withdraw
Click the "Withdraw" tab
Enter the amount
Click "Withdraw"
App checks for sufficient balance automatically
🔄 Transfer
Click the "Transfer" tab
Enter the recipient's Account Number
Enter the amount
Click "Transfer"
🧾 Mini Statement
Last 5 transactions are displayed automatically on the right side of your dashboard
Green = Money In (Credit)
Red = Money Out (Debit)
---
📁 Project Structure
```
cosmos-bank/
├── cosmos_bank.py      # Main application file
├── README.md           # Project documentation
└── screenshots/        # App screenshots
    ├── login.png
    ├── dashboard.png
    └── create_account.png
```
---
⚠️ Important Notes
Data is stored in memory only — it resets when the app is closed
No real banking operations are performed
Aadhaar data is not verified with any government database
Built for learning and portfolio purposes only


Author
Priya Gundale
GitHub: @priyag241006

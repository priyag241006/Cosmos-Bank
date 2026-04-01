# Cosmos Bank

A desktop banking application built using Python and Tkinter that simulates real-world banking operations with a clean dark-themed user interface.

---

## About

Cosmos Bank is a simple desktop-based banking system that allows users to perform essential banking operations such as account creation, login, deposits, withdrawals, fund transfers, and transaction tracking.

The application is built entirely using Python’s built-in libraries and does not require any external installations.

---

## Cosmos Bank App Snapshots:

<img width="400" height="1012" alt="Screenshot 2026-04-01 185500" src="https://github.com/user-attachments/assets/7bd6a75e-9416-47c6-b3b6-4bd88692befb" />
<img width="400" height="1012" alt="Screenshot 2026-04-01 185600" src="https://github.com/user-attachments/assets/060cbd70-2604-456a-8ad8-19ccf006c087" />
<img width="400" height="1011" alt="Screenshot 2026-04-01 185624" src="https://github.com/user-attachments/assets/1c39c2e8-b754-4226-bb87-253693a1d87b" />
<img width="400" height="1017" alt="Screenshot 2026-04-01 185641" src="https://github.com/user-attachments/assets/e260773b-408a-497f-9314-e122b17f7b57" />






## Features

* Secure account creation with Aadhaar and mobile number validation
* Password hashing using SHA-256
* Deposit and withdrawal functionality
* Fund transfer between accounts
* Real-time balance updates
* Mini statement (last 5 transactions)
* Copy account number to clipboard
* Dark-themed user interface
* Notification messages for user actions

---

## Tech Stack

| Technology | Purpose                   |
| ---------- | ------------------------- |
| Python 3.x | Core programming language |
| Tkinter    | GUI framework             |
| Hashlib    | Password hashing          |
| Random     | Account number generation |
| Datetime   | Transaction timestamps    |

No external libraries are required.

---

## How to Run

### Step 1: Check Python Installation

```bash
python --version
```

### Step 2: Clone the Repository

```bash
git clone https://github.com/priyag241006/cosmos-bank.git
cd cosmos-bank
```

### Step 3: Run the Application

```bash
python cosmos_bank.py
```

---

## How to Use

### Create Account

* Click "Create New Account"
* Enter required details:

  * Full Name
  * Aadhaar Number (12 digits)
  * Mobile Number (10 digits)
  * Password (minimum 8 characters)
* Click "Create Account"
* Save your generated account number

### Login

* Enter account number and password
* Click "Login"

### Deposit

* Open Deposit tab
* Enter amount and confirm

### Withdraw

* Open Withdraw tab
* Enter amount and confirm

### Transfer

* Open Transfer tab
* Enter recipient account number and amount
* Confirm transfer

### Mini Statement

* Displays last 5 transactions
* Credit = Money in
* Debit = Money out

---

## Project Structure

```
cosmos-bank/
├── cosmos_bank.py
├── README.md

```
## Author

Priya Gundale
https://github.com/priyag241006

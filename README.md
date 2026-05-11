# expense_tracker

A modern and user-friendly Expense Tracker web application built using Python and Flask. This application helps users manage their daily expenses, track spending habits, and maintain financial records efficiently.

---

## 🚀 Features

- Add, edit, and delete expenses
- Track daily and monthly spending
- Categorize expenses
- Responsive and clean user interface
- Dashboard for expense overview
- Database management using ORM
- Secure backend with Flask

---

## 🛠️ Technologies Used

- Python
- Flask
- SQLAlchemy ORM
- MySQL
- HTML5
- CSS3
- JavaScript

---

## 📂 Project Structure


expense_tracker/
│
├── app/
├── .gitignore
├── Procfile
├── README.md
├── config.py
├── create_db.py
├── requirements.txt
└── run.py
⚙️ Installation
1️⃣ Clone the repository
git clone https://github.com/shrawi10317/expense_tracker.git
cd expense_tracker
2️⃣ Create virtual environment
python -m venv venv
3️⃣ Activate virtual environment
Windows
venv\Scripts\activate
Linux/Mac
source venv/bin/activate
4️⃣ Install dependencies
pip install -r requirements.txt
5️⃣ Configure Database

Update your database configuration inside config.py.

Example:

SQLALCHEMY_DATABASE_URI = "mysql://username:password@localhost/expense_tracker"
SQLALCHEMY_TRACK_MODIFICATIONS = False
6️⃣ Create Database
CREATE DATABASE expense_tracker;

Then run:

python create_db.py
7️⃣ Run the application
python run.py


## 📸 Screenshots

### Dashboard
<img width="1905" alt="Dashboard" src="https://github.com/user-attachments/assets/4a4f2116-b275-4322-ba97-ee873a208d83" />

### Login
<img width="1919" alt="Login" src="https://github.com/user-attachments/assets/baf176d0-827f-438f-a081-0848580acc33" />

### Add Expenses
<img width="1761" alt="Add Expenses" src="https://github.com/user-attachments/assets/6fe159a2-38bc-4929-8991-c65270b02f67" />

🎯 Future Improvements
Expense analytics and charts
User authentication system
Export expenses as PDF/Excel
Budget planning features
Dark mode support
👩‍💻 Author

Shrawani Wankhade

GitHub: shrawi10317
Portfolio: Portfolio Website

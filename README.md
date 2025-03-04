# Library Management System (Django Backend)

Library Management System is built using Django and provides essential functionalities for managing books, users, and transactions efficiently.

## 🚀 Overview
This project is designed to help users manage a library system with features such as book browsing, borrowing, returning, and reservations. Administrators can manage books, users, and fines seamlessly.

## 🛠 Tech Stack
- **Backend:** Django, Django REST Framework (DRF)
- **Database:** SQLite
- **Authentication:** Django's built-in authentication system

## 📌 Features
### User Features:
- User Registration & Authentication (Sign up, Login, Logout, Password Reset)
- Browse, Search, and Filter Books
- Borrow and Return Books
- Manage Book Reservations
- View Borrowing History and Fines

### Admin Features:
- Manage Books (Add, Edit, Delete)
- Manage Users
- Manage Fines and Borrowing Records

## 📂 Project Structure
```
project_root/
│── library_management/  # Main Django app
│   ├── models.py        # Database models
│   ├── views.py         # API views
│   ├── serializers.py   # API serializers
│   ├── urls.py          # API endpoints
│── db.sqlite3           # SQLite database file
│── manage.py            # Django management script
│── requirements.txt     # Project dependencies
```

## 🔧 Installation
### Prerequisites:
- Python 3.x
- Django

### Steps:
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/library-management.git
   cd library-management
   ```
2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Apply database migrations:
   ```bash
   python manage.py migrate
   ```
5. Create a superuser:
   ```bash
   python manage.py createsuperuser
   ```
6. Run the development server:
   ```bash
   python manage.py runserver
   ```
7. Access the API at:
   ```
   http://127.0.0.1:8000/
   ```
8. Admin panel:
   ```
   http://127.0.0.1:8000/admin/
   ```

## 📜 API Endpoints
| Method | Endpoint                | Description                |
|--------|-------------------------|----------------------------|
| POST   | `/api/auth/signup/`     | Register a new user       |
| POST   | `/api/auth/login/`      | Login user                |
| GET    | `/api/books/`           | List all books            |
| GET    | `/api/books/<id>/`      | Retrieve a book           |
| POST   | `/api/books/borrow/`    | Borrow a book             |
| POST   | `/api/books/return/`    | Return a book             |
| GET    | `/api/history/`         | View borrowing history    |
| POST   | `/api/payment/`         | payment through paystack  |

## 🏗 Future Improvements
- Email notifications for due dates
- Integrate payment system for fines
- Advanced book recommendation system

## 🤝 Contributing
Want to contribute? Fork the repo, create a feature branch, and submit a PR!

## 📜 License
This project is licensed under the MIT License.

---



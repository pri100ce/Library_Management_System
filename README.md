# Library Management System

A responsive Library Management System developed using **Python Flask** and **MySQL**. This project was created as a Semester 5 Mini Project for the Bachelor of Computer Applications (BCA).

---

## Features

### Admin

- Secure Login
- Dashboard
- Manage Books
  - Add Book
  - View Books
  - Update Book
  - Delete Book
- Manage Students
  - View Students
  - Update Student
  - Delete Student
- Issue Books
- Return Books
- View Issued Books
- Automatic Fine Calculation
- Search Functionality
- Pagination
- Export Data
  - PDF
  - Excel
  - CSV
  - Print
- Profile Management
  - Change Profile Picture
  - Update Name
  - Update Username
  - Update Email
  - Change Password
  - Theme Selection

---

### Student

- Secure Login
- Dashboard
- Search Available Books
- View Issued Books
- Export Available Books
  - PDF
  - Excel
  - CSV
  - Print
- Profile Management
  - Change Profile Picture
  - Update Name
  - Update Email
  - Change Password
  - Theme Selection

---

## Technologies Used

### Frontend

- HTML5
- CSS3
- JavaScript
- Font Awesome

### Backend

- Python
- Flask

### Database

- MySQL

### Python Libraries

- Flask
- mysql-connector-python
- openpyxl
- reportlab

---

## Project Structure

```
Library_Management_System/
│
├── app.py
├── requirements.txt
├── README.md
│
├── static/
│   ├── style.css
│   ├── script.js
│   ├── images/
│   └── uploads/
│
├── templates/
│
└── database/
```

---

## Installation

### 1. Clone the repository

```bash
git clone <repository-url>
```

### 2. Open the project

```bash
cd Library_Management_System
```

### 3. Install required packages

```bash
pip install -r requirements.txt
```

### 4. Configure MySQL

- Create the database.
- Import the SQL file.
- Update the database credentials in `app.py`.

### 5. Run the application

```bash
python app.py
```

Open:

```
http://127.0.0.1:5000
```

---

## Default Login

### Admin

```
Username : admin
Password : admin123
```

### Student

```
Student ID : 1
Password   : student123
```

*(Use the credentials available in your database.)*

---

## Author

**Prince Thakor**

Bachelor of Computer Applications (BCA)

Semester 5 Mini Project

---

## License

This project is developed for educational purposes.
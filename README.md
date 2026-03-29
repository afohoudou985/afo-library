# 📚 Library Management System

A desktop-based **Library Management System** built using **Python (Tkinter)** and **MySQL**. This application allows users to manage books, issue and return them, and maintain records efficiently with a user-friendly GUI.

---

## 🚀 Features

* 🔐 User Authentication (Login & Signup)
* ➕ Add New Books
* ❌ Delete Books
* 📖 Issue Books to Users
* 🔄 Return Books
* 🔍 Search Books by Title, Author, or ISBN
* 📊 View Issued Books with Details
* 🗂️ MySQL Database Integration
* 🎨 Interactive GUI using Tkinter

---

## 🛠️ Tech Stack

* **Frontend:** Tkinter (Python GUI)
* **Backend:** Python
* **Database:** MySQL
* **Other Libraries:**

  * mysql-connector
  * hashlib
  * datetime

---

## 🗄️ Database Structure

### Tables:

* `books` → Stores book details
* `users` → Stores login credentials
* `issued_books` → Tracks issued books

### Additional:

* Triggers for automatic status updates
* Stored procedure for issuing books
* View for issued book details

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/Anushka0910/library-management-system.git
cd library-management-system
```

### 2️⃣ Install Dependencies

```bash
pip install mysql-connector-python
```

### 3️⃣ Setup MySQL Database

* Create database: `library_system`
* Run the provided SQL file to create tables, triggers, and procedures

### 4️⃣ Run the Application

```bash
python dbms.py
```

---

## 📸 Screenshots

* Login & Signup Page
* Main Dashboard
* Book Management Interface
* Issued Books Section

---

## 💡 Key Highlights

* Real-time database updates
* Secure password hashing using SHA-256
* Clean and user-friendly interface
* Efficient handling of book issuing and returning

---

## 🧑‍💻 Author

**Anushka Diwakar Pawar**
B.Tech IT Student | FullStack Developer | AI/ML Enthusiast | Python | Java

---

## ⭐ Future Enhancements

* 📅 Due date notifications
* 📱 Web-based version using React
* 📊 Analytics dashboard
* 📷 QR code-based book issuing

---

## 📜 License

This project is for educational purposes.

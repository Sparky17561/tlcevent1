````markdown
---

# ✅ QR Attendance System (Django)

A web-based attendance management system that:

- 📤 Imports student details from Excel files
- 📷 Scans QR codes to mark attendance
- 🧾 Shows scanned and registered student info
- 📧 Sends emails with QR codes to students
- 🖱️ Admin toggles attendance manually from dashboard

---

## 🖼️ UI Overview

### 🎯 First Look
<img src="assets/firstlook.png" alt="Dashboard UI" width="700"/>

### ✉️ Send QR Button
<img src="assets/sendqr.png" alt="Send Email UI" width="400"/>

### ✅ Scan Result Example
<img src="assets/example.png" alt="Scanned QR Result" width="600"/>

---

## 📦 Requirements

- Python 3.10+
- pip
- virtualenv (recommended)
- SQLite (default DB, no setup needed)

---

## 🚀 Setup Instructions

### 1. Clone the project

```bash
git clone https://github.com/your-username/qr-attendance.git
cd qr-attendance
````

### 2. Create and activate a virtual environment (recommended)

```bash
python -m venv venv
source venv/bin/activate        # Linux/macOS
venv\Scripts\activate           # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

> **Note**: If `requirements.txt` doesn't exist yet, generate it using:

```bash
pip freeze > requirements.txt
```

---

### 4. Configure Email in `settings.py` (📧)

```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-app-password'
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = 'your-email@gmail.com'
```

> ⚠️ Use an **App Password** if using Gmail.
> (Google Account → Security → App Passwords)

---

### 5. Apply database migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

---

### 6. Run the server

```bash
python manage.py runserver
```

Then visit:
📍 [http://127.0.0.1:8000/scan/](http://127.0.0.1:8000/scan/)

---

## 📂 Project Structure

```
qr-attendance/
│
├── manage.py
├── requirements.txt
├── tlcevent1/              # Django project root
│   └── settings.py
│
└── qrvalidator/            # Main app
    ├── models.py
    ├── views.py
    ├── urls.py
    ├── templates/
    │   └── scan.html
    ├── static/
    │   └── js/
    │       ├── qr-scanner.min.js
    │       └── qr-scanner-worker.min.js
    └── assets/
        ├── firstlook.png
        ├── sendqr.png
        └── example.png
```

---

## ✅ Features

* 📤 Upload Excel files with multiple students per row
* 📷 Real-time QR camera scanning (auto-attendance)
* 🧾 View scanned student and all registered students
* 📧 Send QR codes via email (SMTP config required)
* 🔁 Toggle attendance manually with one click
* 🧠 Auto-parse up to 4 students per row in Excel

---

## 📌 API Endpoints

| Endpoint                         | Method | Purpose                    |
| -------------------------------- | ------ | -------------------------- |
| `/upload/`                       | POST   | Upload Excel file          |
| `/scan/`                         | GET    | Scanner and dashboard page |
| `/api/student/<uuid>/`           | GET    | Fetch student by QR ID     |
| `/api/toggle_attendance/<uuid>/` | POST   | Toggle attendance (admin)  |
| `/api/send_qr_emails/`           | POST   | Email QR codes to students |

---

## 🧪 Testing Sample

You can upload an Excel like `Creathon.xlsx` with:

* Columns: `College`, `Project`, `Domain`, `#Students`
* Then blocks of: `[Name, Email, Contact, Photo]` × N (2–4)
* The `Photo` column is optional and ignored

---

## 🛠 Troubleshooting

| Issue                 | Solution                                      |
| --------------------- | --------------------------------------------- |
| ❌ Camera not working  | Ensure browser permissions are allowed        |
| 📧 Emails not sending | Use correct SMTP credentials and App Password |
| 🌀 Duplicate entries  | The DB uses **email** to ensure uniqueness    |
| ❓ QR not recognized   | Ensure proper UUID string is embedded         |

---

## 📄 License

MIT License © 2025 – Saiprasad Jamdar

---

```

> ✅ **To use the images**, ensure they're placed inside the `assets/` folder and committed to your repo.  
> Markdown auto-renders image links like `![alt](assets/filename.png)` when viewed on GitHub.

Let me know if you want a `Creathon.xlsx` template added as a downloadable file too.
```

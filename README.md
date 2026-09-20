# Nova Tech University — College Management Portal

A full-stack college management portal with three role-based dashboards (Student, Faculty, Admin),
built with **React (Vite) + Flask + SQLite**.

## Project Structure

```
novatech/
├── backend/
│   ├── app.py                 # Flask app factory + blueprint registration
│   ├── config.py              # Config (secret keys, DB URI)
│   ├── extensions.py          # db, jwt, cors singletons
│   ├── models.py              # All SQLAlchemy models
│   ├── auth_utils.py          # role_required() decorator
│   ├── seed.py                # Creates tables + demo data
│   ├── requirements.txt
│   ├── database/              # novatech.db (SQLite) created here
│   └── routes/
│       ├── auth.py            # /api/register /api/login /api/logout /api/me
│       ├── students.py        # /api/students...
│       ├── faculty.py         # /api/faculty...
│       ├── academics.py       # /api/departments /api/courses /api/subjects
│       ├── attendance.py      # /api/attendance...
│       ├── marks.py           # /api/marks...
│       └── misc.py            # assignments, notices, fees, timetable, reports
│
└── frontend/
    ├── index.html
    ├── package.json
    ├── vite.config.js
    └── src/
        ├── main.jsx
        ├── App.jsx            # All routes
        ├── index.css          # Full blue/white theme
        ├── context/AuthContext.jsx
        ├── services/api.js    # Axios wrapper, every API call
        ├── components/        # Navbar, Footer, Sidebar, DashboardLayout,
        │                      # DataTable, UIWidgets, ProtectedRoute
        └── pages/
            ├── Home.jsx
            ├── Login.jsx
            ├── Register.jsx
            ├── StudentDashboard.jsx
            ├── FacultyDashboard.jsx
            └── AdminDashboard.jsx
```

## 1. Run the Backend (Flask)

```bash
cd backend
python -m venv venv

# Activate the virtual environment
venv\Scripts\activate        # Windows
source venv/bin/activate     # macOS / Linux

pip install -r requirements.txt

# Create the database + demo data (run once, or again to reset)
python seed.py

# Start the API server
python app.py
```

Backend runs at **http://127.0.0.1:5000**. Health check: `http://127.0.0.1:5000/api/health`.

## 2. Run the Frontend (React)

Open a **second terminal**:

```bash
cd frontend
npm install
npm run dev
```

Frontend runs at **http://localhost:5173** and proxies all `/api/*` calls to the Flask backend
(see `vite.config.js`), so you don't need to configure CORS URLs manually in the browser.

## 3. Demo Login Credentials (created by `seed.py`)

| Role    | Email                        | Password     |
|---------|-------------------------------|--------------|
| Admin   | admin@novatech.edu            | Admin@123    |
| Faculty | rjames@novatech.edu           | Faculty@123  |
| Student | ava.thompson@novatech.edu     | Student@123  |

You can also register a brand-new student account from the **Register** page.

## 4. How Authentication Works

- Passwords are hashed with Werkzeug's `generate_password_hash` — never stored in plain text.
- Login issues a **JWT** (`flask-jwt-extended`) containing the user's `role` as a claim.
- Every protected backend route is wrapped in `@role_required("admin", ...)`, so even if a
  student edits the URL in the browser and calls `/api/students` with POST, the **server**
  rejects it with `403 Access denied` — role checks are enforced server-side, not just hidden
  in the UI.
- On the frontend, `ProtectedRoute` also redirects a logged-in user away from a dashboard that
  doesn't match their role, and axios interceptors auto-attach the JWT to every request and
  force logout on a `401`.

## 5. Notes & Possible Extensions

- Database is SQLite by default (zero setup). To switch to MySQL, install `PyMySQL` and change
  `SQLALCHEMY_DATABASE_URI` in `config.py` to something like
  `mysql+pymysql://user:password@localhost/novatech`.
- `seed.py` drops and recreates all tables every time it's run — don't run it in production.
- Charts currently use CSS progress bars; swap in `recharts` (already in `package.json`) for
  line/bar charts if you want richer visuals on the dashboards.
- "Forgot Password" currently shows an informational alert; wire it to a real email-based reset
  flow if needed.

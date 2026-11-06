# JanSahay – Maharashtra Citizen Assistance Portal

JanSahay is a web-based citizen assistance portal developed to simplify the process of reporting damage, exploring government schemes, submitting scheme applications, and tracking application status.

The system provides three role-based panels: Citizen, Officer, and Admin.

## Features

### 1. Citizen Panel
- Citizen registration and login.
- Submit damage reports.
- View previously submitted damage reports.
- Explore available government schemes.
- Apply for eligible schemes using submitted damage reports.
- Track application status and officer remarks.

### 2. Officer Panel
- Secure officer login.
- View citizen damage reports.
- View submitted scheme applications.
- Review applications.
- Approve or reject applications.
- Add remarks for citizens.

### 3. Admin Panel
- Secure admin login.
- Create officer accounts.
- Add government schemes.
- Edit scheme information.
- Activate or deactivate schemes.
- Monitor all submitted applications.
- View assigned officer information.

## Technology Stack

| Component | Technology |
|---|---|
| Frontend | HTML, CSS, Bootstrap, JavaScript |
| Backend | Python, Flask |
| Database | MySQL |
| ORM | Flask-SQLAlchemy |
| Authentication | Flask-JWT-Extended |
| Password Security | Werkzeug Password Hashing |
| Development Tools | VS Code, MySQL Workbench, Git, GitHub |

## Project Structure

```text
JanShay/
│
├── app/
│   ├── __init__.py
│   ├── extensions.py
│   ├── models.py
│   │
│   ├── routes/
│   │   └── auth.py
│   │
│   └── templates/
│       ├── auth/
│       ├── citizen/
│       ├── officer/
│       └── admin/
│
├── config.py
├── run.py
├── create_admin.py
├── requirements.txt
├── .env
├── .gitignore
└── README.md
```

## Database

The project uses MySQL with the following main tables:

1. **Users** – Stores citizen, officer, and admin details.
2. **Damage Reports** – Stores damage reports submitted by citizens.
3. **Schemes** – Stores government scheme information.
4. **Applications** – Stores scheme applications and their review status.

## Installation and Setup

### Step 1: Clone the Repository

```bash
git clone https://github.com/Anushka-0422/JanSahay
```

```bash
cd JanSahay
```

### Step 2: Create a Virtual Environment

```bash
python -m venv venv
```

Activate it on Windows:

```powershell
venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Create the MySQL Database

Open MySQL Workbench and execute:

```sql
CREATE DATABASE jansahay;
```

### Step 5: Configure Environment Variables

Create a `.env` file in the root directory.

Add the following configuration with your own database credentials:

```env
SECRET_KEY=your_secret_key
JWT_SECRET_KEY=your_jwt_secret_key

DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_NAME=jansahay
```

### Step 6: Create the Admin Account

Run:

```bash
python create_admin.py
```

Enter the admin name, email, and password when prompted.

### Step 7: Run the Application

```bash
python run.py
```

Open your browser and visit:

```text
http://127.0.0.1:5000
```

## Application Workflow

1. Citizens register and log in.
2. Citizens submit damage reports.
3. Citizens explore active government schemes.
4. Citizens submit applications using their damage reports.
5. Officers review applications and update their status.
6. Citizens track application progress.
7. Admin manages schemes, officers, and applications.

## Security Features

- Password hashing.
- JWT-based authentication.
- Role-based access control.
- CSRF protection for form submissions.
- Environment variables for sensitive configuration.
- Restricted officer and admin account creation.

## Important Note

JanSahay is an academic prototype developed for educational purposes. It is not an official Maharashtra Government portal and does not provide actual government approvals or financial assistance.

Scheme eligibility and application decisions must be verified through the respective official government authorities.

## Developed As

**Project Name:** JanSahay – Maharashtra Citizen Assistance Portal

**Project Type:** MCA Mini Project

**Backend:** Python Flask

**Database:** MySQL
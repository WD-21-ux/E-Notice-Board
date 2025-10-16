# E-Notice-Board (Flask)

A simple electronic notice board built with Python and Flask.

Features
- Create, read, update, delete notices
- Simple admin login (password-based, stored in config/env)
- SQLite database via Flask-SQLAlchemy
- Bootstrap-based responsive UI

Getting started (local)
1. Create a virtual environment:
   python -m venv venv
   source venv/bin/activate   # on Windows: venv\Scripts\activate

2. Install dependencies:
   pip install -r requirements.txt

3. Set environment variables (recommended):
   export FLASK_APP=app.py
   export FLASK_ENV=development
   export SECRET_KEY="replace-with-a-secret"
   export ADMIN_PASSWORD="admin123"

4. Initialize the database:
   python init_db.py

5. Run the app:
   flask run
   or
   python app.py

Open http://127.0.0.1:5000

Default admin login:
- Path: /login
- Password: the value of ADMIN_PASSWORD environment variable (default in code if not set is `admin123` — please change it)

Project structure
- app.py           -- Flask app and routes
- models.py        -- SQLAlchemy model(s)
- init_db.py       -- Create DB and (optional) seed
- requirements.txt -- Python dependencies
- templates/       -- HTML templates
- static/          -- CSS

Next steps you might want:
- Add user accounts and registration
- Add file attachments to notices
- Add pagination and search
- Deploy to a cloud provider with a production database

License: MIT
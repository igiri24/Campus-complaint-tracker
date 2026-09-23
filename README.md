# CampusCare — Campus Complaint Tracker

A Django website for submitting, assigning, and tracking campus complaints.

## Run on macOS

1. Open Terminal and `cd` to this folder.
2. Create and activate a virtual environment:

   ```bash
   # CampusCare — Campus Complaint Tracker

A Django website for submitting, assigning, and tracking campus complaints.

## Run on macOS

1. Open Terminal and `cd` to this folder.
2. Create and activate a virtual environment:

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install requirements:

   ```bash
   python3 -m pip install -r requirements.txt
   ```

4. Create the database tables and an administrator login:

   ```bash
   python3 manage.py migrate
   python3 manage.py createsuperuser
   ```

5. Start the website:

   ```bash
   python3 manage.py runserver
   ```

6. Visit http://127.0.0.1:8000/ . Admin tools are at http://127.0.0.1:8000/admin/ .

Create a regular account through the website. To enable staff workflow, sign in as an administrator and mark a user as staff in Django Admin. SQLite database is created locally as `db.sqlite3`.

3. Install requirements:

   ```bash
   python3 -m pip install -r requirements.txt
   ```

4. Create the database tables and an administrator login:

   ```bash
   python3 manage.py migrate
   python3 manage.py createsuperuser
   ```

5. Start the website:

   ```bash
   python3 manage.py runserver
   ```

6. Visit http://127.0.0.1:8000/ . Admin tools are at http://127.0.0.1:8000/admin/ .

Create a regular account through the website. To enable staff workflow, sign in as an administrator and mark a user as staff in Django Admin. SQLite database is created locally as `db.sqlite3`.

# Payroll Management Application

Contains code and documentation for a simple Payroll Management Application done for my end semester examinations for the OOAD Lab.

The application was developed using **Flask** and **SQLAlchemy**.

---

You can run the application in your localhost machine by doing the following:

1. Clone this repository.
2. Open a Terminal in the project folder.
3. Install the required dependencies: ` pip install Flask Flask-SQLAlchemy `
4. Have MySQL installed in your system, or change the database URI in app.py to sqlite:///
5. Change the database URI for your configuration ` mysql://<user>:<password>@localhost/<database> `
6. Open the Python shell and perform the following: 
    - ` from app import * `
    - ` db.create_all() `
    - ` creds = Creds(userid="admin", password="admin") `
7. Close the Python shell and run the app with:
    - ` python app.py `

---

UML Diagrams were drawn to facilitate the implementation process and to better conceptualize the logic behind the implementation.

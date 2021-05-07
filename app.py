from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://admin:password@localhost/mysql"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Emp(db.Model):
    id = db.Column(db.String(10), primary_key=True)
    ename = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    job = db.Column(db.String(80), nullable=False)
    address = db.Column(db.String(300), nullable=False)
    phone = db.Column(db.Integer, nullable=False)
    doj = db.Column(db.DateTime, nullable=False)
    bpay = db.Column(db.Float, nullable=False, default=0.0)
    da = db.Column(db.Float, nullable=False, default=0.0)
    hra = db.Column(db.Float, nullable=False, default=0.0)
    pf = db.Column(db.Float, nullable=False, default=0.0)
    dedn = db.Column(db.Float, nullable=False, default=0.0)
    gpay = db.Column(db.Float, nullable=False, default=0.0)

    def __repr__(self):
        return "<Emp %r>" % self.id


class Creds(db.Model):
    userid = db.Column(db.String(30), primary_key=True)
    password = db.Column(db.String(30), nullable=False)

    def __repr__(self):
        return "<User %r>" % self.userid


@app.route("/", methods=['POST', 'GET'])
def index():

    if request.method == "POST":
        uname = request.form["uname"]
        pwd = request.form["pwd"]

        creds = Creds.query.get(uname)

        try:
            if uname == "admin" and creds.password == pwd:
                return redirect("/admin")
            elif creds.password == pwd:
                return redirect("/employee/" + uname)
            else:
                return render_template("login.html")

        except Exception as e:
            return "There was a problem finding your account."

    else:
        return render_template("login.html")


@app.route("/admin", methods=['POST', 'GET'])
def admin_dashboard():
    return render_template("admin.html")


@app.route("/employee/<string:eid>", methods=['POST', 'GET'])
def employee_dashboard(eid):
    return render_template("employee.html", employee=Emp.query.get_or_404(eid))


@app.route("/viewprofile/<string:eid>", methods=['POST', 'GET'])
def view_profile(eid):
    emp = [Emp.query.get_or_404(eid)]
    return render_template("view.html", employees=emp, payslip=False, vertical=True)


@app.route("/viewpayslip/<string:eid>", methods=['POST', 'GET'])
def view_payslip(eid):
    emp = [Emp.query.get_or_404(eid)]
    return render_template("view.html", employees=emp, payslip=True,  vertical=True)


@app.route("/add", methods=['POST', 'GET'])
def add_employee():
    if request.method == "POST":
        eid = request.form["id"]
        ename = request.form["pname"]
        age = int(request.form["age"])
        gender = request.form["gender"]
        job = request.form["job"]
        addr = request.form["addr"]
        phone = int(request.form["phone"])
        doj = request.form["doj"]

        doj = datetime.strptime(doj, '%Y-%m-%d')

        #print(type(eid), type(ename), type(age), type(gender), type(job), type(addr), type(phone), type(doj))

        new_emp = Emp(id=eid, ename=ename, age=age, gender=gender,
                      job=job, address=addr, phone=phone, doj=doj)

        new_user = Creds(userid=eid, password=eid)

        try:
            db.session.add(new_emp)
            db.session.add(new_user)
            db.session.commit()
            return redirect("/admin")

        except Exception as e:
            return "There was a problem adding that employee record."

    else:
        return render_template("add.html")


@app.route("/credit/", methods=['POST', 'GET'])
def credit_employee():

    if request.method == "POST":
        emp = Emp.query.get_or_404(request.form["id"])

        emp.bpay = float(request.form["salary"])

        if emp.job == 'Trainee':
            emp.da = 0.1 * emp.bpay
            emp.hra = 0.05 * emp.bpay
            emp.pf = 0.02 * emp.bpay
            emp.dedn = 0.01 * emp.bpay

        elif emp.job == 'Team Leader':
            emp.da = 0.15 * emp.bpay
            emp.hra = 0.1 * emp.bpay
            emp.pf = 0.05 * emp.bpay
            emp.dedn = 0.03 * emp.bpay

        elif emp.job == 'Manager':
            emp.da = 0.2 * emp.bpay
            emp.hra = 0.12 * emp.bpay
            emp.pf = 0.07 * emp.bpay
            emp.dedn = 0.03 * emp.bpay

        elif emp.job == 'HR':
            emp.da = 0.3 * emp.bpay
            emp.hra = 0.15 * emp.bpay
            emp.pf = 0.1 * emp.bpay
            emp.dedn = 0.05 * emp.bpay

        emp.gpay = emp.bpay + emp.da + emp.hra - emp.pf - emp.dedn

        try:
            db.session.commit()
            return redirect("/admin")

        except Exception as e:
            return "There was a problem crediting salary to that employee."

    else:
        return render_template("credit.html")


@app.route("/delete", methods=['POST', 'GET'])
def delete_employee():
    if request.method == "POST":
        emp = Emp.query.get_or_404(request.form["eid"])
        creds = Creds.query.get_or_404(request.form["eid"])
        try:
            db.session.delete(emp)
            db.session.delete(creds)
            db.session.commit()
            return redirect("/admin")
        except Exception as e:
            return "There was a problem deleting that employee."

    else:
        return render_template("delete.html")


@app.route("/update", methods=['POST', 'GET'])
def update_employee():
    if request.method == "POST":
        emp = Emp.query.get_or_404(request.form["id"])
        try:
            emp.phone = request.form["phone"]
            db.session.commit()
            return redirect("/admin")
        except Exception as e:
            return "There was a problem updating that employee's record."

    else:
        return render_template("update.html")


@app.route("/viewrecords", methods=['POST', 'GET'])
def view_records():
    employees = Emp.query.order_by(Emp.id).all()
    #print(employees, type(employees))

    return render_template("view.html", employees=employees, payslip=False, vertical=False)


if __name__ == "__main__":
    app.run(debug=True)

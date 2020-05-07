import os

from flask import Flask
from flask import render_template
from flask import request
from flask import redirect

from flask_sqlalchemy import SQLAlchemy

project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "ticketdatabase.db"))

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = database_file

db = SQLAlchemy(app)

class Ticket(db.Model):
    title = db.Column(db.String(80), unique=True, nullable=False, primary_key=True)

    def __repr__(self):
        return "<Place: {}>".format(self.place)

@app.route("/", methods=["GET", "POST"])
def home():
    if request.form:
        ticket = Ticket(title=request.form.get("place"))
        db.session.add(ticket)
        tickets = Ticket.query.all()
    return render_template("home.html", tickets=tickets)

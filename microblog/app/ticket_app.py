from flask import Flask, render_template
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)

class Ticket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    place = db.Column(db.String(120))
    date = db.Column(db.String(200))

    def __init__(self, place, date):
        self.place = place
        self.date = date
    def __repr__(self):
        return '<Ticket %r: %r>' % (self.place, self.date)

@app.cli.command('createdb') # команда по созданию базы данных для примера
def createdb_command():
    """Create dummy database."""
    db.create_all()
    db.session.add(Ticket('Russia', 'Monday'))
    db.session.commit()

@app.route('/ticket/<place>/<date>')
def show_ticket(place, date):
    ticket = Ticket.query.filter_by(place=place, date=date).first_or_404()
    return render_template('show_ticket.html', ticket=ticket)

if __name__ == "__main__":
    app.run()

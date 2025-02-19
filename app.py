from flask import Flask,render_template,request
from flask_sqlalchemy import SQLAlchemy
from send_mail import send_mail

app = Flask(__name__)

ENV= 'prod'
if ENV == 'dev':
    app.debug=True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Temitope001@@@localhost/Lexus'
else:
    app.debug=False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://pbgchtymzmnjao:81807bfa1e8c014e8786633baba797c7b4cb515dd6284465457d98f39eb68592@ec2-54-235-96-48.compute-1.amazonaws.com:5432/d81acnnjcdcima'

app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False


db = SQLAlchemy(app)


class Feedback(db.Model):
    __tablename__ = 'feedback'
    id = db.Column(db.Integer, primary_key=True)
    customer = db.Column(db.String(200), unique=True)
    dealer = db.Column(db.String(200))
    rating = db.Column(db.Integer)
    comments = db.Column(db.Text())

    def __init__(self, customer,dealer,rating,comments):
        self.customer = customer
        self.dealer = dealer
        self.rating = rating
        self.comments = comments


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/submit', methods=['POST'])
def submit():
    if request.method =='POST':
        customer = request.form['customer']
        dealer = request.form['dealer']
        rating = request.form['rating']
        comments = request.form['comments']
        # print (customer, dealer, rating, comments)
        if customer == '' or dealer == '':
            return render_template('index.html', message='please enter reduired feilds')
        if db.session.query(Feedback).filter(Feedback.customer == customer).count()== 0:
            data = Feedback(customer,dealer,rating,comments)
            db.session.add(data)
            # send_mail(customer,dealer,rating,comments)
            db.session.commit()
            return render_template('success.html')
        return render_template('index.html', message='Sorry, you can only leave a comment once '+ ""+ customer)





if __name__ == '__main__':
    app.run()
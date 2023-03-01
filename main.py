from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request, redirect, jsonify
import requests

app = Flask(__name__,template_folder="docs")
bootstrap = Bootstrap5(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///to-do.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
SQLALCHEMY_SILENCE_UBER_WARNING=1

db = SQLAlchemy(app)

class TO_DO(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    entry = db.Column(db.String(250), nullable=False)
    has_checked = db.Column(db.Boolean, nullable=True)


with app.app_context():
    db.create_all()






@app.route("/",methods = ['POST', 'GET'])
def home():
    entries = db.session.query(TO_DO).all()

    return render_template('index.html',entries=entries)


@app.route("/add",methods = ['POST', 'GET'])
def add():#  + Butona basılınca gelen entry i direkt olarak data base e ekle
    entry = request.form["entry"].strip()
    entry = entry.replace(' ', '_')

    print(entry)
    with app.app_context():
        new_entry = TO_DO(entry=entry,has_checked=False)
        db.session.add(new_entry)
        db.session.commit()

    return redirect("/")


@app.route("/delete<int:id>",methods = ['POST', 'GET'])
def delete_entry(id):
    with app.app_context():
        book_to_delete = TO_DO.query.get(id)


        db.session.delete(book_to_delete)
        db.session.commit()


    return redirect("/")




@app.route("/check<int:id>",methods = ['POST', 'GET'])
def check_entry(id):
    print("selam")
    with app.app_context():
        book_to_update = TO_DO.query.get(id)
        book_to_update.has_checked = True
        db.session.commit()


    return redirect("/")



@app.route("/update<int:id>", methods=['POST'])
def update_entry(id):
    entry = request.form["entry_to"].strip().replace(' ', '_')
    with app.app_context():
        to_do = TO_DO.query.get(id)
        to_do.entry = entry
        db.session.commit()
    return redirect("/")







if __name__=="__main__":
    app.run(debug=True)
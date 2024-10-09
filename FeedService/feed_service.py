from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import datetime
import psycopg2
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://kmmrwsgr:UMg6sKjYUG3nhI6D3fTjSU3vMpjGjYCI@abul.db.elephantsql.com/kmmrwsgr'
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(50), unique=True, nullable=False)


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    content = db.Column(db.String(400), nullable=False)
    username = db.relationship('User', backref='messages')
    date = db.Column(db.DateTime, default=datetime.datetime)


@app.route('/feed', methods = ['GET'])
def get_feed():

    messages = Message.query.order_by(Message.id.desc()).limit(10).all()
    return jsonify(
        [
            {
                'User': msg.user.username,
                'Content': msg.content,
                'Date': msg.date,
            }
            for msg in messages
        ]
    )


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(port=5002)
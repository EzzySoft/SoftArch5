from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from bcrypt import hashpw, gensalt, checkpw
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://kmmrwsgr:UMg6sKjYUG3nhI6D3fTjSU3vMpjGjYCI@abul.db.elephantsql.com/kmmrwsgr'
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique = True, nullable=False)
    password = db.Column(db.String(512),  nullable=False)


@app.route('/register', methods = ['POST'])
def register():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    if User.query.filter_by(username=username).first():
        return jsonify({
            "Message": "User already exists"
        }), 400
    if not username or not password:
        return jsonify({
            "Message": "Username and password are required"
        }), 400
    password = hashpw(password.encode('utf-8'), gensalt())
    user = User(username=username, password=password.decode('utf-8'))
    db.session.add(user)
    db.session.commit()

    return jsonify({
        "Message" : "User registered successfully"
    }), 201


@app.route('/login', methods = ['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    user = User.query.filter_by(username=username)
    if not username or not password:
        return jsonify({
            "Message": "Username and password are required"
        }), 400
    if not user:
        return jsonify({
            "Message": "User does not exist, please register"
        }), 401
    if not checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
        return jsonify({
            "Message": "Passwords don't match. Please try again"
        }), 401
    return jsonify(
        {
            "Message": "Successfull login"
        }
    ), 200


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(port=5001)
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from bcrypt import hashpw, gensalt, checkpw
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://kmmrwsgr:UMg6sKjYUG3nhI6D3fTjSU3vMpjGjYCI@abul.db.elephantsql.com/kmmrwsgr'
db = SQLAlchemy(app)
jwt = JWTManager(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(256), unique=True, nullable=False)


@app.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')

    if User.query.filter_by(username=username).first():
        return jsonify({
            "Message": "User already exists"
        }), 400

    if not username:
        return jsonify({
            "Message": "Username and password are required"
        }), 400

    user = User(username=username)
    db.session.add(user)
    db.session.commit()

    return jsonify({
        "Message": "User registered successfully"
    }), 201


@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')

    if not username:
        return jsonify({
            "Message": "Username and password are required"
        }), 400

    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({
            "Message": "User does not exist, please register"
        }), 401

    access_token = create_access_token(identity=user.id)
    return jsonify({
        "access_token": access_token
    }), 200


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(port=5001)


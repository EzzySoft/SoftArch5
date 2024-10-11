from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from flask_cors import CORS


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://myuser:mypassword@db:5432/softarch5'
app.config['JWT_SECRET_KEY'] = "717ac506950da0ccb6404cdd5e7591f72018a20cbca27c8a423e9c9e5626ac61"
db = SQLAlchemy(app)
jwt = JWTManager(app)
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})


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
            "Message": "Username is required"
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
            "Message": "Username is required"
        }), 400

    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({
            "Message": "User does not exist, please register"
        }), 401

    access_token = create_access_token(identity=user.id)
    return jsonify({
        "access_token": access_token,
        "user_id": user.id
    }), 200


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host = '0.0.0.0', port=5001)


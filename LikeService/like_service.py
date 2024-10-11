from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
from flask_cors import CORS
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://myuser:mypassword@localhost:5432/softarch5'
app.config['JWT_SECRET_KEY'] = "717ac506950da0ccb6404cdd5e7591f72018a20cbca27c8a423e9c9e5626ac61"
db = SQLAlchemy(app)
jwt = JWTManager(app)
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})


class Like(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    message_id = db.Column(db.Integer, nullable=False)


@app.route('/like', methods=['POST'])
@jwt_required()
def like():
    data = request.json
    user_id = get_jwt_identity()
    message_id = data.get('message_id')

    if not message_id:
        return jsonify({
            "Message": "Message ID is required"
        }), 400

    like = Like(user_id=user_id, message_id=message_id)
    db.session.add(like)
    db.session.commit()

    return jsonify({
        "Message": "Message is liked successfully"
    }), 201


@app.route('/dislike', methods=['POST'])
@jwt_required()
def dislike():
    data = request.json
    user_id = get_jwt_identity()
    message_id = data.get('message_id')

    if not message_id:
        return jsonify({
            "Message": "Message ID is required"
        }), 400

    like = Like.query.filter_by(user_id=user_id, message_id=message_id).first()
    if not like:
        return jsonify({
            "Message": "No like is found"
        }), 404

    db.session.delete(like)
    db.session.commit()

    return jsonify({
        "Message": "Message is unliked successfully"
    }), 200


@app.route('/likes/<int:message_id>', methods=['GET'])
def get_likes(message_id):
    likes = Like.query.filter_by(message_id=message_id).count()
    return jsonify({
        "message_id": message_id,
        "likes": likes
    }), 200


@app.route('/likes/user/<int:user_id>', methods=['GET'])
def get_user_likes(user_id):
    likes = Like.query.filter_by(user_id=user_id).all()
    liked_message_ids = [like.message_id for like in likes]
    return jsonify({
        "user_id": user_id,
        "liked_message_ids": liked_message_ids
    }), 200


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(port=5002)